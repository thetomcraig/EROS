"""eros URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

import integrations.views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', integrations.views.home, name='home'),
    url(r'^integrations/', include('integrations.urls')),
    url(r'^scrapers/', include('scrapers.urls')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^get_texts/', 'integrations.views.get_texts', name='get_texts'),
    url(r'^get_markov_texts/', 'integrations.views.get_markov_texts', name='get_markov_texts'),
]