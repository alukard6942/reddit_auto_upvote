# Sem.py
# alukard6942
# 2/7/20

# ██╗   ██╗██████╗ ██╗   ██╗ ██████╗ ████████╗███████╗
# ██║   ██║██╔══██╗██║   ██║██╔═══██╗╚══██╔══╝██╔════╝
# ██║   ██║██████╔╝██║   ██║██║   ██║   ██║   █████╗  
# ██║   ██║██╔═══╝ ╚██╗ ██╔╝██║   ██║   ██║   ██╔══╝  
# ╚██████╔╝██║      ╚████╔╝ ╚██████╔╝   ██║   ███████╗
#  ╚═════╝ ╚═╝       ╚═══╝   ╚═════╝    ╚═╝   ╚══════╝

 import threading

class Sem:
	sem = threading.Semaphore()
	value = -1 
	
	def __init__(self,):
		pass

	def wait(self,):
		self.value -= 1
		self.sem.acquire()

	def unlock(self,):
		if(self.value < 1):
			self.sem.release()
			self.value += 1
			
			
			
