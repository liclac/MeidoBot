from meidobot.model import Emotion

class UI(object):
	currentEmotion = None
	brain = None
	
	def __init__(self, brain):
		self.brain = brain
	def run(self):
		pass
	
	def say(self, text): pass
	def emotion(self, emotion):
		self.currentEmotion = emotion

class CLI(UI):
	def run(self):
		self.brain.respond(raw_input("> "))
	
	def say(self, text):
		print text
		
	def emotion(self, emotion):
		self.currentEmotion = emotion
		if emotion != None:
			print emotion.emote