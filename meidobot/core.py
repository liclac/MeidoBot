import os
import json
import traceback
from pprint import pprint
from importlib import import_module
from itertools import chain
from meidobot.util import normalize

class Command(object):
	actions = []
	objects = []
	targets = []
	
	def __init__(self, actions=[], objects=[], targets=[]):
		self.actions = actions
		self.objects = objects
		self.targets = targets

class Meido(object):
	ui = None
	#parser = None
	plugins = []
	locked_context = None
	running = False
	
	base_path = None
	config_filename = None
	config = {}
	
	def __init__(self, base_path, config_filename):
		self.base_path = base_path
		self.config_filename = config_filename
		with open(os.path.join(base_path, config_filename)) as f:
			self.config = json.loads(f.read())
	
	def load_plugins(self):
		plugins_path = os.path.join(self.base_path, self.get_config('brain.plugins_module', 'plugins'))
		plugins = [os.path.splitext(file)[0] for file in os.listdir(plugins_path)
					if file.lower().endswith('.py') and not file.lower().startswith('_')]
		for plugin_name in plugins:
			try:
				mod = import_module('plugins.%s' % plugin_name)
			except Exception as e:
				print "----------"
				print "Couldn't load plugin: %s" % plugin_name
				print " "
				print traceback.format_exc()
				print "----------"
				continue
			
			if not hasattr(mod, 'plugin_class'):
				print "Plugin %s has no 'plugin_class'!" % plugin_name
				continue
			if not hasattr(mod, mod.plugin_class):
				print "Plugin %s has no attribute named '%s'!" % (plugin_name, plugin_class)
				continue
			plugin = getattr(mod, mod.plugin_class)(self)
			self.plugins.append(plugin)
	
	def run(self):
		'''Runs a main loop'''
		
		if self.ui is None:
			print "ERROR: No UI!"
			return
		self.running = True
		self.ui.run()
		self.running = False
	
	def stop(self):
		'''Stops a running main loop'''
		self.running = False
		self.ui.stop()
			
	def respond(self, string):
		'''Takes an input string, parses it and acts upon it.'''
		
		string = normalize(string)
		has_hit = False
		
		if self.locked_context is None:
			for plugin in self.plugins:
				has_hit = self._dispatch_plugin(plugin, self._make_command(plugin, string), False)
				if has_hit:
					break
		else:
			has_hit = self._dispatch_plugin(self.locked_context, self._make_command(self.locked_context, string), True)
		if not has_hit:
			self.ui.say(self.get_config("brain.fallback"))
			
	
	def _make_command(self, plugin, string):
		'''Creates a Command object from the given string and plugin.
		Returns None if the given plugin can't handle the given string.'''
		c = Command()
		
		attribs = ['actions', 'objects', 'targets']
		has_match = plugin.acts_on_everything
		for attr in attribs:
			array = getattr(c, attr)
			for phrase in getattr(plugin, attr):
				if phrase in string:
					array.append(phrase)
					has_match = True
			if has_match:
				array.extend(self.get_config("brain.default_%s" % attr, []))
		
		if has_match:
			has_match = plugin.interested(c)
		
		if has_match:
			return c
		else:
			return None
	
	def _dispatch_plugin(self, plugin, c, locked_context = False):
		'''Dispatches the given command (c) to the given plugin.
		Returns whether or not the plugin could actually handle it.
		'''
		
		if c is None:
			return False
		#print "-> %s" % plugin.__class__.__name__
		
		has_hit = False
		handlers = plugin.get_handlers(c)
		for handler in handlers:
			has_hit = handler(c, locked_context)
			if has_hit: break
		if not has_hit:
			has_hit = plugin.act(c, locked_context)
		return has_hit
	
	def get_config(self, key, default = None):
		'''Returns the given configuration variable, or default.'''
		try:
			components = key.split('.')
			lastobj = self.config[components[0]]
			for k in components[1:]:
				lastobj = lastobj[k]
			return lastobj
		except KeyError:
			return default
	
	def lock_context(self, plugin):
		'''Locks the context, making sure only the given plugin
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
		