#!/usr/bin/python
import praw
import random
import time 
import sys
from urllib.request import urlopen
from configparser import ConfigParser

def main():
	

	is_shadow_baned("bot1")

	countdown(6*60)

	# reddit = praw.Reddit('bot2', user_agent="bot2")

	# subreddit = reddit.subreddit("JapaneseHotties")
	# repost = reddit.subreddit("asianhotties")

	# i = 0
	# #subreddit.submit("submission test", selftext = "hello world")
	# for submission in subreddit.new(limit=100):
	#     if (i > 13):
	#     	countdown(60*10 + random.randint(100,500))
	#         repost.submit(submission.title, url=submission.url)
	#         print ("I JUST POSTED " + str(i) + ". POST: " + submission.title)
	#     else:
	# 	    pprint( ".",end='')
	#     i += 1

def countdown(t):
	sys.stdout.write("[")
	sys.stdout.flush()
	while (t != 0):
		mins, secs = divmod(t, 60)
		timeformat = '{:02d}:{:02d}'.format(mins, secs)
		if (t %10 == 0): 
			sys.stdout.write('.')
			sys.stdout.flush()
		time.sleep(1)
		t -= 1
	sys.stdout.write("]")
	sys.stdout.flush()


def is_shadow_baned(usr):

	users = ConfigParser()
	users.read('praw.ini')

	url = 'https://www.reddit.com/user/'+users.get(usr, 'username')+'/about,json'
	print( url)

	response = urlopen("https://www.reddit.com")
	countdown(10)
	print (response.read())



if (__name__ == '__main__'):
	main()