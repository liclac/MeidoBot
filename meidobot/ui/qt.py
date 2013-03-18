import sys, os
from PySide.QtCore import *
from PySide.QtGui import *
from meidobot.ui.ui import UI

class Bubble(QWidget):
	opacity = 0.75
	roundness = 10
	color = QColor.fromRgb(255, 255, 255)
	
	def __init__(self, ui):
		super(Bubble, self).__init__()
		self.ui = ui
		
		#print self.__class__.__name__
		# All three are needed to get a transparent window
		self.setStyleSheet("background:transparent;")
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.setWindowFlags(Qt.FramelessWindowHint)
		
		self.setFocusPolicy(Qt.NoFocus)
	
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.save()
		
		path = QPainterPath()
		path.addRoundedRect(self.rect(), self.roundness, self.roundness)
		painter.setClipPath(path)
		
		painter.setOpacity(self.opacity)
		painter.fillPath(path, QBrush(self.color))
		
		painter.restore()
	
	def mousePressEvent(self, event):
		self.ui.window.on_activate()
	
	def __str__(self):
		return "<%s>" % self.__class__.__name__

class SpeechBubble(Bubble):
	color = QColor.fromRgb(150, 150, 255)
	
	def __init__(self, text, ui):
		super(SpeechBubble, self).__init__(ui)
		
		layout = QVBoxLayout()
		layout.setContentsMargins(5, 5, 5, 5)
		self.label = QLabel(self)
		self.label.setText(text)
		layout.addWidget(self.label)
		self.setLayout(layout)
	
	def __str__(self):
		return "<Speech Bubble: %s>" % self.label.text()

class InputBubble(Bubble):
	opacity = 1
	ui = None
	
	def __init__(self, ui):
		super(InputBubble, self).__init__(ui)
		
		layout = QVBoxLayout()
		layout.setContentsMargins(5, 5, 5, 5)
		
		self.field = QLineEdit(self)
		self.field.returnPressed.connect(self.on_return_pressed)
		
		layout.addWidget(self.field)
		self.setLayout(layout)
	
	def on_return_pressed(self):
		self.field.setReadOnly(True)
		self.field.setFrame(False)
		self.ui.respond(self.field.text())
	
	def __str__(self):
		return "<Input Bubble>"

class MainWindow(QWidget):
	brain = None
	bubbles = []
	
	def __init__(self, ui, brain, parent=None):
		super(MainWindow, self).__init__(parent)
		self.ui = ui
		self.brain = brain
		
		# All three are needed to get a transparent window
		self.setStyleSheet("background:transparent;")
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.setWindowFlags(Qt.FramelessWindowHint)
		
		screenSize = QDesktopWidget().availableGeometry()
		windowSize = self.sizeHint()
		self.move(screenSize.width() - windowSize.width(), screenSize.height() - windowSize.height())
		
		self.setup()
		self.createTrayIcon()
	
	def sizeHint(self):
		return QSize(200, 200)
	
	def setup(self):
		self.pixmap = QPixmap(os.path.join(self.brain.base_path, "resources/icon.png"))
		
		self.label = QLabel(self)
		self.label.setPixmap(self.pixmap.scaled(self.sizeHint(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
	
	def createTrayIcon(self):
		iconPath = os.path.join(self.brain.base_path, "resources/icon.png")
		icon = QIcon(iconPath)
		
		self.trayMenu = QMenu(self)
		#self.trayMenu.addAction(QAction("&Appear", self, triggered=self.on_activate))
		#self.trayMenu.addAction(QAction("&Disappear", self, triggered=self.on_deactivate))
		#self.trayMenu.addSeparator()
		self.trayMenu.addAction(QAction("&Exit", self, triggered=self.on_exit))
		
		self.trayIcon = QSystemTrayIcon(self)
		self.trayIcon.setIcon(icon)
		self.trayIcon.setContextMenu(self.trayMenu)
		self.trayIcon.activated.connect(self.on_activate)
		self.trayIcon.show()
	
	def mousePressEvent(self, event):
		if event.buttons() == Qt.LeftButton:
			print "Left Click"
			self.on_activate()
			event.accept()
		elif event.buttons() == Qt.RightButton:
			print "Right Click"
			self.on_deactivate()
			event.accept()
	
	def on_activate(self):
		print "Activate"
		self.show()
		self.clear_bubbles()
		if len(self.bubbles) == 0:# or type(self.bubbles[-1]) is not InputBubble:
			self.push_bubble(InputBubble(self.ui))
		self.bubbles[-1].raise_()
		self.bubbles[-1].setFocus()
	
	def on_deactivate(self):
		print "Deactivate"
		
		for bubble in self.bubbles:
			print "- deleting %s" % bubble
			bubble.deleteLater()
		self.bubbles = []
		
		#self.hide()
	
	def on_exit(self):
		self.brain.stop()
	
	def push_bubble(self, bubble):
		print "Pushing %s" % bubble
		bubble.show()
		bubble.move(self.pos().x() - bubble.size().width(), self.pos().y())
		for old_bubble in self.bubbles:
			old_bubble.move(old_bubble.pos().x(), old_bubble.pos().y() - bubble.size().height() - 10)
		self.bubbles.append(bubble)
	def clear_bubbles(self):
		for bubble in self.bubbles:
			bubble.hide()
			bubble.deleteLater()
		self.bubbles = []

class QtUI(UI):
	def __init__(self, brain):
		super(QtUI, self).__init__(brain)
		
		self.application = QApplication(sys.argv)
		QApplication.setQuitOnLastWindowClosed(False)
		self.window = MainWindow(self, self.brain)
		
	def run(self):
		self.window.show()
		self.window.push_bubble(InputBubble(self))
		self.application.exec_()
	
	def stop(self):
		self.application.exit()
	
	def say(self, text):
		self.window.push_bubble(SpeechBubble(text, self))
	
	def respond(self, string):
		self.brain.respond(string)
		self.window.push_bubble(InputBubble(self))
