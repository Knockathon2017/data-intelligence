from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings


class MorningPlugin(WillPlugin):

	@respond_to("^good morning")
	def good_morning(self, message):
		self.reply(message, "oh, g'morning!")

	@route("/pages")
	@rendered_template("basic.html")
	def pages(self):
		return {}