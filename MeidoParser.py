import string, json
from pprint import pprint

class MeidoParserResult(object):
	string = ""
	words = {}
	
	verbs = {}
	objects = {}
	subjects = {}
	
	def __str__(self):
		return "<\n\tMeidoParserResult of '%s':\n\t- W: { %s }\n\t- V: { %s }\n\t- O: { %s }\n\t- S: { %s }\n>" % (self.string, ', '.join(self.words), ', '.join(self.verbs), ', '.join(self.objects), ', '.join(self.subjects))

class MeidoParser(object):
	brain = None
	
	verbs = {'look', 'check', 'exit'}
	objects = {'mail', 'email', 'syslog'}
	subjects = {'me', 'my', 'you', 'your'}
	
	def __init__(self, brain):
		self.brain = brain
	
	def parse(self, s):
		'''Parses an input string and returns '''
		res = MeidoParserResult()
		res.string = self.normalize(s)
		res.words = set(res.string.split())
		res.verbs = res.words & self.verbs
		res.objects = res.words & self.objects
		res.subjects = res.words & self.subjects
		return res
		
	def normalize(self, s):
		'''Normalizes a given string for further processing'''
		return s.translate(None, string.punctuation).lower()
	
	def learn(self, set, words):
		'''Teaches the parser to recognize the given word'''
		for word in words: set.add(word)
	def learn_verbs(self, words): self.learn(self.verbs, words)
	def learn_objects(self, words): self.learn(self.objects, words)
	def learn_subjects(self, words): self.learn(self.subjects, words)