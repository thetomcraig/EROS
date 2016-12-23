from django.conf.urls import url
from scrapers import views as scrapers_views


urlpatterns = [
    url(r'^train_on_text_messages', scrapers_views.train_on_text_messages),
    url(r'^apply_markov_chains', scrapers_views.apply_markov_chains),
    url(r'^sentiment_analyze', scrapers_views.sentiment_analyze),
]
