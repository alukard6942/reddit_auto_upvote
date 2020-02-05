#!/usr/bin/python
import praw
import random
import time 
import sys
import os
import pickle
import math

class Reddit:

	config = {
		"wait": 5,
		"lengh" : 5, # we have to insure all posts are new 
		"subreddit" : "funny",
		"bot" : "bot3",
		"print" : 10
	}

	count = {
		"[up]" : [0,0],
		"[dw]" : [0,0],
		"time" : [0,0]
	}

	def averige(self,element, round_flag = True):
		if (self.count[element][1] == 0):
			a = 0
		else:
			a = self.count[element][0]/self.count[element][1]

		if (round_flag):
			return round(a)
		else:
			return a

	def printavgs(self):
		print ("avereges:")
		for k in self.count:
			print(k, "\t",self.averige(k))


	# agent
	reddit = praw.Reddit(config["bot"], user_agent=config["bot"])

	# subreddit we are focesed on
	subreddit = reddit.subreddit(config["subreddit"])

	# my paylaod
	PayLoad = []

	def __init__(self):
		print("__init__ <-- Reddit")

	def clear(self):
		self.PayLoad = []
		self.write()
		print("Paylode is emptyed")

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
	def print(self,n=config["print"]):
		print("-------------PayLoad------------------------------------------")
		l = 0
		for pay in self.PayLoad:
			l+=1
			if (l <= n or n == -1):
				print (pay)
		print("------------ [", l,"] --------------------------------------")

	# Last post in PayLoad
	def PayLast(self):
		last = []
		if (self.PayLoad != []):
			for p in self.PayLoad:
				last.append(p[1])
		#print (last, "--> end of last Pay")
		return last

