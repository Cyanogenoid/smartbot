Smart Bot
=========

A supposedly smart IRC bot.

Configuration
-------------

The configuration file is a very simple and self-explanatory YAML based file.
Before you run the bot you must create a configuration file similar to this
with the filename `config.yaml`::

    bot:
        name: SmartBot

    backend:
        name: irc
        hostname: my.irc.server

    storage:
        name: yaml

    plugins:
        - name: autojoin
          channels: [ "#robots" ]

Building & Running
------------------

SmartBot uses a standard ``setup.py`` script, like so::

    $ ./setup.py install
    $ smartbot

Plugins
-------

To see the list of plugins, look in the ``plugins`` directory.
