import os, django
if __name__ == "__main__":
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
	django.setup()

from scrapers import models
from scrapers.models.twitter import TwitterPost, TwitterPerson


person = TwitterPerson.objects.all()[0]

#person.scrape()
person.apply_markov_chains()

#print person.twitterpostmarkov_set.all().last()

"""
posts = TwitterPost.objects.all()
for post in posts:
	print post.updated_at
	if hasattr(post, 'happiness'):
		if post.happiness != 0.0:
			print post.happiness
"""
	
