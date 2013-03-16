from meidobot.plugin import Plugin

plugin_class = "SystemPlugin"

class SystemPlugin(Plugin):
	actions = ['exit', 'quit']
	handlers = {
		('exit', 'quit'): ('do_exit', -1)
	}
	
	def do_exit(self, c, locked = False):
		self.brain.stop()
		return True
