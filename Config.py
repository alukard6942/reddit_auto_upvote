# Config.py
# alukard6942
# 12/7/20

# ██╗   ██╗██████╗ ██╗   ██╗ ██████╗ ████████╗███████╗
# ██║   ██║██╔══██╗██║   ██║██╔═══██╗╚══██╔══╝██╔════╝
# ██║   ██║██████╔╝██║   ██║██║   ██║   ██║   █████╗  
# ██║   ██║██╔═══╝ ╚██╗ ██╔╝██║   ██║   ██║   ██╔══╝  
# ╚██████╔╝██║      ╚████╔╝ ╚██████╔╝   ██║   ███████╗
#  ╚═════╝ ╚═╝       ╚═══╝   ╚═════╝    ╚═╝   ╚══════╝
                                                     
                                                    
                                                    
                                                    
                                                    
                                                    
                                                    
                                                    

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
		"image_size"	: 300,

		# ["enable", "disenable", "only", "else"]
		"NSFW"			: "enable",  # has to be also enabled in the account

		"blacklist"		: ["wtf", "pcmasterrace"],
		# ["enable", "disenable", "only", "else"]
		"collect_users"	: "disenable"
	}

	Flag = "c"
	dbg  = False

	def __init__(self, File):
		self.File = File
	
	def listenLoop(self):
		while True:
			f = self.read_flag(True)
			if (f in "eq"): return

	envent_dic = {
		"d" : lambda : self.set_dbg(not self.dbg),
		
	}


	def read_flag(self):
		char = sys.stdin.read(1)[-1]

		if (char not in "widplafLsceq+-"): 
			return "-" # default state

		elif (self.config["debugFlag"]): print ("youve preased: ", char)

		if ( char == "d" ): 
			self.set_dbg(not self.dbg)
		
		#elif (char == "q" or char == "e"):
		#	self.PayLoad.quit_image_loop()				

		elif (char == "l" or char == "L" ):
			for i in range(self.config["clear"]): print()
			char = "p"

		elif (char == "i"):
			self.set_image_flag()
			char = self.get_flag()

		elif (char == "+"):
			self.PayLoad.update_img_size(+10)

		elif (char == "-"):
			self.PayLoad.update_img_size(-10)

		elif (char == "f"):
			self.print_Config()

		if (char in "Llp"):
			self.get_window()

		elif (char == "c"):
			self.init = time.time()

		self.prev_flag = char
		self.Flag = char
		return char

	def __getitem__(self, key):
		return self.config[key]	
	def __setitem__(self, key, data):
		self.config[key] = data

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
		

