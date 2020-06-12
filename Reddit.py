#!/usr/bin/python3
import praw
import random
import time 
import sys
import os
import pickle
import math
# import multiprocessing
import _thread

# keystrokes 
import tty
#import sys
import termios

class Reddit:

	config = {
		"wait"			: 5,
		"lengh" 		: 5, # we have to insure all posts are new 
		"subreddit"     : "funny",
		"file" 			: "PayLoad.bin",
		"bot" 			: "bot1",
		"print" 		: 10,
		"choises"		: ["[up]","[dw]","[no]"],
		"lastposts"     : 25,
		"intwait"       : 0*60*2,
		"sleep"			: 0.1,
		"save_time"		: 60
	}

	count = {
		"[up]" : [0,0],
		"[dw]" : [0,0],
		"[no]" : [0,0],
		"[al]" : [0,0],
		"time" : [0,0]
	}

	# agent
	reddit = []
	# subreddit we are focesed on
	subreddit = []

	# payloade
	PayLoad = []


	def __init__(self):
		self.cache_new = []
		self.time_last = time.time()
		self.message = "[no] ----nothing----"
		self.flag = "c"
		self.init = time.time()

	def collect(self):
		# prep work
		self.set_bot()
		print("connection to reddit:",self.reddit.user.me())
		self.set_sub()
		print("connection to subreddit:",self.subreddit)
		self.read()


		# thread each process 
		# streaming = multiprocessing.Process(target=self.stream,    args=()) 
		# streaming.start() 
		# nice_line = multiprocessing.Process(target=self.nice_line, args=())
		# nice_line.start()
		# save_loop = multiprocessing.Process(target=self.saveLoop,  args=())
		# save_loop.start()
		
		try:
			_thread.start_new_thread( self.stream,() )
			_thread.start_new_thread( self.nice_line,() )
			_thread.start_new_thread( self.saveLoop,() )
		except:
			print ("Error: unable to start thread")

		# event looop
		while True:
			if (self.flag != "q"):
				return
			self.flag = sys.stdin.read(1)[0]
		

		# orig_settings = termios.tcgetattr(sys.stdin)

		# tty.setcbreak(sys.stdin)
		# x = 0
		# while x != chr(27): # ESC
		#     x=sys.stdin.read(1)[0]
		#     print("You pressed", x)

		# termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)    


		# streaming.terminate()
		# nice_line.terminate()
		# save_loop.terminate()


	def saveLoop(self):
		while True:
			time.sleep(self.config["save_time"])
			self.write()

	def vote(self):
		# prep work
		self.set_bot()
		self.set_sub()
		self.read()
		print("connection to reddit:",self.reddit.user.me())
		print("connection to subreddit:",self.subreddit)

		try:
			while True:
				self.stream()
		except Exception as e:
			self.flag = "q"
			print("----END OF STREAM-------")

		self.write()
		print("paylode has been saved")

	def stream(self):
		try:
		#while True:
			# endless stream of new posts
			for submission in self.subreddit.stream.submissions():
				if (self.flag == "c"):
					#time.sleep(5)
					continue
				if (self.flag == "q"):
					break

				rnd = random.choice(self.config["choises"])
				if ( rnd == "[up]"):
					submission.upvote()
				elif(rnd == "[dw]"):
					submission.downvote()
				else:
					rnd = "[no]"
				self.PayLoad.append([rnd, submission.id, time.time()])

				self.update_line("{1} {0}".format(submission.title, rnd))
			
		except:
			print ("exeptin when streeaming submission")

	def get_flag(self):
		return '-'
	
	def update_line(self,message):
		self.message = message.encode("ascii","ignore")
		self.count["time"][1] += 1
		self.count["time"][0] += time.time() - self.time_last
		self.time_last = time.time()

	def nice_line(self):
		while(self.flag != "q" and self.flag != "c" ):
			print("Ima wait",round(time.time() - self.init, 4), "outa", self.config["intwait"], "\r", end = "")
			if (time.time() - self.init > self.config["intwait"]):
				self.flag = "g"
				break

		# headline
		print("now:    avg t:    choise:    title:                           debug flag:")

		self.time_last = time.time()
		while(self.flag != "q" ):
			diff = time.time() - self.PayLoad[-1][2]
			#t = time.strftime("%H:%M")
			now= "{0}s".format(round(diff)).center(5," ") 
			avg= "{0}s".format(round(self.averige("time", 3, diff),2)).center(7," ") 
			print("\r[{0}] [{2}] {1}".format(now, self.message, avg)[:72].ljust(73," "), self.flag, end = "")
			#time.sleep(config["sleep"])
		print ("end")

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

	def set_bot(self, bot = ""):
		if (bot != ""):
			self.config["bot"] = bot
		# agent
		self.reddit = praw.Reddit(self.config["bot"], user_agent=self.config["bot"])

	def set_sub(self, sub = "", file_flag = True):
		if (sub != ""):
			self.config["subreddit"] = sub
		if (self.reddit == []):
			self.set_bot()
		# subreddit we are focesed on
		self.subreddit = self.reddit.subreddit(self.config["subreddit"])
		if (file_flag):
			self.set_file()

	def set_file(self,file = ""):
		if (file == ""):
			self.config["file"] = self.config["subreddit"] + ".bin"
		else:
			self.config["file"] = file

	def set_choise(self, choises = ["[up]","[dw]","[no]"]):
		self.config["choises"] = choises

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

	def averige(self,element, positon = 0, diff = -1):
		if (diff != -1):
			a = (self.count[element][0]+diff)/(self.count[element][1]+1)
		elif (self.count[element][1] == 0):
			a = 0
		else:
			a = self.count[element][0]/self.count[element][1]

		return round(a,positon)

	def printavgs(self):
		print ("avereges:")
		for k in self.count:
			print(k, "\t",self.averige(k))

	
