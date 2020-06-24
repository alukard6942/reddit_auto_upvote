import pickle
import time

class PayLoad:
	
	dbg = True
	PayLoad = []
	File = "PayLoad"

	def __init__(File = "PayLoad.bin"):
		if (self.dbg): print ("Payload init")
		self.File = File	
	
	# append to Payload
	def append   (choise, id):
		self.PayLoad.append([choise, id, time.time()])
		
	# set first 
	# to use when PayLoad doesnt matter
	def set_first(chose, id):
		self.PayLoad[0] =   [choise, id, time.time()]

	# read Payload from dest
	def read():
		if (self.dbg): print ("saving to", dest)
		try:
			with open(File, "rb") as fp:   #Pickling
				self.PayLoad = pickle.load(fp)
				
		except Exception as e:
			print ("could not open:",File)			
			if (self.dbg): print(e)

		if (self.PayLoad == []):
			print ("PayLoad is empty")	
	
	# write Payload to dest
	def write():
		if (self.dbg): print ("writing to", File)
		try:
			with open(file, "wb") as fp:   #Pickling
				pickle.dump(self.PayLoad, fp)
		except Exception as e:
			print ("could not open:",File)			
			if (self.dbg): print(e)

	def __str__(n = 20):
		line = 50
		out  = ("-------------PayLoad-".ljust(line,"-")+"\n")
		lengh = len(self.PayLoad)
		if (n > lengh): n = lengh
		if (n < 0): n = lengh + n + 1
		for pay in range(n):
			out += str(self.PayLoad[-pay]) + "\n"
			if(self.flag == "q"): break
			if(self.flag == "e"): return
		out += (("-------- ["+str(lengh).center(6," ")+"], "+str(time.time())+" ").ljust(line,"-"))
		return out
