from MeidoMood import Emotion

class MeidoUI(object):
	currentEmotion = None
	brain = None
	
	def __init__(self, brain):
		self.brain = brain
	
	def say(self, text): pass
	def emotion(self, emotion):
		self.currentEmotion = emotion

class MeidoCLI(MeidoUI):
	def say(self, text):
		print text
		
	def emotion(self, emotion):
		self.currentEmotion = emotion
		if emotion != None:
			print emotion.emote