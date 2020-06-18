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
		"subreddit"     : "all",
		"file" 			: "PayLoad.bin",
		"folder"        : "PayLoad",
		"bot" 			: "bot1",
		"print" 		: 10,
		"choises"		: ["[up]","[dw]","[no]"],
		"lastposts"     : 25,
		"intwait"       : 60*2*0+5,
		"sleep"			: 1,
		"lsleep"		: 0,
		"save_time"		: 15*60,
		"debugFlag"     : False,
		"clear"         : 50,
		"line_len"      : 80,
		"nsfwC"			: False,

		"forceStream"   : True,

		"dbgDir"        : True,
		"dbgText"       : False,
		"qOnUP"       	: False,
		"dbgErm"       	: False,
	}

	count = {
		"[up]" : [0,0],
		"[dw]" : [0,0],
		"[no]" : [0,0],
		"[al]" : [0,0],
		"time" : [0,0],
		"errs" : [0,0],
		"NSFW" : [0,0],
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
		self.prev_flag = "c"
		self.init = time.time()
		self.time_last = time.time() + self.config["intwait"]
		self.loading_char = "|"

		self.get_window()


		try:
			_thread.start_new_thread( self.listenLoop,() )
		except Exception as e:
			print ("\nError: unable to start listening thread \n\t", e)
			self.flag  = "q"


	def collect(self):
		# prep work
		self.set_bot()
		print("connection to reddit as : ",self.reddit.user.me())
		self.set_sub()
		print("connection to subreddit : ",self.subreddit)
		self.read()

		try:
			_thread.start_new_thread( self.stream,() )
			# _thread.start_new_thread( self.nice_line,() )
			_thread.start_new_thread( self.saveLoop,() )
		except Exception as e:
			print ("\nError: unable to start thread\n\t", e)
			self.flag  = "q"

		chars = "|\\-/"
		counter = 0

		# event looop
		while True:
			if (self.flag == "w"):
				self.write()
				self.get_flag()
			if (self.flag == "q"):
				self.write()
				break
			if (self.flag == "e"):
				break

			self.nice_line()
			self.loading_char = chars[counter]
			counter = (counter + 1) % 4

			time.sleep(self.config["sleep"])

		self.flag = "q"

		print ("\ngood bye")

	def listenLoop(self):
		f = "a"
		while True:
			f = self.get_flag(True)
			if (f in "eq"): return


	def saveLoop(self):
		while True:
			self.write()
			time.sleep(self.config["save_time"])
			if(self.flag == "q"):
				self.write()
				break
			if(self.flag == "e"):
				return


	
	def stream(self):
		try:
		#while True:
			# endless stream of new posts
			for submission in self.subreddit.stream.submissions():
				if (self.flag == "c"):
					#time.sleep(5)
					continue
				elif (self.flag == "q"):
					break
				elif (self.flag == "e"):
					return
				if (self.flag == "s"):
					self.flag = self.get_flag()
					continue

				self.count["errs"][1] += 1


				nsfw = submission.over_18
				if (self.config["debugFlag"]): print(nsfw)
				if (nsfw):
					if(self.config["nsfwC"]): self.loading_char = "F"
					self.count["NSFW"][0] += 1

				rnd = random.choice(self.config["choises"])
				if ( rnd == "[up]"):
					submission.upvote()
					if (self.config["debugFlag"]):
						print ("^\r", end="")
				elif(rnd == "[dw]"):
					submission.downvote()
					if (self.config["debugFlag"]):
						print (",\r", end="")
				else:
					rnd = "[no]"
				self.PayLoad.append([rnd, submission.id, time.time(), nsfw])

				self.update_line("{1} {0}".format(submission.title, rnd))

				if (self.config["debugFlag"] and self.config["dbgDir"]): 
					print (" dir(submission) ")
					print (dir(submission))
					print (" dir(submission.thumbnail) ") 
					print (dir(submission.thumbnail))
					self.flag = "e"
				if (self.config["debugFlag"] and self.config["dbgText"]):
					if (self.flag != "c"): print ()
					print (submission, "text: |" + submission.selftext + "|") 


			
		except Exception as e:			
			if(self.config["forceStream"]):
				if (self.config["debugFlag"]): print ("connection faild.... reconecting")
				self.init = time.time()
				# self.flag = "c" 
				self.count["errs"][0] += 1
				self.stream()
			else: 
				self.flag = "q"
				print ("\nexeptin when streeaming submission\n\t",e)


	def get_flag(self, evLoop = False):
		if (not evLoop):
			if (self.prev_flag in "qe"): return self.prev_flag
			
			else:
				if (self.config["debugFlag"]): print (self.flag) 
				self.flag = "-"
				return "-"

		else:

			char = sys.stdin.read(1)[-1]

			if (char not in "wdplaLsceq"): 
				return "-"
				char = self.prev_flag
				if (self.config["debugFlag"]): print ("flag to: ", char)
			elif (self.config["debugFlag"]): print ("youve preased: ", char)


			if ( char == "d" ): 
				self.config["debugFlag"] = not self.config["debugFlag"]

			elif (char == "l" or char == "L" ):
				for i in range(self.config["clear"]): print()
				char = "p"

			if (char in "Llp"):
				self.get_window()

			elif (char == "c"):
				self.init = time.time()

			self.prev_flag = char
			self.flag =  char
			return char


	def update_line(self,message):
		self.message = message #"{:{line_len}}".format(message,line_len=self.config["line_len"]-22)
		self.count["time"][1] += 1
		self.count["time"][0] += time.time() - self.time_last
		self.time_last = time.time()

	def nice_line(self):
		self.get_window()
		line_len = self.config["line_len"]

		if( self.flag == "c" ):
			print("Ima wait",round(time.time() - self.init, 4), "outa", self.config["intwait"], "\r", end = "")
			if (time.time() - self.init > self.config["intwait"]):
				self.flag = "p"
				self.time_last = time.time()

		# headline
		elif (self.flag == "p"):
			print("Collecting....           ")
			print("User      : ",self.reddit.user.me())
			print("Subreddit : ",self.subreddit)
			print("file      : ", self.config["file"])
			print("t:      avg t:   choise:    title:".ljust(line_len - 5), "flag:")
			self.flag == self.get_flag()

		elif (self.flag == "a"):
			self.printavgs()
			self.get_flag()

		elif(self.flag != "q" and self.flag != "c" ):
			# try:
			# 	diff = time.time() - self.PayLoad[-1][2]
			# except:
			# 	diff = 0
			diff = time.time() - self.time_last
			#t = time.strftime("%H:%M")
			now= "{0}s".format(str(round(diff,2))[:6]).center(6," ") 
			avg= "{0}s".format(str(round(self.averige("time", 3, diff),2))[:6]).center(6," ") 
			out = "\r[{0}][{2}] {1}".format(now, self.message, avg)

			out = self.get_aligned_string(out,self.config["line_len"]-2)			
			print ("\r ".ljust(self.config["line_len"])+ self.loading_char + self.flag, end = "")
			print ("\r" +out, end = "")
			time.sleep(self.config["sleep"])

	def list(self, time_diff = 0):
		self.get_window()
		self.read()
		line_len = self.config["line_len"]

		self.count["[up]"] = [0,0]
		self.count["[dw]"] = [0,0]
		self.count["[al]"] = [0,0]

		self.flag = "p"

		for pay in self.PayLoad:
			self.count["errs"][1] += 1

			if (self.flag == "q"): break
			
			elif (self.flag == "e"): 
				print ("\ngood bye")
				return 

			elif (self.flag == "s"): continue

			elif (self.flag == "p"):
				print()
				print("listing....")
				print("User      : ", self.reddit.user.me())
				print("file      : ", self.config["file"])
				print("downvotes:   upvotes:      nothing:       title")
				self.flag = self.get_flag()

			elif (self.flag == "a"):
				self.printavgs()
				self.get_flag()

			if (time.time() - pay[2] < time_diff):
				break

			try:
				if (self.config["lsleep"] != 0):
					if (self.config["debugFlag"]): print ("zz..")
					time.sleep(self.config["lsleep"])
				
				post = self.reddit.submission(pay[1])
				ups   = post.ups
				title = post.title
				nsfw  = post.over_18
				if (nsfw):
					if (self.config["nsfwC"]):
						self.loading_char = "F"
					self.count["NSFW"][0] += 1

					# each choise
				self.count[pay[0]][1] += 1 
				self.count[pay[0]][0] += ups 
				# averidge of all
				self.count["[al]"][1] += 1 
				self.count["[al]"][0] += ups 

			except Exception as e:
				self.count["errs"][0] += 1
				if(self.config["debugFlag"]): 
					print (pay[1],"doesnt exists | count:", self.count["errs"])
				if(self.config["debugFlag"] and self.config["dbgErm"]): 
					print ("|",e,"|")
				if(self.config["qOnUP"]):
					self.flag  = "q"
				else:
					out = "\r[dw:{2}] {0} [up:{3}] {1} [no:{5}] {4} | {6}".format(
					self.averige("[dw]"),self.averige("[up]"),
					self.count["[dw]"][1],self.count["[up]"][1],
					self.averige("[no]"),self.count["[no]"][1], 
					"========redacted========") 
					print ("\r"+ out[:self.config["line_len"]], end = "")
				continue

			if ( self.flag != "p"):
				out = "\r[dw:{2}] {0} [up:{3}] {1} [no:{5}] {4} | {6}".format(
					self.averige("[dw]"),self.averige("[up]"),
					self.count["[dw]"][1],self.count["[up]"][1],
					self.averige("[no]"),self.count["[no]"][1], 
					title) 
				out = self.get_aligned_string(out,self.config["line_len"])
				print ("\r ".ljust(self.config["line_len"]), end = "")
				print ("\r" + out, end = "")
			
		print("")
		
		self.printavgs()

	def set_bot(self, bot = ""):
		if (bot != ""):
			self.config["bot"] = bot
		# agent
		self.reddit = praw.Reddit(self.config["bot"], user_agent=self.config["bot"])

	def set_sub(self, sub = "", file_flag = False):
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


	def set_debug_flag(self, bolleon = True):
		self.config["debugFlag"] = bolleon

	def clear(self):
		self.PayLoad = []
		self.write()
		print("Paylode is emptyed")

	# write down Payload
	def read(self,file = ""):
		#self.set_file(file)
		if (file == ""):
			file = self.config["file"]

		if not os.path.exists(self.config["folder"]):
		    os.mkdir(self.config["folder"])
		    
		file = self.config["folder"]+"/"+file

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

		if not os.path.exists(self.config["folder"]):
		    os.mkdir(self.config["folder"])

		file = self.config["folder"]+"/"+file

		self.loading_char = "O"

		with open(file, "wb") as fp:   #Pickling
				pickle.dump(self.PayLoad, fp)

	# Print PayLoad
	def print(self, n=config["print"]):
		self.get_window()
		self.read()
		print("-------------PayLoad-".ljust(self.config["line_len"],"-"))

		lengh = len(self.PayLoad)
		if (n > lengh): n = lengh
		if (n < 0): n = lengh + n + 1
		for pay in range(n):
			print (self.PayLoad[-pay])
			if(self.flag == "q"): break
			if(self.flag == "e"): return
		print(("-------- ["+str(lengh).center(6," ")+"], "+str(time.time())+" ").ljust(self.config["line_len"],"-"))

	def averige(self,element, positon = 0, diff = -1):
		if (diff != -1):
			a = (self.count[element][0]+diff)/(self.count[element][1]+1)
		elif (self.count[element][1] == 0):
			a = 0
		else:
			a = self.count[element][0]/self.count[element][1]

		return round(a,positon)

	def printavgs(self):
		#print ("avereges:")
		self.count["N"] = [self.count["errs"][1], len(self.PayLoad)]
		self.count["NSFW"][1] = self.count["errs"][1]
		print (" ")
		print ("\t-------------------------------------")
		print ("\t| type:  sum,      count:    avg:")
		print ("\t-------------------------------------")
		for k in self.count:
			avg = self.averige(k,5)
			if (avg != 0):
				print("\t|",k.ljust(4), "|",
					str(round(self.count[k][0],2)).ljust(8)+ "|",
					str(round(self.count[k][1],2)).ljust(8)+ "|",
					avg)
		print ("\t-------------------------------------")

	def get_window(self):
		rows, columns = os.popen('stty size', 'r').read().split()

		self.config["line_len"] = int(columns)-1
		self.config["clear"] = int(rows)

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
	

# old legacy code
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



