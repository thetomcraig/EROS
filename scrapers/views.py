from django.shortcuts import render
from django.http import JsonResponse

from integrations.models.twitter import TwitterPerson, TwitterPost, TwitterPostMarkov
from integrations.helpers.utils import scrape_top_twitter_people as utils_scrape_top_twitter_people
from integrations.helpers.utils import scrape_twitter_person, refresh_instagram_followers, follow_my_instagram_followers

def scrape_top_twitter_people(request):
    """
    API for manually scraping
    """
    names_and_unames = utils_scrape_top_twitter_people()

    for entry in names_and_unames:
        person = None
        person = TwitterPerson.objects.get_or_create(username=entry['uname'])[0]

        person.username = entry['uname']
        person.real_name= entry['name']
        person.avatar = entry['avatar']
        person.save()

    all_twitter_people = TwitterPerson.objects.all()
    for person in all_twitter_people:
        scrape_twitter_person(person)

    all_twitter_posts = TwitterPost.objects.all()
    num = len(all_twitter_posts)
    data = {'total num posts': num}
    return JsonResponse({'success': data})

def train_on_text_messages(request):
    """
    Build the markov chain text messages based on a dump
    """
    template = loader.get_template('scrapers/text_message_upload_and_anaylze.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def apply_markov_chains(request):
    """
    API for manually applying markov chains
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
