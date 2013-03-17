import sys, os
from meidobot.core import Meido

def main(argv):
	brain = Meido(os.path.dirname(os.path.abspath(__file__)), 'config.json')
	if "--cli" in sys.argv:
		from meidobot.ui.cli import CLI
		brain.ui = CLI(brain)
	else:
		try:
			from meidobot.ui.qt import QtUI
			brain.ui = QtUI(brain)
		except ImportError:
			try:
				from meidobot.ui.tk import TkUI
				brain.ui = TkUI(brain)
			except ImportError:
				from meidobot.ui.cli import CLI
				brain.ui = CLI(brain)
	brain.load_plugins()
	brain.run()
	
if __name__ == "__main__":
	main(sys.argv)
