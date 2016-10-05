from django.db import models
from django.contrib.auth.models import User
import base

# INSTAGRAM VERSION
class InstagramPerson(base.Person):
    username_id = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)

# INSTAGRAM VERSION
class InstagramPost(base.Sentence):
    author = models.ForeignKey(InstagramPerson, default=None, null=True)

class InstagramHashtag(models.Model):
    original_post = models.ForeignKey(InstagramPost)
    content = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)

    def __str__(self):
        return self.content
