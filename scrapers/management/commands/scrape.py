from django.contrib.auth.models import User

from scrapers import utils
from scrapers.models.literature import LiteratureSentence, LiteraturePerson
from scrapers.models.twitter import TwitterPerson
from scrapers.models.text_message import TextMessagePerson
from django.core.management import BaseCommand


command_arguments = {
    "--twitter": "top|existing",
    "--intake_iOSBackup_for_text_messages_at": "path",
    "--intake_file_for_plain_text_at": "path"}

usage = "python manage.py scrape "


class Command(BaseCommand):
    for arg in command_arguments:
        usage += arg

    def add_arguments(self, parser):
        for arg in command_arguments:
            parser.add_argument(arg, default=False)

    def handle(self, *args, **options):
        if options['twitter']:
            if options['twitter'] == 'top':
                u = User.objects.first()
                u.scrape_top_twitter_people()
            if options['twitter'] == 'existing':
                for person in TwitterPerson.objects.all():
                    person.scrape()

        if options['intake_iOSBackup_for_text_messages_at']:
            u = User.objects.first()
            t = TextMessagePerson.objects.get_or_create(user=u)[0]
            t.intake_raw_io_backup_texts(options['intake_iOSBackup_for_text_messages_at'] + "/_export")
            t.save()

        if options['intake_file_for_plain_text_at']:
            file_name = options['intake_file_for_plain_text_at']
            sentences = utils.read_source_into_sentence_list(file_name)
            author = LiteraturePerson.objects.get_or_create(username=options['author'], real_name=options['author'])[0]
            for sentence in sentences:
                l = LiteratureSentence(author=author, content=" ".join(sentence))
                l.save()
                author.cache_sentence(l)
