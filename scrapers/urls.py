from django.conf.urls import url
from . import views

urlpatterns = [
		url(r'^post_index', views.post_index, name='post_index'),
		url(r'^twitter_people', views.twitter_people, name='twitter_people'),
		url(r'^twitter_person_detail/(?P<twitter_person_username>[a-zA-Z0-9]+[\w|\W]+)/$', views.twitter_person_detail, name='detail'),
		url(r'^scrape_top_twitter_people', views.scrape_top_twitter_people),
		url(r'^apply_markov_chains', views.apply_markov_chains),
		url(r'^sentiment_analyze', views.sentiment_analyze),
]

