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
            if options['transfer'] == 'twitter_to_text_messages':
                people = TwitterPerson.objects.all()
                for twitter_person in people:
                    try:
                        text_person = TextMessagePerson.objects.get(username=u.username)
                    except:
                        text_person = TextMessagePerson(
                            username=twitter_person.username,
                            first_name=twitter_person.username,
                            last_name=twitter_person.username)
                        text_person.save()

                    # Deep copy of the post/message objects from twitter to text messages
                    for twitter_post in twitter_person.twitterpost_set.all():
                        text_person.textmessage_set.create(
                            content=twitter_post.content
                        )

                    # Deep copy of the cache objects from twitter to text messages
                    for twitter_post_cache in twitter_person.twitterpostcache_set.all():
                        text_person.textmessagecache_set.create(
                            word1=twitter_post_cache.word1,
                            word2=twitter_post_cache.word2,
                            final_word=twitter_post_cache.final_word,
                            beginning=twitter_post_cache.beginning
                        )
