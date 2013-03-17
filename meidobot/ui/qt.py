import sys, os
from PySide.QtCore import *
from PySide.QtGui import *
from meidobot.ui.ui import UI

class MainWindow(QWidget):
	brain = None
	
	def __init__(self, brain, parent=None):
		super(MainWindow, self).__init__(parent)
		self.brain = brain
		
		# All three are needed to get a transparent window
		self.setStyleSheet("background:transparent;");
		self.setAttribute(Qt.WA_TranslucentBackground);
		self.setWindowFlags(Qt.FramelessWindowHint);
		
		screenSize = QDesktopWidget().availableGeometry()
		windowSize = self.sizeHint()
		self.move(screenSize.width() - windowSize.width(), screenSize.height() - windowSize.height())
		
		self.setup()
		self.createTrayIcon()
	
	def setup(self):
		self.pixmap = QPixmap(os.path.join(self.brain.base_path, "resources/icon.png"))
		
		self.label = QLabel(self)
		self.label.setPixmap(self.pixmap.scaled(self.sizeHint(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
	
	def createTrayIcon(self):
		iconPath = os.path.join(self.brain.base_path, "resources/icon.png")
		icon = QIcon(iconPath)
		
		self.trayMenu = QMenu(self)
		self.trayMenu.addAction(QAction("&Appear", self, triggered=self.on_activate))
		self.trayMenu.addAction(QAction("&Disappear", self, triggered=self.on_deactivate))
		self.trayMenu.addSeparator()
		self.trayMenu.addAction(QAction("&Exit", self, triggered=self.on_exit))
		
		self.trayIcon = QSystemTrayIcon(self)
		self.trayIcon.setIcon(icon)
		self.trayIcon.setContextMenu(self.trayMenu)
		self.trayIcon.activated.connect(self.on_activate)
		self.trayIcon.show()
		
		print self.trayIcon
	
	def on_activate(self):
		print "Activate"
		self.show()
	
	def on_deactivate(self):
		print "Deactivate"
		self.hide()
	
	def on_exit(self):
		self.brain.stop()
	
	def mousePressEvent(self, event):
		if event.buttons() == Qt.LeftButton:
			print "Left Click"
			event.accept()
		elif event.buttons() == Qt.RightButton:
			print "Right Click"
			self.on_deactivate()
			event.accept()
	
	def sizeHint(self):
		return QSize(200, 200)

class QtUI(UI):
	def __init__(self, brain):
		super(QtUI, self).__init__(brain)
		
		self.application = QApplication(sys.argv)
		self.window = MainWindow(self.brain)
		
	def run(self):
		self.window.show()
		self.application.exec_()
	
	def stop(self):
		self.application.exit()