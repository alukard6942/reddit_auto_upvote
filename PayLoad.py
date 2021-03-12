#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: PayLoad.py
# Author: alukard <alukard@github>
# Date: 01.02.2021
#
# ██╗   ██╗██████╗ ██╗   ██╗ ██████╗ ████████╗███████╗
# ██║   ██║██╔══██╗██║   ██║██╔═══██╗╚══██╔══╝██╔════╝
# ██║   ██║██████╔╝██║   ██║██║   ██║   ██║   █████╗  
# ██║   ██║██╔═══╝ ╚██╗ ██╔╝██║   ██║   ██║   ██╔══╝  
# ╚██████╔╝██║      ╚████╔╝ ╚██████╔╝   ██║   ███████╗
#  ╚═════╝ ╚═╝       ╚═══╝   ╚═════╝    ╚═╝   ╚══════╝
 
import time
import configparser
from collections import namedtuple

class PayLoad ( list ) :

    conf = configparser.ConfigParser()

    def __init__(self, File = None):
        super().__init__()

        self.conf.read("config.ini")
        self.time_last = time.time()

        # may specifi file 
        if (File):   self.database = str(File)
        else:        self.database = str(self.conf["PayLoad"]["default_file"])

    def append(self, post, meta="----"):
        super().append(Element(post, meta ))

    def write(self):
        with open(self.database, "w") as f:
            for pay in self:
                f.write(str(pay)+"\n")


    def __str__(self, n = 20):
        line = 50
        out  = ("-------------PayLoad-".ljust(line,"-")+"\n")
        lengh = len(self)
        if (n > lengh): n = lengh
        if (n < 0): n = lengh + n + 1
        for pay in range(n):
            out += str(self[-pay]) + "\n"
        out += (("-------- ["+str(lengh).center(6," ")+"], "+str(time.time())+" ").ljust(line,"-"))
        return out


class Element(namedtuple('Element', ['time', 'post', 'title', 'meta'])):
    def __new__(cls, post, meta):
        t = time.time()
        return super(Element, cls).__new__(cls, t, str(post), post.title, meta)

    def __str__(self, ):
        return f"{self.time} {self.post} {self.meta} {self.title}" 

