from django.conf.urls import url
from bots.views import api_views

urlpatterns = [
    url(r'^list_all_bots/', api_views.list_all_bots),
    url(r'^get_bot_info/?P<bot_id>[0-9]+', api_views.get_bot_info),
]
