import sys, os
from meidobot.core import Meido
from meidobot.ui import CLI

def main(argv):
	brain = Meido(os.path.dirname(os.path.abspath(__file__)), 'config.json')
	brain.ui = CLI(brain)
	brain.load_plugins()
	brain.run()
	
if __name__ == "__main__":
	main(sys.argv)
