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

<<<<<<< HEAD
			post = TwitterPost.objects.get_or_create(author=self, \
																				content=final_tweet)[0]
			post.save()
=======
			TwitterPost.objects.get_or_create(author=self, \
																				content=final_tweet)
			TwitterPost.save()
>>>>>>> 1bcaa646c41495b3e7af694c1d732836252d0b74

	def apply_markov_chains(self):
		"""
		Just roll this into the actual calculation and have it make the django objects
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
		markov_twitter_post = m.generate_markov_twitter_post()

		parent = TwitterPostMarkov.objects.create(author=self)
		for pair in markov_twitter_post:
			content = pair[0]
			id = pair[1]
			part = TwitterPostMarkovPart.objects.get_or_create(
								parent_post=parent,
								content=content, 
								original_tweet_id=id)
			part[0].save()

		parent.save()
		return 

	def get_full_markov_posts(self):
		"""
		Look though the markov posts and their corresponding
		parts and return composite posts for the views

		returns list of strings
		"""
		all_composite_parts = []
	
		for m_post in self.twitterpostmarkov_set.all():
			part_string = ""
			for m_part in m_post.twitterpostmarkovpart_set.all():
				part_string = part_string + " " + m_part.content
			all_composite_parts.append(part_string[:-1])

		return all_composite_parts
			

class TwitterPost(models.Model):
	author = models.ForeignKey(TwitterPerson, default=None, null=True)
	content = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
		
	def __str__(self):
		return self.content

class TwitterPostMarkov(models.Model):
	author = models.ForeignKey(TwitterPerson, default=None, null=True)

	def __str__(self):
		all_parts = TwitterPostMarkovPart.objects.filter(parent_post__id=self.id)
		content = ''
		for part in all_parts:
			content += part.content

		return_str = \
				' author: ' + str(self.author) + '\n' + \
				' content: ' + content
		return return_str

class TwitterPostMarkovPart(models.Model):
	parent_post = models.ForeignKey(TwitterPostMarkov)
	content = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
	original_tweet_id = models.IntegerField(default=0)

	def __str__(self):
		return self.content

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
