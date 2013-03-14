import sys, os
from meidobot.core import Meido
from meidobot.ui import CLI

def main(argv):
	brain = Meido()
	brain.ui = CLI(brain)
	brain.load_plugins(os.path.dirname(os.path.abspath(__file__)))
	brain.run()

if __name__ == "__main__":
	main(sys.argv)
