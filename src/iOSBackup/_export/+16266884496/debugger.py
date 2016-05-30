from bs4 import BeautifulSoup
import re
import urllib2
from datetime import datetime

partner = r"20160512.html"
url = partner
page = open(url)
soup = BeautifulSoup(page.read())

raw_replies = soup.find_all('div', {'class' : 'sent'})
raw_text = soup.find_all('div')

replies = []
for reply in raw_replies:
	date_and_text = re.search('([0-9]+:)+([0-9][0-9])(.*)', reply.text)
	text = date_and_text.group(3)
	print text
