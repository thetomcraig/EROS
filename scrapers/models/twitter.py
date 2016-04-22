#at artandlogic.com modles for comment storing)

import hashlib
import json
from django.db import models, IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import requests
from TweepyScraper import TweepyScraper
from Markov import Markov 

from constants import *

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
		new_post_ids = []
		for tweet in tweets:
			words = tweet.split()

			if ('RT' in tweet):
				continue
			if (len(words) < 1):
				continue
	
			final_tweet = ""
			for word in words:
				if "@" in word:
					new_mention = TwitterMention(author=self, content=word)
					word = "@user"
				if "http" in words[0]:
					new_link = TwitterLink(author=self, content=word)
					word = "link"
				if "#" in words[0]:
					new_tag  = TwitterHashtag(author=self, content=word)
					word = "#tag"
				final_tweet = final_tweet + word + " "
			final_tweet = final_tweet[:-1]

			post = TwitterPost.objects.get_or_create(author=self, \
																				content=final_tweet)[0]
			post.save()
			new_post_ids.append(post.id)
		return new_post_ids

	def apply_markov_chains(self):
		"""
		Takes all the words from all the twittter 
		posts on the twitterperson.  
		Sticks them all into a giant 
		list and gives this to the markov calc.
		Save this as a new twitterpostmarkov
		"""

		#Make this take in instance of tpmpart
		#The markov stuff to keep here
		#Now to the markov calc
		#Generates single post
		words = []
		for twitter_post in self.twitterpost_set.all():
			for word in twitter_post.content.split():
				words.append(word)

		m = Markov() 
		m.words = words
		m.database()
		markov_sentence = m.generate_markov_sentence(length=10)

		self.twitterpostmarkov_set.create(content=markov_sentence)


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

def scrape_top_twitter_people(self):
	"""
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
