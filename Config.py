# Config.py
# alukard6942
# 12/7/20

# ██╗   ██╗██████╗ ██╗   ██╗ ██████╗ ████████╗███████╗
# ██║   ██║██╔══██╗██║   ██║██╔═══██╗╚══██╔══╝██╔════╝
# ██║   ██║██████╔╝██║   ██║██║   ██║   ██║   █████╗  
# ██║   ██║██╔═══╝ ╚██╗ ██╔╝██║   ██║   ██║   ██╔══╝  
# ╚██████╔╝██║      ╚████╔╝ ╚██████╔╝   ██║   ███████╗
#  ╚═════╝ ╚═╝       ╚═══╝   ╚═════╝    ╚═╝   ╚══════╝

import time 
import os

class Config:
	
	# be avere these config options are badly named becouse I am an idiot
	# yes there is no reason for me to be so creative with how bad can i name an option
	# FAQ: why are the options not at least commeted?
	#		" Fuck you thats why ! "
	#						--- the guy you now hate  
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
		"dbgTime"		: False,


		"show_img"		: False,
		"image_show"    : False,
		"image_size"	: 300,

		# ["enable", "disenable", "only", "else"]
		"NSFW"			: "enable",  # has to be also enabled in the account

		"blacklist"		: ["wtf", "pcmasterrace"],
		# ["enable", "disenable", "only", "else"]
		"collect_users"	: "disenable"
	}

	Flag = "c"
	dbg  = False
	init = time.time()

	def __init__(self, File = None):
		if File == None : File = self["file"]
		self.File = File
		self.time_last = time.time()
		self.flag = "c"
		self.prev_flag = "c"
		self.init = time.time()
		self.time_last = time.time() + self.config["intwait"]
		self.loading_char = "|"

		self.get_window()


		try:
			_thread.start_new_thread( 		self.listenLoop,() )

		except Exception as e:
			print ("\nError: unable to start listening thread \n\t", e)
			self.flag  = "q"

	
	def listenLoop(self):
		while True:
			f = self.read_flag(True)
			if (f in "eq"): return

	event_dic = {
#		"N" : [lambda : sys.stdin.read(1)[-1].lower],			# default state 
#		"d" : [lambda : self.set_dbg(not self.dbg)],			# debug mode
#		"q" : [self.__quit  ],							 		# quit 
#		"e" : [self.__quit  ],									# force quit  
#		"l" : [self.__flag_l],									# clear display	
#		"p" : [lambda : print("TODO: vital info")],				# print header
#		"f" : [lambda self : print( self )],							# print contend of configs
#		"c" : [self.__flag_c], 									# do nothing state
	}
	
	def __quit(self):
		raise Exception("quit")
	
	def __flag_c(self):
		self.init = time.time()		  
	def __flag_l(self):
		for x in range(self.get_window()[1]): print ()
		return "p"

	def read_flag(self):
		flag = self.Flag
		if (flag not in self.event_dic):
			flag = "N"
		for event in self.event_dic[flag]:
			tmp = event()
			if tmp is not None:
				flag = tmp
		self.Flag = flag
		return flag

	# return dimensions of terminal
	def get_window(self):
		rows, columns = os.popen('stty size', 'r').read().split()
		
		columns = int(columns)-1
		rows    = int(rows)
		self.config["line_len"] = columns
		self.config["clear"] = rows

		return columns, rows 

	def __getitem__(self, key):
		return self.config[key]	
	def __setitem__(self, key, data):
		self.config[key] = data
	
	def __str__(self):
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

	def get_dbg(self):
		return self.dbg
	def set_dbg(self, dbg):
		self["debugFlag"] = dbg # legacy option 
		self.dbg = dbg

	def get_flag (self,):
		flag = self.Flag
		if (flag in "asplLf"):
		#	if(flag == "l"):
		#		flag = "p"
		#	else:
			self.Flag = "-"
		return flag
		

