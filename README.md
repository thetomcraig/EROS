Bots
=====================
The goal of the project is to teach myself about natural language processing and databasing, and hopefully do something interesting with tweets scraped from various sources.  By collecting a large number of tweets and classifying them in various ways I want to see if I can create an algorithm to determine sentiment and emotion behind tweets, effectively seeing how well I can "program" emotion.
Unless otherwise specified, all code is written by me, Tom Craig.

Preface
=======
I have always been interested in how the Internet has affected the way humans communicate with each other, and this was the impetus for the formation of the project.  

This idea has been around for a long time, an early example is the program ELIZA written at MIT in the 1960s.  ELIZA aimed to do just what @Trackgirl did, carry out a relationship with a user like a real person would.  Needless to say, the techniques for algorithms such as these are constantly being refined and implemented as a form of social commentary; evidently the average person is not hard to convince.

This project aims to simulate emotional analysis algorithmically, using data in the form of tweets.  

What I Have Accomplished (So Far)
=================================
*	Creation of a scraper using the tweepy module.  This scraper can find tweets with a given word contained, scrape top users and trends, and obtain all the tweets from a given user.
* Creation of a parser, though this has not been linked up to the rest of the project yet.
* Creation of databasing class using mongodb to store the tweets.
* Began work on a classifier, code present in the driver file.  I want to start with simple sentiment analysis, (positive/negative) and model this in some way.

What I Have Learned (So Far) & Challenges
=========================================
*	Much of Twitter culture can be viewed through simple scraping, something I did not anticipate.  This might be something to explore later in the project.
*	Tweets are notoriously lacking in proper grammar.  There is going to be much more work to do in that respect.  
*	Many of the Tweets encountered are not usable because they contain references to the content of shared links, an a host of other niche reasons.
*	There is a lot of "garbage" (information not applicable to my goals), in the tweets, and this is something to be filtered out and delt with.

Next Steps
==========
*	Working with the databasing code to store large amount of twitter data.
* Working on a front end to see what it being collected, I am consider looking into an iPhone app to do this.



