import urllib
from django.contrib.auth.models import User
from scrapers.models import TwitterPerson, FacebookPerson, FacebookPost, TwitterPost, TwitterPostMarkov
from django.core.management import BaseCommand

class Command(BaseCommand):
  def add_arguments(self, parser):
    parser.add_argument('twitter_users')
    parser.add_argument('facebook_users')

  def handle(self, *args, **options):
    #Twiter stuff
    if ('all' in options['twitter_users']):
      tom = User.objects.get_or_create(username='tom')[0]
      tom.scrape_top_twitter_people()

      all_twitter_people = TwitterPerson.objects.all()
      for person in all_twitter_people:
        tom.scrape_twitter_person(person.username)

      print "Scraped all Twitter people"
    
    #Facebook stuff
    if ('all' in options['facebook_users']):
      pass

    #Done - print the size of the database 
    all_twitter_posts = TwitterPost.objects.all()
    num = len(all_twitter_posts)
    print "There are %d twitter posts in the db" % num

   
