import datetime
from random import randint
import requests
import re
from time import sleep
import sys

import pynder


DEBUG = False


class AutoTinder():
    session = False
    exp_no = -1

    def __init__(self, facebok_id, fb_token, exp_no):
        requests.packages.urllib3.disable_warnings()
        token_regex = re.match(r"(fbconnect://success#access_token=)(.*)(&)", fb_token)
        self.session = pynder.Session(facebok_id, token_regex.group(2))
        self.exp_no = exp_no

    def like_people(self, number):
        like_log = []
        like_log_ids = []
        counter = 0
        print('Starting')
        while counter < number:
            if DEBUG:
                keep_liking = raw_input('Keep liking? >')
                print keep_liking
                if keep_liking != 'y':
                    self.write_likes(like_log, like_log_ids)
                    return like_log
            try:
                users = self.session.nearby_users()
                print('Found %d users' % len(users))
                if len(users) == 0:
                    break

                for u in users:
                    print('%d/%d' % (counter, number))
                    if counter >= number:
                        self.write_likes(like_log, like_log_ids)
                        return like_log
                    u.like()
                    like_log.append(str(u.__dict__))
                    like_log_ids.append(u.id)
                    sleep(randint(1, 5))
                    counter = counter + 1
            except:
                e = sys.exc_info()[0]
                print str(e)

        return like_log, like_log_ids

    # TODO, move to utils
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

    # TODO, move to utils
    def get_matches_in_id_list(self, id_list):
        matches = []
        for match in self.session._api.matches():
            person = match['person']
            if person['_id'] in id_list:
                matches.append(match)
        return matches

    def get_all_matches(self):
        return self.session._api.matches()
