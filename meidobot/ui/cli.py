from meidobot.ui.ui import UI

class CLI(UI):
	def run(self):
		super(CLI, self).run()
		while self.running:
			for notification in self.notificationQueue:
				print "-- %s --" % notification.title
				print notification.text
				print "---%s---" % ("-"*len(notification.title))
				self.notificationQueue.remove(notification)
			self.brain.respond(raw_input("> "))
	
	def say(self, text):
		print text
		
	def emotion(self, emotion):
		super(CLI, self).emotion(emotion)
		if emotion != None:
			print emotion.emote