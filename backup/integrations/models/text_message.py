from django.db import models
import base


# TEXT MESSAGE VERSION
class TextMessagePerson(base.Person):
    happiness = models.IntegerField(default=0)

    def __str__(self):
        return self.username


# TEXT MESSAGE VERSION
class TextMessage(base.Sentence):
    author = models.ForeignKey(TextMessagePerson, default=None, null=True)
    time_sent = models.DateTimeField(null=True)
    partner = models.CharField(max_length=100)


# TEXT MESSAGE VERSION
class TextMessageCache(base.SentenceCache):
    author = models.ForeignKey(TextMessagePerson, default=None, null=True)


# TEXT MESSAGE VERSION
class TextMessageMarkov(base.MarkovChain):
    author = models.ForeignKey(TextMessagePerson, default=None)
