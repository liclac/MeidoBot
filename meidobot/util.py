import threading

class MeidoWorker(threading.Thread, name = None, interval = 60, function = None):
	def __init__(self, **kwargs):
		threading.Thread(self, kwargs)
		