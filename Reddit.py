# 2/7/20

# ██╗   ██╗██████╗ ██╗   ██╗ ██████╗ ████████╗███████╗
# ██║   ██║██╔══██╗██║   ██║██╔═══██╗╚══██╔══╝██╔════╝
# ██║   ██║██████╔╝██║   ██║██║   ██║   ██║   █████╗  
# ██║   ██║██╔═══╝ ╚██╗ ██╔╝██║   ██║   ██║   ██╔══╝  
# ╚██████╔╝██║      ╚████╔╝ ╚██████╔╝   ██║   ███████╗
#  ╚═════╝ ╚═╝       ╚═══╝   ╚═════╝    ╚═╝   ╚══════╝

# import multiprocessing
import configparser
from functools import wraps
import math
import os
import random
import sys
import threading
import time

import numpy as np
import praw

from PayLoad import PayLoad


class Reddit ( praw.Reddit ):

    # configuration handlaler
    conff = configparser.ConfigParser()

    payload = PayLoad()

    class decorators:
        @staticmethod
        def handle( func ):
            """
            decorator for all post handeling functions
            example of such fc: def fc (self, post, Payload):
            """
            @wraps(func)
            def wrapper (self, sub="all"):
                payload = self.payload

                def asyncf(self, sub, payload):
                    """ asyced part """
                    self.running = True
                    i = self.__iter__(sub)
                    for post in i:
                        if not self.running: break
                        try: func(self, post, payload)
                        except Exception as e: print(e, post)
                    print("collection stop")

                thr = threading.Thread(target=asyncf, args=(self, sub, payload))
                thr.start()

                return payload

            return wrapper

    @decorators.handle
    def updown(self, post="sub", Payload=None):
        """
        ! takes only one arg Subrrddit !
        ! synchrones function          !

        rondomly upvotes/downvotes post

        returs Payload containig all tuched posts
        """

        rn = random.randint(0,5)
        if ( rn == 1 ):
            post.upvote()
            Payload.append(post, "up")
        elif(rn == 2 ):
            post.downvote()
            Payload.append(post, "down")

    @decorators.handle
    def logall(self, post="sub", Payload=None):
        """
        ! takes only one arg Subrrddit !
        ! synchrones function          !

        returs Payload containig all tuched posts
        """
        Payload.append(post)


    def __init__(self, bot):
        super().__init__(bot , user_agent=bot)
        self.conff.read("config.ini") 
        self.conff = self.conff["Reddit"]
        self.running = True
        self.time_last = time.time()
        self.time_diff = 0

    def quit(self):
        self.running = False



    def __iter__(self, sub = None):
        if(sub == None): sub = str(self.conff["default_sub"])
        sub = self.subreddit(sub)
        self.iter = iter(sub.stream.submissions())
        return self

    def __next__(self):
        return next(self.iter)
