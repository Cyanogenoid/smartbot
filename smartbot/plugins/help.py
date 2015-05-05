import itertools

import smartbot.plugin
from smartbot.exceptions import StopCommand
from smartbot.formatting import Style


class Plugin(smartbot.plugin.Plugin):
    """Get help information about loaded plugins."""
    names = ["help", "what?"]

    def on_command(self, msg, stdin, stdout):
        plugin_name = None
        if len(msg["args"]) >= 2:
            plugin_name = msg["args"][1]
        else:
            plugin_name = stdin.read().strip()

        if plugin_name:
            plugin = self.bot.find_plugin(plugin_name)
            if plugin:
                print(plugin.on_help(), file=stdout)
            else:
                raise StopCommand("{} does not exist.".format(plugin_name))
        else:
            names = itertools.chain.from_iterable(
                plugin.names for plugin in self.bot.plugins)
            plugin_names = ", ".join(sorted(names))
            print("Help about:", plugin_names, file=stdout)

    def on_help(self):
        return "{} [{}]".format(
            self.bot.format("help", Style.bold),
            self.bot.format("plugin", Style.underline)
        )
