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

class Reddit:

	config = {
		"cvtitle"		: "upvote",
		"wait"			: 5,
		"lengh" 		: 5, # we have to insure all posts are new 
		"subreddit"     : "all",
		"file" 			: "PayLoad.bin",
		"folder"        : "PayLoad",
		"bot" 			: "bot1",
		"print" 		: 10,
		"choises"		: ["[up]","[dw]","[no]"],
		"lastposts"     : 25,
		"intwait"       : 15,
		"sleep"			: 1,
		"lsleep"		: 0,
		"save_time"		: 15*60,
		"debugFlag"     : False,
		"clear"         : 50,
		"line_len"      : 80,
		"nsfwC"			: False,
		"time_diff"		: 1*60*60,

		"forceStream"   : True,

		"dbgDir"        : False,
		"dbgText"       : True,
		"qOnUP"       	: False,
		"dbgErm"       	: False,
		"dbgTime"		: True,


		"show_img"		: False,
		"image_size"	: 300,

		# ["enable", "disenable", "only", "else"]
		"NSFW"			: "enable",  # has to be also enabled in the account

		"blacklist"		: ["wtf", "pcmasterrace"],
		"collect_users"	: False,
	}

	count = {
		"[up]" : [0,0],
		"[dw]" : [0,0],
		"[no]" : [0,0],
		"[al]" : [0,0],
		"time" : [0,0],
		"errs" : [0,0],
		"NSFW" : [0,0],
		"N"    : [0,0],
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
		self.image_url = ""
		self.toimg = None, False

		self.get_window()


		try:
			_thread.start_new_thread( 		self.listenLoop,() )
			_thread.start_new_thread( 	self.imageLoop,() )

		except Exception as e:
			print ("\nError: unable to start listening thread \n\t", e)
			self.flag  = "q"

	def prototype(self, arg = "invalid"):
		#self.show_more_of_post_prototype(arg)
		self.auto_subscibe(arg)

	def auto_subscibe(self, outFile = "allSub.bin"):
		print ("THIS IS ONLY A PROTOTYPE")
		self.set_sub("all") # from where else would you autosubsribe
		diff2 = time.time() 
		diff = diff2

		hashmap = {}
		try:
			new = self.read(outFile, "object")
			if (new != None):
				hashmap = new
		except Exception as e:
			pass

		try:
			for submission in self.subreddit.stream.submissions():
				flag = self.flag
				line_l = self.get_window()
				dbg = self.config["debugFlag"]
				if (dbg): 
					print(submission, submission.id, submission.subreddit)
					# print(dir(submission))
				if (dbg and self.config["dbgTime"]): diff = time.time() 
				if (flag != "-"):
					if (self.flag == "c"):
						print (".", end = "")
						continue
					elif (self.flag == "w"):
						self.write(outFile, "object", hashmap)
					elif (self.flag == "q"):
						break
					elif (self.flag == "e"):
						return
					elif (self.flag == "s"):
						self.flag = self.get_flag()
						continue
					elif (self.flag == "p"):
						
						print("prototyping....".ljust(line_l))
						print("User      : ",self.reddit.user.me())
						self.flag == self.get_flag()
					elif (self.flag == "a"):
						self.printavgs()
						self.print_Dic_content(hashmap)
						self.flag == self.get_flag()

				nsfw = submission.over_18
				if (dbg): print(nsfw)
				enable = self.config["NSFW"]
				if (nsfw):
					if(self.config["nsfwC"]): self.loading_char = "F"
					self.count["NSFW"][0] += 1
				if (not enable == "enable"):
					# nsfw = post.over_18
					if(enable == "disenable" and nsfw): continue
					elif(enable == "only" and not nsfw): continue

				sub = submission.subreddit
				ssub = str(sub)

				if ( ssub[:2] == "u_" and not self.config["collecg_users"]): continue

				if (ssub in self.config["blacklist"]): continue

				if (ssub in hashmap):
					hashmap[ssub]+= 1 
					print("\r",ssub.ljust(line_l), end = "")
				else:
					
					try: 
						print("\n", hashmap[ssub])
					except:
						pass

					hashmap[ssub] = 1

					sub.subscribe()
					print("\r"+ssub.ljust(line_l))
				
				
				if(self.config["show_img"]): 
					#self.update_image_url(submission, nsfw)
					self.toimg = submission, nsfw
				if (dbg and self.config["dbgTime"]):
					t = time.time()
					diff2 = t - diff2
					diff = t - diff

					print ("\r",diff,diff2, diff2-diff)
					diff2 = t

		except Exception as e:			
			if(self.config["forceStream"]):
				if (self.config["debugFlag"]): 
					print ("connection faild.... reconecting")
					if (self.config["dbgText"]): print (e)
				self.init = time.time()
				# self.flag = "c" 
				self.count["errs"][0] += 1
				self.write(outFile, "object", hashmap)
				self.auto_subscibe(outFile)
			else: 
				self.flag = "q"
				print ("\nexeptin when streeaming submission\n\t",e)

		self.write(outFile, "object", hashmap)

		print ("END OF PROTOTYPE")


	def update_image_url(self, post, nsfw = False ,classFlag = True):
		if (not self.config["show_img"]): return
		if (not classFlag):	post = self.reddit.submission(post)
		# nsfw = False
		if (not self.config["NSFW"] == "enable"):
			# nsfw = post.over_18
			if(self.config["NSFW"] == "disenable" and nsfw): return
			elif(self.config["NSFW"] == "only" and not nsfw): return

		fetched = post._fetch_data()
		thumbnail = fetched[0]["data"]["children"][0]["data"]["thumbnail"]
		if (thumbnail[:7] == "https://"[:7]):
			if (self.config["debugFlag"]): print (thumbnail)
			self.image_url = nsfw, thumbnail

	def imageLoop (self):
		prev_img = ""
		prev_size = 0
		img = np.zeros((30,30,3))
		# imgr = img
		nsfw = False
		while True:
			if(self.flag == "q"):
				self.write()
				break
			if(self.flag == "e"):
				return
			if(not self.config["show_img"]):
				cv2.destroyAllWindows() 
				time.sleep(10)
				continue

			# if (self.image_url == ""):
			# 	continue



			try:
				post, nsfw = self.toimg
				self.update_image_url(post, nsfw)
				if (prev_img != self.image_url ):
					prev_img =  self.image_url
					prev_size = 0

					nsfw, url = self.image_url
					img = self.url_to_image(url)
				if (prev_size != self.config["image_size"]):
					scale_percent = self.config["image_size"] / img.shape[1]
					prev_size = self.config["image_size"]
					width = int(img.shape[1] * scale_percent )
					height = int(img.shape[0] * scale_percent)
					dim = (width, height)
					# resize image
					img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
				
				title = self.config["cvtitle"]
				cv2.imshow(title,img)
				cv2.waitKey(10)
			except Exception as e:
				if (self.config["debugFlag"]): print (e, "error in imageLOOP")
				pass




	def url_to_image(self,url):
		# download the image, convert it to a NumPy array, and then read
		# it into OpenCV format
		
		http = urllib3.PoolManager()
		resp = http.request('GET', url)
		image = np.asarray(bytearray(resp.data), dtype="uint8")
		image = cv2.imdecode(image, cv2.IMREAD_COLOR)
		# return the image
		return image


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
		diff2 = time.time() 
		diff = diff2
		try:
		#while True:
			# endless stream of new posts
			for submission in self.subreddit.stream.submissions():
				flag = self.flag
				dbg = self.config["debugFlag"]
				if (dbg and self.config["dbgTime"]): diff = time.time() 
				if (flag != "-"):
					if (self.flag == "c"):
						print (".", end = "")
						continue
					elif (self.flag == "q"):
						break
					elif (self.flag == "e"):
						return
					elif (self.flag == "s"):
						self.flag = self.get_flag()
						continue

				nsfw = submission.over_18
				if (dbg): print(nsfw)
				enable = self.config["NSFW"]
				if (nsfw):
					if(self.config["nsfwC"]): self.loading_char = "F"
					self.count["NSFW"][0] += 1
				if (not enable == "enable"):
					# nsfw = post.over_18
					if(enable == "disenable" and nsfw): continue
					elif(enable == "only" and not nsfw): continue

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
				
			

				self.PayLoad.append([rnd, submission.id, time.time()])
				self.count["errs"][1] += 1
				self.message = "{1} {0}".format(submission.title, rnd) 
				self.count["time"][1] += 1
				now = time.time()
				self.count["time"][0] += now - self.time_last
				self.time_last = now

				if(self.config["show_img"]): 
					#self.update_image_url(submission, nsfw)
					self.toimg = submission, nsfw
				if (dbg and self.config["dbgTime"]):
					t = time.time()
					diff2 = t - diff2
					diff = t - diff

					print ("\r",diff,diff2, diff2-diff)
					diff2 = t
		except Exception as e:			
			if(self.config["forceStream"]):
				if (self.config["debugFlag"]): 
					print ("connection faild.... reconecting")
					if (self.config["dbgText"]): print (e)
				self.init = time.time()
				# self.flag = "c" 
				self.count["errs"][0] += 1
				self.loading_char = "X"
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

			if (char not in "widplafLsceq+-"): 
				return "-"
				char = self.prev_flag
				if (self.config["debugFlag"]): print ("flag to: ", char)
			elif (self.config["debugFlag"]): print ("youve preased: ", char)


			if ( char == "d" ): 
				self.config["debugFlag"] = not self.config["debugFlag"]

			elif (char == "l" or char == "L" ):
				for i in range(self.config["clear"]): print()
				char = "p"
			elif (char == "i"):
				self.config["show_img"] = not self.config["show_img"]
			elif (char == "+"):
				self.config["image_size"] +=10
			elif (char == "-"):
				self.config["image_size"] -=10 
			elif (char == "f"):
				self.print_Config()

			if (char in "Llp"):
				self.get_window()

			elif (char == "c"):
				self.init = time.time()

			self.prev_flag = char
			self.flag =  char
			return char

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
			print("Collecting....".ljust(line_len))
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
			self.messege = out		
			print ("\r ".ljust(self.config["line_len"])+ self.loading_char + self.flag, end = "")
			print ("\r" +out, end = "")
			time.sleep(self.config["sleep"])

	def list(self, time_diff = -1):
		if (time_diff == -1): time_diff = self.config["time_diff"]
		self.get_window()
		self.read()
		self.read(thing = "count")
		line_len = self.config["line_len"]

		# self.count["[up]"] = [0,0]
		# self.count["[dw]"] = [0,0]
		# self.count["[al]"] = [0,0]
		# self.count["N"][0] = start


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
				self.printavgs()
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
				self.count[pay[0]][1] += 1 
				self.count[pay[0]][0] += ups 
				# averidge of all
				self.count["[al]"][1] += 1 
				self.count["[al]"][0] += ups 

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
		
		self.printavgs()

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
			self.config["file"] = self.config["subreddit"] + ".bin"
		else:
			self.config["file"] = file

	def set_choise(self, choises = ["[up]","[dw]","[no]"]):
		self.config["choises"] = choises


	def set_debug_flag(self, bolleon = True):
		self.config["debugFlag"] = bolleon
	
	def set_image_flag(self, bolleon = True):
		self.config["show_img"] = bolleon

	def set_nsfw_flag(self, nsfw = "only"):
		self.config["NSFW"] = nsfw


	def set_no_wait_time(self):
		self.flag = "-"

	def set_collect_user(self, bolleon = True):
		self.config["collect_users"] = bolleon

	def clear(self):
		self.PayLoad = []
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
			self.PayLoad = []
			try:
				with open(file, "rb") as fp:   #Pickling
					self.PayLoad = pickle.load(fp)
				
			except Exception as e:
				pass

			if (self.PayLoad == []):
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
	# Laad PayLoad
	def write(self,file = "", thing = "file", object_O = None):
		if (file == ""):
			file = self.config["file"]

		if not os.path.exists(self.config["folder"]):
		    os.mkdir(self.config["folder"])

		file = self.config["folder"]+"/"+file

		self.loading_char = "O"

		if (thing == "object"):
			with open(file, "wb") as fp:   #Pickling
				pickle.dump(object_O, fp)
		if (thing == "file"):
			with open(file, "wb") as fp:   #Pickling
				pickle.dump(self.PayLoad, fp)
		if (thing == "count"):
			file += ".count"
			with open(file, "wb") as fp:   #Pickling
				pickle.dump(self.count, fp)

	# Print content of files
	# though this is not the best solution it took 3 min
	def print(self, n=config["print"]):
		self.get_window()
		self.read()
		try:
			p = self.PayLoad[-1]
		except Exception as e:
			try:
				self.count = self.PayLoad
				self.printavgs()
			except Exception as e:
				try: 
					dic = self.PayLoad
					self.print_Dic_content(dic, n)
				except Exception as e:
					print (self.PayLoad)
			return

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
	def print_Dic_content(self, dictionary, topn = 50):

		if (topn < 0):
			topn += len(dictionary)

		sort_dic = sorted(dictionary, key = dictionary.get, reverse = True)

		print (" ")
		print ("\t-------------------------------------".ljust(62,"-"))
		print ("\t|","name:".ljust(25), " ", "count".ljust(5), " ", "frequenci:".ljust(21), "|")
		print ("\t-------------------------------------".ljust(62,"-"))
		suma  = 0
		users = 0
		for k in dictionary:	
			suma += dictionary[k]
			if (k[:2]=="u_"): users += 1
		if (suma == 0): suma = 1
		for k in sort_dic[:topn]:
			s = dictionary[k]
			print("\t|",k.ljust(25), "|", str(s).ljust(5),"|", str(round(s/suma,19)).ljust(21), "|" )
		print ("\t-------------------------------------".ljust(62,"-"))
		print ("\t|","sum:".ljust(25)," ",str(suma).ljust(5)," ", len(dictionary) )
		if(users):
			print ("\t|","users:".ljust(25)," ",str(users).ljust(5)," ", users / len(dictionary) )
		print ("\t-------------------------------------".ljust(62,"-"))

	def print_Config(self):
		print (" ")
		print ("\t-------------------------------------".ljust(62,"-"))
		print ("\t|","seting".ljust(25), " ", "value".ljust(5))
		print ("\t-------------------------------------".ljust(62,"-"))
		for k in self.config:
			s = self.config[k]
			print("\t|",k.ljust(25), "|", str(s).ljust(5), )
		print ("\t-------------------------------------".ljust(62,"-"))
		print ("\t|","sum:".ljust(25)," ",len(self.config) )
		print ("\t-------------------------------------".ljust(62,"-"))


	def printavgs(self):
		#print ("avereges:")
		self.count["N"] = [self.count["errs"][1], len(self.PayLoad)]
		self.count["NSFW"][1] = self.count["errs"][1]
		doany = False
		for k in self.count:
			if (self.averige(k,5) != 0):
				doany = True
				break
		if (not doany): return

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

	def show_more_of_post_prototype(self,post):

		obj = self.read("hashmap","object")
		self.print_Dic_content(obj)
		return


		dbg = self.config["debugFlag"]
		if(dbg):	print(post, type(post))
		post = self.reddit.submission(post)
		fetched = post._fetch_data()
		print (dir(post))
		print (post.delete())
		thumbnail = fetched[0]["data"]["children"][0]["data"]["thumbnail"]
		print (thumbnail)
		cv2.imshow(thumbnail,self.url_to_image(thumbnail))

		for f in fetched[0]:
			print (f ,fetched[0][f])
			for f2 in fetched[0][f]:
				try: print ("\t",fetched[0][f][f2])
				except: pass
		cv2.waitKey(1000)

