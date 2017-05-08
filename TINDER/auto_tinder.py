import datetime
import itertools
from random import randint
import requests
import re
from time import sleep
import config
import csv
import subprocess
import sys

import pynder

DEBUG = True
class AutoTinder():
    session = False
    
    def __init__(self):
        requests.packages.urllib3.disable_warnings()
        token_regex = re.match(r"(fbconnect://success#access_token=)(.*)(&)", config.FACEBOOK_AUTH_TOKEN)
        self.session = pynder.Session(config.FACEBOOK_ID, token_regex.group(2))

    def like_people(self, number, like_log):
        counter = 0
        print('Starting')
        while counter < number:
            if DEBUG:
                keep_liking = raw_input('Keep liking? >')
                print keep_liking
                if keep_liking != 'y':
                    sys.exit(0)

            try:
                users = session.nearby_users()
                print('Found %d users' % len(users))
                if len(users) == 0:
                    break

                for u in users:
                    u.like()
                    print('%d/%d' % (counter, number))
                    like_log.append(u)
                    sleep(randint(1, 5))
                    counter = counter + 1
            except:
                pass

    def write_likes(self, like_log):
        now = str(datetime.datetime.now())
        now_file = 'logs/{0}.csv'.format(now)
        subprocess.check_call(['touch', now_file])

        with open(now_file, 'wb') as now_file_csv:
            file_writer = csv.writer(now_file_csv, delimiter=',')

            header = ['Bio', 'Images', 'Likes']
            file_writer.writerow(header)

            rows = itertools.izip_longest([session.profile.bio], session.profile.photos, like_log)

            for row in rows:
                file_writer.writerow(row)

    def get_matches_for_time_window(self, from_time, until_time):
        """
        Match holds inforamtion on the person and meta data (when you matched, etc)
        """
        matches_in_time_window = []
        for match in self.session._api.matches():
            date = match['created_date']
            date = date[:-5]
            datetime_date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
            if from_time <= datetime_date <= until_time:
                matches_in_time_window.append(match)

        return matches_in_time_window


    def go(self):

#    like_log = []
#    like_people(100, like_log)
#    write_likes(like_log)
        end = datetime.datetime.now()
        start = end - datetime.timedelta(days=7)    
        matches = self.get_matches_for_time_window(start, end)
        print len(matches)
        print matches[len(matches)-1]
        
a = AutoTinder()
a.go()
