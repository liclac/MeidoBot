import threading
from time import sleep

class ticking(object):
	interval = None
	
	def __init__(self, interval):
		self.interval = interval
	def __call__(self, f):
		def wrapper():
			while True:
				print "Wrapper!"
				sleep(self.interval)
		t = threading.Thread(target = wrapper)
		t.daemon = True
		t.start()
		return f
