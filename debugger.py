import os
import django
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
    django.setup()

from scrapers import models, utils
from scrapers.models.twitter import TwitterPost, TwitterPerson
from scrapers.models.plain_text_classes import Person
from scrapers.models.literature import LiteraturePerson
from scrapers.models.text_message import TextMessagePerson
from scrapers.models.instagram import InstagramPerson 
from scrapers import utils

utils.collect_hashtags()



"""
t = TextMessagePerson.objects.get_or_create(username="tomcraig", real_name="Tom Craig")[0]
t.save()
t.intake_raw_io_backup_texts("./src/iOSBackup/_export/")

for i in range(100):
    t.apply_markov_chains()

for m in t.textmessagemarkov_set.all():
    try:
        print m.content
    except:
        pass

"""
"""
person = TwitterPerson.objects.all()[0]
print person.username
#all_markov_posts = person.twitterpostmarkov_set.all()
#all_markov_posts.delete()
#print person
#person.scrape()

print [(x.content) for x in person.twitterpost_set.all()]
print [(x.content, x.randomness) for x in person.twitterpostmarkov_set.all()]

"""
"""
for c in person.twitterpostcache_set.all():
  if c.beginning:
    print c.word1
    print c.word2
    print c.final_word
    print "\n"
    next_cache = person.twitterpostcache_set.filter(word1=c.word2, word2=c.final_word)[0]
    print next_cache


#print person.twitterpostmarkov_set.all().last()

posts = TwitterPost.objects.all()
for post in posts:
  print post.updated_at
  if hasattr(post, 'happiness'):
    if post.happiness != 0.0:
      print post.happiness
"""
