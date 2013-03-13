import sys
from MeidoPlugin import MeidoPlugin

plugin_class = "SystemPlugin"

class SystemPlugin(MeidoPlugin):
	verbs = ['exit']
	
	def act(self, res, context = False):
		if 'exit' in res.verbs: sys.exit()
		else: return False
		
		return True
