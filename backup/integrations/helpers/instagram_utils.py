from django.conf import settings

from integrations.models.instagram import InstagramPerson, InstagramPost, InstagramHashtag
from integrations.helpers.InstagramAPI.InstagramAPI import InstagramAPI

from .utils import (
    create_post_cache,
)


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


def clear_follower_posts(author):
    [x.delete() for x in author.instagrampost_set.all()]
