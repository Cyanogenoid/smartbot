var moment = require("moment");
var parseDateTime = require("parsedatetime");

var REGEX = /remind me (to|about) (.*) (in|at) (.*)$/i;

module.exports = function(bot, config) {
  bot.respond(REGEX, function(msg, reply) {
    var toAbout = msg.match[1];
    var action = msg.match[2];
    var timeInAt = msg.match[3];
    var time = msg.match[4];

    var date = parseDateTime(timeInAt + " " + time);
    if (date) {
      reply("Sure thing, " + msg.from + " (" + date.toString() + ")!");
      setTimeout(function() {
        reply(msg.from + ": you asked me to remind you " + toAbout + " " + action);
      }, date - Date.now());
    } else {
      reply("I don't understand that date.");
    }
  });
};

