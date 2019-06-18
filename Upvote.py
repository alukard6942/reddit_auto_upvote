#!/usr/bin/python
import praw
import random

reddit = praw.Reddit('bot1', user_agent="bot1")

subreddit = reddit.subreddit("all")

for submission in subreddit.new(limit=5):
    print("Title: ", submission.title)
    if (random.randint(0,1) == 0):
    	submission.upvote()
    	print ("upvoted")
    else: 
    	submission.downvote()
    	print("downvoted")
    print("---------------------------------")



