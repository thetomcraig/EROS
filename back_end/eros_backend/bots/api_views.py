from django.http import JsonResponse
from django.shortcuts import render

from bots.helpers.twitter_utils import get_top_twitter_bots


def list_all_bots(limit=None):
    top = get_top_twitter_bots()
    return JsonResponse(top)


def get_bot_info(bot_id):
    pass
