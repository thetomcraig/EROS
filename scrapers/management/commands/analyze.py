import urllib
from django.contrib.auth.models import User
from scrapers.models.twitter import TwitterPerson, TwitterPost, TwitterPostMarkov
from scrapers.models.facebook import FacebookPerson, FacebookPost
from django.core.management import BaseCommand
from scrapers.models.twitter import TwitterPost 
from datetime import datetime
from django.conf import settings


command_arguments = { \
  "--apply_markov_chains": ",".join(settings.OUTLETS), 
  "--sentiment_analyze": ",".join(settings.OUTLETS) }

usage = "python manage.py analyze "

class Command(BaseCommand):
  for arg in command_arguments:
    usage += arg

  def add_arguments(self, parser):
    for arg in command_arguments:
      parser.add_argument(arg, default=False)


  def handle(self, *args, **options):
    if options['apply_markov_chains']:
      if options['apply_markov_chains'] == 'plain_text':
        pass

      if options['apply_markov_chains'] == 'text_messages':
        u = User.objects.first()
        t = TextMessagePerson.objects.get_or_create(user=u)[0]
        t.apply_markov_chains()
        t.save()

      if options['apply_markov_chains'] == 'twitter':
        for person in TwitterPerson.objects.all():
          person.apply_markov_chains()

      if options['apply_markov_chains'] == 'facebook':
        print "stubbed"
        pass

    if options['sentiment_analyze']:
      if options['sentiment_analyze'] == 'plain_text':
        pass
      if options['sentiment_analyze'] == 'text_messages':
        pass
      if options['sentiment_analyze'] == 'twitter':
        pass
      if options['sentiment_analyze'] == 'facebook':
        print "stubbed"
        pass
