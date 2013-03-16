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
		pairs = (
					(self.actions, c.actions),
					(self.objects, c.objects),
					(self.targets, c.targets)
		)
		for pl, cl in pairs:
			for item in pl:
				if item in cl:
					return True
		return False
	
	def get_handlers(self, c):
		all_handlers = {}
		chain = [x for x in itertools.chain(c.actions, c.objects, c.targets)]
		for triggers, handler in self.handlers.iteritems():
			if type(triggers) is str:
				all_handlers[triggers] = handler
			else:
				for trigger in triggers:
					all_handlers[trigger] = handler
		handlers = [h for t, h in all_handlers.iteritems() if t in chain]
		handlers.append(('do_fallback', -10))
		return [(getattr(self, h), w) for h, w in handlers]
	
	def do_context(self, c):
		return False
	
	def do_fallback(self, c):
		return False
	
	
	
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
	