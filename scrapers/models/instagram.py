from django.db import models
from django.contrib.auth.models import User
from django.conf import settings 
import plain_text_classes

from scrapers.InstagramAPI.InstagramAPI import InstagramAPI

# INSTAGRAM VERSION
class InstagramPerson(plain_text_classes.Person):
    def collect_hashtags(self):
        """
        Look at my timeline and collect posts
        Strip out hash tabs and save them as objects
        """
        api = InstagramAPI(settings.instagram_username, settings.instagram_password)
        api.login() 
        api.timelineFeed()
        result = api.LastJson

        if result['status'] != 'ok':
            pass

        num_results = result['num_results']

        items = result['items']

        for item in items:
            print item['user']['username']
            print item['user']['full_name']
            print item['user']['profile_pic_url']
            
            print item['caption']['text']
            
            for comment in item['comments']:
                print comment['text']
                print comment['user']['username']

            print "\n"
                

    def follow_my_followers(self):
        self.api.getSelfUserFollowers()
        result = self.api.LastJson
        for user in result['users']:
            print user['username']
            print user['full_name']
            print user['profile_pic_url']


        
class InstagramHashtag(models.Model):
    author = models.ForeignKey(InstagramPerson)
    content = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)

    def __str__(self):
        return self.content
