from bs4 import BeautifulSoup
import csv
from datetime import datetime
import glob
import itertools
from matplotlib.pyplot import Figure
import matplotlib.pyplot as plt
import os
import pandas
import random
import re
import subprocess

from django.conf import settings

from integrations.models.instagram import InstagramPerson, InstagramPost, InstagramHashtag
from integrations.models.text_message import TextMessagePerson, TextMessageCache
from integrations.helpers.InstagramAPI.InstagramAPI import InstagramAPI
from integrations.helpers.Tinder.auto_tinder import AutoTinder


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


def scrape_all_followers():
    """
    Look at my timeline and collect posts
    Strip out hash tags and save them as objects
    """
    api = InstagramAPI(settings.INSTAGRAM_USERNAME,
                       settings.INSTAGRAM_PASSWORD)
    api.timelineFeed()
    result = api.LastJson

    if result['status'] != 'ok':
        pass

    items = result['items']

    for item in items:
        user = item['user']
        # Grab the user and update their avatar
        i = InstagramPerson.objects.get_or_create(
            username=user['username'],
            real_name=user['full_name'])[0]
        i.avatar = user['profile_pic_url']
        i.save()
        # Save the post
        text = item['caption']['text']
        post = InstagramPost.objects.get_or_create(content=text)[0]

        create_post_cache(post, i.instagrampostcache_set)

        for word in text.split():
            if word[0] == '#':
                InstagramHashtag.objects.get_or_create(
                    original_post=post, content=word)


def get_instagram_followers():
    followers = InstagramPerson.objects.all().exclude(
        username=settings.INSTAGRAM_USERNAME)
    return followers


def refresh_and_return_me_from_instagram():
    api = InstagramAPI(settings.INSTAGRAM_USERNAME,
                       settings.INSTAGRAM_PASSWORD)
    api.login(force=True)
    api.getProfileData()
    result = api.LastJson
    me = InstagramPerson.objects.get_or_create(
        username=settings.INSTAGRAM_USERNAME,
        first_name='Tom',
        last_name='Craig',
        real_name=result['user']['full_name'],
        avatar=str(result['user']['hd_profile_pic_versions'][0]['url'])
    )

    return me


def get_text_message_me():
    return TextMessagePerson.objects.get_or_create(first_name='Tom', last_name='Craig')[0]


def get_me_from_instagram():
    try:
        return InstagramPerson.objects.get(username=settings.INSTAGRAM_USERNAME)
    except:
        return refresh_and_return_me_from_instagram()


def refresh_instagram_followers():
    api = InstagramAPI(settings.INSTAGRAM_USERNAME,
                       settings.INSTAGRAM_PASSWORD)
    api.login()
    api.getSelfUserFollowers()
    result = api.LastJson

    for user in result['users']:
        person = None
        try:
            person = InstagramPerson.objects.get(
                username=user['username'],
                username_id=user['pk'],
                real_name=user['full_name'])
        except:
            person = InstagramPerson.objects.create(
                username=user['username'],
                username_id=user['pk'],
                real_name=user['full_name'])

        person.avatar = user['profile_pic_url']
        person.save()


def follow_my_instagram_followers():
    api = InstagramAPI(settings.INSTAGRAM_USERNAME,
                       settings.INSTAGRAM_PASSWORD)
    api.login()

    followers = InstagramPerson.objects.all()

    for follower in followers:
        try:
            api.follow(str(follower.username_id))
        except AttributeError as e:
            print e
            return False


def scrape_follower(person):
    api = InstagramAPI(settings.INSTAGRAM_USERNAME,
                       settings.INSTAGRAM_PASSWORD)
    api.login()
    api.getUserFeed(person.username_id)
    result = api.LastJson

    posts = result['items']
    for post in posts:
        caption = post['caption']['text']
        post = person.instagrampost_set.create(content=caption)

        create_post_cache(post, person.instagrampostcache_set)


def generate_instagram_post(author):
    return generate_markov_instagram_post(author)


def generate_markov_instagram_post(person):
    print "Applying markov chains"
    all_caches = person.instagrampostcache_set.all()
    all_beginning_caches = all_caches.filter(beginning=True)

    new_markov_post = person.apply_markov_chains_inner(all_beginning_caches, all_caches)

    content = ""
    for word in new_markov_post[0]:
        content = content + word + " "

    print content[:-1]
    return content[:-1]


def clear_set(set_to_clear):
    [x.delete() for x in set_to_clear]


def clear_follower_posts(author):
    [x.delete() for x in author.instagrampost_set.all()]


def clear_texts(author):
    [x.delete() for x in author.textmessage_set.all()]
    [x.delete() for x in author.textmessagecache_set.all()]


def create_post_cache(post, cache_set):
    """
    Create the postcache item from the new post
    to be used to make the markov post
    """
    word_list = post.content.split()
    for index in range(len(word_list) - 2):
        word1 = word_list[index]
        word2 = word_list[index + 1]
        final_word = word_list[index + 2]

        print "caching:"
        print word1
        print word2
        print "|"
        print "`--> " + final_word

        beginning = False
        if (index == 0):
            beginning = True

        cache_set.create(word1=word1, word2=word2, final_word=final_word, beginning=beginning)


def generate_text():
    me = get_text_message_me()
    all_caches = TextMessageCache.objects.all()
    all_beginning_caches = all_caches.filter(beginning=True)
    print me.apply_markov_chains_inner(all_beginning_caches, all_caches)


def replace_tokens(word_list_and_randomness, token, model_set):
    """
    Takes a list of words and replaces tokens with the
    corresonding models linked to the user
    """
    word_list = word_list_and_randomness[0]
    for word_index in range(len(word_list)):
        if token in word_list[word_index]:
            seed_index = 0
            if len(model_set) > 1:
                seed_index = random.randint(0, len(model_set) - 1)
            try:
                word_list[word_index] = (model_set[seed_index]).content
                print "Replaced " + token

            except IndexError:
                print "failed to replace token:"
                print word_list[word_index]

    return (word_list, word_list_and_randomness[1])


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


def get_tinder_figures_for_time_window(start, end):
    a = AutoTinder(settings.FACEBOOK_ID, settings.FACEBOOK_AUTH_TOKEN, settings.CURRENT_TINDER_EXPERIMENT_NO)

    x_experiment_numbers = [0, 1, 2]
    y_experiment_matches = []
    for i in x_experiment_numbers:
        matches = a.get_matches_for_time_window(start, end)
        y_experiment_matches.append(len(matches))

    fig = Figure()
    ax = fig.add_subplot(111)
    data_df = pandas.read_csv(settings.TINDER_LOGS_LOCATION + 'swipe_sessions/test.csv')
    data_df = pandas.DataFrame(data_df)
    data_df.plot(ax=ax)

    return [fig]


def get_all_tinder_figures():
    y_axis_match_numbers = []

    for i in range(settings.CURRENT_TINDER_EXPERIMENT_NO + 1):
        match_number = get_match_number_for_exp_number(i)
        y_axis_match_numbers.append(match_number)

    fig = plt.figure()
    N = len(y_axis_match_numbers)
    x = range(N)
    width = 1 / 1.5
    plt.bar(x, y_axis_match_numbers, width, color="blue")

    return [fig]


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
