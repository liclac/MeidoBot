from meidobot.model import Emotion

class Notification(object):
	title = "Untitled"
	text = "No Text"
	
	def __init__(self, title="Untitled", text="No Text"):
		self.title = title
		self.text = text
	
	def __str__(self):
		return "[Notification - %s: %s]" % (self.title, self.text)



class UI(object):
	currentEmotion = None
	brain = None
	notificationQueue = []
	running = False
	
	def __init__(self, brain):
		self.brain = brain
	def run(self):
		self.running = True
	def stop(self):
		self.running = False
	
	def say(self, text):
		pass
	def emotion(self, emotion):
		self.currentEmotion = emotion
	def notify(self, notification = None, title="Untitled", text="No Text"):
		if notification is None:
			notification = Notification(title=title, text=text)
		self.notificationQueue.append(notification)