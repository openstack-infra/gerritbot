#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import collections

import testtools
import yaml

import gerritbot.bot as bot

CHANNEL_CONFIG_YAML = """
openstack-dev:
    events:
      - patchset-created
      - change-merged
      - ^x-(crvw|vrif)-(plus|minus)-2$
    projects:
      - openstack/nova
      - openstack/swift
    branches:
      - master
      - stable/queens
openstack-infra:
    events:
      - patchset-created
      - change-merged
      - comment-added
      - ref-updated
      - ^x-(crvw|vrif)-(plus|minus)-2$
    projects:
      - ^openstack/
    branches:
      - master
      - stable/queens
"""


class ChannelConfigTestCase(testtools.TestCase):
    def test_missing_octothorpe(self):
        channel_config = bot.ChannelConfig(yaml.load(CHANNEL_CONFIG_YAML))
        # TODO(jlvillal): Python 2 only assert. Must change to use
        # six.assertCountEqual() for Python 2/3 compatibility
        self.assertItemsEqual(['#openstack-dev', '#openstack-infra'],
                              channel_config.channels)

    def test_branches(self):
        channel_config = bot.ChannelConfig(yaml.load(CHANNEL_CONFIG_YAML))
        expected_channels = {'#openstack-dev', '#openstack-infra'}
        self.assertEqual(
            {
                'master': expected_channels,
                'stable/queens': expected_channels,
            },
            channel_config.branches)

    def test_events(self):
        channel_config = bot.ChannelConfig(yaml.load(CHANNEL_CONFIG_YAML))
        expected_channels = {'#openstack-dev', '#openstack-infra'}
        self.assertEqual(
            {
                'change-merged': expected_channels,
                'comment-added': {'#openstack-infra'},
                'patchset-created': expected_channels,
                'ref-updated': {'#openstack-infra'},
                '^x-(crvw|vrif)-(plus|minus)-2$': expected_channels,
            },
            channel_config.events)

    def test_projects(self):
        channel_config = bot.ChannelConfig(yaml.load(CHANNEL_CONFIG_YAML))
        self.assertEqual(
            {
                '^openstack/': {'#openstack-infra'},
                'openstack/nova': {'#openstack-dev'},
                'openstack/swift': {'#openstack-dev'},
            },
            channel_config.projects)


Message = collections.namedtuple('Message', ['channel', 'msg'])


class IrcBotHelper(object):
    """Dummy class to use for testing the Gerrit and GerritMQTT classes

    For testing the Gerrit and GerritMQTT classes we need a dummy IrcBot.
    """
    def __init__(self):
        self.messages = []

    def send(self, channel, msg):
        self.messages.append(Message(channel=channel, msg=msg))


class GerritTestCase(testtools.TestCase):

    def setUp(self):
        super(GerritTestCase, self).setUp()
        self.ircbot = IrcBotHelper()
        self.channel_config = bot.ChannelConfig(yaml.load(CHANNEL_CONFIG_YAML))
        self.channel = "#openstack-infra"
        self.gerrit = bot.Gerrit(ircbot=self.ircbot,
                                 channel_config=self.channel_config,
                                 server='localhost',
                                 username='username',
                                 port=29418)

        self.sample_data = {
            'change': {
                'branch': 'master',
                'project': 'openstack/gerritbot',
                'subject': 'More unit tests',
                'url': 'https://review.openstack.org/123456',
            },
            'patchSet': {
                'uploader': {
                    'name': 'John L. Villalovos',
                },
            },
            'refUpdate': {
                'project': 'openstack/gerritbot',
                'refName': 'refs/tags/pike',
            },
            'submitter': {
                'username': 'elmo',
            },

        }

    def _validate_patchset_created(self):
        self.assertEqual(1, len(self.ircbot.messages))
        message = self.ircbot.messages[0]
        self.assertEqual(self.channel, message.channel)
        self.assertEqual(
            'John L. Villalovos proposed openstack/gerritbot master: More '
            'unit tests  https://review.openstack.org/123456',
            message.msg)

    def test_patchset_created(self):
        self.gerrit.patchset_created(self.channel, self.sample_data)
        self._validate_patchset_created()

    def test__read_patchset_created(self):
        self.gerrit._read(dict(self.sample_data, type='patchset-created'))
        self._validate_patchset_created()

    def _validate_ref_updated(self):
        self.assertEqual(1, len(self.ircbot.messages))
        message = self.ircbot.messages[0]
        self.assertEqual(self.channel, message.channel)
        self.assertEqual('elmo tagged project openstack/gerritbot with pike',
                         message.msg)

    def test_ref_updated(self):
        self.gerrit.ref_updated(self.channel, self.sample_data)
        self._validate_ref_updated()

    def test__read_ref_updated(self):
        self.gerrit._read(dict(self.sample_data, type='ref-updated'))
        self._validate_ref_updated()

    def _validate_change_merged(self):
        self.assertEqual(1, len(self.ircbot.messages))
        message = self.ircbot.messages[0]
        self.assertEqual(self.channel, message.channel)
        self.assertEqual(
            'Merged openstack/gerritbot master: More unit tests  '
            'https://review.openstack.org/123456',
            message.msg)

    def test_change_merged(self):
        self.gerrit.change_merged(self.channel, self.sample_data)
        self._validate_change_merged()

    def test__read_change_merged(self):
        self.gerrit._read(dict(self.sample_data, type='change-merged'))
        self._validate_change_merged()

    def _validate_comment_added(self):
        self.assertEqual(1, len(self.ircbot.messages))
        message = self.ircbot.messages[0]
        self.assertEqual(self.channel, message.channel)
        self.assertEqual(
            'A comment has been added to a proposed change to '
            'openstack/gerritbot: More unit tests  '
            'https://review.openstack.org/123456',
            message.msg)

    def test_comment_added(self):
        self.gerrit.comment_added(self.channel, self.sample_data)
        self._validate_comment_added()

    def test__read_comment_added(self):
        self.gerrit._read(dict(self.sample_data, type='comment-added'))
        self._validate_comment_added()

    def _validate_comment_added_vrif(self):
        self.assertEqual(2, len(self.ircbot.messages))

        # The test function 'test_comment_added()' verifies that index 0 is
        # correct, so we will only check index 1
        message = self.ircbot.messages[1]
        self.assertEqual(self.channel, message.channel)
        self.assertEqual(
            'Verification of a change to openstack/gerritbot failed: '
            'More unit tests  https://review.openstack.org/123456',
            message.msg)

    def test_comment_added_vrif(self):
        self.gerrit.comment_added(
            self.channel,
            dict(self.sample_data, approvals=[{
                'type': 'VRIF',
                'value': '-2',
            }]))
        self._validate_comment_added_vrif()

    def test__read_comment_added_vrif(self):
        self.gerrit._read(
            dict(self.sample_data, type='comment-added', approvals=[{
                'type': 'VRIF',
                'value': '-2',
            }]))
        self._validate_comment_added_vrif()
