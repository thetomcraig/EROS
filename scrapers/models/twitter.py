#at artandlogic.com modles for comment storing)

import hashlib
import random
import json
from django.db import models, IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import requests
from TweepyScraper import TweepyScraper
from Markov import Markov 

from scrapers.constants import *

tweepy_consumer_key = 'ZKx8Yg55evn1U65vRWQ0Zj7Jr'
tweepy_consumer_secret = '26OYZDNj0hC17ei6JplHuerzoaxokQBpU9X2dsegkLLCShBK2y'
tweepy_access_token = '14404065-baBGgZmVoCnZEU1L0hCVq6ed6qHDFXVrLSQpAKXcw'
tweepy_access_token_secret = '3jbRjcgZV82OGLOsxv9Xg8G29h1oc9l9kqKTMXH4vEPNi'


#Classes for storing twitter data
class TwitterPerson(User, models.Model):
	real_name = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
	avatar = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
	happiness = models.IntegerField(default=0)

	def __str__(self):
		return self.username

	def scrape(self):
		"""
		Scrape the given user with tweepy
		take all of their tweets and 
		turn them into TwitterPost objects
		strip out uncommon words (links, hashtags, users)
		and save them seperately in instances, then
		replace with dummy words.
		"""
		t = TweepyScraper(tweepy_consumer_key, 
			tweepy_consumer_secret,
			tweepy_access_token,
			tweepy_access_token_secret)

		tweets = t.get_tweets_from_user(self.username, 100)
		print "scraped %d new tweets" % len(tweets)
		new_post_ids = []
		for tweet in tweets:
			words = tweet.split()

			if ('RT' in tweet):
				print "skipping retweets"
				continue
			if (len(words) < 1):
				print "skipping short tweets"
				continue
	
			final_tweet = ""
			for word in words:
				if "@" in word:
					new_mention = TwitterMention(author=self, content=word)
					word = "<<user>>"
				if "http" in word:
					new_link = TwitterLink(author=self, content=word)
					word = "<<link>>"
				if "#" in word:
					new_tag  = TwitterHashtag(author=self, content=word)
					word = "<<tag>>"
				final_tweet = final_tweet + word + " "
			final_tweet = final_tweet[:-1]
			print "final tweet:"
			print final_tweet
		
			post = TwitterPost.objects.create(author=self, content=final_tweet)
			self.create_post_cache(post)
			new_post_ids.append(post.id)

		return new_post_ids

	def create_post_cache(self, post):
		"""
		Create the postcache item from the new post
		to be used to make the markov post
		"""
		word_list = post.content.split()
		for index in range(len(word_list)-2):
			print "caching:"
			word1 = word_list[index]
			word2 = word_list[index+1]
			final_word = word_list[index+2]
			print word1
			print word2
			print final_word

			beginning = False
			if (index == 0):
				beginning = True
			post_cache = TwitterPostCache(author=self, word1=word1, word2=word2, final_word=final_word, beginning=beginning)
			post_cache.save()


	def apply_markov_chains(self):
		"""
		Takes all the words from all the twittter 
		posts on the twitterperson.  
		Sticks them all into a giant 
		list and gives this to the markov calc.
		Save this as a new twitterpostmarkov
		"""
		print "Applying markov chains"
		all_beginning_caches = self.twitterpostcache_set.filter(beginning=True)
		seed_index = random.randint(0, len(all_beginning_caches)-1)
		seed_cache = all_beginning_caches[seed_index]

		all_caches = self.twitterpostcache_set.all()
		new_markov_post = []
		w0 = seed_cache.word1
		w1 = seed_cache.word2
		w2 = seed_cache.final_word
		new_markov_post.append(w0)
		new_markov_post.append(w1)

		while True:
			try:
				new_markov_post.append(w2)
				next_cache = all_caches.filter(word1=w1, word2=w2)[0]
				w1 = next_cache.word2
				w2 = next_cache.final_word
					
			except Exception as e:
				print e
				break
	
		#Done making the post
		print new_markov_post

		#self.twitterpostmarkov_set.create(content=markov_sentence, randomness=randomness)


class TwitterPost(models.Model):
	author = models.ForeignKey(TwitterPerson, default=None, null=True)
	content = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
	happiness = models.FloatField(default=0)
		
	def __str__(self):
		return self.content

	def sentiment_analyze(self):
		self.happiness = 5
		

class TwitterPostMarkov(models.Model):
	author = models.ForeignKey(TwitterPerson, default=None, null=True)
	content = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
	original_tweet_id = models.IntegerField(default=0)
	randomness = models.FloatField(default=0.0)

	def __str__(self):
		return ' author: ' + str(self.author) + '\n' + \
						' content: ' + self.content

class TwitterLink(models.Model):
	author = models.ForeignKey(TwitterPerson)
	content = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)

	def __str__(self):
		return self.content
	
class TwitterHashtag(models.Model):
	author = models.ForeignKey(TwitterPerson)
	content = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)

	def __str__(self):
		return self.content

class TwitterMention(models.Model):
	author = models.ForeignKey(TwitterPerson)
	content = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)

	def __str__(self):
		return self.content

class TwitterPostCache(models.Model):
	"""
	Used to cache words from the original posts
	the markov posts uses these
	"""
	author = models.ForeignKey(TwitterPerson, default=None, null=True)
	word1 = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
	word2 = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
	final_word = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
	beginning = models.BooleanField(default=False)


def scrape_top_twitter_people(self):
	"""
	Fille db with metadata from top 50 users
	Used to update avatars etc
	"""
	t = TweepyScraper(tweepy_consumer_key, 
		tweepy_consumer_secret,
		tweepy_access_token,
		tweepy_access_token_secret)
	names_and_unames = t.scrape_top_users(50)
	for entry in names_and_unames:
		existing_person = TwitterPerson.objects.get_or_create(username=entry['uname'])[0]
		existing_person.real_name = entry['name']
		existing_person.avatar = entry['avatar']
		existing_person.save()

	return names_and_unames
User.add_to_class('scrape_top_twitter_people', scrape_top_twitter_people)
