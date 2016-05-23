import random

def read_source_into_sentance_list(source_file):
	"""
	Reads a text file and returns its contents as list of sentances
	Split at punctuations
	Ignores words with punctuation in them, like Mr. and Mrs.
	"""
	lines = []
	punctuations = [".", "!", "?"]
	ignored_words = ["Mr.", "Mrs."]
	with open(source_file, "r") as file:
		line = []
		for file_line in file:
			for word in file_line.split():
				line.append(word)
				if any(p in word for p in punctuations):
					if all(not i in word for i in ignored_words):					
						lines.append(line)
						line = []

	return lines


def apply_markov_chains_inner(beginning_caches, all_caches):
	"""
	Takes a series of caches, with two consecutive words mapped to at third
	Starts with a random choice from the beginning caches
	makes random choices from the all_caches set, constructing a markov chain 
	'randomness' value determined by totalling the number of words that were chosen
	randomly
	"""
	new_markov_chain = []
	randomness = -0.0

	if not beginning_caches:
		print "Not enough data, skipping"
		return (new_markov_chain, randomness)

	seed_index = 0
	if len(beginning_caches) != 0:
		seed_index = random.randint(0, len(beginning_caches)-1)
	seed_cache = beginning_caches[seed_index]

	w0 = seed_cache.word1
	w1 = seed_cache.word2
	w2 = seed_cache.final_word
	new_markov_chain.append(w0)
	new_markov_chain.append(w1)

	#percentage, calculated by the number of random 
	#choices made to create the markov post
	randomness = 0
	while True:
		try:
			new_markov_chain.append(w2)
			all_next_caches = all_caches.filter(word1=w1, word2=w2)
			next_cache_index = random.randint(0, len(all_next_caches)-1)
			next_cache = all_next_caches[next_cache_index]
			w1 = next_cache.word2
			w2 = next_cache.final_word

			if len(all_next_caches) > 1:
				randomness = randomness + 1
				
		except Exception as e:
			print e
			break

	#Determind random level, and save the post
	randomness = 1.0 - float(randomness)/len(new_markov_chain)
	#Done making the post

	return (new_markov_chain, randomness)


