from django.views.generic.detail import DetailView
from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.models import User

from scrapers.models.plain_text_classes import Person, Sentence, MarkovChain, SentenceCache
from scrapers.models.twitter import TwitterPerson, TwitterPost, TwitterPostMarkov
from scrapers.models.facebook import FacebookPerson, FacebookPost
from scrapers.models.literature import LiteraturePerson, LiteratureSentence, LiteratureSentenceMarkov
from scrapers.models.text_message import TextMessagePerson, TextMessage, TextMessageCache, TextMessageMarkov

from constants import *
import json
import re

def home(request):
  if(request.GET.get('go_to_dash')):
    favorite_people = [] 
    #TODO - force the first one here to see on the dash
    #favorite_people.append(TwitterPerson.objects.all()[0])
    #favorite_people.append(LiteraturePerson.objects.all()[0])
    context = RequestContext(request, \
      {'favorite_people': favorite_people})
    return render_to_response('scrapers/dashboard.html', context_instance=context)

  if(request.GET.get('collect_fb_data')):
    request.user.save_clean_fb_feed()
    post_list = FacebookPost.objects.all()
    context = RequestContext(request, \
      {'request': request, 'user': request.user, 'post_list': post_list})
    return render_to_response('scrapers/post_index.html', context_instance=context)

  if(request.GET.get('go_to_my_texts')):
    markov_texts = TextMessageMarkov.objects.all()
    first_words = TextMessageCache.objects.filter(beginning=True)
    first_words_no_dupes = set([x.word1 for x in first_words])
    context = RequestContext(request,  \
      {'request': request, 'user': request.user, 'first_words': first_words_no_dupes, 'markov_texts': markov_texts})
    return render_to_response('scrapers/text_message_dashboard.html', context_instance=context)

  if(request.GET.get('view_twitter_data')):
    twitter_people = TwitterPerson.objects.all()
    context = RequestContext(request, \
      {'request': request, 'user': request.user, 'twitter_people': twitter_people})
    return render_to_response('scrapers/twitter_people.html', context_instance=context)

  if(request.GET.get('scrape_top_twitter_people')):
    return HttpResponseRedirect('/scrapers/scrape_top_twitter_people/')

  context = RequestContext(request, {'request': request,'user': request.user})
  return render_to_response('scrapers/home.html', context_instance=context)


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
    print text.content
    try:
      if re.match(query, text.content, re.I):
        results.append(text.content)
    except:
      pass

  data = json.dumps(results)
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)


def post_index(request):
  """
  listing all of the posts that belong to a user
  """
  post_list = FacebookPost.objects.all()
  template = loader.get_template('scrapers/post_index.html')
  context = RequestContext(request, {
      'post_list': post_list,
  })
  return HttpResponse(template.render(context))

def twitter_people(request):
  """
  The top twitter profiles, that link to particular users
  """
  twitter_people = TwitterPerson.objects.all()
  template = loader.get_template('scrapers/twitter_people.html')
  context = RequestContext(request, {
      'twitter_people': twitter_people,
  })
  return HttpResponse(template.render(context))
  
def person_detail(request, person_username):
  author = None
  for person in TwitterPerson.objects.all():
    if person.username.strip() == person_username.strip():
      author = person

  if not author:
    for person in LiteraturePerson.objects.all():
      if person.username.strip() == person_username.strip():
        author = person

  #If you are already on the page, these things 
  #will happen when you click buttons
  if(request.GET.get('go_back_to_list')):
    return HttpResponseRedirect('/scrapers/twitter_people/')

  if(request.GET.get('scrape')):
    author.scrape()
    return HttpResponseRedirect('/scrapers/person_detail/'+person_username)

  if(request.GET.get('apply_markov_chains')):
    author.apply_markov_chains()
    return HttpResponseRedirect('/scrapers/person_detail/'+person_username)

  template = loader.get_template('scrapers/person_detail.html')
    
  sentences = []
  markov_sentences = []
  person_type = ''
  
  #Grab data from author if twitter person  
  if isinstance(author, TwitterPerson):
    person_type = str(TwitterPerson)
    twitter_sentences = TwitterPost.objects.filter(author=author)
    sentences = [t.content for t in twitter_sentences] 

    twitter_markov_sentences = author.twitterpostmarkov_set.all().order_by('-randomness')
    markov_sentences = \
      [(t.content.encode('ascii', 'ignore'), \
      t.randomness) for t in twitter_markov_sentences]

  #Grab data from author if literature person  
  if isinstance(author, LiteraturePerson):
    person_type = str(LiteraturePerson)
    literature_sentences = LiteratureSentence.objects.filter(author=author)
    sentences = [t.content for t in literature_sentences] 

    literature_markov_sentences = \
      author.literaturesentencemarkov_set.all().order_by('-randomness')
    markov_sentences = \
      [(t.content.encode('ascii', 'ignore'), \
      t.randomness) for t in literature_markov_sentences]


  context = RequestContext(request, {
      'person': author,
      'person_type': person_type,
      'sentences' : sentences,
      'markov_sentences'  : markov_sentences,
      'len_sentences'  : len(sentences),
      'len_markov_sentences'  : len(markov_sentences),
  })

  return HttpResponse(template.render(context))

def scrape_top_twitter_people(request):
  """
  API for manually scraping
  """
  tom = User.objects.get_or_create(username='tom')[0]
  tom.scrape_top_twitter_people()

  all_twitter_people = TwitterPerson.objects.all()
  for person in all_twitter_people:
    person.scrape()

  all_twitter_posts = TwitterPost.objects.all()
  num = len(all_twitter_posts)
  data = {'total num posts': num}
  return JsonResponse({'success': data})
  
def apply_markov_chains(request):
  """
  API for manually applyin markov chains
  """
  all_twitter_people = TwitterPerson.objects.all()
  for person in all_twitter_people:
    person.apply_markov_chains()

  all_markov_posts = TwitterPostMarkov.objects.all()
  num = len(all_markov_posts)

  data = {'total num posts': num}
  return JsonResponse({'success': data})

def sentiment_analyze(request):
  """
  API for manually applyin markov chains
  """
  all_twitter_people = TwitterPerson.objects.all()
  for person in all_twitter_people:
    for post in person.twitter_post_set.all():
      post.sentiment_analyze()

  data = {'total num posts': num}
  return JsonResponse({'success': data})
