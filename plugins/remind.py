import datetime
import io
import re
import time
import threading
import unittest

from smartbot import utils


class Plugin:
    def on_command(self, bot, msg, stdin, stdout, reply):
        pattern_str = r"remind (me|[^\s]+) (to|about|that) (.*) (in|at) (.*)$"
        match = re.match(pattern_str, msg["message"], re.IGNORECASE)
        if not match:
            match = re.match(pattern_str, stdin.getvalue().strip(), re.IGNORECASE)

        if match:
            try:
                date = utils.datetime.parse("{0} {1}".format(match.group(4), match.group(5)))
            except ValueError:
                print("I don't understand that date.", file=stdout)
            else:
                message = None
                if match.group(1) == "me" or match.group(1) == msg["sender"]:
                    print("Sure thing {0}, I'll remind you on {1}.".format(msg["sender"], date.strftime("%c").strip()), file=stdout)
                    message = "{0}: you asked me to remind you {1} {2}".format(msg["sender"], match.group(2), match.group(3))
                else:
                    print("Sure thing {0}, I'll remind {1} on {2}.".format(msg["sender"], match.group(1), date.strftime("%c").strip()), file=stdout)
                    message = "{0}: {1} asked me to remind you {2} {3}".format(match.group(1), msg["sender"], match.group(2), match.group(3))

                duration = max(0, (date - datetime.datetime.now()).total_seconds())
                time.sleep(duration)
                print(message, file=stdout)

    def on_help(self):
        return "Usage: remind me|<target> to|about|that <something> in|at <time>"


class Test(unittest.TestCase):
    class ExampleBot:
        def __init__(self, test):
            self.test = test
            self.start_time = datetime.datetime.now()

        def send(self, target, message):
            self.test.assertIs(target, None)
            self.test.assertEqual(int((datetime.datetime.now() - self.start_time).total_seconds()), 2)

    def setUp(self):
        self.plugin = Plugin()

    def test_me_remind(self):
        stdout = io.StringIO()
        bot = Test.ExampleBot(self)
        msg = {"message": "remind me to do something in 2 seconds", "sender": "test"}
        self.plugin.on_command(bot, msg, None, stdout, lambda x: bot.send(None, x))
        self.assertTrue(stdout.getvalue().strip().startswith("Sure thing test, I'll remind you on"))
        self.assertNotEqual("I don't understand that date.", stdout.getvalue().strip())

    def test_target_remind(self):
        stdout = io.StringIO()
        bot = Test.ExampleBot(self)
        msg = {"message": "remind test2 to do something in 2 seconds", "sender": "test"}
        self.plugin.on_command(bot, msg, None, stdout, lambda x: bot.send(None, x))
        self.assertTrue(stdout.getvalue().strip().startswith("Sure thing test, I'll remind test2 on"))
        self.assertNotEqual("I don't understand that date.", stdout.getvalue().strip())

    def test_help(self):
        self.assertTrue(self.plugin.on_help())
