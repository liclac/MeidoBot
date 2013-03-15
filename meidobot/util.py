import threading
from functools import wraps
from time import sleep

def async(f):
	'''Makes calls to a function asynchronous.
	Asynchronous functions cannot return a value.'''
	@wraps(f)
	def wrapper(*args, **kwargs):
		def run():
			f(*args, **kwargs)
		t = threading.Thread(target = run)
		t.start()
		return t
	
	return wrapper

def background(f):
	'''Makes a function asynchronous and starts it immediately when it's loaded'.'''
	@wraps(f)
	def wrapper(*args, **kwargs):
		def run():
			f(*args, **kwargs)
		t = threading.Thread(target = run)
		t.daemon = True
		t.start()
		return t
	
	wrapper()
	return wrapper

# We need a class for this, since it takes parameters
# I don't think it's possible to make function decorators
# take parameters, but I've been wrong before...
class ticking(object):
	'''Makes a function fire once every n seconds, starting from
	when the function is first loaded. Make sure any objects you want
	to use are actually available!'''
	interval = None
	args = []
	kwargs = {}
	
	def __init__(self, interval, args = [], kwargs = {}):
		self.interval = interval
		self.args = args
		self.kwargs = kwargs
	def __call__(self, f):
		@background
		def wrapper():
			while True:
				f(*self.args, **self.kwargs)
				sleep(self.interval)
		wrapper()
		return f
