from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse


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

    if(request.GET.get('tinder_home')):
        return HttpResponseRedirect(reverse('tinder_home'))

    context = RequestContext(request, {'request': request, 'user': request.user})
    return render_to_response('integrations/home.html', context_instance=context)


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
