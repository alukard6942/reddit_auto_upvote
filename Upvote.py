#!/usr/bin/python
import praw
import random
import time 

reddit = praw.Reddit('bot1', user_agent="bot1")

subreddit = reddit.subreddit("blowjob")
repost = reddit.subreddit("blowjobs")

i = 0
#subreddit.submit("submission test", selftext = "hello world")
for submission in subreddit.new(limit=100):
    if (i > 13):
        repost.submit(submission.title, url=submission.url)
        print ("I JUST POSTED " + str(i) + ". POST: " + submission.title)
        time.sleep(60*10 + random.randint(10,60))
    else:
	    print ".",
    i += 1



