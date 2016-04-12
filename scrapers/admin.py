from django.contrib import admin
from scrapers.models.twitter import TwitterPost
from scrapers.models.facebook import FacebookPost

admin.site.register(FacebookPost)
admin.site.register(TwitterPost)
