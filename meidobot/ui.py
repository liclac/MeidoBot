from meidobot.model import Emotion

# Attempt to load the Tk UI (should always work)
try:
	import Tkinter
	import tkMessageBox
except ImportError:
	print "Tk UI not available"



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

class Tk(UI):
	def __init__(self, brain):
		super(Tk, self).__init__(brain)
		self.root = Tkinter.Tk()
	
	def create_UI(self, root):
		from Tkinter import Frame, Scrollbar, Text, StringVar, Entry, Button
		from Tkinter import LEFT, RIGHT, TOP, BOTTOM, BOTH, X, Y, DISABLED, NORMAL
		
		# Copypaste from http://stackoverflow.com/questions/4220702/terminating-raw-input-if-other-text-displays
		topframe=Frame(root)
		bottomframe=Frame(root)
		bottomframe.pack(side=BOTTOM, fill=X)
		topframe.pack(side=TOP, fill=BOTH)
		scrollbar = Scrollbar(topframe)
		scrollbar.pack(side=RIGHT, fill=Y)
		
		self.text = Text(topframe, yscrollcommand=scrollbar.set)
		self.text.pack(side=LEFT, fill=BOTH)
		scrollbar.config(command=self.text.yview)
		self.text.config(state=DISABLED)
		
		self.v = StringVar()
		e = Entry(bottomframe, textvariable=self.v)
		
		e.bind('<Return>', self.submit)
		button=Button(bottomframe, text='RUN', command=self.submit)
		button.pack(side=RIGHT)
		e.pack(expand=True, side=LEFT, fill=X)
		
	def submit(self, *args):
		command = self.v.get()
		self.v.set('')
		
		self.wprint("> %s" % command)
		self.brain.respond(command)
	
	def wprint(self, obj):
		self.text.config(state=Tkinter.NORMAL)
		self.text.insert(Tkinter.END, str(obj) + '\n')
		self.text.config(state=Tkinter.DISABLED)
	
	def run(self):
		self.create_UI(self.root)
		self.root.mainloop()
		self.root.destroy()
	
	def stop(self):
		self.root.quit()
	
	def say(self, string):
		self.wprint(string)
	def emotion(self, emotion):
		super(Tk, self).emotion(emotion)
		if emotion != None:
			self.wprint(emotion.emote)
	def notify(self, notification = None, title="Untitled", text="No Text"):
		if notification is None:
			notification = Notification(title=title, text=text)
		tkMessageBox.showinfo(title=notification.title, message=notification.text)
		