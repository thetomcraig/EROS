from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^post_index', views.post_index, name='post_index'),
    url(r'^twitter_people', views.twitter_people, name='twitter_people'),
    url(r'^twitter_person_detail/(?P<twitter_person_username>[a-zA-Z0-9]+)/$', views.twitter_person_detail, name='detail'),
]
