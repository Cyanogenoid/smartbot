import re

from smartbot import utils


class Plugin:
    def on_message(self, bot, msg):
        match = re.findall(r"(https?://[^\s]+)", msg["message"], re.IGNORECASE)
        for i, url in enumerate(match):
            title = utils.web.get_title(url)
            if title:
                bot.send(msg["reply_to"], "[{0}]: {1}".format(i, title))

    def on_help(self, bot, msg, reply):
        return "Echos the titles of websites for any HTTP(S) URL."
