from django.http import JsonResponse
from django.shortcuts import render

from bots.helpers.twitter_utils import (
    get_top_twitter_bots,
    get_info,
    scrape,
    create_markov_post,
)


def list_all_bots(limit=None):
    top = get_top_twitter_bots()
    return JsonResponse(top)


def get_bot_info(request, bot_id):
    info = get_info(bot_id)
    return JsonResponse(info)


def scrape_bot(request, bot_id):
    response_data = scrape(bot_id)
    return JsonResponse(response_data)


def get_conversation(bot1_id, bot2_id):
    pass


def create_post(request, bot_id):
    new_markov_post = create_markov_post(bot_id)
    return JsonResponse({'new post': new_markov_post})


def get_conversation(bot1_id, bot2_id):
    pass


def clear_conversation(bot1_id, bot2_id):
    pass


def clear_all_conversations(bot_id):
    pass
