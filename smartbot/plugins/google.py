import smartbot.plugin
from smartbot.utils.web import requests_session
from smartbot.exceptions import StopCommand, StopCommandWithHelp
from smartbot.formatting import Style


class Plugin(smartbot.plugin.Plugin):
    """Perform a Google search and get the results."""
    names = ["google", "search"]

    def __init__(self, key, cx):
        self.key = key
        self.cx = cx

    def on_command(self, msg, stdin, stdout):
        query = " ".join(msg["args"][1:])
        if not query:
            query = stdin.read().strip()

        if not query:
            raise StopCommandWithHelp(self)

        url = "https://www.googleapis.com/customsearch/v1"
        payload = {
            "key": self.key,
            "cx": self.cx,
            "q": query,
            "num": 4,
        }

        session = requests_session()
        res = session.get(url, params=payload).json()
        if "error" in res:
            raise StopCommand(res["error"]["message"])
        elif "items" in res:
            for i, item in enumerate(res["items"]):
                print("[{0}]: {1} - {2}".format(i, item["title"],
                                                item["link"]), file=stdout)
        else:
            raise StopCommand("No results!")

    def on_help(self):
        return "{}|{} {}".format(
            self.bot.format("google", Style.bold),
            self.bot.format("search", Style.bold),
            self.bot.format("query", Style.underline),
        )
