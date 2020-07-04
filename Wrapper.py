# RedditWrapper.py
# alukard6942
# 2/7/20

import random
import time 
import sys
import os
import math

class Wrapper:
	
	def __init__(self, reddit):
		self.reddit = reddit
		
	
	def __iter__(self,):
		self.reddit.set_bot()
		print("connection to reddit as : ",self.reddit.reddit.user.me())
		self.reddit.set_sub()
		print("connection to subreddit : ",self.reddit.subreddit)
		
		for i in self.reddit.subreddit.stream.submissions():
			print (i)
			break 


		self.iter = iter(self.reddit.subreddit.stream.submissions())
		self.diff2 = time.time()
		self.diff  = self.diff2	

		return self
	
	def __next__(self,):
		reddit = self.reddit	
		dbg = reddit.config["debugFlag"]

		if (dbg and reddit.config["dbgTime"]):
			t = time.time()
			self.diff2 = t - self.diff2
			self.diff =  t - self.diff

			print ("\r",diff,diff2, diff2-diff)
			diff2 = t

		try:
			submission = next(self.iter)
		
		except Exception as e:			
			if(reddit.config["forceStream"]):
				if (reddit.config["debugFlag"]): 
					print ("connection faild.... reconecting")
					if (reddit.config["dbgText"]): print (e)
				reddit.init = time.time()
				# self.flag = "c" 
				reddit.count["errs"][0] += 1
				self.__iter__()
				return self.__next__()
			else: 
				self.flag = "q"
				print ("\nexeptin when streeaming submission\n\t",e)


		reddit.count.void("errs")
		flag = reddit.flag
		#line_l = reddit.get_window()
		if (dbg): 
			print(submission, submission.id, submission.subreddit)
			# print(dir(submission))
		if (dbg and reddit.config["dbgTime"]): self.diff = time.time() 
		if (flag != "-"):
			if (flag == "c"):
				print (".", end = "")
				return  self.__enter__()
			elif (flag == "q"):	
				print ("ending")
				raise StopIteration
			elif (flag == "e"):	sys.exit()
			elif (flag == "s"):
				reddit.flag = reddit.get_flag()
				return self.__enter__()
		nsfw = submission.over_18
		enable = reddit.config["NSFW"]
		if (nsfw):
			if(reddit.config["nsfwC"]): reddit.loading_char = "F"
			reddit.count.void("NSFW")
			if (not enable == "enable"):
			# nsfw = post.over_18
				if  (enable == "disenable" and nsfw): return self.__next__()
				elif(enable == "only" and  not nsfw): return self.__next__()
		
		return submission
			
		

		


