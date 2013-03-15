import threading
from functools import wraps
from time import sleep

def __f_thread(f, *args, **kwargs):
	def run():
		f(*args, **kwargs)
	t = threading.Thread(target=run)
	return t

def async(f):
	'''Makes calls to a function asynchronous.
	Asynchronous functions cannot return a value.'''
	@wraps(f)
	def wrapper(*args, **kwargs):
		t = __f_thread(f, *args, **kwargs)
		t.start()
		return t
	
	return wrapper

def daemon(f):
	'''Makes calls to a function asynchronous on a daemon thread.
	The daemon property means it's possible to cancel execution at
	any time, so don't use this for things that have to finish!
	Asynchronous functions cannot return a value.'''
	@wraps(f)
	def wrapper(*args, **kwargs):
		t = __f_thread(f, *args, **kwargs)
		t.daemon = True
		t.start()
		return t
	return wrapper

# We need a class for this, since it takes parameters.
# I don't think it's possible to make decorator functions
# take parameters, but I've been wrong before...
class ticking(object):
	'''Makes a function fire once every n seconds, starting from
	when the function is first loaded.
	The function will not be called as a daemon; it's (mostly)
	guaranteed to finish executing (bar interpreter crashes).'''
	interval = None
	args = []
	kwargs = {}
	
	def __init__(self, interval, args = [], kwargs = {}):
		self.interval = interval
		self.args = args
		self.kwargs = kwargs
	def __call__(self, f):
		@async
		def wrapper():
			while True:
				f(*self.args, **self.kwargs)
				sleep(self.interval)
		wrapper()
		return f
