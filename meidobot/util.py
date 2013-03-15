import threading
from functools import wraps
from time import sleep

def async(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		t = threading.Thread(target = f)
		t.start()
	return wrapper

def background(f):
	def wrapper():
		t = threading.Thread(target = f)
		t.daemon = True
		t.start()
		return t
	return wrapper

# We need a class for this, since it takes parameters
# I don't think it's possible to make function decorators
# take parameters, but I've been wrong before...
class ticking(object):
	interval = None
	
	def __init__(self, interval):
		self.interval = interval
	def __call__(self, f):
		@background
		def wrapper():
			while True:
				f()
				sleep(self.interval)
		return f
