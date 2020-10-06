# Reddit.py
# alukard6942
# 2/7/20

# ██╗   ██╗██████╗ ██╗   ██╗ ██████╗ ████████╗███████╗
# ██║   ██║██╔══██╗██║   ██║██╔═══██╗╚══██╔══╝██╔════╝
# ██║   ██║██████╔╝██║   ██║██║   ██║   ██║   █████╗  
# ██║   ██║██╔═══╝ ╚██╗ ██╔╝██║   ██║   ██║   ██╔══╝  
# ╚██████╔╝██║      ╚████╔╝ ╚██████╔╝   ██║   ███████╗
#  ╚═════╝ ╚═╝       ╚═══╝   ╚═════╝    ╚═╝   ╚══════╝

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

import numpy as np
import cv2
import urllib3


from PayLoad import PayLoad
from Counter import Count, SubDic
from Wrapper import Wrapper
from Config  import Config

class Reddit:
	
	# configuration handlaler
	# also functions as a automat viz. config.get_flag
	config = Config()
	count  = Count()
	# agent
	reddit = []
	# subreddit we are focesed on
	subreddit = []
	# payloade
	PayLoad = PayLoad()

	def __init__(self):
		self.loading_char = "|"		

	def prototype(self, arg = "invalid"):
		#self.show_more_of_post_prototype(arg)
		self.auto_subscibe(arg)

	def auto_subscibe(self, outFile = "allSub.bin"):
		print ("THIS IS ONLY A PROTOTYPE")
		
		sub_dic = SubDic(outFile)

		for submission in Wrapper(self):

			if (self.flag == "a"): 
				print (self.count, sub_dic)
				self.flag = self.get_flag()
		
			sub = submission.subreddit
			ssub = str(sub)
	
			sub_dic[ssub]+= 1
			
			if (sub_dic[ssub] == 1):
				print("\r",ssub.ljust(40), end = "")
			else:
				print("\r"+ssub.ljust(40))
			
			self.PayLoad.set_first("-no-", submission )
		
		sub_dic.write

		print ("END OF PROTOTYPE")

	def collect(self):
		# prep work
		self.set_bot()
		print("connection to reddit as : ",self.reddit.user.me())
		self.set_sub()
		print("connection to subreddit : ",self.subreddit)
		self.PayLoad.read()

		try:
			_thread.start_new_thread( self.stream,() )
			# _thread.start_new_thread( self.nice_line,() )
		except Exception as e:
			print ("\nError: unable to start thread\n\t", e)
			self.flag  = "q"

		chars = "|\\-/"
		counter = 0

		# event looop
		while True:
			flag = self.config.get_flag()	
			if (flag == "w"):
				self.PayLoad.write()
				self.get_flag()
			if (flag == "q"):
				self.PayLoad.write()
				break
			if (flag == "e"):
				break

			self.nice_line()
			self.loading_char = chars[counter]
			counter = (counter + 1) % 4

			time.sleep(self.config["sleep"])

		self.flag = "q"

		print ("\ngood bye")

	def stream(self):
		diff2 = time.time() 
		diff = diff2
	
		# endless stream of new posts	
		for submission in Wrapper(self):
			rnd = random.choice(self.config["choises"])
			if ( rnd == "[up]"):
				submission.upvote()
				if (dbg):
					print ("^\r", end="")
			elif(rnd == "[dw]"):
				submission.downvote()
				if (dbg):
					print (",\r", end="")
			else:
				rnd = "[no]"
			
		
			now = time.time()
			self.PayLoad.append(rnd, submission)

	def nice_line(self):
		col, row = self.config.get_window()
		flag     = self.config.get_flag()

		if(flag == "c" ):
			print("Ima wait",round(time.time() - self.config.init, 4), "outa", self.config["intwait"], "\r", end = "")
			if (time.time() - self.config.init > self.config["intwait"]):
				self.flag = "p"
				self.time_last = time.time()

		# headline
		elif (flag == "p"):
			print("Collecting....".ljust(col))
			print("User      : ",self.reddit.user.me())
			print("Subreddit : ",self.subreddit)
			print("file      : ", self.config["file"])
			print("t:      avg t:   choise:    title:".ljust(col - 5), "flag:")
	
		elif (flag == "a"):
			print(self.count)
	
		elif(flag != "q" and self.flag != "c" ):
			# try:
			# 	diff = time.time() - self.PayLoad[-1][2]
			# except:
			# 	diff = 0
			diff = time.time() - self.time_last
			#t = time.strftime("%H:%M")
			now= "{0}s".format(str(round(diff,2))[:6]).center(6," ") 
			avg= "{0}s".format(str(round(self.averige("time", 3, diff),2))[:6]).center(6," ") 
			out = "\r[{0}][{2}] {1}".format(now, self.PayLoad.last() , avg)
	
			out = self.get_aligned_string(out, col, 2)	
			self.messege = out		
			print ("\r ".ljust(col)+ self.loading_char + self.flag, end = "")
			print ("\r" +out, end = "")
			time.sleep(self.config["sleep"])
    	
	def list(self, time_diff = -1):
		if (time_diff == -1): time_diff = self.config["time_diff"]
		self.get_window()
		self.read()
		self.read(thing = "count")
		line_len = self.config["line_len"]

		self.flag = "p"

		for pay in self.PayLoad[self.count["N"][0]:]:
			dbg = self.config["debugFlag"]

			if (self.flag == "q"): 
				self.write(thing = "count")
				break

			elif (self.flag == "w"): 
				self.write(thing = "count")

			elif (self.flag == "e"): 
				print ("\ngood bye")
				return 

			elif (self.flag == "s"): continue

			elif (self.flag == "p"):
				print()
				print("listing....")
				print("User      : ", self.reddit.user.me())
				print("file      : ", self.config["file"])
				print("downvotes:   upvotes:      nothing:       title".ljust(line_len - 5), "flag:")
				self.flag = self.get_flag()

			elif (self.flag == "a"):
				print(self.count)
				self.get_flag()

			if (time.time() - pay[2] < time_diff):
				break

			diff = - time.time()
			ups = 0
			title= "========redacted========"
			self.count["errs"][1] += 1
			try:
				if (self.config["lsleep"] != 0):
					if (dbg): print ("zz..")
					time.sleep(self.config["lsleep"])
				
				post = self.reddit.submission(pay[1])

				ups   = post.ups
				title = post.title
				nsfw  = post.over_18

				if(self.config["show_img"]): 
					#self.update_image_url(post,nsfw)
					self.toimg = post, nsfw

				if (nsfw):
					if (self.config["nsfwC"]):
						self.loading_char = "F"
					self.count["NSFW"][0] += 1

				# each choise
				self.count.add(pay[0], ups)
				# averidge of all
				self.count.add("[al]", ups)

			except Exception as e:
				self.count["errs"][0] += 1
				if(dbg): 
					print (pay[1],"doesnt exists | count:", self.count["errs"])
				if(self.config["debugFlag"] and self.config["dbgErm"]): 
					print ("|",e,"|")
				if(self.config["qOnUP"]):
					self.flag  = "q"
			diff += time.time()

			if ( self.flag != "p"):
				out = "\r[dw:{2}] {0} [up:{3}] {1} [no:{5}] {4} | {6}".format(
					self.averige("[dw]"),self.averige("[up]"),
					self.count["[dw]"][1],self.count["[up]"][1],
					self.averige("[no]"),self.count["[no]"][1], 
					title) 
				out = self.get_aligned_string(out,self.config["line_len"]-3)
				print ("\r ".ljust(self.config["line_len"]-4)+ str(diff)[:5]+ self.flag, end = "")
				print ("\r" + out, end = "")
			
		print("")
		
		print(self.count)

	def set_bot(self, bot = ""):
		if (bot != ""):
			self.config["bot"] = bot
		# agent
		self.reddit = praw.Reddit(self.config["bot"], user_agent=self.config["bot"])

	def set_sub(self, sub = "", file_flag = False):
		if (sub != ""):
			self.config["subreddit"] = sub
		else:
			sub = self.config["subreddit"]

		if (sub == "all"):
			choise = ["[up]","[dw]"]
			for x in range(10):
				choise.append("[no]")
			self.set_choise(choise)
		if (self.reddit == []):
			self.set_bot()
		# subreddit we are focesed on
		self.subreddit = self.reddit.subreddit(sub)
		if (file_flag):
			self.set_file()

	def set_file(self,file = ""):
		if (file == ""):
			file = self.config["subreddit"] + ".bin"
	
		if (file != self.config["file"]):
			self.PayLoad = PayLoad(self.config["file"], self.config["image_show"])

	def set_choise(self, choises = ["[up]","[dw]","[no]"]):
		self.config["choises"] = choises


	def set_debug_flag(self, bolleon = True):
		self.config["debugFlag"] = bolleon
	
	def set_image_flag(self):
		if(self.config["show_img"]):
			self.config["show_img"] = False
			self.PayLoad.quit_image_loop()
		else:
			self.config["show_img"] = True
			self.PayLoad.start_image_loop()

	def set_nsfw_flag(self, nsfw = "only"):
		self.config["NSFW"] = nsfw


	def set_no_wait_time(self):
		self.flag = "-"

	def set_collect_user(self, collect = "enable"):
		self.config["collect_users"] = collect

	def clear(self):
		self.PayLoad = PayLoad()
		self.write()
		print("Paylode is emptyed")

	# write down Payload
	def read(self,file = "", thing = "file"):
		#self.set_file(file)
		if (file == ""):
			file = self.config["file"]

		if not os.path.exists(self.config["folder"]):
		    os.mkdir(self.config["folder"])
		    
		file = self.config["folder"]+"/"+file

		if (thing == "file"):
			self.PayLoad.read()
			if (not len(self.PayLoad)):
				print ("PayLoad is empty")
				return

		if (thing == "count"):
			file += ".count"
			try:
				with open(file, "rb") as fp:   #Pickling
					self.count = pickle.load(fp)
				
			except Exception as e:
				pass
		if (thing == "object"):
			try:
				with open(file, "rb") as fp:   #Pickling
					return pickle.load(fp)
				
			except Exception as e:
				pass
	
	# Print content of files
	# though this is not the best solution it took 3 min
	def print(self, n=config["print"]):
		try:
			with open(file, "rb") as fp:   #Pickling
				f = pickle.load(fp)
				print(f)

		except Exception as e:
			print(e)
			pass

		return

	def get_window(self):
		rows, columns = os.popen('stty size', 'r').read().split()

		self.config["line_len"] = int(columns)-1
		self.config["clear"] = int(rows)

		return int(columns)-1

	def get_aligned_string(self,string,width):
		string = string.ljust(width)
		width = width -1
		string = "{:{width}}".format(string,width=width)
		bts = bytes(string,'utf-8')
		string = str(bts[0:width],encoding='utf-8',errors='backslashreplace')
		new_width = len(string) + int((width - len(string))/2)
		if new_width!=0:
			string = '{:{width}}'.format(str(string),width=new_width)
		return string
	
