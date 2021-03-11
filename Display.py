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

        print(url, self.reddit.submission(post.post).subreddit)


        if url.endswith(('.jpg', '.png', '.gif', '.jpeg')):
            return url


    # def show_image(self, ):                                               
    #     if (last != self._prev_e):                    
    #             self._prev_e = last                                   
    #             if last is None:                                      
    #                     return                                        
    #             new_img = last.image()                                
    #             if new_img is not None:                               
    #                     self.img = new_img            
    #                                                   
    #     img = self.img                                
    #                                                   
    #     if (self.dbg): print ("resiaved image")       
    #     scale_percent = self.image_size / img.shape[1]
    #     width = int(img.shape[1] * scale_percent )    
    #     height = int(img.shape[0] * scale_percent)    
    #     dim = (width, height)                         
    #                                                   
    #     # resize image                                
    #     img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA) 
    #                                      
    #     title = self.image_title         
    #     cv2.imshow(title,img)            
    #                                      
    #     key = cv2.waitKey(1) & 0xFF      
    #                                      
    #     if (key == ord("+")):            
    #             self.update_img_size(+10)
    #                                      
    #     elif (key == ord("-")):          
    #             self.update_img_size(-10)
    # 
    #     return True    

    # def image (self, ):                                                                                                                              
    #     # download the image, convert it to a NumPy array, and then read
    #     # it into OpenCV format                                         
    #                                                                     
    #     url = self.url()                                                
    #     if ( not url ): return    
    #     http = urllib3.PoolManager()                           
    #     resp = http.request('GET', url)                        
    #     image = np.asarray(bytearray(resp.data), dtype="uint8")
    #     image = cv2.imdecode(image, cv2.IMREAD_COLOR)          
    #     # return the image                                     
    #     return image    
