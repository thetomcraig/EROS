from django.contrib import admin
from .models import FacebookPost, TwitterPost

admin.site.register(FacebookPost)
admin.site.register(TwitterPost)
