#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: upvote.py
# Author: alukard <alukard@github>
# Date: 07.02.2021
#
# ██╗   ██╗██████╗ ██╗   ██╗ ██████╗ ████████╗███████╗
# ██║   ██║██╔══██╗██║   ██║██╔═══██╗╚══██╔══╝██╔════╝
# ██║   ██║██████╔╝██║   ██║██║   ██║   ██║   █████╗  
# ██║   ██║██╔═══╝ ╚██╗ ██╔╝██║   ██║   ██║   ██╔══╝  
# ╚██████╔╝██║      ╚████╔╝ ╚██████╔╝   ██║   ███████╗
#  ╚═════╝ ╚═╝       ╚═══╝   ╚═════╝    ╚═╝   ╚══════╝


import configparser
import sys
import time
import functools
import threading

import praw

from Display import Display
from Reddit import Reddit

top = []
def asyncf(f):
    ''' This decorator executes a function in a Thread'''
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        thr = threading.Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
        top.append(thr)
    return wrapper

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
def help():
    usage()
    exit(0)

@asyncf
def display(pay):
    run = True
    while run:
        post = pay[-1]
        try: d.show(post)
        except Exception as e: 
            print(e, post, d.url(post))

def nice_line(pay):
    line_len = 80
    diff = "none"
    out  = "none"

    while True:
        try:
            diff = round(pay[-1].time - pay[-2].time)
            top = pay[-1].title
            out = f"{diff} {top}"
            out = _get_aligned_string(out, line_len-2)    
        except: pass

        print (f"\r{out}".ljust(line_len), end = "")
        time.sleep(2)


def _get_aligned_string(string, width):
    string = string.ljust(width)
    width = width -1
    string = "{:{width}}".format(string,width=width)
    bts = bytes(string,'utf-8')
    string = str(bts[0:width],encoding='utf-8',errors='backslashreplace')
    new_width = len(string) + int((width - len(string))/2)
    if new_width!=0:
        string = '{:{width}}'.format(str(string),width=new_width)
    return string


conff = configparser.ConfigParser()
conff.read("config.ini")
conff = conff["GENERAL"]
argc = len(sys.argv)

User = conff["User"]
Sub = conff["Sub"]

itert = iter(range(1,argc))
shift = 0
for flag in itert:
    if (sys.argv[flag] == "--help" or sys.argv[flag] == "-h" ):
        usage()
        exit(0)

    elif (sys.argv[flag] == "--user" or sys.argv[flag] == "-u" ):
        User = sys.argv[flag+1]
        next(itert)
        shift += 2

    elif (sys.argv[flag] == "--collect-user" ):
        pass

    elif (sys.argv[flag] == "--image" or sys.argv[flag] == "-i" ):
        pass

    elif (sys.argv[flag] == "--nsfw" or sys.argv[flag] == "-NSFW" ):
        pass

    elif (sys.argv[flag] == "--" or sys.argv[flag][0] != "-" ): 
        break

    else: 
        print ("invalid flag",sys.argv[flag])
        usage()


r = Reddit(User)

bot = 'bot1'
d = Display(praw.Reddit(bot , user_agent=bot))


if (argc > shift + 1 and (sys.argv[shift + 1] == "list" or sys.argv[shift + 1] == "l" )):
    pass

elif (argc > shift + 1 and (sys.argv[shift + 1] == "print" or sys.argv[shift + 1] == "p" )):
    pass

elif (argc > shift + 1 and (sys.argv[shift + 1] == "collect" or sys.argv[shift + 1] == "c" )):
    payload = r.updown(Sub)
    payload.write()


elif (argc > shift + 1 and (sys.argv[shift + 1] == "prototype" or sys.argv[shift + 1] == "x" )):
    pass

