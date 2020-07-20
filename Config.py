# Config.py
# alukard6942
# 12/7/20

# _/\\\________/\\\__/\\\\\\\\\\\\\____/\\\________/\\\_______/\\\\\_______/\\\\\\\\\\\\\\\__/\\\\\\\\\\\\\\\_        
#  _\/\\\_______\/\\\_\/\\\/////////\\\_\/\\\_______\/\\\_____/\\\///\\\____\///////\\\/////__\/\\\///////////__       
#   _\/\\\_______\/\\\_\/\\\_______\/\\\_\//\\\______/\\\____/\\\/__\///\\\________\/\\\_______\/\\\_____________      
#    _\/\\\_______\/\\\_\/\\\\\\\\\\\\\/___\//\\\____/\\\____/\\\______\//\\\_______\/\\\_______\/\\\\\\\\\\\_____     
#     _\/\\\_______\/\\\_\/\\\/////////______\//\\\__/\\\____\/\\\_______\/\\\_______\/\\\_______\/\\\///////______    
#      _\/\\\_______\/\\\_\/\\\________________\//\\\/\\\_____\//\\\______/\\\________\/\\\_______\/\\\_____________   
#       _\//\\\______/\\\__\/\\\_________________\//\\\\\_______\///\\\__/\\\__________\/\\\_______\/\\\_____________  
#        __\///\\\\\\\\\/___\/\\\__________________\//\\\__________\///\\\\\/___________\/\\\_______\/\\\\\\\\\\\\\\\_ 
#         ____\/////////_____\///____________________\///_____________\/////_____________\///________\///////////////__


class Config:
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
	
	def read_flag(self):
		if (not evLoop):
			
		else:

			char = sys.stdin.read(1)[-1]

			if (char not in "widplafLsceq+-"): 
				return "-"

			elif (self.config["debugFlag"]): print ("youve preased: ", char)


			if ( char == "d" ): 
				self.config["debugFlag"] = not self.config["debugFlag"]
			
			elif (char == "q" or char == "e"):
				self.PayLoad.quit_image_loop()				

			elif (char == "l" or char == "L" ):
				for i in range(self.config["clear"]): print()
				char = "p"
			elif (char == "i"):
				self.set_image_flag()
				self.flag = self.get_flag()

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
			self.flag =  char
			return char

	def __getitem__(self, key):
		return self.config[key]	
	def __setitem__(self, key, data):
		self.config[key] = data
		
	def get_dbg(self):
		return self.dbg
	def set_dbg(self, dbg):
		self.dbg = dbg

	def get_flag (self,):
		flag = self.Flag
		if (flag in "asplLf"):
			if(flag == "l"):
				flag = "p"
			else:
				self.Flag = "-"
		return flag
		

