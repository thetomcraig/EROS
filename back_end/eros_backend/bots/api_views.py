from django.http import JsonResponse
from django.shortcuts import render

from bots.helpers.twitter_utils import (
    get_top_twitter_bots,
    get_info,
    scrape,
)


def list_all_bots(limit=None):
    top = get_top_twitter_bots()
    return JsonResponse(top)


def get_bot_info(request, bot_id):
    info = get_info(bot_id)
    return JsonResponse(info)


def scrape_bot(response, bot_id):
    response_data = scrape(bot_id)
    return JsonResponse(response_data)


def get_conversation(bot1_id, bot2_id):
    pass


def create_post(bot_id):
    pass


def get_conversation(bot1_id, bot2_id):
    pass


def clear_conversation(bot1_id, bot2_id):
    pass


def clear_conversations(bot_id):
    pass
