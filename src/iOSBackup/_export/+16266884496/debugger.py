from bs4 import BeautifulSoup
import re
import urllib2
from datetime import datetime

partner = r"20160512.html"
day = datetime.strptime(partner.split('.')[0], '%Y%m%d')
url = partner
page = open(url)
soup = BeautifulSoup(page.read())

raw_replies = soup.find_all('div', {'class' : 'sent'})
raw_text = soup.find_all('div')

replies = []
for reply in raw_replies:
	date_and_text = re.search('([0-9][0-9])(:)([0-9][0-9])(:)([0-9][0-9])(.*)', reply.text)
	text_hour = int(date_and_text.group(1))
	text_minute = int(date_and_text.group(3))
	text_second = int(date_and_text.group(5))
	text = date_and_text.group(6)
	time_sent = datetime(day.year, day.month, day.day, text_hour, text_minute, text_second)

	replies.append(time_sent, text)
