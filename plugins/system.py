import sys
from meidobot.plugin import Plugin

plugin_class = "SystemPlugin"

class SystemPlugin(Plugin):
	actions = ['exit']
	
	def act(self, c, context = False):
		print vars(c)
		return False
	
	#def act(self, c, context = False):
	#	if 'exit' in c.actions: sys.exit()
	#	else: return False
	#	
	#	return True
