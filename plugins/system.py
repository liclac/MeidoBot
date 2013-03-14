import sys
from meidobot.plugin import Plugin

plugin_class = "SystemPlugin"

class SystemPlugin(Plugin):
	verbs = ['exit']
	
	def act(self, res, context = False):
		if 'exit' in res.verbs: sys.exit()
		else: return False
		
		return True
