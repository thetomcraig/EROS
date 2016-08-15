import urllib
from django.contrib.auth.models import User
from scrapers.models.text_message import TextMessagePerson
from django.core.management import BaseCommand
from scrapers.models.twitter import TwitterPost 
from datetime import datetime

usage = "python manage text_message" + \
        "[--intake_iOSBackup_at <path>]" + \
        "[--apply_markov_chains yes]"

class Command(BaseCommand):
  help = usage
  def add_arguments(self, parser):
    parser.add_argument('--intake_iOSBackup_at', default=False)
    parser.add_argument('--apply_markov_chains', default=False)

  def handle(self, *args, **options):
    
    if options['intake_iOSBackup_at']:
      u = User.objects.first()
      t = TextMessagePerson.objects.get_or_create(user=u)[0]
      t.intake_raw_io_backup_texts(options['intake_iOSBackup_at'] + "/_export")
      t.save()

    if options['apply_markov_chains']:
      u = User.objects.first()
      t = TextMessagePerson.objects.get_or_create(user=u)[0]
      t.apply_markov_chains()
      t.save()


