import urllib
from django.contrib.auth.models import User
from scrapers.models.twitter import TwitterPerson, TwitterPost, TwitterPostMarkov
from scrapers.models.facebook import FacebookPerson, FacebookPost
from django.core.management import BaseCommand
from scrapers.models.twitter import TwitterPost 
from datetime import datetime

usage = "python manage scrape " + \
				"--twitter_users top|existing] " + \
				"[--sentiment_analyze] " + \
				"[--apply_markov_chains id=id|all] " + \
				"[--facebook_users all (stubbed out)]"

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument('--twitter_users', default=False)
		parser.add_argument('--sentiment_analyze', default=False)
		parser.add_argument('--apply_markov_chains', default=False)
		parser.add_argument('--facebook_users', default=False)

	def handle(self, *args, **options):
		#Twitter stuff
		if options['twitter_users']:
			if ('top' in options['twitter_users']):
				#Only do this to refresh the db
				#Makes external api call
				tom = User.objects.get_or_create(username='tom')[0]
				tom.scrape_top_twitter_people()

			elif 'existing' in options['twitter_users']:
				#Scrapes new posts for all the existing peeps
				all_twitter_people = TwitterPerson.objects.all()
				all_new_post_ids = []

				for person in all_twitter_people:
					new_post_ids = person.scrape()
					all_new_post_ids = all_new_post_ids + new_post_ids
				print datetime.now()

				print "Scraped all Twitter people"
				print "There are %d new twitter posts in the db" % len(all_new_post_ids)

		if (options['sentiment_analyze']):
			#Analyze any posts updated in the last 24 hours
			"""
			new_posts = TwitterPost.objects.filter(created_at__gt(
			for post in new_posts:
				post.sentiment_analyze()
			"""

		if (options['apply_markov_chains']):
			if ('all' in options['apply_markov_chains']):
				print "Markov chains created:"
				for person in TwitterPerson.objects.all():
					person.apply_markov_chains()
					print person.twitterpostmarkov_set.last()
		
		#Facebook stuff
		if (options['facebook_users']):
			if ('all' in options['facebook_users']):
				pass


	 
