import sys, os
from MeidoParser import MeidoParser
from MeidoUI import MeidoCLI
from MeidoBrain import MeidoBrain
import plugins.system

def main(argv):
	brain = MeidoBrain()
	brain.parser = MeidoParser(brain)
	brain.ui = MeidoCLI(brain)
	brain.load_plugins()
	
	while True:
		input = raw_input("> ")
		brain.respond(input)

if __name__ == "__main__":
	main(sys.argv)
