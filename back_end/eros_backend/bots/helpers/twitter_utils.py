import json
import nltk
from nltk.probability import FreqDist
import random
import HTMLParser

from django.conf import settings

from bots.models.twitter import TwitterPost, TwitterBot, TwitterConversation, TwitterConversationPost
from bots.helpers.TweepyScraper import TweepyScraper

from .utils import (
    replace_tokens,
    create_post_cache,
)


def get_top_twitter_users(limit=50):
    t = TweepyScraper(
        settings.TWEEPY_CONSUMER_KEY,
        settings.TWEEPY_CONSUMER_SECRET,
        settings.TWEEPY_ACCESS_TOKEN,
        settings.TWEEPY_ACCESS_TOKEN_SECRET)

    names_and_unames = t.scrape_top_users(limit)

    return names_and_unames


def get_top_twitter_bots(limit=50):
    # TODO Use order_by
    top_bots = TwitterBot.objects.all()
    if limit:
        top_bots = top_bots[:limit]
    bot_data = {x.id: {'first_name': x.first_name, 'username': x.username} for x in top_bots}
    return bot_data


def scrape(bot_id):
    bot = TwitterBot.objects.get(id=bot_id)
    scrape_response = scrape_twitter_bot(bot)
    data = {'success': True, 'new tweets': scrape_response['new tweets'], 'tweets':
    scrape_response['tweets']}
    return data
    

def get_info(bot_id):
    bot = TwitterBot.objects.get(id=bot_id)
    fake_posts = {x.id: x.content for x in bot.twitterpost_set.all()}
    real_posts = {x.id: x.content for x in bot.twitterpostmarkov_set.all()}
    bot_data = {
        'real_name': bot.real_name,
        'first_name': bot.first_name,
        'last_name': bot.last_name,
        'username': bot.username,
        'avatar': bot.avatar,
        'real posts': real_posts,
        'fake posts': fake_posts,
    }
    return bot_data


def update_top_twitter_bots():
    names_and_unames = get_top_twitter_users()

    for entry in names_and_unames:
        bot = None
        bot = TwitterBot.objects.get_or_create(username=entry['uname'])[0]

        bot.username = entry['uname']
        bot.real_name= entry['name']
        bot.avatar = entry['avatar']
        bot.save()

    return True


def scrape_top_twitter_bots():
    update_top_twitter_bots()

    all_twitter_bots = TwitterBot.objects.all()
    for bot in all_twitter_bots:
        scrape_twitter_bot(bot)


def scrape_twitter_bot(bot):
    """
    Scrape the given user with tweepy
    take all of their tweets and
    turn them into TwitterPost objects
    strip out uncommon words (links, hashtags, users)
    and save them seperately in instances, then
    replace with dummy words.
    """
    response_data = {}

    t = TweepyScraper(
        settings.TWEEPY_CONSUMER_KEY,
        settings.TWEEPY_CONSUMER_SECRET,
        settings.TWEEPY_ACCESS_TOKEN,
        settings.TWEEPY_ACCESS_TOKEN_SECRET)

    tweets = t.get_tweets_from_user(bot.username, 100)

    response_data['new tweets'] = len(tweets)
    response_data['tweets'] = {}

    new_post_ids = []
    for idx, tweet in enumerate(tweets):
        words = tweet.split()

        final_tweet = ""
        for word in words:
            if "@" in word:
                bot.twittermention_set.create(content=word)
                word = settings.USER_TOKEN
            if "http" in word:
                bot.twitterlink_set.create(content=word)
                word = settings.LINK_TOKEN
            if "#" in word:
                bot.twitterhashtag_set.create(content=word)
                word = settings.TAG_TOKEN

            final_tweet = final_tweet + word + " "
        final_tweet = final_tweet[:-1]

        response_data['tweets'][idx] = final_tweet

        h = HTMLParser.HTMLParser()
        final_tweet = h.unescape(final_tweet.decode('utf-8'))

        post = TwitterPost.objects.create(author=bot, content=final_tweet, fake=False)

        create_post_cache(post, bot.twitterpostcache_set)

    return response_data 


def get_or_create_conversation(bot_username, partner_username):
    bot = TwitterBot.objects.get(username=bot_username)
    partner = TwitterBot.objects.get(username=partner_username)

    conversation = None
    try:
        conversation = TwitterConversation.objects.get(author=bot, partner=partner)
    except:
        try:
            conversation = TwitterConversation.objects.get(author=partner, partner=bot)
        except:
            pass
    if not conversation:
        conversation = TwitterConversation.objects.create(author=bot, partner=partner)

    return conversation


def clear_twitter_conversation(bot_username, partner_username):
    conversation = get_or_create_conversation(bot_username, partner_username)
    if conversation:
        conversation.twitterconversationpost_set.all().delete()
        return True
    return False


def clear_all_twitter_conversations(bot_username):
    bot = TwitterBot.objects.get(username=bot_username)
    conversations = TwitterConversation.objects.filter(author=bot)
    for c in conversations:
        c.delete()


def generate_new_conversation_post_text(current_conversation):
    sorted_conversation = current_conversation.twitterconversationpost_set.order_by('index').all()
    last_post = sorted_conversation.last()
    last_speaker = last_post.post.author if last_post else current_conversation.author
    next_speaker = \
        current_conversation.author if current_conversation.author != last_speaker else current_conversation.partner

    # Aanalyze what's been said
    index = 0
    for p in sorted_conversation:
        index += 1
        # fancy alg here
        pass

    # Pick something new to say in response
    posts = [x.content for x in next_speaker.twitterpost_set.all()]
    retweets = [x for x in posts if 'RT' in x and settings.LINK_TOKEN not in x]

    reply_source = retweets if len(retweets) else posts
    # pick a random retweet to respond with
    reply = reply_source[random.randrange(0, len(reply_source)) - 1]
    # replace the user token tag with the user who is in the convo
    reply = reply.replace(settings.USER_TOKEN, '@' + last_speaker.username, 1)
    # Remove multiple tags
    reply = reply.replace(settings.USER_TOKEN, '')
    # replace the hashtag token with a random hashtag
    hashtags = [x.content for x in next_speaker.twitterhashtag_set.all()]
    random_hashtag = 'HASHTAG'
    if len(hashtags):
        random_hashtag = hashtags[random.randrange(0, len(hashtags) - 1)]
    reply = reply.replace(settings.TAG_TOKEN, random_hashtag, 1)
    # Remove multiple tags
    reply = reply.replace(settings.TAG_TOKEN, '')

    # Remove RT
    reply = reply.replace('RT', '')
    # Fix spacing
    reply = reply.replace('  ', ' ')
    return index, next_speaker, reply


def add_to_twitter_conversation(bot_username, partner_username):
    conversation = get_or_create_conversation(bot_username, partner_username)

    new_index, new_author, new_content = generate_new_conversation_post_text(conversation)
    new_post = new_author.twitterpost_set.create(content=new_content, fake=True)

    TwitterConversationPost.objects.create(
        post=new_post,
        conversation=conversation,
        author=new_author,
        index=new_index
    )


def create_markov_post(bot_id):
    """
    Takes all the words from all the twitter
    posts on the twitterbot.
    Sticks them all into a giant
    list and gives this to the markov calc.
    Save this as a new twitterpostmarkov
    """
    bot = TwitterBot.objects.get(id=bot_id)

    all_beginning_caches = bot.twitterpostcache_set.filter(beginning=True)
    all_caches = bot.twitterpostcache_set.all()
    new_markov_post = bot.apply_markov_chains_inner(all_beginning_caches, all_caches)

    # Replace the tokens (twitter specific)
    replace_tokens(new_markov_post, settings.USER_TOKEN,
                   bot.twittermention_set.all())
    replace_tokens(new_markov_post, settings.LINK_TOKEN,
                   bot.twitterlink_set.all())
    replace_tokens(new_markov_post, settings.TAG_TOKEN,
                   bot.twitterhashtag_set.all())

    randomness = new_markov_post[1]
    content = " ".join(new_markov_post[0])

    new_markov_post = bot.twitterpostmarkov_set.create(content=content, randomness=randomness)
    return new_markov_post.content


def find_word_frequency_for_user(username):
    words = FreqDist()

    bot = TwitterBot.objects.get(username=username)
    for post in bot.twitterpost_set.all():
        for word in nltk.tokenize.word_tokenize(post.content):
            words[word] += 1


def get_bot_attributes(username):
    classifier_metrics = {
        'mention_percentage': -1,
        'retweet_percentage': -1,
        'link_percentage': -1,
        'hash_percentage': -1,
        'verbosity': -1,
    }
    bot = TwitterBot.objects.get(username=username)
    real_posts = bot.twitterpost_set.filter(fake=False)

    mention_tweets = 0
    retweet_tweets = 0
    link_tweets = 0
    hash_tweets = 0
    total_word_number = 0
    for post in real_posts:
        mention_tweets += 1 if settings.USER_TOKEN in post.content else 0
        retweet_tweets += 1 if 'RT' in post.content else 0
        link_tweets += 1 if settings.LINK_TOKEN in post.content else 0
        hash_tweets += 1 if settings.TAG_TOKEN in post.content else 0
        total_word_number += len(post.content.split(' '))

    total_posts_len = 1.0
    if len(real_posts) > 0:
        total_posts_len = float(len(real_posts))

    classifier_metrics['mention_percentage'] = mention_tweets / total_posts_len
    classifier_metrics['retweet_percentage'] = retweet_tweets / total_posts_len
    classifier_metrics['link_percentage'] = link_tweets / total_posts_len
    classifier_metrics['hash_percentage'] = hash_tweets / total_posts_len
    classifier_metrics['verbosity'] = total_word_number / 144 * total_posts_len
    return classifier_metrics
