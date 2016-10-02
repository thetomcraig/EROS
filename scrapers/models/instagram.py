from django.db import models
from django.contrib.auth.models import User
import plain_text_classes

# INSTAGRAM VERSION
class InstagramPerson(plain_text_classes.Person):
    pass

# INSTAGRAM VERSION
class InstagramPost(plain_text_classes.Sentence):
    author = models.ForeignKey(InstagramPerson, default=None, null=True)

class InstagramHashtag(models.Model):
    original_post = models.ForeignKey(InstagramPost)
    content = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)

    def __str__(self):
        return self.content
