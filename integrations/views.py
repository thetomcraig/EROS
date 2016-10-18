from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from integrations.models.twitter import TwitterPerson, TwitterPost
from integrations.models.text_message import TextMessage, TextMessageCache, TextMessageMarkov
from integrations.helpers.utils import (
    scrape_twitter_person,
    apply_markov_chains_twitter,
    get_num_instagram_followers,
    get_me_from_instagram,
    refresh_instagram_followers,
    follow_my_instagram_followers,
    refresh_and_return_me_from_instagram,
    generate_instagam_post)

import json
import re


def home(request):
    if(request.GET.get('text_message_home')):
        texts = TextMessage.objects.all()
        markov_texts = TextMessageMarkov.objects.all()
        first_words = TextMessageCache.objects.filter(beginning=True)
        first_words_no_dupes = set([x.word1 for x in first_words])
        context = RequestContext(request, {
            'request': request,
            'first_words': first_words_no_dupes,
            'texts': texts,
            'markov_texts': markov_texts})
        return render_to_response('integrations/text_message_home.html', context_instance=context)

    if(request.GET.get('twitter_home')):
        return HttpResponseRedirect(reverse('twitter_home'))

    if(request.GET.get('instagram_home')):
        return HttpResponseRedirect(reverse('instagram_home'))

    context = RequestContext(request, {'request': request, 'user': request.user})
    return render_to_response('integrations/home.html', context_instance=context)


def get_texts(request):
    texts = TextMessage.objects.all()
    q = request.GET.get('term', '')
    return fuzzy_search_query(q, texts)


def get_markov_texts(request):
    texts = TextMessageMarkov.objects.all()
    q = request.GET.get('term', '')
    return fuzzy_search_query(q, texts)


def fuzzy_search_query(query, query_set):
    results = []
    for text in query_set:
        try:
            if re.match(query, text.content, re.I):
                results.append(text.content)
        except:
            pass

    data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def twitter_home(request):
    """
    The top twitter profiles, that link to particular users
    """
    if(request.GET.get('go_back_to_home')):
        return HttpResponseRedirect(reverse('home'))

    if(request.GET.get('scrape_top_twitter_people')):
        return HttpResponseRedirect('/scrapers/scrape_top_twitter_people/')

    twitter_people = TwitterPerson.objects.all()
    template = loader.get_template('integrations/twitter_home.html')
    context = {'twitter_people': twitter_people}
    return HttpResponse(template.render(context, request))


def twitter_person_detail(request, person_username):
    author = None
    for person in TwitterPerson.objects.all():
        if person.username.strip() == person_username.strip():
            author = person

    # If you are already on the page, these things
    # will happen when you click buttons
    if(request.GET.get('go_back_to_list')):
        return HttpResponseRedirect(reverse('twitter_home'))

    if(request.GET.get('scrape')):
        scrape_twitter_person(author)
        return HttpResponseRedirect('/integrations/twitter_person_detail/' + person_username)

    if(request.GET.get('apply_markov_chains')):
        apply_markov_chains_twitter(author)
        return HttpResponseRedirect('/integrations/twitter_person_detail/' + person_username)

    template = loader.get_template('integrations/twitter_person_detail.html')

    sentences = []
    markov_sentences = []
    person_type = ''

    # Grab data from author if twitter person
    if isinstance(author, TwitterPerson):
        person_type = str(TwitterPerson)
        twitter_sentences = TwitterPost.objects.filter(author=author)
        sentences = [t.content for t in twitter_sentences]

        twitter_markov_sentences = author.twitterpostmarkov_set.all().order_by('-randomness')
        markov_sentences = [(t.content.encode('ascii', 'ignore'), t.randomness) for t in twitter_markov_sentences]

    context = RequestContext(request, {
        'person': author,
        'person_type': person_type,
        'sentences': sentences,
        'markov_sentences': markov_sentences,
        'len_sentences': len(sentences),
        'len_markov_sentences': len(markov_sentences),
    })

    return HttpResponse(template.render(context))


def instagram_home(request):
    """
    The top twitter profiles, that link to particular users
    """
    me = get_me_from_instagram()

    if(request.GET.get('go_back_to_home')):
        return HttpResponseRedirect(reverse('home'))

    if(request.GET.get('refresh_followers')):
        refresh_instagram_followers()

    if(request.GET.get('follow_my_followers')):
        follow_my_instagram_followers()

    if(request.GET.get('refresh_me')):
        me = refresh_and_return_me_from_instagram()

    if(request.GET.get('generate_post')):
        generate_instagam_post()

    template = loader.get_template('integrations/instagram_home.html')
    num_posts = 0
    num_followers = get_num_instagram_followers()
    context = {'num_posts': num_posts, 'num_followers': num_followers, 'me': me}
    return HttpResponse(template.render(context, request))
