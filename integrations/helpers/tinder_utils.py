import csv
from datetime import datetime
import glob
import itertools
import os
import pandas
import subprocess

from django.conf import settings

from integrations.helpers.Tinder.auto_tinder import AutoTinder


def get_tinder_experiment_data():
    """
    Get logged data
    Change the functions to read logs/cached data
    """
    experiments = []

    for i in range(settings.TINDER_EXPERIMENT_NO):
        exp_i = {}
        exp_i['exp_num'] = i
        exp_i['exp_name'] = settings.TINDER_EXPERIMENT_NAMES.get(i)
        exp_i['like_number'] = len(get_like_ids_for_exp_no(i))
        exp_i['match_number'] = get_match_number_for_exp_number(i)
        experiments.append(exp_i)
    return experiments


def refresh_tinder():
    """
    Use API to get matches
    cross reference with the logs
    """
    # Get the matches
    a = AutoTinder(settings.FACEBOOK_ID, settings.FACEBOOK_AUTH_TOKEN, settings.CURRENT_TINDER_EXPERIMENT_NO)
    all_matches = a.get_all_matches()
    matches = []

    for i in range(settings.CURRENT_TINDER_EXPERIMENT_NO):
        pass
    # TODO - do all the below code, but put each id into a list for a corresponding exp no
    # get this number from the swip csvs
    for match in all_matches:
        person = match['person']
        if person['_id'] == settings.CURRENT_TINDER_EXPERIMENT_NO:
            matches.append(match)

    # Write the file
    now = str(datetime.datetime.now())
    now_file = settings.TINDER_LOGS_LOCATION + 'matches/{0}.csv'.format(now)
    subprocess.check_call(['touch', now_file])

    with open(now_file, 'wb') as now_file_csv:
        file_writer = csv.writer(now_file_csv, delimiter=',')
        header = ['Experiment Number', 'Match Number']
        file_writer.writerow(header)

        rows = itertools.izip_longest([settings.CURRENT_TINDER_EXPERIMENT_NO], [len(matches)])
        for row in rows:
            file_writer.writerow(row)

def get_match_number_for_exp_number(exp_no):
    # TODO - read from csv file here
    matches = []
    return len(matches)


def get_like_ids_for_exp_no(exp_no):
    """
    Read the csv logs with all the likes in them
    """
    all_like_ids_for_exp_no = []
    logs_location = settings.TINDER_LOGS_LOCATION + '/swipe_sessions'
    cwd = os.getcwd()
    os.chdir(logs_location)
    files = [x for x in glob.glob('*.{}'.format('csv'))]
    os.chdir(cwd)

    for f in files:
        full_path = '/'.join([logs_location, f])
        with open(full_path, 'rU') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            rows = [x for x in reader]
            # header is first row
            # top row of data is second row
            # header = rows[0]
            top_row = rows[1]
            csv_exp_no = top_row[0]
            if int(csv_exp_no) == int(exp_no):
                # we transpose the rows to get all the likes in 1 row
                # images will be in fourth row
                transposed_rows = map(list, zip(*rows))
                all_like_ids_for_exp_no.extend(transposed_rows[3])
    return all_like_ids_for_exp_no


def write_likes(self, like_log, like_log_ids):
    now = str(datetime.datetime.now())
    now_file = settings.TINDER_LOGS_LOCATION + 'swipe_sessions/{0}.csv'.format(now)
    subprocess.check_call(['touch', now_file])

    with open(now_file, 'wb') as now_file_csv:
        file_writer = csv.writer(now_file_csv, delimiter=',')
        header = ['Experiment Number', 'Bio', 'Images', 'Likes - ID', 'Likes - Metadata']
        file_writer.writerow(header)

        rows = itertools.izip_longest([self.exp_no], [self.session.profile.bio], self.session.profile.photos, like_log_ids, like_log)
        for row in rows:
            file_writer.writerow(row)


def auto_tinder_like(people_number):
    a = AutoTinder(settings.FACEBOOK_ID, settings.FACEBOOK_AUTH_TOKEN, settings.CURRENT_TINDER_EXPERIMENT_NO)
    like_log, like_log_ids = a.like_people(people_number)
    write_likes(like_log, like_log_ids)
