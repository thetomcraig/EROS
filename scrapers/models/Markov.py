import random
import re

class Markov(object):
	
	def __init__(self):
		self.cache = {}
		self.words = []
		self.database()
	
	def triples(self):
		""" 
		Generates triples from the given data string. So if our string were
		"What a lovely day", we'd generate (What, a, lovely) and then
		(a, lovely, day).
		"""
		
		if len(self.words) < 3:
			return
		
		for i in range(len(self.words) - 2):
			yield (self.words[i], self.words[i+1], self.words[i+2])
			
	def database(self):
		for w1, w2, w3 in self.triples():
			key = (w1, w2)
			if key in self.cache:
				self.cache[key].append(w3)
			else:
				self.cache[key] = [w3]

	def generate_markov_sentence(self, length=None):
		"""
		Generates the markov twitter
		"""
		unoriginal_words = 0
		if not length:
			length=10
		
		word_size = len(self.words)
		if word_size < 4:
			return []
		seed = random.randint(0, word_size-3)
		seed_word, next_word = self.words[seed], self.words[seed+1]
		w1, w2 = seed_word, next_word
		gen_words = []

		for i in xrange(length):
			gen_words.append(w1)
			
			#search for a tuple but with the words and ignore the keys
			if len(self.cache[w1, w2]) > 1:
				unoriginal_words = unoriginal_words + 1
			w1, w2 = w2, random.choice(self.cache[w1, w2])
		#add fina word
		gen_words.append(w2)

		if unoriginal_words == 0:
			randomness = 0
		else:
			randomness = float(unoriginal_words)/(length-1)
		return gen_words, randomness
