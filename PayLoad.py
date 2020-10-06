# PayLoad.py
# alukard6942
# 2/7/20

# ██╗   ██╗██████╗ ██╗   ██╗ ██████╗ ████████╗███████╗
# ██║   ██║██╔══██╗██║   ██║██╔═══██╗╚══██╔══╝██╔════╝
# ██║   ██║██████╔╝██║   ██║██║   ██║   ██║   █████╗  
# ██║   ██║██╔═══╝ ╚██╗ ██╔╝██║   ██║   ██║   ██╔══╝  
# ╚██████╔╝██║      ╚████╔╝ ╚██████╔╝   ██║   ███████╗
#  ╚═════╝ ╚═╝       ╚═══╝   ╚═════╝    ╚═╝   ╚══════╝
 
import pickle
import time
import numpy as np
import cv2
import urllib3
import _thread

from Sem import Sem

class PayLoad:
	
	dbg = True
	PayLoad = []
	File = [] 
	image_title = File
	image_size = 300
	sem = Sem()
	image_thread = False
	
	img = np.zeros((3,3,3), np.uint8)
	_prev_e = None
	flag = "-"

	def __init__(self, File = None, show_img = False):
		if (self.dbg): print ("Payload init")
		if File == None : File = "TODO-add-config.bin"
		self.File = File	
		self.image_title = File
		self.read()
		
		if(show_img):
			self.start_image_loop()	
	
		try:
			_thread.start_new_thread( self.saveLoop,() )
		except Exception as e:
			print ("\nError: unable to start thread\n\t", e)
			self.flag  = "q"
	
	def __iter__(self, n = 0):
		print("TODO: __iter__ Payload")		

	def __next__(self):
		print("TODO: __next__ Payload")

	def saveLoop(self):
		while True:
			self.write()
			time.sleep(10)
			if(self.flag == "q"):
				self.write()
				break
			if(self.flag == "e"):
				return

	# append to Payload
	def append   (self, choise, post):
		self.PayLoad.append(PayLoad_element(choise, post, time.time()))
		self.sem.unlock()

	# set first 
	# to use when PayLoad doesnt matter
	def set_first(self, choise, post):
		# if (len(self.PayLoad)<= 1): 
		if (not len(self.PayLoad)): self.PayLoad = [[]]
		self.PayLoad[-1] =  PayLoad_element(choise, post, time.time())
		self.sem.unlock()

	def last(self, ):
		if (len(self.PayLoad)):
			return self.PayLoad[-1]
		
	def set_file(self, File):
		self.File = File
	
	# read Payload from dest
	def read(self, ):
		if (self.dbg): print ("saving to", self.File)
		PayLoad = []
		try:
			with open(self.File, "rb") as fp:   #Pickling
				PayLoad = pickle.load(fp).PayLoad
				
		except Exception as e:
			if (self.dbg): print(e)

		if (PayLoad != []):
			self.PayLoad = PayLoad
	
	# write Payload to dest
	def write(self, ):
		if (self.dbg): print ("writing to", self.File)
		try:
			with open(self.File, "wb") as fp:   #Pickling
				pickle.dump(self, fp)
		except Exception as e:
			print ("could not open:",self.File)			
			if (self.dbg): print(e)

	def __str__(self, n = 20):
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

	def __len__(self, ):
		return len(self.PayLoad)

	def update_img_size(self, size):
		self.image_size += size
		self.sem.unlock()
		return self.image_size 
			
	def start_image_loop(self,):
		if (self.image_thread): return False
		try:
			self.image_thread = True
			_thread.start_new_thread(self.image_loop_fc, ())
			return True
		except Exception as e:
			print ("image_loop faild: \n ", e)
			if (self.dbg): sys.exit()
			return False

	def quit_image_loop(self, ):
		self.image_thread = False
			

	def image_loop_fc(self,):
		while self.image_thread:			
			self.show_image()
			self.sem.wait()

		cv2.destroyAllWindows()
	
	def show_image(self, ):

		last = self.last()
		if (last != self._prev_e):
			self._prev_e = last
		
			if last is None: 
				return 
			new_img = last.image()
			if new_img is not None:
				self.img = new_img 
				
		img = self.img

		if (self.dbg): print ("resiaved image")
		scale_percent = self.image_size / img.shape[1]
		width = int(img.shape[1] * scale_percent )
		height = int(img.shape[0] * scale_percent)
		dim = (width, height)
		
		# resize image
		img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
		
		title = self.image_title
		cv2.imshow(title,img)

		key = cv2.waitKey(1) & 0xFF
			
		if (key == ord("+")):
			self.update_img_size(+10)
		
		elif (key == ord("-")):
			self.update_img_size(-10)
    
		return True

	def __getitem__(self, key):
		return self.PayLoad[key]
		
	def __setitem__(self, key, data):
		self.PayLoad[key] = data




class PayLoad_element:

	def __init__(self, choise, post, time):
		self.data =   [choise, post, time]	
	
	def __str__(self, ):
		return "{0} {1}".format(self.data[0], self.data[1].title)

	def __getitem__(self, key):
		return self.data[key]
		
	def __setitem__(self, key, data):
		self.data[key] = data


	def url(self, ):
		post = self.data[1]
		# post = self.reddit.submission(post)
		fetched = post._fetch_data()
		thumbnail = fetched[0]["data"]["children"][0]["data"]["thumbnail"]
		if (thumbnail[:7] == "https://"[:7]):
			return thumbnail

	def image (self, ):
		# download the image, convert it to a NumPy array, and then read
		# it into OpenCV format
		
		url = self.url()
		if ( not url ): return

		http = urllib3.PoolManager()
		resp = http.request('GET', url)
		image = np.asarray(bytearray(resp.data), dtype="uint8")
		image = cv2.imdecode(image, cv2.IMREAD_COLOR)
		# return the image
		return image





