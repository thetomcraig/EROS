#Class for databasing tasks

import pymongo

class Databaser: 

  ##############################################################################
  # Init
  # Setup the connection to the server and connect up the data base that has 
  # tweet and trend collections.  They are called "tweetsCollection" and 
  # "trendsCollection", but we can access with the class variables in the init
  ##############################################################################
  def __init__(self):
    #Connecting to Mongo DB, this requires
    #that a mongod instance is running, and
    #I do this with the "mongod" command
    try:
        self.conn=pymongo.MongoClient()
        print "Connected to client"
    except pymongo.errors.ConnectionFailure, e:
       print "Could not connect to client: %s" % e 
    
    #creating a database dynamically
    #If this has aready been created,
    #it will just connect
    self.db = self.conn.tweetsDB
      
    #Creating collections for this database
    #testing one for top tweets and one for
    #trending topics
    self.tweets = self.db.tweetsCollection
    self.trends = self.db.trendsCollection
    self.users = self.db.usersCollection
    
  ##############################################################################
  # Inserts multiple tweets that are all in a list, by calling the singular 
  # insert tweet function
  ##############################################################################
  def insertTweets(self, tweetsList):
    pass
    
  ##############################################################################
  # Inserting a single tweet.  Not sure yet what features I want to save from
  # the tweets, but this wil look at all those features and put them in a JSON
  # like data structure for storing in the database
  ##############################################################################
  def insertTweet(self, tweet):
    #Creating the object and filling its fields
    data = {}
    data['tweet'] = tweet
    self.tweets.insert(data)
    
  ##############################################################################
  # Inserts multiple users in a list, calling the singular function
  ##############################################################################
  def insertUsers(self, userList):
    map(lambda i: self.insertUser(i), userList)
    
  ##############################################################################
  # Inserting a single user.
  ##############################################################################
  def insertUser(self, user):
    data = {}
    data['user'] = user
    self.users.insert(data)
    
  ##############################################################################
  # Retrun a requested database, 0 = tweets, 1 = trends, 2 = users
  ############################################################################## 
  def listDB(self, databaseNo):
    if (databaseNo == 0):
      return list(self.tweets.find())
    if (databaseNo == 1):
      return list(self.trends.find())
    if (databaseNo == 2):
      return list(self.users.find())



    
    
  
