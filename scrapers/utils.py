import random
from scrapers.InstagramAPI.InstagramAPI import InstagramAPI
from scrapers.models.instagram import InstagramPerson, InstagramPost, InstagramHashtag
from django.conf import settings 

def read_source_into_sentence_list(source_file):
	"""
	Reads a text file and returns its contents as list of sentances
	Split at punctuations
	Ignores words with punctuation in them, like Mr. and Mrs.
	"""
	lines = []
	punctuations = [".", "!", "?"]
	ignored_words = ["Mr.", "Mrs."]
	with open(source_file, "r") as file:
		line = []
		for file_line in file:
			for word in file_line.split():
				line.append(word)
				if any(p in word for p in punctuations):
					if all(not i in word for i in ignored_words):					
						lines.append(line)
						line = []

	return lines

 
def collect_hashtags():
    """
    Look at my timeline and collect posts
    Strip out hash tabs and save them as objects
    """
    api = InstagramAPI(settings.INSTAGRAM_USERNAME, settings.INSTAGRAM_PASSWORD)
    api.login() 
    api.timelineFeed()
    result = api.LastJson

    if result['status'] != 'ok':
        pass

    num_results = result['num_results']

    items = result['items']

    for item in items:
        user = item['user']

        i = InstagramPerson.objects.get_or_create(
            username = user['username'], 
            real_name = user['full_name'])[0]

        i.avatar = user['profile_pic_url']
        i.save()

        post = InstagramPost.objects.get_or_create(content = item['caption']['text'])
        
        for comment in item['comments']:
            print comment['text']
            print comment['user']['username']

        print "\n"
            

def follow_my_followers():
    api = InstagramAPI(settings.INSTAGRAM_USERNAME, settings.INSTAGRAM_PASSWORD)
    api.login() 
    api.getSelfUserFollowers()
    result = api.LastJson
    for user in result['users']:
        print user['username']
        print user['full_name']
        print user['profile_pic_url']


    
