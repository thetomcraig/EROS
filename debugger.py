import os, django
if __name__ == "__main__":
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
	django.setup()

from scrapers import models
from scrapers.models.twitter import TwitterPost, TwitterPerson


person = TwitterPerson.objects.all()[0]
print person
#person.scrape()
person.apply_markov_chains()
print [(x.content, x.randomness) for x in person.twitterpostmarkov_set.all()]

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
	
