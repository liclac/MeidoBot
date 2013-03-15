import re
from meidobot.core import Command

class Plugin(object):
	brain = None
	
	actions = []
	objects = []
	targets = []
	
	# If this is True, the plugin will receive ALL inputs
	# If False, it will only receive inputs containing
	# Actions or Objects it recognizes
	acts_on_everything = False
	
	def __init__(self, brain):
		self.brain = brain
	
	def act(self, c, context = False):
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
	