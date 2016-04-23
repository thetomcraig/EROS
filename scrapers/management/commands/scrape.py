import urllib
from django.contrib.auth.models import User
from scrapers.models.twitter import TwitterPerson, TwitterPost, TwitterPostMarkov
from scrapers.models.facebook import FacebookPerson, FacebookPost
from django.core.management import BaseCommand
from scrapers.models.twitter import TwitterPost 
from datetime import datetime

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument('twitter_users')
		parser.add_argument('facebook_users')

	def handle(self, *args, **options):
		#Twitter stuff
		if ('all' in options['twitter_users']):
			tom = User.objects.get_or_create(username='tom')[0]
			#Only do this to refresh the db
			#tom.scrape_top_twitter_people()

			all_twitter_people = TwitterPerson.objects.all()
			for person in all_twitter_people:
				new_post_ids = person.scrape()
				print "Performing sentiment analysis on %d new posts" % len(new_post_ids)
				for post_id in new_post_ids:
					post = TwitterPost.objects.filter(pk=post_id)[0]
					post.sentiment_analyze()

				#person.apply_markov_chains()
			
			print datetime.now()
			print "Scraped all Twitter people"
			all_twitter_posts = TwitterPost.objects.all()
			num = len(all_twitter_posts)
			print "There are %d twitter posts in the db" % num
		
		#Facebook stuff
		if ('all' in options['facebook_users']):
			pass


	 
