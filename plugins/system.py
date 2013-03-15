import sys
from meidobot.plugin import Plugin

plugin_class = "SystemPlugin"

class SystemPlugin(Plugin):
	actions = ['exit']
	handlers = {
		'exit': 'do_exit'
	}
	
	def do_exit(self, c, context = False):
		sys.exit()
		return True # This won't ever happen, but... consistency!
