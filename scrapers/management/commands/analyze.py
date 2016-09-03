from django.contrib.auth.models import User
from scrapers.models.twitter import TwitterPerson
from scrapers.models.text_message import TextMessagePerson
from django.core.management import BaseCommand
from django.conf import settings


command_arguments = {
    "--apply_markov_chains": ",".join(settings.OUTLETS),
    "--sentiment_analyze": ",".join(settings.OUTLETS),
    "--transfer": "twitter_to_text_messages"}

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
                t.apply_markov_chains(100)
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
                pass

        if options['transfer']:
            print options['transfer']
            if options['transfer'] == "twitter_to_text_messages":
                people = TwitterPerson.objects.all()
                for person in people:
                    u = User.objects.get_or_create(username=person.username)[0]
                    print "u: ", u

                    print len(TextMessagePerson.objects.all())
                    print [str(x.__dict__) + "\n" for x in TextMessagePerson.objects.all()]
                    print [str(x.user.__dict__) + "\n" for x in TextMessagePerson.objects.all()]
                    try:
                        t = TextMessagePerson.objects.get(username=u.username)
                    except:
                        t = TextMessagePerson(
                            username=u.username,
                            first_name=u.username,
                            last_name=u.username)
                        t.save()
