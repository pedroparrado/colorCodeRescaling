#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 12:31:15 2018

@author: pedro

explores all 1,2 and 3 error combinations in the m=1 colorcode
"""


import numpy as np
import matplotlib.pyplot as plt
import time
from colorCodeh import *
import sys
import os

code=ColorCode(1,.01)

errorchains1=[]
errorchains2=[]
errorchains3=[]

methodtext=['init0','hard','soft']
#1 error configuration
for method in range(3):
    ##################### ONE ERROR CHAINS #################
    errorchains1.append([])
    nerr=0
    for i in range(len(code.p)):
        code.e[i]=0
        code.c[i]=0
    code.s=[0]*(code.L**2)
    for i in range(len(code.e)):
        code.e[i]=1
        code.syndrome()    
        res,loger=code.hardDecoder(splitmethod=method)
        if res==1:
            errorchains1[method].append(code.e)
            nerr+=1        
        code.e[i]=0
    print "Failures with one error: "+str(nerr)+"with method "+methodtext[method]
    
    ##################### TWO ERROR CHAINS #################
    errorchains2.append([])
    nerr=0
    for i in range(len(code.p)):
        code.e[i]=0
        code.c[i]=0
    code.s=[0]*(code.L**2)
    for i in range(len(code.e)):
        code.e[i]=1
        for j in range(i+1,len(code.e)):
            prev1=code.e[j]
            code.e[j]=1
            
            code.syndrome()    
            res,loger=code.hardDecoder(splitmethod=method)
            if res==1:
                errorchains2[method].append(code.e)
                nerr+=1    
            code.e[j]=prev1    
        code.e[i]=0
        
    print "Failures with 2 errors: "+str(nerr)+"with method "+methodtext[method]
    ##################### 3 ERROR CHAINS #################
    errorchains3.append([])
    nerr=0
    for i in range(len(code.p)):
        code.e[i]=0
        code.c[i]=0
    code.s=[0]*(code.L**2)
    for i in range(len(code.e)):
        code.e[i]=1
        for j in range(i+1,len(code.e)):
            prev1=code.e[j]
            code.e[j]=1
            for k in range(j+1,len(code.e)):
                prev2=code.e[k]
                code.e[k]=1
                
                code.syndrome()    
                res,loger=code.hardDecoder(splitmethod=method)
                if res==1:
                    errorchains3[method].append(code.e)
                    nerr+=1    
                code.e[k]=prev2  
            code.e[j]=prev1        
        code.e[i]=0
        
    print "Failures with 3 errors: "+str(nerr)+"with method "+methodtext[method]