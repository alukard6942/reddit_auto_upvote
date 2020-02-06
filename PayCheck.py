#!/usr/bin/python
import praw
import random
import time 
import sys

from Reddit import Reddit

class PayCheck(Reddit):

	# checks all of posts on PayLoad
	def __init__(self):
		print("__init__ <-- PayCheck")

	def list(self):
		for pay in self.PayLoad:
			post = self.reddit.submission(pay[1])
			
			self.count[pay[0]][1] += 1 
			self.count[pay[0]][0] += post.ups 

			sys.stdout.write("\r[dw:{2}] {0} [up:{3}] {1} [no:{5}] {4}\t{6}".format(self.averige("[dw]"),self.averige("[up]"),self.count["[dw]"][1],self.count["[up]"][1],self.averige("[no]"),self.count["[no]"][1], post.title[:43]).ljust(76," "))
			
		print("")
		
		self.printavgs()


