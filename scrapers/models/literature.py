from django.db import models
from scrapers.constants import *
from .. import utils
import plain_text_classes

#LITERATURE VERSION
class LiteraturePerson(plain_text_classes.Person):
	happiness = models.IntegerField(default=0)

	def __str__(self):
		return self.username

	def scrape(self,input_text_as_sentences):
		for sentence in input_text_as_sentences:
		
			sentence = Sentence.objects.create(author=self, content=final_sentence)
			self.cache_sentence(sentence)

	def cache_sentence(self, sentence):
		"""
		"""
		word_list = sentence.content.split()
		for index in range(len(word_list)-2):
			word1 = word_list[index]
			word2 = word_list[index+1]
			final_word = word_list[index+2]

			print "caching:"
			print word1.encode('utf-8')
			print word2.encode('utf-8')
			print final_word.encode('utf-8')

			post_cache = SentenceCache(
				author=self, 
				word1=word1, 
				word2=word2, 
				final_word=final_word, 
				beginning=(index==0))
			post_cache.save()

	def apply_markov_chains(self):
		"""
		"""
		print "Applying markov chains"
		all_beginning_caches = self.sentencepostcache_set.filter(beginning=True)
		all_caches = self.sentencecache_set.all()
		new_markov_post = self.apply_markov_chains_inner(all_beginning_caches, all_caches)

		randomness = new_markov_post[1]
		content = ""
		for word in new_markov_post[0]:
			content = content + word + " "

		self.sentencemarkov_set.create(content=content[:-1], randomness=randomness)

#LITERATURE VERSION
class LiteratureSentence(plain_text_classes.Sentence):
	author = models.ForeignKey(LiteraturePerson, default=None, null=True)
		
#LITERATURE VERSION
class LiteratureSentenceMarkov(plain_text_classes.MarkovChain):
	author = models.ForeignKey(LiteraturePerson, default=None)

class SentenceCache(plain_text_classes.SentenceCache):
	author = models.ForeignKey(LiteraturePerson, default=None, null=True)

