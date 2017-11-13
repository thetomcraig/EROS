from django.conf.urls import url
from bots import api_views

urlpatterns = [
    url(r'^list_all_bots/', api_views.list_all_bots),
    url(r'^scrape_bot/([0-9]+)/$', api_views.scrape_bot),
    url(r'^get_bot_info/([0-9]+)/$', api_views.get_bot_info),
    url(r'^get_conversation/<bot1_id>(0-9)+/?<bot1_id>(0-9)', api_views.get_conversation),
]
