import urllib
from django.contrib.auth.models import User
from scrapers.models.twitter import TwitterPerson, TwitterPost, TwitterPostMarkov
from scrapers.models.facebook import FacebookPerson, FacebookPost
from django.core.management import BaseCommand
from scrapers.models.twitter import TwitterPost 
from datetime import datetime
from settings import OUTLETS

usage = "python manage.py scrape "

class Command(BaseCommand):
  for arg in OUTLETS:
    usage += arg 

  def add_arguments(self, parser):
    for arg in command_arguments:
      parser.add_argument(arg, default=False)


  def handle(self, *args, **options):
    if options['plain_text']:
      pass

    if options['text_message']:
      pass

    if options['twitter']:
      tom = User.objects.get_or_create(username='tom')[0]
      tom.scrape_top_twitter_people()
      
    if options['facebook']:
      pass

