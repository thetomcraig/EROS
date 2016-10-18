import os, sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eros.settings")

from django.conf import settings
from integrations.helpers.InstagramAPI.InstagramAPI import InstagramAPI
from integrations.models.instagram import InstagramPerson

api = InstagramAPI('thetomcraig@icloud.com', settings.INSTAGRAM_PASSWORD)
print settings.INSTAGRAM_USERNAME
print settings.INSTAGRAM_PASSWORD

api.login()

print InstagramPerson.objects.filter(username=settings.INSTAGRAM_USERNAME)
# api.getProfileData()
# result = api.LastJson
