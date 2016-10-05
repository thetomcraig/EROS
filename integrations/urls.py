from django.conf.urls import url                                                                                           
from integrations import views as integrations_views
                                                                                                                           
urlpatterns = [                                                                                                            
    url(r'^twitter_person_detail/(?P<person_username>[a-zA-Z0-9]+[\w|\W]+)/$', \
        integrations_views.twitter_person_detail, name='twitter_person_detail'),
    url(r'^twitter_home', integrations_views.twitter_home, name='twitter_home'),
    url(r'^instagram_home', integrations_views.instagram_home, name='instagram_home'),
]
