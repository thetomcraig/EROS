import django
django.setup()
from integrations.helpers.twitter_utils import find_word_frequency_for_user

find_word_frequency_for_user('justinbieber')
find_word_frequency_for_user('Pink')
