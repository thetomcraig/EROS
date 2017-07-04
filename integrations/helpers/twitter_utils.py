from datetime import datetime
import HTMLParser

from django.conf import settings

from integrations.models.twitter import TwitterPost, TwitterPerson, TwitterConversation, TwitterConversationPost
from integrations.helpers.TweepyScraper import TweepyScraper

from .utils import (
    replace_tokens,
    create_post_cache,
)


def get_top_twitter_users():
    t = TweepyScraper(
        settings.TWEEPY_CONSUMER_KEY,
        settings.TWEEPY_CONSUMER_SECRET,
        settings.TWEEPY_ACCESS_TOKEN,
        settings.TWEEPY_ACCESS_TOKEN_SECRET)

    names_and_unames = t.scrape_top_users(50)

    return names_and_unames


def update_top_twitter_people():
    names_and_unames = get_top_twitter_users()

    for entry in names_and_unames:
        print entry
        person = None
        person = TwitterPerson.objects.get_or_create(username=entry['uname'])[0]

        person.username = entry['uname']
        person.real_name= entry['name']
        person.avatar = entry['avatar']
        print entry['avatar']
        person.save()

    return True


def scrape_top_twitter_people():
    update_top_twitter_people()

    all_twitter_people = TwitterPerson.objects.all()
    for person in all_twitter_people:
        scrape_twitter_person(person)


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


def get_or_create_conversation(person_username, partner_username):
    person = TwitterPerson.objects.get(username=person_username)
    partner = TwitterPerson.objects.get(username=partner_username)

    conversation = None
    try:
        conversation = TwitterConversation.objects.get(author=person, partner=partner)
    except:
        try:
            conversation = TwitterConversation.objects.get(author=partner, partner=person)
        except:
            pass
    if not conversation:
        print 'beta'
        conversation = TwitterConversation.objects.create(author=person, partner=partner)

    return conversation


def clear_twitter_conversation(person_username, partner_username):
    conversation = get_or_create_conversation(person_username, partner_username)
    if conversation:
        conversation.twitterconversationpost_set.all().delete()
        return True
    return False


def clear_all_twitter_conversations(person_username):
    person = TwitterPerson.objects.get(username=person_username)
    conversations = TwitterConversation.objects.filter(author=person)
    for c in conversations:
        c.delete()


def generate_new_conversation_post(current_conversation):
    index = 0
    for post in current_conversation.twitterconversationpost_set.all():
        index = index + 1
        print post
    return 'TEST + %s' % str(datetime.now()), index


def add_to_twitter_conversation(person_username, partner_username):
    person = TwitterPerson.objects.get(username=person_username)
    conversation = get_or_create_conversation(person_username, partner_username)
    print conversation.id

    new_content, new_index = generate_new_conversation_post(conversation)
    print new_content
    print new_index
    new_post = person.twitterpost_set.create(content=new_content)

    TwitterConversationPost.objects.create(
        post=new_post,
        conversation=conversation,
        author=person,
        index=new_index
    )


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
