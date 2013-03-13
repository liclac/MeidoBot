import os
from pprint import pprint
from importlib import import_module

class MeidoBrain(object):
	ui = None
	parser = None
	plugins = []
	locked_context = None
	
	def load_plugins(self):
		plugins_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plugins')
		plugins = [os.path.splitext(file)[0] for file in os.listdir(plugins_path)
					if file.lower().endswith('.py') and not file.lower().startswith('_')]
		for plugin in plugins:
			mod = import_module('plugins.%s' % plugin)
			if not hasattr(mod, 'plugin_class'):
				print "Plugin %s has no 'plugin_class'!" % plugin
				continue
			if not hasattr(mod, mod.plugin_class):
				print "Plugin %s has no '%s' class!" % plugin_class
				continue
			plug = getattr(mod, mod.plugin_class)(self)
			self.plugins.append(plug)
			
	def respond(self, string):
		'''Takes an input string, parses it and acts upon it.'''
		data = self.parser.parse(string)
		self.act(data)
	
	def act(self, res):
		'''Acts upon the tagged data it receives.'''
		
		if self.locked_context != None:
			self.locked_context.act(res, True)
		else:
			has_hit = False
			for plug in self.plugins:
				plug.act(res, False)
			if not has_hit:
				self.ui.say("I'm sorry, I'm not sure what you mean...")
	
	def lock_context(self, plugin):
		'''
		Locks the context, making sure only the given plugin
		gets to act. This gives plugins the ability to act 
		on arbitrary input without using keywords.
		'''
		
		# Make sure there aren't accidental relocks
		if self.locked_context != None: return
		
		self.locked_context = plugin
		plugin.on_context_locked()
	
	def release_context(self, plugin):
		'''
		Releases a locked context, giving other plugins back the
		ability to act.
		
		The 'plugin' parameter must hold the plugin that locked the
		context to ensure that there are no accidental mislocks.
		Yes, you can just read that from the brain if you really
		have to for whatever reason.
		'''
		
		# Make sure there is a context to release
		if self.locked_context == None: return
		
		self.locked_context = None
		plugin.on_context_released()
	