from django.views.generic.detail import DetailView
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from scrapers.models import TwitterPerson, FacebookPerson
from .models import FacebookPost, TwitterPost, TwitterPostMarkov

def home(request):
  if(request.GET.get('collect_fb_data')):
    request.user.save_clean_fb_feed()
    post_list = FacebookPost.objects.all()
    context = RequestContext(request, {'request': request, 'user': request.user, 'post_list': post_list})
    return render_to_response('scrapers/post_index.html', context_instance=context)

  if(request.GET.get('collect_twitter_data')):
    #request.user.scrape_top_twitter_people()
    twitter_people = TwitterPerson.objects.all()
    context = RequestContext(request, {'request': request, 'user': request.user, 'twitter_people': twitter_people})
    return render_to_response('scrapers/twitter_people.html', context_instance=context)
  
  context = RequestContext(request, {'request': request,'user': request.user})
  return render_to_response('scrapers/home.html', context_instance=context)

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
  
def twitter_person_detail(request, twitter_person_username):
  template = loader.get_template('scrapers/twitter_person_detail.html')
  author = TwitterPerson.objects.filter(username=twitter_person_username)[0]

  #request.user.scrape_twitter_person(twitter_person_username)

  twitter_posts = TwitterPost.objects.filter(author=author)
  twitter_posts = [t.content for t in twitter_posts] 

  request.user.apply_markov_chains(author, twitter_posts)

  twitter_posts_markov_objects = TwitterPostMarkov.objects.filter(author=author)
  twitter_posts_markov = [t.content for t in twitter_posts_markov_objects]
  #Why can't it find id's ? json error...
  markov_ids = [t.get_ids() for t in twitter_posts_markov_objects]

  context = RequestContext(request, {
      'uname': twitter_person_username,
      'twitter_posts' : twitter_posts,
      'twitter_posts_markov'  : twitter_posts_markov,
      'markov_ids'  : markov_ids 
  })

  return HttpResponse(template.render(context))
