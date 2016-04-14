import random
import re

class Markov(object):
	
	def __init__(self):
		self.cache = {}
		self.words = []
		self.word_size = len(self.words)
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

	def generate_markov_twitter_post(self):
		self.word_size = len(self.words)
		if self.word_size < 4:
			return []
		size = 10
		seed = random.randint(0, self.word_size-3)
		seed_word, next_word = self.words[seed], self.words[seed+1]
		w1, w2 = seed_word[0], next_word[0]
		w1_key = seed_word[1]
		w2_key = next_word[1]

		gen_words = []

		for i in xrange(size):
			gen_words.append((w1,w1_key))
			
			#search for a tuple but with the words and ignore the keys
			possible_next_words = self.cache[((w1,w1_key),(w2,w2_key))]
			#chose RANDOMLY intead of [0]
			(w1,w1_key), (w2,w2_key) = (w2,w2_key), possible_next_words[0]
		gen_words.append((w2,w2_key))

		return gen_words
