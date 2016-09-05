import facebook
from django.db import models
import plain_text_classes
# at artandlogic.com modles for comment storing)


# Classes for storing fb data
class FacebookPerson(plain_text_classes.Person):

    def __str__(self):
        return username


class FacebookPost(models.Model):
    author = models.ForeignKey(FacebookPerson, default=None, null=True)
    index = models.IntegerField(default=0)
    story = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
    message = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
    picture = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
    link = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)
    content = models.CharField(max_length=1000, default='PLACEHOLDER', null=True)

    def __str__(self):
        return_str = \
            ' author: ' + str(self.author) + '\n' + \
            ' index: ' + str(self.index) + '\n' + \
            ' story: ' +str(self.story) + '\n' + \
            ' message: ' + str(self.message) + '\n' + \
            ' picture: ' + str(self.picture) + '\n' + \
            ' link: ' + str(self.link) + '\n' + \
            ' content: ' + self.content
        return return_str


# Classes for scraping and collecting data
# This could be fucked, havet look at it in a while
# SO sorry, I know I'm a bad person
    def get_clean_fb_feed(self):
        """
        For interpreting the raw facebook information and
        storing corresponding objects in the db
        """

        auth = self.social_auth.first()
        graph = facebook.GraphAPI(auth.extra_data['access_token'])
        raw_data = graph.get_object('/me/home')

        data = None
        for key in raw_data:
            if key == 'data':
                data = raw_data[key]
                break

        if not data:
            return data

        clean_data = [
            {
                'from': x['from']['name'],
                'name': x.get('name'),
                'story': x.get('story'),
                'message': x.get('message'),
                'picture': x.get('picture'),
                'link': x.get('link'),
                'friends': x.get('friends'),
                'comments': process_comments(x.get('comments'))
            } for x in data
        ]

        return clean_data


def save_clean_fb_feed(self):
    """
    Takes clean fb data and saves it to the db
    """

    clean_data = self.get_clean_fb_feed()

    for raw_post in clean_data:
        content = {}
        content['story'] = raw_post['story']
        content['message'] = raw_post['message']
        content['picture'] = raw_post['picture']
        content['link'] = raw_post['link']
        content['friends'] = raw_post['story']
        # I want to loop through comments as well


def process_comments(comments):
    """
    Organizes the comment data into a dictionary
    """

    if not comments:
        return None

    data = comments.get('data')
    if not data:
        return None

    clean_data = [
        [
            {'from': x['from']['name']},
            {'message': x.get('message')},
            {'like count': x.get('like_count')}
        ] for x in data
    ]

    return clean_data
