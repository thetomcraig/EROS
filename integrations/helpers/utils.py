import random
import os
import re

import HTMLParser
from datetime import datetime
from bs4 import BeautifulSoup

from django.conf import settings

from integrations.models.twitter import TwitterPost
from integrations.models.instagram import InstagramPerson, InstagramPost, InstagramHashtag
from integrations.models.text_message import TextMessagePerson, TextMessageCache
from integrations.helpers.InstagramAPI.InstagramAPI import InstagramAPI
from integrations.helpers.TweepyScraper import TweepyScraper


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


def scrape_top_twitter_people():
    """
    Fill db with metadata from top 50 users
    Used to update avatars etc
    """
    t = TweepyScraper(
        settings.TWEEPY_CONSUMER_KEY,
        settings.TWEEPY_CONSUMER_SECRET,
        settings.TWEEPY_ACCESS_TOKEN,
        settings.TWEEPY_ACCESS_TOKEN_SECRET)

    names_and_unames = t.scrape_top_users(50)

    return names_and_unames


def scrape_twitter_person(person):
    """
    Scrape the given user with tweepy
    take all of their tweets and
    turn them into TwitterPost objects
    strip out uncommon words (links, hashtags, users)
    and save them seperately in instances, then
    replace with dummy words.
    """
    t = TweepyScraper(
        settings.TWEEPY_CONSUMER_KEY,
        settings.TWEEPY_CONSUMER_SECRET,
        settings.TWEEPY_ACCESS_TOKEN,
        settings.TWEEPY_ACCESS_TOKEN_SECRET)

    tweets = t.get_tweets_from_user(person.username, 100)
    print "scraped %d new tweets" % len(tweets)
    new_post_ids = []
    for tweet in tweets:
        words = tweet.split()

        final_tweet = ""
        for word in words:
            if "@" in word:
                person.twittermention_set.create(content=word)
                word = settings.USER_TOKEN
            if "http" in word:
                person.twitterlink_set.create(content=word)
                word = settings.LINK_TOKEN
            if "#" in word:
                person.twitterhashtag_set.create(content=word)
                word = settings.TAG_TOKEN

            final_tweet = final_tweet + word + " "
        final_tweet = final_tweet[:-1]
        print "final tweet:"
        print final_tweet

        h = HTMLParser.HTMLParser()
        final_tweet = h.unescape(final_tweet.decode('utf-8'))

        post = TwitterPost.objects.create(author=person, content=final_tweet)
        new_post_ids.append(post.id)

        create_post_cache(post, person.twitterpostcache_set)

    return new_post_ids


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


def apply_markov_chains_twitter(person):
    """
    Takes all the words from all the twittter
    posts on the twitterperson.
    Sticks them all into a giant
    list and gives this to the markov calc.
    Save this as a new twitterpostmarkov
    """
    print "Applying markov chains"
    all_beginning_caches = person.twitterpostcache_set.filter(beginning=True)
    all_caches = person.twitterpostcache_set.all()
    new_markov_post = person.apply_markov_chains_inner(
        all_beginning_caches, all_caches)

    # Replace the tokens (twitter specific)
    replace_tokens(new_markov_post, settings.USER_TOKEN,
                   person.twittermention_set.all())
    replace_tokens(new_markov_post, settings.LINK_TOKEN,
                   person.twitterlink_set.all())
    replace_tokens(new_markov_post, settings.TAG_TOKEN,
                   person.twitterhashtag_set.all())

    randomness = new_markov_post[1]
    content = ""
    for word in new_markov_post[0]:
        content = content + word + " "

    person.twitterpostmarkov_set.create(
        content=content[:-1], randomness=randomness)


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
