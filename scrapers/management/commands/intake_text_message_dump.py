import urllib
from django.contrib.auth.models import User
from scrapers.models.text_message import TextMessagePerson
from django.core.management import BaseCommand
from scrapers.models.twitter import TwitterPost 
from datetime import datetime

usage = "python manage intake_text_message_dump" + \
        "--path_to_iOSBackup <path> " 

class Command(BaseCommand):
  help = usage
  def add_arguments(self, parser):
    parser.add_argument('--path_to_iOSBackup', default=False)

  def handle(self, *args, **options):
    if options['path_to_iOSBackup']:
      peeps = TextMessagePerson.objects.all()
      for p in peeps:
        p.delete()
      if len(TextMessagePerson.objects.all()) != 0:
       TextMessagePerson.objects.create(username="tomcraig", real_name="Tom Craig")
      t = TextMessagePerson.get(username="tomcraig")
      t.intake_raw_io_backup_texts(options['path_to_iOSBackup'] + "/_export")
      t.save()

