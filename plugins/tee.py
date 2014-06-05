import smartbot


class Plugin(smartbot.Plugin):
    names = ["tee"]

    def on_command(self, msg, stdin, stdout, reply):
        text = stdin.read().strip()

        reply(text)
        print(text, file=stdout)

    def on_help(self):
        return "Copy standard input to reply, and also to standard output."
