import urllib
from django.contrib.auth.models import User
from scrapers.models.twitter import TwitterPerson, TwitterPost, TwitterPostMarkov
from scrapers.models.facebook import FacebookPerson, FacebookPost
from django.core.management import BaseCommand

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument('twitter_users')
		parser.add_argument('facebook_users')

	def handle(self, *args, **options):
		#Twitter stuff
		if ('all' in options['twitter_users']):
			tom = User.objects.get_or_create(username='tom')[0]
			tom.scrape_top_twitter_people()

			"""
			all_twitter_people = TwitterPerson.objects.all()
			for person in all_twitter_people:
				person.scrape()
				person.apply_markov_chains()
			"""

			print "Scraped all Twitter people"
			all_twitter_posts = TwitterPost.objects.all()
			num = len(all_twitter_posts)
			print "There are %d twitter posts in the db" % num
		
		#Facebook stuff
		if ('all' in options['facebook_users']):
			pass


	 
