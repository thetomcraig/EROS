import os
#Get the path of the data directory
#Give it to the mongodb initialize command
try:
  os.system("mongod --config=/Users/thetomcraig/Dropbox/TomCraig/Projects/Bots/Bots/data/mongo.conf --nojournal &")
except:
  print "mongod startup failed"
  
  