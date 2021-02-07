#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: Counter.py
# Author: alukard <alukard@github>
# Date: 07.02.2021

# ██╗   ██╗██████╗ ██╗   ██╗ ██████╗ ████████╗███████╗
# ██║   ██║██╔══██╗██║   ██║██╔═══██╗╚══██╔══╝██╔════╝
# ██║   ██║██████╔╝██║   ██║██║   ██║   ██║   █████╗  
# ██║   ██║██╔═══╝ ╚██╗ ██╔╝██║   ██║   ██║   ██╔══╝  
# ╚██████╔╝██║      ╚████╔╝ ╚██████╔╝   ██║   ███████╗
#  ╚═════╝ ╚═╝       ╚═══╝   ╚═════╝    ╚═╝   ╚══════╝

class Count (dict):

    def add (self, element, n=1):
        if not element in self:
            self[element] = [0,0]

        self[element][0] += n
        self[element][1] += 1
    
    def void (self, element, ):
        if not element in self:
            self[element] = [0,0]

        self[element][1] += 1
    
    def sub (self, element, n=1):
        if not element in self:
            self[element] = [0,0]

        self[element][0] -= n
        self[element][1] -= 1

    def averige(self,element, positon = 0, diff = -1):
        if (diff != -1):
            a = (self[element][0]+diff)/(self[element][1]+1)
        elif (self[element][1] == 0):
            a = 0
        else:
            a = self[element][0]/self[element][1]

        return round(a,positon)
    
    def __str__(self):
        out = " "
        out += "\t-------------------------------------\n"
        out += "\t| type:  sum,      count:    avg:\n"
        out += "\t-------------------------------------\n"
        for k in self:
            avg = self.averige(k,5)
            if (avg != 0):
                out += "\t| " + k.ljust(4) + " | " 
                out += str(round(self[k][0],2)).ljust(8)+ "| " 
                out += str(round(self[k][1],2)).ljust(8)+ "| " 
                out += str(avg) + "\n"
        out += "\t-------------------------------------"
        return out

