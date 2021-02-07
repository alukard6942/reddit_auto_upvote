# 2/7/20

# ██╗   ██╗██████╗ ██╗   ██╗ ██████╗ ████████╗███████╗
# ██║   ██║██╔══██╗██║   ██║██╔═══██╗╚══██╔══╝██╔════╝
# ██║   ██║██████╔╝██║   ██║██║   ██║   ██║   █████╗  
# ██║   ██║██╔═══╝ ╚██╗ ██╔╝██║   ██║   ██║   ██╔══╝  
# ╚██████╔╝██║      ╚████╔╝ ╚██████╔╝   ██║   ███████╗
#  ╚═════╝ ╚═╝       ╚═══╝   ╚═════╝    ╚═╝   ╚══════╝

# import multiprocessing
import _thread
import configparser
import math
import os
import random
import sys
import time

import numpy as np
import praw

from PayLoad import PayLoad


class Reddit ( praw.Reddit ):

    # configuration handlaler
    conff = configparser.ConfigParser()


    # payloade
    PayLoad = PayLoad()

    def __init__(self, bot):
        super().__init__(bot , user_agent=bot)
        self.conff.read("CONFIG.INI") 
        self.conff = self.conff["Reddit"]
        self.running = True
        self.time_last = time.time()
        self.time_diff = 0

    def __collect_decorator( func ):
        def wrapper (self, sub):
        
            i = self.__iter__(sub)
            for post in i:
                if not self.running: break
                func(self, post)
            print("collection stop")

            return self.PayLoad
        
        return wrapper

    @__collect_decorator
    def updown(self, post):

        rn = random.randint(0,200)
        if ( rn == 1 ):
            post.upvote()
            self.PayLoad.append(post, "up")
        elif(rn == 2 ):
            post.downvote()
            self.PayLoad.append(post, "down")

    def __iter__(self, sub = None):
        if(sub == None): sub = str(self.conff["default_sub"])
        sub = self.subreddit(sub)
        self.iter = iter(sub.stream.submissions())
        return self

    def __next__(self):
        return next(self.iter)


