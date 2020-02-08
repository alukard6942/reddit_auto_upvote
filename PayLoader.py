#!/usr/bin/python
import praw
import random
import time 
import sys
import os
import pickle
import pandas as pd

from Reddit import Reddit

class PayLoader(Reddit):

	def __init__(self):
		#print(dir(subreddit))
		self.cache_new = []
		self.time_last = time.time()
		self.message = "[no] ----nothing----"
		self.flag = "init"

	def vote(self):
		# prep work
		self.set_bot()
		self.set_sub()
		self.read()
		print("connection to reddit:",self.reddit.user.me())
		print("connection to subreddit:",self.subreddit)
		print("now:    avg t:    choise:    title:                           debug flag:")

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
			if (self.flag == "skip"):
				continue
			if (self.flag == "break"):
				break

			rnd = random.choice(self.config["choises"])
			if ( rnd == "[up]"):
				submission.upvote()
			elif(rnd == "[dw]"):
				submission.downvote()
			else:
				rnd = "[no]"
			
			self.PayLoad.append([rnd, submission.id, time.time()])
			self.time_last = time.time()
			self.nice_line("{1} {0}".format(submission.title, rnd))


	def get_flag(self):
		return '-'
	
	def nice_line(self, message = ""):
		diff = time.time() - self.time_last
		now= "{0}".format(time.strftime("%H:%M")).center(5," ") 
		if (message != ""):
			self.message = message
			self.time_last = time.time()
			# log diff
			self.count["time"][1] += 1
			self.count["time"][0] += diff
		avg= "{0}s".format(round(self.averige("time", 3, diff),2)).center(7," ") 
		print("\r[{0}] [{2}] {1}".format(now, self.message,avg)[:74].ljust(75," "), self.flag, end = "")
