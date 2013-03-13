class MeidoPlugin(object):
	brain = None
	
	verbs = []
	objects = []
	subjects = []
	
	def __init__(self, brain):
		self.brain = brain
	
	def act(self, res, context = False):
		'''
		Your plugin should override this function to react
		to user input. This function will get called regardless of
		the presence of keywords in the string.
		
		Arguments:
			res		-- a MeidoParserResult of the input string
			context	-- True if this is called from the plugin's locked context
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
	