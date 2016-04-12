#at artandlogic.com modles for comment storing)

import hashlib
import json
from django.db import models, IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import facebook
import requests

from constants import *

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
				' story: '	+str(self.story) + '\n' + \
				' message: ' + str(self.message) + '\n' + \
				' picture: ' + str(self.picture) + '\n' + \
				' link: ' + str(self.link) + '\n' + \
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

