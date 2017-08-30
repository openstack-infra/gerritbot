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

import testtools
import yaml

import gerritbot.bot as bot

CHANNEL_CONFIG_YAML = """
openstack-dev:
    events:
      - patchset-created
      - change-merged
    projects:
      - openstack/nova
      - openstack/swift
    branches:
      - master
"""


class ChannelConfigTestCase(testtools.TestCase):
    def test_missing_octothorpe(self):
        channel_config = bot.ChannelConfig(yaml.load(CHANNEL_CONFIG_YAML))
        self.assertEqual(['#openstack-dev'], channel_config.channels)
