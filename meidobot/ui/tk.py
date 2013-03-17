from meidobot.ui.ui import UI
from Tkinter import *

class TkUI(UI):
	def __init__(self, brain):
		super(TkUI, self).__init__(brain)
		self.root = Tk()
	
	def create_UI(self, root):
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
		self.text.config(state=NORMAL)
		self.text.insert(END, str(obj) + '\n')
		self.text.config(state=DISABLED)
	
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