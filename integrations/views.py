from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from integrations.models.instagram import InstagramPerson, InstagramPost, InstagramHashtag
from integrations.models.text_message import TextMessage, TextMessageCache, TextMessageMarkov

from integrations.helpers.instagram_utils import (
    generate_instagram_post,
    scrape_all_followers,
    get_instagram_followers,
    get_me_from_instagram,
    refresh_instagram_followers,
    follow_my_instagram_followers,
    refresh_and_return_me_from_instagram,
    scrape_follower,
    clear_follower_posts,
)

from integrations.helpers.text_message_utils import (
    get_text_message_me,
    generate_text,
    clear_texts,
    read_raw_texts,
)

from integrations.helpers.tinder_utils import (
    refresh_tinder,
    auto_tinder_like,
    get_tinder_experiment_data,
)


def home(request):
    if(request.GET.get('text_message_home')):
        return HttpResponseRedirect(reverse('text_message_home'))

    if(request.GET.get('twitter_home')):
        return HttpResponseRedirect(reverse('twitter_home'))

    if(request.GET.get('instagram_home')):
        return HttpResponseRedirect(reverse('instagram_home'))

    if(request.GET.get('tinder_home')):
        return HttpResponseRedirect(reverse('tinder_home'))

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


def instagram_home(request):
    """
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


def tinder_home(request):
    if(request.GET.get('go_back_to_home')):
        return HttpResponseRedirect(reverse('home'))

    if(request.GET.get('refresh')):
        refresh_tinder()
        return HttpResponseRedirect('tinder_home/')

    if(request.GET.get('auto_like')):
        auto_tinder_like(500)
        return HttpResponseRedirect('tinder_home/')

    template = loader.get_template('integrations/tinder_home.html')

    experiment_data = get_tinder_experiment_data()
    context = RequestContext(request, {
        'experiment_data': experiment_data
    })
    return HttpResponse(template.render(context))


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
