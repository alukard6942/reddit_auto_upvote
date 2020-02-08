#!/usr/bin/python3
import praw
import random
import time 
import sys
import os
import pickle
import math

reddit = praw.Reddit("bot4", user_agent="bot4")

for submission in reddit.subreddit('memes').stream.submissions():
    print(submission.title)

