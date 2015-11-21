from django.test import Client, TestCase
from TweepyScraper import TweepyScraper
from .models import FacebookPerson, FacebookPost, TwitterPerson, TwitterPost
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import facebook

class FacebookPersonMethodTests(TestCase):
  def test_poster_name_is_valid(self):
    """
    The poster name should be something valid
    do not allow empty strings
    """
    failed = 'idk'
    try:
      p = FacebookPerson(username='')
      p.full_clean()
    except ValidationError:
      failed = 'yes'
    
    self.assertEqual(failed,'yes')

  

class FacebookPostMethodTests(TestCase):
  def test_post_is_nonempty(self):
    """
    FacebookPosts must have content.
    """
    failed = 'idk'
    try:
      tom = FacebookPerson(username='Tom')
      tom.save()
      p = FacebookPost(author=tom,index=0,content='')
      p.full_clean()
    except ValidationError:
      failed = 'yes'
  
    self.assertEqual(failed,'yes')

class TwitterPersonMethodTests(TestCase):
  def test_can_grab_twitter_top_users(self):
    """
    Can scape the top top twitter accounts?
    """ 
    failed = 'idk'
    top_users = []
    try:
      tom = User(username='tom')
      tom.save()
      top_users = tom.scrape_top_twitter_people()
    except ValidationError:
      failed = 'yes'

    self.assertNotEqual(top_users, [])

class TweepyTests(TestCase):
  def test_tweepy_can_scrape_top_users(self):
    tweepy_consumer_key = 'ZKx8Yg55evn1U65vRWQ0Zj7Jr'
    tweepy_consumer_secret = '26OYZDNj0hC17ei6JplHuerzoaxokQBpU9X2dsegkLLCShBK2y'
    tweepy_access_token = '14404065-baBGgZmVoCnZEU1L0hCVq6ed6qHDFXVrLSQpAKXcw'
    tweepy_access_token_secret = '3jbRjcgZV82OGLOsxv9Xg8G29h1oc9l9kqKTMXH4vEPNi'

    t = TweepyScraper(tweepy_consumer_key, tweepy_consumer_secret, tweepy_access_token, tweepy_access_token_secret)

    names_and_unames = t.scrape_top_users(50)

    print names_and_unames



class FacebookStatusTests(TestCase):
  def test_feed_scrape(self):
    """
    Grabs the user - me - verifies ability to read the feed 
    """
    """
    c = Client()
    response = c.post('/admin/',
      {'username': 'admin', 'password': 'password'})
    response = c.get('/admin/auth/user//')
    """
    #SELENIUM
    """
    user = User.objects.create_user(username='TomCraig',
      email='thetomcraig@icloud.com')
    auth = user.social_auth.first()
    graph = facebook.GraphAPI(auth.extra_data['access_token'])
    print graph.get_object('/me/home')
    """
    #user = User.objects.get(email='thetomcraig@icloud.com')
    #user = FBUser()
    #user.scrape_feed()
    pass
