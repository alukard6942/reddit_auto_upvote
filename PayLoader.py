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
		self.cache_new = []
		self.time_last = time.time()
		self.message = "[no] ----nothing----"
		self.flag = "-"

	def vote(self):
		# prep work
		self.set_bot()
		self.set_sub()
		self.read()
		print("connection to reddit:",self.reddit.user.me())
		print("connection to subreddit:",self.subreddit)
		print("wait time:  avg t:    choise:    title:                           debug flag:")

		self.stream()

		try:
			self.stream()
		except Exception as e:
			print("----END OF STREAM-------")

		self.write()
		print("paylode has been saved")




	def stream(self):
		# endless stream of new posts
		for submission in self.subreddit.stream.submissions():
			if (self.flag == 'c'):
				continue
			if (self.flag == 'b'):
				break

			rnd = random.choice(self.config["choises"])
			if ( rnd == "[up]"):
				submission.upvote()
				self.PayLoad.append([rnd, submission.id, time.time()])
				#print("[up]", submission)
			elif(rnd == "[dw]"):
				submission.downvote()
				self.PayLoad.append([rnd, submission.id, time.time()])
				#print("[dw]", submission)
			else:
				self.PayLoad.append(["[no]", submission.id, time.time()])

			self.nice_line("{1} {0}".format(submission.title, rnd))


	def get_flag(self):
		return '-'
		

	def oldvote(self):
		self.set_bot()
		self.set_sub()

		print("connection to reddit:",self.reddit)
		print("connection to subreddit:",self.subreddit)

		# nice loking table
		print("wait time:  avg t:    choise:    title:                           debug flag:")

		last_new = ""
		self.read()
		self.time_last = time.time()
		while (True):
			cache_new = self.get_new()
			for first in cache_new:
				self.nice_line()
				new = first
				break

			if (self.PayLoad == [] or (self.PayLoad[-1][1] != new.id and last_new != new )):
				last_new = new
				self.update(cache_new)
				self.write()				

			time.sleep(self.config["wait"])

	def get_new(self):
		return self.subreddit.new(limit=self.config["lengh"])

	
	
	def nice_line(self, message = ""):
		diff = time.time() - self.time_last
		now= " {0}s ".format(round(diff,2)).center(8," ") 
		if (message != ""):
			self.message = message
			self.time_last = time.time()
			# log diff
			self.count["time"][1] += 1
			self.count["time"][0] += diff
		avg= "{0}s".format(round(self.averige("time", 3, diff),2)).center(7," ") 
		print("\r[ {0}] [{2}] {1}".format(now, self.message,avg)[:74].ljust(75," "), self.flag, end = "")











# this is a relic

	# updetes the Payload
	def update(self, new_submissions = []):

		print("\r[>", end = "")

		if (new_submissions == []):
			new_submissions = self.get_new()

		# last posts
		last = self.PayLast();
		# stores all new posts
		cache =[]

		counter = 0

		# for all new vote up or donw
		for submission in new_submissions:

			if (self.PayLoad != [] and self.PayLoad[-1][1] == submission.id):
				self.PayLoad.extend(cache)
				return

			if (submission.id in last):
				print ("ok")
				self.PayLoad.extend(cache)
				return

			rnd = random.choice(self.config["choises"])
			if ( rnd == "[up]"):
				submission.upvote()
				cache.insert(0,[rnd, submission.id, time.time()])
				#print("[up]", submission)
			elif(rnd == "[dw]"):
				submission.downvote()
				cache.insert(0,[rnd, submission.id, time.time()])
				#print("[dw]", submission)
			else:
				cache.insert(0,["[no]", submission.id, time.time()])
			counter += 1
			self.nice_line("{0} {1}".format(cache[0][0], submission.title), counter)
			

		# update PayLoad
		self.PayLoad.extend(cache)
		print(counter)

	# Last posts in PayLoad
	# TODO:
	#   	optimalization
	#		this method is very unefective at best
	#		good enough
	def PayLast(self):
		
		if (len(self.PayLoad) < self.config["lastposts"] +1):
			return self.PayLoad[:][1]
		else:
			return self.PayLoad[-self.config["lastposts"]:-1][1]