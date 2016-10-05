# at artandlogic.com modles for comment storing)
import random
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

import base

class TwitterPerson(base.Person):
    happiness = models.IntegerField(default=0)

    def __str__(self):
        return self.username


class TwitterPost(base.Sentence):
    author = models.ForeignKey(TwitterPerson, default=None, null=True)


class TwitterPostCache(base.SentenceCache):
    author = models.ForeignKey(TwitterPerson, default=None, null=True)


class TwitterPostMarkov(base.MarkovChain):
    author = models.ForeignKey(TwitterPerson, default=None)


class TwitterLink(models.Model):
    author = models.ForeignKey(TwitterPerson)
    content = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)

    def __str__(self):
        return self.content


class TwitterHashtag(models.Model):
    author = models.ForeignKey(TwitterPerson)
    content = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)

    def __str__(self):
        return self.content


class TwitterMention(models.Model):
    author = models.ForeignKey(TwitterPerson)
    content = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)

    def __str__(self):
        return self.content
