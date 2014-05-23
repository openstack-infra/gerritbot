Installation
============

To install Gerritbot run ::

  sudo python setup.py install

Configuration File
==================

Gerritbot has two configuration files. The first configures the IRC server and
Gerrit server details and is the config file whose path you pass to gerritbot
when starting the bot. It should look like::

  [ircbot]
  nick=NICKNAME
  pass=PASSWORD
  server=irc.freenode.net
  port=6667
  force_ssl=True or False (Defaults to False)
  server_password=SERVERPASS
  channel_config=/path/to/yaml/config
  
  [gerrit]
  user=gerrit2
  key=/path/to/id_rsa
  host=review.example.com
  port=29418

The second configures the IRC channels and the events and projects that each
channel is interested in. This config file is written in yaml and should look
like::

  example-channel1:
      events:
        - patchset-created
        - change-merged
      projects:
        - example/project1
        - example/project2
      branches:
        - master
        - development
  example-channel2:
      events:
        - change-merged
      projects:
        - example/project3
        - example/project4
      branches:
        - master

Running
=======

To run Gerritbot `$PATH/gerritbot /path/to/config`. $PATH is usually something
like /usr/local/bin and /path/to/config should be whatever path you have hidden
the config at.
