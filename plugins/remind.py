import datetime
import re
import time
import threading

from smartbot import utils


class Plugin:
    def on_timeout(self, message, duration, bot, msg):
        time.sleep(duration)
        bot.send(msg["reply_to"], message)

    def on_respond(self, bot, msg):
        try:
            match = re.match(r"remind me (to|about|that) (.*) (in|at) (.*)$", msg["message"], re.IGNORECASE)
            if match:
                date = utils.datetime.parse("{0} {1}".format(match.group(3), match.group(4)))
                bot.send(msg["reply_to"], "Sure thing {0}, I'll remind you at {1}.".format(msg["sender"], date))
                message = "{0}: you asked me to remind you {1} {2}".format(msg["sender"], match.group(1), match.group(2))
                duration = max(0, (date - datetime.datetime.now()).total_seconds())
                t = threading.Thread(target=self.on_timeout, args=(message, duration, bot, msg))
                t.start()
        except ValueError:
            bot.send(msg["reply_to"], "I don't understand that date.")

    def on_help(self):
        return "Usage: remind me to|about|that <something> in|at <time>"
