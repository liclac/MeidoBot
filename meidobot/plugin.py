import re
import itertools
from meidobot.core import Command

class Plugin(object):
	brain = None
	
	actions = []
	objects = []
	targets = []
	handlers = {}
	
	# If this is True, the plugin will receive ALL inputs
	# If False, it will only receive inputs containing
	# Actions or Objects it recognizes
	acts_on_everything = False
	
	def __init__(self, brain):
		self.brain = brain
	
	def interested(self, c):
		return True
	
	def get_handlers(self, c):
		'''Returns a list of all available handler functions.'''
		# I have no idea why you'd ever want to act on a target, but why not.
		handlers = []
		for trigger in itertools.chain(c.actions, c.objects, c.targets):
			if trigger in self.handlers:
				handlers.append(getattr(self, self.handlers[trigger]))
		return handlers
	
	def act(self, c, context = False):
		'''
		Default handler if no handler matches.
		All handlers should have this signature.
		Return False to pass to the next handler.
		'''
		pass
	
	
	
	def on_context_locked(self):
		'''
		Called when the context is locked onto your plugin.
		Use this to establish/load any necessary context data
		or lazy-loaded resources.
		'''
		pass
	
	def on_context_released(self):
		'''
		Called when the context is released from your plugin.
		Use this to clear context data and unload any lazy-loaded
		resources.
		'''
		pass
	