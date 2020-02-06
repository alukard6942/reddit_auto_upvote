#!/usr/bin/python
import praw
import random
import time 
import sys
import os
import pickle

from Reddit import Reddit

class PayLoader(Reddit):


	def __init__(self):
		#print(dir(subreddit))
		self.read()
		self.cache_new = []
		

	def vote(self):
		last_new = ""
		self.read()
		while (True):
			cache_new = self.get_new()
			for first in cache_new:
				print("-",end ="", flush = True)
				new = first
				break

			if (self.PayLoad == [] or (self.PayLoad[-1][1] != new.id and last_new != new )):
				last_new = new
				print(">")
				self.update(cache_new)
				self.write()				

			time.sleep(self.config["wait"])

	def get_new(self):
		return self.subreddit.new(limit=self.config["lengh"])

	# updetes the Payload
	def update(self, new_submissions = []):

		if (new_submissions == []):
			new_submissions = self.get_new()

		# last post
		last = self.PayLast();
		# stores all new posts
		cache =[]

		# for all new vote up or donw
		for submission in new_submissions:

			if (self.PayLoad != [] and self.PayLoad[-1][1] == submission.id):
				self.PayLoad.extend(cache)
				return

			if (submission.id in last[-20:-1]):
				print ("ok")
				self.PayLoad.extend(cache)
				return


			if (submission.id in last):
				print (">>>PANIC<<<<", submission.id, submission.title, self.PayLoad[-1])
				self.PayLoad.extend(cache)
				return

			rnd = random.choice(["[up]","[dw]","[no]"])

			if ( rnd == "[up]"):
				submission.upvote()
				cache.insert(0,["[up]", submission.id, time.time()])
				#print("[up]", submission)


			elif(rnd == "[dw]"):
				submission.downvote()
				cache.insert(0,["[dw]", submission.id, time.time()])
				#print("[dw]", submission)

			elif(rnd == "[no]"):
				cache.insert(0,["[no]", submission.id, time.time()])

			print(">",cache[0],submission.title)

		# update PayLoad
		self.PayLoad.extend(cache)
		print("----------------------------------------------------------")
	