from meidobot.plugin import Plugin

plugin_class = "TwitterPlugin"

class TwitterPlugin(Plugin):
	actions = ["login", "log in", "monitor", "watch", "track", "keep an eye on"]
	objects = ["twitter"]
	handlers = {
		('login', 'log in'): ('do_login', 1),
		('monitor', 'watch', 'track', 'keep an eye on'): ('do_monitor', 1)
	}
	
	def __init__(self, brain):
		super(TwitterPlugin, self).__init__(brain)
	
	def interested(self, c):
		# Only act on commands referring to Twitter
		return ('twitter' in c.objects)
	
	def do_login(self, c):
		self.brain.ui.say("Login to Twitter")
		return True
		
	def do_monitor(self, c):
		self.brain.ui.say("Monitor Twitter")
		return True
