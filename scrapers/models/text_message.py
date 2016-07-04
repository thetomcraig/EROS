from bs4 import BeautifulSoup
import os
import re
import urllib2

from datetime import datetime
from django.db import models, IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import plain_text_classes

from scrapers.constants import *

from .. import utils

#TEXT MESSAGE VERSION
class TextMessagePerson(plain_text_classes.Person, models.Model):
  happiness = models.IntegerField(default=0)

  def __str__(self):
    return self.username

  def intake_raw_io_backup_texts(self, iOSBackup_folder_location):
    root = iOSBackup_folder_location
    for directory, subdirectories, files, in os.walk(root):
      m = re.match(r"(.*)(\+1)([0-9]{10})$", directory)
      if m:
        for f in files:
          if re.match(r"([0-9]{8})(\.html)", f):
            date = datetime.strptime(f.split('.')[0], '%Y%m%d')
            self.scrape_replies_from_html_file(directory+"/"+f, date, m.group(3))

      if re.match(r"(.*)(\+1)([0-9]{10})(\/)([0-9]{8})$", directory):
        #files will all be pictures from that day
        pass

  def scrape_replies_from_html_file(self, filename, day, partner):
    url = filename
    page = open(url)
    soup = BeautifulSoup(page.read())

    raw_replies = soup.find_all('div', {'class' : 'sent'})
    raw_text = soup.find_all('div')

    for reply in raw_replies:
      date_and_text = re.search('([0-9][0-9])(:)([0-9][0-9])(:)([0-9][0-9])(.*)', reply.text)
      text_hour = int(date_and_text.group(1))
      text_minute = int(date_and_text.group(3))
      text_second = int(date_and_text.group(5))
      content = date_and_text.group(6)
      time_sent = datetime(day.year, day.month, day.day, text_hour, text_minute, text_second)

      text_message = self.textmessage_set.create(author=self, \
        time_sent=time_sent, \
        content=content, \
        partner=partner)
      self.create_text_message_cache(text_message)
        

  def create_text_message_cache(self, post):
    """
    """
    word_list = post.content.split()
    for index in range(len(word_list)-2):
      print "caching:"
      word1 = word_list[index]
      word2 = word_list[index+1]
      final_word = word_list[index+2]
      print word1.encode('utf-8')
      print word2.encode('utf-8')
      print final_word.encode('utf-8')

      beginning = False
      if (index == 0):
        beginning = True
      text_cache = TextMessageCache(author=self, word1=word1, word2=word2, final_word=final_word, beginning=beginning)
      text_cache.save()


  def apply_markov_chains(self):
    print "Applying markov chains"
    all_beginning_caches = self.textmessagecache_set.filter(beginning=True)
    all_caches = self.textmessagecache_set.all()
    new_markov_message = self.apply_markov_chains_inner(all_beginning_caches, all_caches)

    randomness = new_markov_message[1]
    content = ""
    for word in new_markov_message[0]:
      content = content + word + " "

    self.textmessagemarkov_set.create(content=content[:-1], randomness=randomness)

  
#TEXT MESSAGE VERSION
class TextMessage(plain_text_classes.Sentence):
  author = models.ForeignKey(TextMessagePerson, default=None, null=True)
  time_sent = models.DateTimeField()
  partner = models.CharField(max_length=8)

#TEXT MESSAGE VERSION
class TextMessageCache(plain_text_classes.SentenceCache):
  author = models.ForeignKey(TextMessagePerson, default=None, null=True)

#TEXT MESSAGE VERSION
class TextMessageMarkov(plain_text_classes.MarkovChain):
  author = models.ForeignKey(TextMessagePerson, default=None)

