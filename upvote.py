#!/usr/bin/python3

# upvote.py
# alukard6942
# 2/7/20

# _/\\\________/\\\__/\\\\\\\\\\\\\____/\\\________/\\\_______/\\\\\_______/\\\\\\\\\\\\\\\__/\\\\\\\\\\\\\\\_        
#  _\/\\\_______\/\\\_\/\\\/////////\\\_\/\\\_______\/\\\_____/\\\///\\\____\///////\\\/////__\/\\\///////////__       
#   _\/\\\_______\/\\\_\/\\\_______\/\\\_\//\\\______/\\\____/\\\/__\///\\\________\/\\\_______\/\\\_____________      
#    _\/\\\_______\/\\\_\/\\\\\\\\\\\\\/___\//\\\____/\\\____/\\\______\//\\\_______\/\\\_______\/\\\\\\\\\\\_____     
#     _\/\\\_______\/\\\_\/\\\/////////______\//\\\__/\\\____\/\\\_______\/\\\_______\/\\\_______\/\\\///////______    
#      _\/\\\_______\/\\\_\/\\\________________\//\\\/\\\_____\//\\\______/\\\________\/\\\_______\/\\\_____________   
#       _\//\\\______/\\\__\/\\\_________________\//\\\\\_______\///\\\__/\\\__________\/\\\_______\/\\\_____________  
#        __\///\\\\\\\\\/___\/\\\__________________\//\\\__________\///\\\\\/___________\/\\\_______\/\\\\\\\\\\\\\\\_ 
#         ____\/////////_____\///____________________\///_____________\/////_____________\///________\///////////////__


from Reddit import Reddit
import sys


def usage():
	print (
"""upvote [flag] [option] 
	--help              -h |	prints this help
	--debug             -d |	enable debug mode
	--image             -i |	enable image mode ie. shows prewie
	--nsfw [option]        |	[enable|disenable|only] nsfw content
	--no-choise            |	disable up\\downvoting
	--no-wait              |	disenable wait time
	--collect-user         |	enable subing to users ie. u_*

	list    [file]       l |	lists averige upvode/downvote/none count
	print   [file] [n]   p |	prints last n collected posts 
	collect [sub] [file] c |	starts collecting posts to file
	
	controls:      q       |	save and exit
	               w       |	save
	               e       |	exit without saving (saves each minute)
	               s       |	skip one post
	               l       |	clear display
	               d       |	enable debug mode
	               i       |	enable image modea
	               +-      |	configure image size
	               a       |	lists averiges 
	               f       |	shows curent configuratios
	                        	! very badly named ! only a pet project
	""")	

def main():
	argc = len(sys.argv)

	r = Reddit()

	r.set_choise(["[up]","[dw]"])
	# r.set_choise(["[no]"])
	r.set_bot("bot4")
	r.set_sub("all")
	shift = 0

	itert = iter(range(1,argc))
	for flag in itert:
		if (sys.argv[flag] == "--debug" or sys.argv[flag] == "-d" ):
			r.set_debug_flag()
			shift += 1

		elif (sys.argv[flag] == "--help" or sys.argv[flag] == "-h" ):
			usage()
			return

		elif (sys.argv[flag] == "--user" or sys.argv[flag] == "-u" ):
			r.set_bot(sys.argv[flag+1])
			next(itert)
			shift += 2

		elif (sys.argv[flag] == "--no-choise" ):
			r.set_choise(["[no]"])
			shift += 1

		elif (sys.argv[flag] == "--no-wait" ):
			r.set_no_wait_time()
			shift += 1

		elif (sys.argv[flag] == "--collect-user" ):
			if (sys.argv[flag +1] in ["enable", "disenable", "only"]):
				r.set_collect_user(sys.argv[flag +1])
				shift += 1
				next(itert)
			else: r.set_collect_user()
			shift += 1

		elif (sys.argv[flag] == "--image" or sys.argv[flag] == "-i" ):
			r.set_image_flag()
			shift += 1
		elif (sys.argv[flag] == "--nsfw" or sys.argv[flag] == "-NSFW" ):
			if (sys.argv[flag +1] in ["enable", "disenable", "only", "else"]):
				r.set_nsfw_flag(sys.argv[flag +1])
				shift += 1
				next(itert)
			else: r.set_nsfw_flag()
			shift += 1

		elif (sys.argv[flag] == "--" or sys.argv[flag][0] != "-" ): 
			break

		else: 
			print ("invalid flag",sys.argv[flag])
			usage()
	

	if (argc > shift + 1 and (sys.argv[shift + 1] == "list" or sys.argv[shift + 1] == "l" )):
		if (argc > shift + 2):
			r.set_file(sys.argv[shift + 2])
		else:
			r.set_file()

		if (argc > shift + 3):
			r.list(start = int(sys.argv[shift + 3]))
		else:
			r.list()  # to see results		

	elif (argc > shift + 1 and (sys.argv[shift + 1] == "print" or sys.argv[shift + 1] == "p" )):
		if (argc > shift + 2):
			r.set_file(sys.argv[shift + 2])
		else:
			r.set_file()

		if (argc > shift + 3):
			r.print(int(sys.argv[shift + 3]))
		else:
			r.print()  # to see results
	
	elif (argc > shift + 1 and (sys.argv[shift + 1] == "collect" or sys.argv[shift + 1] == "c" )):
		if (argc > shift + 2):
			r.set_sub (sys.argv[shift + 2])
		if (argc > shift + 3): # file
			r.set_file(sys.argv[shift + 3])
		else:
			r.set_file(sys.argv[shift + 2]+".bin")
		r.collect()  # endless loop

	elif (argc > shift + 1 and (sys.argv[shift + 1] == "prototype" or sys.argv[shift + 1] == "x" )):
		if (argc > shift + 2):
			r.prototype (sys.argv[shift + 2])
		else:
			r.prototype ()		

	else: 
			print ("invalid option",sys.argv[shift + 1])
			usage()


if (__name__ == '__main__'):
	main()
