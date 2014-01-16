import operator

class Plugin:
    def __call__(self, bot):
        bot.on_hear(r"(lol|:D|:P)", self.on_hear)
        bot.on_respond(r"stats", self.on_respond)
        bot.on_help("stats", self.on_help)

    def on_hear(self, bot, msg, reply):
        stats = bot.storage.get("stats", {})

        for word in msg["match"]:
            word_stats = stats.get(word, {})
            word_stats[msg["sender"]] = word_stats.get(msg["sender"], 0) + 1
            stats[word] = word_stats

        bot.storage["stats"] = stats

    def on_respond(self, bot, msg, reply):
        def respond(word, description):
            stats = bot.storage.get("stats", {}).get(word, {})
            if stats:
                person = max(stats.items(), key=operator.itemgetter(1))[0]
                reply(description.format(person))

        respond("lol", "{0} laughs the most.")
        respond(":D", "{0} is the happiest.")
        respond(":P", "{0} is the most sarcastic.")

    def on_help(self, bot, msg, reply):
        reply("Syntax: stats")
