#at artandlogic.com modles for comment storing)
import HTMLParser
import hashlib
import random
import json
from django.db import models, IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import requests
from TweepyScraper import TweepyScraper
import plain_text_classes

from scrapers.constants import *

from .. import utils

tweepy_consumer_key = 'ZKx8Yg55evn1U65vRWQ0Zj7Jr'
tweepy_consumer_secret = '26OYZDNj0hC17ei6JplHuerzoaxokQBpU9X2dsegkLLCShBK2y'
tweepy_access_token = '14404065-baBGgZmVoCnZEU1L0hCVq6ed6qHDFXVrLSQpAKXcw'
tweepy_access_token_secret = '3jbRjcgZV82OGLOsxv9Xg8G29h1oc9l9kqKTMXH4vEPNi'

USER_TOKEN = "<<user>>"
LINK_TOKEN = "<<link>>"
TAG_TOKEN = "<<tag>>"

#TWITTER VERSION
class TwitterPerson(plain_text_classes.Person, models.Model):
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
          self.twittermention_set.create(content=word)
          word = USER_TOKEN
        if "http" in word:
          self.twitterlink_set.create(content=word)
          word = LINK_TOKEN
        if "#" in word:
          self.twitterhashtag_set.create(content=word)
          word = TAG_TOKEN

        final_tweet = final_tweet + word + " "
      final_tweet = final_tweet[:-1]
      print "final tweet:"
      print final_tweet

      h = HTMLParser.HTMLParser()
      final_tweet = h.unescape(final_tweet.decode('utf-8'))
      
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
      print word1.encode('utf-8')
      print word2.encode('utf-8')
      print final_word.encode('utf-8')

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
    all_caches = self.twitterpostcache_set.all()
    new_markov_post = self.apply_markov_chains_inner(all_beginning_caches, all_caches)

    #Replace the tokens (twitter specific)
    self.replace_tokens(new_markov_post, USER_TOKEN, self.twittermention_set.all())
    self.replace_tokens(new_markov_post, LINK_TOKEN, self.twitterlink_set.all()) 
    self.replace_tokens(new_markov_post, TAG_TOKEN, self.twitterhashtag_set.all())

    randomness = new_markov_post[1]
    content = ""
    for word in new_markov_post[0]:
      content = content + word + " "

    self.twitterpostmarkov_set.create(content=content[:-1], randomness=randomness)

  
  def replace_tokens(self, word_list_and_randomness, token, model_set):
    """
    Takes a list of words and replaces tokens with the 
    corresonding models linked to the user
    """
    word_list = word_list_and_randomness[0]
    for word_index in range(len(word_list)):
      if token in word_list[word_index]:
        seed_index = 0
        if len(model_set) > 1:
          seed_index = random.randint(0, len(model_set)-1)
        try:
          word_list[word_index] = (model_set[seed_index]).content
          print "Replaced " + token

        except IndexError:
          print "failed to replace token:"
          print word_list[word_index]

    return (word_list, word_list_and_randomness[1])

#TWITTER VERSION
class TwitterPost(plain_text_classes.Sentence):
  author = models.ForeignKey(TwitterPerson, default=None, null=True)

#TWITTER VERSION
class TwitterPostCache(plain_text_classes.SentenceCache):
  author = models.ForeignKey(TwitterPerson, default=None, null=True)

#TWITTER VERSION
class TwitterPostMarkov(plain_text_classes.MarkovChain):
  author = models.ForeignKey(TwitterPerson, default=None)

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
  Fille db with metadata from top 50 users
  Used to update avatars etc
  """
  t = TweepyScraper(tweepy_consumer_key, 
    tweepy_consumer_secret,
    tweepy_access_token,
    tweepy_access_token_secret)
  names_and_unames = t.scrape_top_users(50)

  for entry in names_and_unames:
    person = None
    person = TwitterPerson.objects.get_or_create(username=entry['uname'])[0]

    person.username = entry['uname']
    person.real_name= entry['name']
    person.avatar = entry['avatar']
    person.save()

  return names_and_unames
User.add_to_class('scrape_top_twitter_people', scrape_top_twitter_people)
