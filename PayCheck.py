#!/usr/bin/python
import praw
import random
import time 
import sys

from Reddit import Reddit

class PayCheck(Reddit):

	# checks all of posts on PayLoad
	def __init__(self):
		self.config["file"] = self.config["subreddit"] + ".bin"

	def list(self, time_diff = 0):

		self.count["[up]"] = [0,0]
		self.count["[dw]"] = [0,0]
		self.count["[al]"] = [0,0]

		print("downvotes:   upvotes:      nothing:       title                               ")

		for pay in self.PayLoad:

			if (time.time() - pay[2] < time_diff):
				break

			post = self.reddit.submission(pay[1])
			
			# each choise
			self.count[pay[0]][1] += 1 
			self.count[pay[0]][0] += post.ups 
			# averidge of all
			self.count["[al]"][1] += 1 
			self.count["[al]"][0] += post.ups 

			sys.stdout.write("\r[dw:{2}] {0} [up:{3}] {1} [no:{5}] {4}    {6}".format(self.averige("[dw]"),self.averige("[up]"),self.count["[dw]"][1],self.count["[up]"][1],self.averige("[no]"),self.count["[no]"][1], post.title)[:79].ljust(79," "))
			
		print("")
		
		self.printavgs()


