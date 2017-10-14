from bs4 import BeautifulSoup
from datetime import datetime
import os
import re

from integrations.models.text_message import TextMessagePerson, TextMessageCache


def read_raw_texts(iOSBackup_folder_location):
    print "intaking texts"
    root = iOSBackup_folder_location
    for directory, subdirectories, files, in os.walk(root):
        m = re.match(r"(.*)(\+1)([0-9]{10})$", directory)
        if m:
            for f in files:
                if re.match(r"([0-9]{8})(\.html)", f):
                    date = datetime.strptime(f.split('.')[0], '%Y%m%d')
                    print "intaking texts for date:"
                    print date
                    scrape_replies_from_html_file(directory + "/" + f, date, m.group(3))

        if re.match(r"(.*)(\+1)([0-9]{10})(\/)([0-9]{8})$", directory):
            # files will all be pictures from that day
            pass


def scrape_replies_from_html_file(filename, day, partner):
    me = get_text_message_me()

    url = filename
    page = open(url)
    soup = BeautifulSoup(page.read())

    raw_replies = soup.find_all('div', {'class': 'sent'})

    for reply in raw_replies:
        date_and_text = re.search('([0-9][0-9])(:)([0-9][0-9])(:)([0-9][0-9])(.*)', reply.text)
        text_hour = int(date_and_text.group(1))
        text_minute = int(date_and_text.group(3))
        text_second = int(date_and_text.group(5))
        content = date_and_text.group(6)
        time_sent = datetime(day.year, day.month, day.day, text_hour, text_minute, text_second)

        text_message = me.textmessage_set.create(
            author=me,
            time_sent=time_sent,
            content=content,
            partner=partner)

        create_post_cache(text_message, me.textmessagecache_set)


def get_text_message_me():
    return TextMessagePerson.objects.get_or_create(first_name='Tom', last_name='Craig')[0]


def clear_texts(author):
    [x.delete() for x in author.textmessage_set.all()]
    [x.delete() for x in author.textmessagecache_set.all()]


def generate_text():
    me = get_text_message_me()
    all_caches = TextMessageCache.objects.all()
    all_beginning_caches = all_caches.filter(beginning=True)
    print me.apply_markov_chains_inner(all_beginning_caches, all_caches)
