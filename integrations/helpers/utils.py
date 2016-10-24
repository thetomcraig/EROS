import random
import HTMLParser
from django.conf import settings

from integrations.models.twitter import TwitterPerson, TwitterPost, TwitterPostCache, TwitterPostMarkov
from integrations.models.instagram import InstagramPerson, InstagramPost, InstagramHashtag
from integrations.helpers.InstagramAPI.InstagramAPI import InstagramAPI
from integrations.helpers.TweepyScraper import TweepyScraper

def read_source_into_sentence_list(source_file):
    """
    Reads a text file and returns its contents as list of sentances
    Split at punctuations
    Ignores words with punctuation in them, like Mr. and Mrs.
    """
    lines = []
    punctuations = [".", "!", "?"]
    ignored_words = ["Mr.", "Mrs."]
    with open(source_file, "r") as file:
        line = []
        for file_line in file:
            for word in file_line.split():
                line.append(word)
                if any(p in word for p in punctuations):
                    if all(not i in word for i in ignored_words):
                        lines.append(line)
                        line = []

    return lines


def scrape_all_followers():
    """
    Look at my timeline and collect posts
    Strip out hash tags and save them as objects
    """
    api = InstagramAPI(settings.INSTAGRAM_USERNAME, settings.INSTAGRAM_PASSWORD)
    api.login()
    api.timelineFeed()
    result = api.LastJson

    if result['status'] != 'ok':
        pass

    items = result['items']

    for item in items:
        user = item['user']
        # Grab the user and update their avatar
        i = InstagramPerson.objects.get_or_create(
            username = user['username'],
            real_name = user['full_name'])[0]
        i.avatar = user['profile_pic_url']
        i.save()
        # Save the post 
        text = item['caption']['text']
        post = InstagramPost.objects.get_or_create(content=text)[0]

        for word in text.split():
            if word[0] == '#':
                InstagramHashtag.objects.get_or_create(original_post=post, content=word)

def get_instagram_followers():
    followers = InstagramPerson.objects.all().exclude(username=settings.INSTAGRAM_USERNAME)
    return followers


def refresh_and_return_me_from_instagram():
    api = InstagramAPI(settings.INSTAGRAM_USERNAME, settings.INSTAGRAM_PASSWORD)
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

def get_me_from_instagram():
    try:
        return InstagramPerson.objects.get(username=settings.INSTAGRAM_USERNAME)
    except:
        return refresh_and_return_me_from_instagram()

def refresh_instagram_followers():
    api = InstagramAPI(settings.INSTAGRAM_USERNAME, settings.INSTAGRAM_PASSWORD)
    api.login()
    api.getSelfUserFollowers()
    result = api.LastJson

    for user in result['users']:
        person = None
        try:
            person = InstagramPerson.objects.get(
                username = user['username'],
                username_id = user['pk'],
                real_name = user['full_name'])
        except:
            person = InstagramPerson.objects.create(
                username = user['username'],
                username_id = user['pk'],
                real_name = user['full_name'])

        person.avatar = user['profile_pic_url']
        person.save()

def follow_my_instagram_followers():
    api = InstagramAPI(settings.INSTAGRAM_USERNAME, settings.INSTAGRAM_PASSWORD)
    api.login()

    followers = InstagramPerson.objects.all()

    for follower in followers:
        try:
            api.follow(str(follower.username_id))
        except AttributeError as e:
            print e
            return False

def generate_instagam_post():
    api = InstagramAPI(settings.INSTAGRAM_USERNAME, settings.INSTAGRAM_PASSWORD)
    api.login()

    isabel = InstagramPerson.objects.get(username='lemonadventuretime')
    person = isabel 

    api.getUserFeed(person.username_id)
    result = api.LastJson
    posts = result['items']
    for post in posts:
        caption = post['caption']['text']

        new_caption = ''
        new_post = person.instagrampost_set.create(content=new_caption)

        for word in caption:
            if "#" in word:
                new_post.instagramhashtag_set.create(content=word, original_post=new_post)
                word = settings.TAG_TOKEN

            new_caption= new_caption + word + ' '
        new_caption = new_caption[:-1]

        new_post.content = new_caption
        new_post.save()



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

        if ('RT' in tweet):
            print "skipping retweets"
            continue
        if (len(words) < 1):
            print "skipping short tweets"
            continue

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
        create_post_cache(person, post)
        new_post_ids.append(post.id)

    return new_post_ids

def create_post_cache(person, post):
    """
    Create the postcache item from the new post
    to be used to make the markov post
    """
    word_list = post.content.split()
    for index in range(len(word_list) - 2):
        print "caching:"
        word1 = word_list[index]
        word2 = word_list[index + 1]
        final_word = word_list[index + 2]

        beginning = False
        if (index == 0):
            beginning = True
        post_cache = TwitterPostCache(author=person, word1=word1, word2=word2, final_word=final_word, beginning=beginning)
        post_cache.save()

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
    new_markov_post = person.apply_markov_chains_inner(all_beginning_caches, all_caches)

    # Replace the tokens (twitter specific)
    replace_tokens(new_markov_post, settings.USER_TOKEN, person.twittermention_set.all())
    replace_tokens(new_markov_post, settings.LINK_TOKEN, person.twitterlink_set.all())
    replace_tokens(new_markov_post, settings.TAG_TOKEN, person.twitterhashtag_set.all())

    randomness = new_markov_post[1]
    content = ""
    for word in new_markov_post[0]:
        content = content + word + " "

    person.twitterpostmarkov_set.create(content=content[:-1], randomness=randomness)

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


