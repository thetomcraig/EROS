from django.http import JsonResponse

from integrations.models.twitter import TwitterPerson, TwitterPostMarkov


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
    API for manually applying markov chains
    """
    all_twitter_people = TwitterPerson.objects.all()
    for person in all_twitter_people:
        for post in person.twitter_post_set.all():
            post.sentiment_analyze()

    data = {'total num posts': num}
    return JsonResponse({'success': data})
