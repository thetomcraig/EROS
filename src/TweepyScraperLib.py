#streamer class for realtime feedback of a tweets using a given topic

from bs4 import BeautifulSoup
import urllib
import tweepy
import json

class TweepyScraper: 

  ##############################################################################
  # Init
  # Setup the auth info and the api for tweepy
  ##############################################################################
  def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
    '''Setup, using credentials from Twitter'''
    self.consumer_key = consumer_key
    self.consumer_secret = consumer_secret
    self.access_token = access_token
    self.access_token_secret = access_token_secret
    
    self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
    self.auth.set_access_token(self.access_token, self.access_token_secret)
    
    self.api = tweepy.API(self.auth)
    
  ##############################################################################
  # Scrapes the top users on twitter using the top 100 users frontend
  # Returns the list of their usernames
  ##############################################################################
  def scrape_top_users(self):
    url = 'http://twittercounter.com/pages/100'
    response = urllib.urlopen(url)
    html = response.read().decode('utf-8')
    raw = BeautifulSoup(html)
    
    users = raw.findAll('a', {'class': 'uname'})
    #extract just the text, take the @ off their usernames
    users = map(lambda i: i.text, users)
    users = map(lambda i: i.replace("@", ""), users)
          
    return users
    
  ##############################################################################
  # Grabs the tweets from a given user
  ##############################################################################
  def getAllTweetsFromUser(self, screenName):
    alltweets = []  
    #Most recent tweets   
    new_tweets = self.api.user_timeline(screen_name = screenName,count=200)
    #save most recent tweets
    alltweets.extend(new_tweets)
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) < 2000:
      print "getting tweets before %s" % (oldest)
      #all subsiquent requests use the max_id param to prevent duplicates
      new_tweets = self.api.user_timeline(screen_name = screenName,count=200,max_id=oldest)
      #save most recent tweets
      alltweets.extend(new_tweets)
      #update the id of the oldest tweet less one
      oldest = alltweets[-1].id - 1
      
      print "...%s tweets downloaded so far" % (len(alltweets))
    
    #transform the tweepy tweets into a 2D array that will populate the csv  
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
     
    ### 
    #print outtweets
    ###
    
  ##############################################################################
  # Finds trending topics on twitter, returns them in a list
  ##############################################################################  
  def findTrends(self):
    #This will be a one element dict
    trends = self.api.trends_place(1)
    #Extract the actual trends
    data = trends[0] 
    #These are all JSON objects
    #with a name element
    parsedTrends = data['trends']
    #Taking out just the names
    names = [trend['name'] for trend in parsedTrends]
    #Finally, fixing the encoding
    for i in range (len(names)):
      names[i] = names[i].encode('ascii', 'ignore')    
    return names
  
  ##############################################################################
  # Searches for tweets that use a given tag
  ##############################################################################
  def search(self, tag):
    results = self.api.search(q=tag)
    for i in range (len(results)):
      results[i] = (results[i]).text.encode('ascii', 'ignore')
    return results
    
  def stream(self, tag):
    '''Setting up the streamer'''
    l = StdOutListener()
    # There are different kinds of streams: public stream, user stream, multi-user streams
    # In this example follow tag
    # For more details refer to https://dev.twitter.com/docs/streaming-apis
    stream = tweepy.Stream(self.auth, l)
    stream.filter(track=[tag])
  
    
# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)
        # Also, we convert UTF-8 to ASCII ignoring all bad characters sent by users
        print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        print ''
        return True

    def on_error(self, status):
        print status
