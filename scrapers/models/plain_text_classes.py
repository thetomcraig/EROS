import hashlib
import random
from django.db import models, IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

#SUPER CLASS
class Person(User, models.Model):
	real_name = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
	avatar = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)

#SUPER CLASS
class Sentence(models.Model):
	author = models.ForeignKey(Person, default=None, null=True)
	content = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)

	def __str__(self):
		return self.content
		
#SUPER CLASS
class MarkovChain(models.Model):
	author = models.ForeignKey(Person, default=None)
	content = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
	randomness = models.FloatField(default=0.0)

	def __str__(self):
		return ' author: ' + str(self.author) + '\n' + \
						' content: ' + self.content.encode('utf-8') + '\n' + \
						' randomness ' + str(self.randomness) + '\n'
