#Driver file tests all the python classes

#########
# Setup #
#########

#Tweepy
from TweepyScraper import TweepyScraper

scraper = TweepyScraper('cTNpzIz6JxC9MwwmtKuMTYshL', 'TfUjt5LjbL2Rrrj8Q4bMF6muNJ8qUeChIMhKjm6ohsNbUqMkgo', '14404065-baBGgZmVoCnZEU1L0hCVq6ed6qHDFXVrLSQpAKXcw', '3jbRjcgZV82OGLOsxv9Xg8G29h1oc9l9kqKTMXH4vEPNi')

"""
#Databaser
from Databaser import Databaser
import subprocess as sub

#Starting the mongod server
p = sub.Popen('mongod', stdout=sub.PIPE, stderr=sub.PIPE)

#databaser = Databaser()
"""

###########
# Testing #
###########
#Grab the top 100 twitter users
topUsers = scraper.scrapeTopUsers()

#Add these to the users collection in the database
#databaser.insertUsers(topUsers)

allTweetsFromAllUsers = map(lambda i: scraper.getAllTweetsFromUser(i), topUsers)
print topUsers

"""
import nltk

pos_tweets = [('I love this food', 'positive'), \
('I really like this band', 'positive'), \
('This is my favorite place to eat', 'positive'), \
('I feel really good', 'positive'), \
]

neg_tweets = [('I hate this food', 'negative'), \
('I do not like this band', 'negative'), \
('This is my least favorite place to eat', 'negative'), \
('I feel really bad', 'negative'), \
]

tweets = []
#Making the list of tweets with sentiments attached
#Took out words with less than 3 letters
for (words, sentiment) in pos_tweets + neg_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered, sentiment))

#Functions used below
#Returns all the words from the tweets
def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words

#Returns the features, using the distribution of words in the tweets
def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features
    
word_features = get_word_features(get_words_in_tweets(tweets))

#This will take the words from all the tweets and list them in order of frequency
print word_features


def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features
    


"""

  
  
  

























#####################
#   Bot testing     #
#####################
'''
#Bot2 testing....
import Bot2

Eve = Bot2.Bot2()
Adam = Bot2.Bot2()

Eve.setEmotionRange("happiness", 5)
Eve.setEmotionRange("sadness", 2)
Eve.setEmotion("happiness", 7)
Eve.setEmotion("sadness", 4)


#####################
#  Parser testing   #
#####################

import os
import Parser
import QuoteItem
#Create list of quotes from the database
quotePath = os.path.realpath(__file__)             #These three lines find the
quotePath = quotePath[:(len(quotePath)-10)]        #path to the database, this
textFilePath = quotePath + "/quoteDB.example.txt"  #could cause problems later...

raw = open(textFilePath).read()                    #Reading the database
quoteList = raw.split("\n")						   #List constructed

#Now we have a list with all he quotes
#Testing the quoteItem and Parser classes
print "The original quote:"
print quoteList[4]                                 #Print the orginal line

quoteItem1 = QuoteItem.QuoteItem(quoteList[4])     #Make a new quoteItem w/ the line
parser1 = Parser.Parser(quoteItem1)			       #Make a new parser w/ the quoteitem
parser1.parse()   							       #Parse the parser's quote
'''
