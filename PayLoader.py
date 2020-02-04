#!/usr/bin/python
import praw
import random
import time 
import sys
import os
import pickle

from urllib.request import urlopen
from configparser import ConfigParser


class PayLoader:

	config = {
		"waitTime": 5,
		"PayLodeLen" : 50
	}
	


	# agent
	reddit = praw.Reddit('bot4', user_agent="bot4")

	# subreddit we are focesed on
	subreddit = reddit.subreddit("funny")

	# my paylaod
	PayLoad = []

	def __init__(self):
		#print(dir(subreddit))
		self.read()


	def vote(self):
		while (True):
			for ajkh in self.subreddit.new(limit=1):
				new = ajkh
			if (self.PayLoad == [] or self.PayLoad[0][1] != new.id ):
				print(new.title)
				self.PayLoad = []
				self.read()
				self.update()
				self.write()
			else:
				print(".",end ="", flush = True)

			time.sleep(self.config["waitTime"])



	def clear(self):
		self.PayLoad = []
		self.write()
		print("Paylode is emptyed")

	def update(self):
		print("...voting")
		# last post
		last = self.PayLast();
		# stores all new posts
		cache =[]

		# for all new vote up or donw
		for submission in self.subreddit.new(limit=self.config["PayLodeLen"]):
			if (submission.id in last):
				print ("<--")
				self.PayLoad = cache + self.PayLoad
				return

			if (random.choice([1,0]) == 0):
				submission.upvote()
				cache.append(["[up]", submission.id, time.time()])
				#print("[up]", submission)

			else:
				submission.downvote()
				cache.append(["[dw]", submission.id, time.time()])
				#print("[dw]", submission)

			print(">",cache[-1],submission.title)

		# update PayLoad
		self.PayLoad = cache + self.PayLoad
		print("----------------------------------------------------------")

	# write down Payload
	def read(self):
		self.PayLoad = []
		try:
			with open("PayLoad.bin", "rb") as fp:   #Pickling
				self.PayLoad = pickle.load(fp)
			
		except Exception as e:
			pass

		if (self.PayLoad == []):
			print ("PayLoad is empty")
			return

		
	# Laad PayLoad
	def write(self):
		with open("PayLoad.bin", "wb") as fp:   #Pickling
				pickle.dump(self.PayLoad, fp)

	# Print PayLoad
	def PayPrint(self,n=10):
		print("-------------PayLoad-----------------------------------------------------------------------")
		for pay in self.PayLoad:
			print (pay)
			n -= 1
			if (n==0):
				return
		print("--------------------------------------------------------------------------------")

	# Last post in PayLoad
	def PayLast(self):
		last = []
		if (self.PayLoad != []):
			for p in self.PayLoad:
				last.append(p[1])
		#print (last, "--> end of last Pay")
		return last
