# Counter.py
# alukard6942
# 2/7/20

class SubDic:
	
	dbg = True
	
	dic = {}

	def __init__(self, File):
		self.File = File
		self.read()

	def __getitem__(self, key):
		if key in self.dic:
			return self.dic[key]
		else: return 0
	
	def __setitem__(self, key, value):
		self.dic[key] = value

	def set_file(self, File):
		self.File = File
	
	def read(self, ):
		if (self.dbg): print ("saving to", self.File)
		dic = []
		try:
			with open(self.File, "rb") as fp:   #Pickling
				dic = pickle.load(fp)
				
		except Exception as e:
			if (self.dbg): print(e)

		if (dic != []):
			self.dic = dic
	
	# write Payload to dest
	def write(self, ):
		if (self.dbg): print ("writing to", self.File)
		try:
			with open(self.File, "wb") as fp:   #Pickling
				pickle.dump(self.dic, fp)
		except Exception as e:
			print ("could not open:",self.File)			
			if (self.dbg): print(e)

	




	def __str__ (self, topn = 50):

		if (topn < 0):
			topn += len(self.dic)

		sort_dic = sorted(self.dic, key = self.dic.get, reverse = True)

		out = " " + "\n"
		out += "\t-------------------------------------".ljust(62,"-") + "\n"
		out += "\t|"+"name:".ljust(25) + " count".ljust(13) +"frequenci:".ljust(21)+ " |" + "\n"
		out += "\t-------------------------------------".ljust(62,"-") + "\n"
		suma  = 0
		users = 0
		for k in self.dic:	
			suma += self.dic[k]
			if (k[:2]=="u_"): users += 1
		if (suma == 0): suma = 1
		for k in sort_dic[:topn]:
			s = self.dic[k]
			out += "\t|"+ k.ljust(25)+ "| " + str(s).ljust(10) + "| " + str(round(s/suma,19)).ljust(21) + "|"  + "\n"
		out += "\t-------------------------------------".ljust(62,"-") + "\n"
		out += "\t|"+"sum:".ljust(25)+" "+str(suma).ljust(10)+"  " + str(len(self.dic))  + "\n"
		if(users):
			out += "\t|"+"users:".ljust(25)+" "+str(users).ljust(10)+"  "+ str(users / len(self.dic))  + "\n"
		out += "\t-------------------------------------".ljust(62,"-")

		return out





class Count:

	count = {
	#         count/sum
		"[up]" : [0,0],
		"[dw]" : [0,0],
		"[no]" : [0,0],
		"[al]" : [0,0],
		"time" : [0,0],
		"errs" : [0,0],
		"NSFW" : [0,0],
		"N"    : [0,0],
	}

	dbg = True

	def __init__(self, File = "count.bin"):
		self.File = File
		self.read()

	def add (self, element, n=1):
		self.count[element][0] += n
		self.count[element][1] += 1
	
	def void (self, element, ):
		self.count[element][1] += 1

	
	def sub (self, element, n=1):
		self.count[element][0] -= n
		self.count[element][1] -= 1
	
	def __getitem__(self, key):
		return self.count[key]
	
	def __setitem__(self, key, value):
		self.count[key] = value

	def averige(self,element, positon = 0, diff = -1):
		if (diff != -1):
			a = (self.count[element][0]+diff)/(self.count[element][1]+1)
		elif (self.count[element][1] == 0):
			a = 0
		else:
			a = self.count[element][0]/self.count[element][1]

		return round(a,positon)
	
	def __str__(self):
		self.count["NSFW"][1] = self.count["errs"][1]
		doany = False
		for k in self.count:
			if (self.averige(k,5) != 0):
				doany = True
				break
		if (not doany): return ""
 
		out = " "
		out += "\t-------------------------------------\n"
		out += "\t| type:  sum,      count:    avg:\n"
		out += "\t-------------------------------------\n"
		for k in self.count:
			avg = self.averige(k,5)
			if (avg != 0):
				out += "\t| " + k.ljust(4) + " | " 
				out += str(round(self.count[k][0],2)).ljust(8)+ "| " 
				out += str(round(self.count[k][1],2)).ljust(8)+ "| " 
				out += str(avg) + "\n"
		out += "\t-------------------------------------"
		
		return out

	def __len__(self, ):
		return len(self.count)


	def set_file(self, File):
		self.File = File
	
	def read(self, ):
		if (self.dbg): print ("saving to", self.File)
		count = []
		try:
			with open(self.File, "rb") as fp:   #Pickling
				count = pickle.load(fp)
				
		except Exception as e:
			if (self.dbg): print(e)

		if (count != []):
			self.count = count
	
	# write Payload to dest
	def write(self, ):
		if (self.dbg): print ("writing to", self.File)
		try:
			with open(self.File, "wb") as fp:   #Pickling
				pickle.dump(self.count, fp)
		except Exception as e:
			print ("could not open:",self.File)			
			if (self.dbg): print(e)

	


