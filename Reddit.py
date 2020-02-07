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
		"file" : "PayLoad.bin",
		"bot" : "bot4",
		"print" : 10,
		"choises" : ["[up]","[dw]","[no]"]
	}

	count = {
		"[up]" : [0,0],
		"[dw]" : [0,0],
		"[no]" : [0,0],
		"[al]" : [0,0],
		"time" : [0,0]
	}

	def averige(self,element, positon = 0, diff = -1):
		if (diff != -1):
			a = self.count[element][0]+diff/(self.count[element][1]+1)
		elif (self.count[element][1] == 0):
			a = 0
		else:
			a = self.count[element][0]/self.count[element][1]

		return round(a,positon)

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
	def read(self,file = ""):
		if (file == ""):
			file = self.config["file"]

		self.PayLoad = []
		try:
			with open(file, "rb") as fp:   #Pickling
				self.PayLoad = pickle.load(fp)
			
		except Exception as e:
			pass

		if (self.PayLoad == []):
			print ("PayLoad is empty")
			return

	# Laad PayLoad
	def write(self,file = ""):
		if (file == ""):
			file = self.config["file"]

		with open(file, "wb") as fp:   #Pickling
				pickle.dump(self.PayLoad, fp)

	# Print PayLoad
	def print(self, n=config["print"]):
		print("-------------PayLoad------------------------------------------")
		l = 0
		for pay in self.PayLoad:
			l+=1
			if (l <= n or n == -1):
				print (pay)
		print("------------ [", l,"] --------------------------------------")

	def join(self,origin, destiny):
		origin_list = []
		destiny_list = []
		try:
			with open(origin, "rb") as fp:   #Pickling
				origin_list = pickle.load(fp)
			with open(destiny, "rb") as fp:   #Pickling
				destiny_list = pickle.load(fp)
		except Exception as e:
			pass

		with open(destiny, "wb") as fp:   #Pickling
				pickle.dump(origin_list.extend(destiny_list), fp)