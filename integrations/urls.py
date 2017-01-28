from django.conf.urls import url
from integrations import views as integrations_views


urlpatterns = [
    url(r'^twitter_home', integrations_views.twitter_home, name='twitter_home'),
    url(r'^instagram_home', integrations_views.instagram_home, name='instagram_home'),

    url(r'^twitter_person_detail/(?P<person_username>[a-zA-Z0-9]+[\w|\W]+)/$',
        integrations_views.twitter_person_detail, name='twitter_person_detail'),
    url(r'^instagram_person_detail/(?P<person_username>[a-zA-Z0-9]+[\w|\W]+)/$',
        integrations_views.instagram_person_detail, name='instagram_person_detail'),

    url(r'^twitter_conversation/(?P<person_username>\w+)/(?P<partner_username>\w+)/$', integrations_views.twitter_conversation, name='twitter_conversation'),

    url(r'^text_message_home', integrations_views.text_message_home, name='text_message_home'),
]
