from django.views.generic.detail import DetailView
from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from scrapers.models.twitter import TwitterPerson, TwitterPost, TwitterPostMarkov, TwitterPostMarkovPart
from scrapers.models.facebook import FacebookPerson, FacebookPost

from constants import *

def home(request):
	if(request.GET.get('collect_fb_data')):
		request.user.save_clean_fb_feed()
		post_list = FacebookPost.objects.all()
		context = RequestContext(request, {'request': request, 'user': request.user, 'post_list': post_list})
		return render_to_response('scrapers/post_index.html', context_instance=context)

	if(request.GET.get('collect_twitter_data')):
		request.user.scrape_top_twitter_people()
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
	author = TwitterPerson.objects.get_or_create(username=twitter_person_username)[0]

	twitter_posts = TwitterPost.objects.filter(author=author)
	twitter_posts = [t.content for t in twitter_posts] 
	twitter_posts_markov = author.get_full_markov_posts()

	#TODO - this is not returning anything...
<<<<<<< HEAD
	print "alpha"
=======
	twitter_posts_markov_objects = TwitterPostMarkov.objects.filter(author=author)
	print "alpha"
	print twitter_posts
	twitter_posts_markov_objects

	twitter_posts_markov = []
	for post in twitter_posts_markov_objects:
		all_parts = TwitterPostMarkovPart.objects.filter(parent_post__id=post.id)
		complete_post = []
		for part in all_parts:
			complete_post.append([part.content, part.original_tweet_id])

		twitter_posts_markov.append(complete_post)

>>>>>>> 1bcaa646c41495b3e7af694c1d732836252d0b74
	print twitter_posts
	print twitter_posts_markov
	print colors

	context = RequestContext(request, {
			'uname': twitter_person_username,
			'twitter_posts' : twitter_posts,
			'twitter_posts_markov'	: twitter_posts_markov,
			'colors': colors,
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
	tom = User.objects.get_or_create(username='tom')[0]

	all_twitter_people = TwitterPerson.objects.all()
	for person in all_twitter_people:
		person.apply_markov_chains()

	all_markov_posts = TwitterPostMarkov.objects.all()
	num = len(all_markov_posts)
	data = {'total num posts': num}
	return JsonResponse({'success': data})
