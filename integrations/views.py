from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse


from integrations.models.twitter import TwitterPerson, TwitterPost
from integrations.models.instagram import InstagramPerson, InstagramPost, InstagramHashtag
from integrations.models.text_message import TextMessage, TextMessageCache, TextMessageMarkov
from integrations.forms import PoolForm
from integrations.helpers.utils import (
    scrape_twitter_person,
    add_to_twitter_conversation,
    apply_markov_chains_twitter,
    get_conversation,
    get_instagram_followers,
    get_text_message_me,
    get_me_from_instagram,
    scrape_all_followers,
    refresh_instagram_followers,
    follow_my_instagram_followers,
    refresh_and_return_me_from_instagram,
    scrape_follower,
    scrape_top_twitter_people,
    update_top_twitter_people,
    clear_follower_posts,
    clear_set,
    generate_text,
    clear_texts,
    generate_instagram_post,
    read_raw_texts)


def home(request):
    if(request.GET.get('text_message_home')):
        return HttpResponseRedirect(reverse('text_message_home'))

    if(request.GET.get('twitter_home')):
        return HttpResponseRedirect(reverse('twitter_home'))

    if(request.GET.get('instagram_home')):
        return HttpResponseRedirect(reverse('instagram_home'))

    context = RequestContext(request, {'request': request, 'user': request.user})
    return render_to_response('integrations/home.html', context_instance=context)


def text_message_home(request):
    me = get_text_message_me()

    if(request.GET.get('go_back_to_home')):
        return HttpResponseRedirect(reverse('home'))

    if(request.GET.get('read_raw_texts')):
        read_raw_texts('/Users/tom/Dropbox/TomCraig/Projects/EROS/iOS_backup/')
        return HttpResponseRedirect('text_message_home/')

    if(request.GET.get('generate_text')):
        generate_text()
        return HttpResponseRedirect('text_message_home/')

    if(request.GET.get('clear_texts')):
        clear_texts(me)
        return HttpResponseRedirect('text_message_home/')

    texts = TextMessage.objects.all()
    caches = TextMessageCache.objects.all()
    beginning_caches = caches.filter(beginning=True)
    markov_texts = TextMessageMarkov.objects.all()

    template = loader.get_template('integrations/text_message_home.html')
    context = RequestContext(request, {
        'request': request,
        'texts': texts,
        'len_texts': len(texts),
        'len_caches': len(caches),
        'len_beginning_caches': len(beginning_caches),
        'markov_texts': markov_texts})
    return HttpResponse(template.render(context, request))


def twitter_home(request):
    """
    The top twitter profiles, that link to particular users
    """
    if(request.GET.get('go_back_to_home')):
        return HttpResponseRedirect(reverse('home'))

    if(request.GET.get('scrape_top_twitter_people')):
        scrape_top_twitter_people()
        return HttpResponseRedirect('twitter_home/')

    if(request.GET.get('update_top_twitter_people')):
        update_top_twitter_people()
        return HttpResponseRedirect('twitter_home/')

    twitter_people = TwitterPerson.objects.all()
    template = loader.get_template('integrations/twitter_home.html')
    context = {'twitter_people': twitter_people}
    return HttpResponse(template.render(context, request))


def instagram_home(request):
    """
    The top twitter profiles, that link to particular users
    """
    me = get_me_from_instagram()

    if(request.GET.get('go_back_to_home')):
        return HttpResponseRedirect(reverse('home'))

    if(request.GET.get('scrape_all_followers')):
        scrape_all_followers()
        return HttpResponseRedirect('instagram_home/')

    if(request.GET.get('refresh_followers')):
        refresh_instagram_followers()
        return HttpResponseRedirect('instagram_home/')

    if(request.GET.get('follow_my_followers')):
        follow_my_instagram_followers()
        return HttpResponseRedirect('instagram_home/')

    if(request.GET.get('refresh_me')):
        me = refresh_and_return_me_from_instagram()
        return HttpResponseRedirect('instagram_home/')

    if(request.GET.get('generate_post')):
        generate_instagram_post()
        return HttpResponseRedirect('instagram_home/')

    template = loader.get_template('integrations/instagram_home.html')
    num_posts = 0
    followers = get_instagram_followers()
    num_followers = len(followers)
    context = {'num_posts': num_posts, 'followers': followers, 'num_followers': num_followers, 'me': me}
    return HttpResponse(template.render(context, request))


def twitter_person_detail(request, person_username):
    if request.method == 'POST':
        form = PoolForm(request.POST)
        if 'go_to_conversation' in request.POST.keys():
            form.is_valid()
            for key in request.POST.keys():
                if key.startswith('twitter_people__'):
                    partner_username = key.replace('twitter_people__', '')
                    return HttpResponseRedirect(reverse('twitter_conversation', 
                           args=(person_username, partner_username)))

    author = None
    all_people = TwitterPerson.objects.all()
    for person in all_people:
        if person.username.strip() == person_username.strip():
            author = person

    all_people_json = {x.username: x.real_name for x in all_people}
    pool_json = {x.username: x.real_name for x in author.pool.all()}
    pool_form = PoolForm(initial={'twitter_people': all_people_json})

    sentences = []
    markov_sentences = []
    person_type = ''

    # Grab data from author if twitter person
    if isinstance(author, TwitterPerson):
        person_type = str(TwitterPerson)
        sentences = TwitterPost.objects.filter(author=author)

        markov_sentences = author.twitterpostmarkov_set.all().order_by('-randomness')

    sentences_to_render = markov_sentences
    # If you are already on the page, these things
    # will happen when you click buttons
    if(request.GET.get('go_back_to_list')):
        return HttpResponseRedirect(reverse('twitter_home'))

    if(request.GET.get('scrape')):
        scrape_twitter_person(author)
        return HttpResponseRedirect('/integrations/twitter_person_detail/' + person_username)

    if(request.GET.get('show_original')):
        sentences_to_render = sentences

    if(request.GET.get('show_markov')):
        sentences_to_render = markov_sentences

    if(request.GET.get('generate_post')):
        apply_markov_chains_twitter(author)
        return HttpResponseRedirect('/integrations/twitter_person_detail/' + person_username)

    if(request.GET.get('clear_posts')):
        clear_set(author.twitterpost_set.all())
        clear_set(author.twitterpostcache_set.all())
        clear_set(author.twitterpostmarkov_set.all())
        return HttpResponseRedirect('/integrations/twitter_person_detail/' + person_username)

    if(request.GET.get('show_pool')):
        pool_form = PoolForm(initial={'twitter_people': pool_json})

    if(request.GET.get('show_all')):
        pool_form = PoolForm(initial={'twitter_people': all_people_json})

    if(request.GET.get('add_selected_to_pool')):
        pass

    template = loader.get_template('integrations/twitter_person_detail.html')
    context = RequestContext(request, {
        'pool_form': pool_form,
        'person': author,
        'person_type': person_type,
        'sentences': sentences_to_render,
        'len_sentences': len(sentences),
        'len_markov_sentences': len(markov_sentences),
    })

    return HttpResponse(template.render(context))


def twitter_conversation(request, person_username, partner_username):
    if(request.GET.get('go_back_to_list')):
        return HttpResponseRedirect('/integrations/')

    if(request.GET.get('generate_conversation')):
        add_to_twitter_conversation(person_username, partner_username)
        return HttpResponseRedirect('/integrations/twitter_conversation/%s/%s/' % (person_username, partner_username))

    template = loader.get_template('integrations/twitter_conversation.html')
    person = TwitterPerson.objects.get(username=person_username)
    partner = TwitterPerson.objects.get(username=partner_username)
    conversation = person.twitterconversation_set.get_or_create(author=person, partner=partner)[0]
    sentences = person.twitterconversationpost_set.filter(conversation__id=conversation.id)
    context = RequestContext(request, {
        'request': request,
        'sentences': sentences,
        'person_username': person_username,
        'partner_username': partner_username,
    })
    return HttpResponse(template.render(context, request))


def instagram_person_detail(request, person_username):
    author = None
    for person in InstagramPerson.objects.all():
        if person.username.strip() == person_username.strip():
            author = person

    if(request.GET.get('go_back_to_list')):
        return HttpResponseRedirect('/integrations/instagram_home')

    if(request.GET.get('scrape')):
        scrape_follower(author)
        return HttpResponseRedirect('/integrations/instagram_person_detail/' + person_username)

    if(request.GET.get('generate_post')):
        generate_instagram_post(author)
        return HttpResponseRedirect('/integrations/instagram_person_detail/' + person_username)

    if(request.GET.get('clear_follower_posts')):
        clear_follower_posts(author)
        return HttpResponseRedirect('/integrations/instagram_person_detail/' + person_username)

    posts = InstagramPost.objects.filter(author=author)
    hashtags = InstagramHashtag.objects.filter(original_post__author=author)
    context = RequestContext(request, {
        'person': author,
        'posts': posts,
        'len_posts': len(posts),
        'hashtags': hashtags,
        'len_hashtags': len(hashtags),
    })

    template = loader.get_template('integrations/instagram_person_detail.html')

    return HttpResponse(template.render(context))
