#!/usr/bin/python
import praw
import random

reddit = praw.Reddit('bot1', user_agent="bot1")

subreddit = reddit.subreddit("nsfw")
repost = reddit.subreddit("ass")

i =0
#subreddit.submit("submission test", selftext = "hello world")
for submission in subreddit.new(limit=500):
    if (random.randint(0,100) == 0):
    	repost.submit(submission.title, url=submission.url)
    	print (" -->")
    else: 
    	print ".",
    
    i += 1



