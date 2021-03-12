#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: Display.py
# Author: alukard <alukard@github>
# Date: 07.02.2021
#
# ██╗   ██╗██████╗ ██╗   ██╗ ██████╗ ████████╗███████╗
# ██║   ██║██╔══██╗██║   ██║██╔═══██╗╚══██╔══╝██╔════╝
# ██║   ██║██████╔╝██║   ██║██║   ██║   ██║   █████╗  
# ██║   ██║██╔═══╝ ╚██╗ ██╔╝██║   ██║   ██║   ██╔══╝  
# ╚██████╔╝██║      ╚████╔╝ ╚██████╔╝   ██║   ███████╗
#  ╚═════╝ ╚═╝       ╚═══╝   ╚═════╝    ╚═╝   ╚══════╝
 

import sys

import cv2
import numpy as np
import urllib3


class Display:

    resolution = (640, 360)

    def __init__(self, reddit = None):
        self.reddit = reddit
        # cv2.namedWindow("image", cv2.WINDOW_NORMAL)

    def show(self, post):
        im = self.image(post)
        if im is None: return

        cv2.imshow( "image", im )
        cv2.waitKey(100) # 3sec


    def image(self, post):
        url = self.url(post)                                                
        if ( not url ): return    

        http = urllib3.PoolManager()                           
        resp = http.request('GET', url)                        

        image = np.asarray(bytearray(resp.data), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)          

        image = cv2.resize(image, self.resolution)

        # return the image                                     
        return image    


    def close(self):
        cv2.destroyAllWindows()

    def url(self, post):
        url = self.reddit.submission(post.post).url

        # print(url, self.reddit.submission(post.post).subreddit)

        if url.endswith(('.jpg', '.png', '.gif', '.jpeg')):
            return url

