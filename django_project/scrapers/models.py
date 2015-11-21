#at artandlogic.com modles for comment storing)

import hashlib
import json
from django.db import models, IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import facebook
import requests
from TweepyScraper import TweepyScraper
from Markov import Markov 

tweepy_consumer_key = 'ZKx8Yg55evn1U65vRWQ0Zj7Jr'
tweepy_consumer_secret = '26OYZDNj0hC17ei6JplHuerzoaxokQBpU9X2dsegkLLCShBK2y'
tweepy_access_token = '14404065-baBGgZmVoCnZEU1L0hCVq6ed6qHDFXVrLSQpAKXcw'
tweepy_access_token_secret = '3jbRjcgZV82OGLOsxv9Xg8G29h1oc9l9kqKTMXH4vEPNi'

#Classes for storing fb data
class FacebookPerson(User, models.Model):
  def __str__(self):
    return username

class FacebookPost(models.Model):
  author = models.ForeignKey(FacebookPerson, default=None, null=True)
  index = models.IntegerField(default=0)
  story = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
  message = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
  picture = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
  link = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
  content = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
    
  def __str__(self):
    return_str = \
        ' author: ' + str(self.author) + '\n' + \
        ' index: ' + str(self.index) + '\n' + \
        ' story: '  +str(self.story) + '\n' + \
        ' message: ' + str(self.message) + '\n' + \
        ' picture: ' + str(self.picture) + '\n' + \
        ' link: ' + str(self.link) + '\n' + \
        ' content: ' + self.content
    return return_str

#Classes for storing twitter data
class TwitterPerson(User, models.Model):
  real_name = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
  avatar = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
  def __str__(self):
    return self.username

class TwitterPost(models.Model):
  author = models.ForeignKey(TwitterPerson, default=None, null=True)
  content = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
    
  def __str__(self):
    return_str = \
        ' author: ' + str(self.author) + '\n' + \
        ' content: ' + self.content
    return return_str

class TwitterPostMarkov(models.Model):
  author = models.ForeignKey(TwitterPerson, default=None, null=True)
  content = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
  ids = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
  
  def set_ids(self, ids_as_list):
    self.ids = json.dumps(ids_as_list)
   
  def get_ids(self):
    return json.loads(self.ids)
 
  def __str__(self):
    return_str = \
        ' author: ' + str(self.author) + '\n' + \
        ' content: ' + self.content
    return return_str

#Classes for scraping and collecting data
def get_clean_fb_feed(self):
  """
  For interpreting the raw facebook information and 
  storing corresponding objects in the db
  """

  auth = self.social_auth.first()
  graph = facebook.GraphAPI(auth.extra_data['access_token']) 
  raw_data = graph.get_object('/me/home')
 
  data = None
  for key in raw_data:
    if key == 'data':
      data = raw_data[key]
      break 

  if (data == None):
    return data

  clean_data = [
  {
    'from' : x['from']['name'],
    'name' : x.get('name'),
    'story' : x.get('story'),
    'message' : x.get('message'),
    'picture' : x.get('picture'),
    'link' : x.get('link'),
    'friends' : x.get('friends'),
    'comments' : process_comments(x.get('comments'))
  } for x in data]

  return clean_data
User.add_to_class('get_clean_fb_feed', get_clean_fb_feed)


def save_clean_fb_feed(self):
  """
  Takes clean fb data and saves it to the db
  """
 
  clean_data = self.get_clean_fb_feed()
  
  post_owner = User.objects.get_or_create(username="SELF")
  
  for raw_post in clean_data:
    content = {}
    content['story'] = raw_post['story']
    content['message'] = raw_post['message']
    content['picture'] = raw_post['picture']
    content['link'] = raw_post['link']
    content['friends'] = raw_post['story']
    #I want to loop through comments as well

    message=raw_post['message']
    story=raw_post['story']
    poster = User.objects.get_or_create(username=raw_post['from'])
    post = FacebookPost.objects.get_or_create(poster=poster[0],
      index=0,
      story=content['story'],
      message=content['message'],
      picture=content['picture'],
      link=content['link'], 
      content=content
    )
User.add_to_class('save_clean_fb_feed', save_clean_fb_feed)

def process_comments(comments):
  """
  Organizes the comment data into a dictionary
  """
  
  if (comments == None):
    return None
 
  data = comments.get('data')
  if (data == None):
    return None
  
  clean_data = [
  [
    {'from' : x['from']['name']},
    {'message' : x.get('message')},
    {'like count' : x.get('like_count')}
  ] for x in data]

  return clean_data

def scrape_top_twitter_people(self):
  """
  """
  t = TweepyScraper(tweepy_consumer_key, 
    tweepy_consumer_secret,
    tweepy_access_token,
    tweepy_access_token_secret)
  names_and_unames = t.scrape_top_users(50)
  for entry in names_and_unames:

    #get the obj if its in the db
    #if it is, update the avatar code 
    try:
      existing_person = TwitterPerson.objects.get(username=entry['uname'])
      existing_person.avatar = entry['avatar']
      existing_person.save()
    except:
      TwitterPerson.objects.create(
        username=entry['uname'],
        real_name=entry['name'],
        avatar=entry['avatar']
      )

  return names_and_unames
User.add_to_class('scrape_top_twitter_people', scrape_top_twitter_people)

def scrape_twitter_person(self, uname):
  """
  """
  t = TweepyScraper(tweepy_consumer_key, 
    tweepy_consumer_secret,
    tweepy_access_token,
    tweepy_access_token_secret)

  tweets = t.get_tweets_from_user(uname, 100)
  person = TwitterPerson.objects.get_or_create(username=uname)
  for tweet in tweets:
    if ('RT' in tweet):
      continue
    if (len(tweet.split()) < 4):
      continue
    
    TwitterPost.objects.get_or_create(author=person[0], content=tweet)

  return tweets
User.add_to_class('scrape_twitter_person', scrape_twitter_person)

def apply_markov_chains(self, author, twitter_posts):
  """
  """
  m = Markov() 
  words = []
  for twitter_post in twitter_posts:
    hex_key = hashlib.md5(twitter_post.encode('utf-8').strip()).hexdigest()
    key = str(int(hex_key, 16) % 100)
    for word in twitter_post.split():
      words.append((word.encode('utf-8'),key))

  #To better test the m chains - generalize users and pics/links
  for i in range (len(words)):
    if "@" in words[i][0]:
      words[i] = ("@user", words[i][1])
    if "http" in words[i][0]:
      words[i] = ("link", words[i][1])
    if "#" in words[i][0]:
      words[i] = ("#tag", words[i][1])

  m.words = words
  m.database()
  markov_twitter_post = m.generate_markov_twitter_post()
  text = ''
  tweet_ids = []
  for pair in markov_twitter_post:
    text += (' ' + pair[0])
    tweet_ids.append(pair[1]) 
   
  post = TwitterPostMarkov.objects.get_or_create(author=author, content=text)
  post[0].set_ids(tweet_ids)

  return 
User.add_to_class('apply_markov_chains', apply_markov_chains)
