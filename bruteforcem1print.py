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


methodtext=['init0','hard','soft']
#1 error configuration
for method in range(1):
    '''
    filen="errors1"+methodtext[method]+".txt"
    f1=open(filen,"w")    
    filen="errors2"+methodtext[method]+".txt"
    f2=open(filen,"w")    
    filen="errors3"+methodtext[method]+".txt"
    f3=open(filen,"w")    
    '''
    ##################### ONE ERROR CHAINS #################
    
    nerr=0
    for i in range(len(code.p)):
        code.e[i]=0
        code.c[i]=0
        
    code=ColorCode(1,.01)
    code.s=[0]*(code.L**2)
    
    code=ColorCode(1,.01)
    for i in range(len(code.e)):
        code.e[i]=1
        code.syndrome()    
        res,loger=code.hardDecoder(splitmethod=method,plotall=True,fignum=27)
        if res==1:
            #f1.write(str(code.e))
            texter=" "
            for ki in range(len(code.e)):
                if code.e[ki]==1:
                    texter+=str(ki)+" "
            print texter
            nerr+=1        
        code.e[i]=0
    print "Failures with one error: "+str(nerr)+"with method "+methodtext[method]
    
    '''
    ##################### TWO ERROR CHAINS #################
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
                f2.write(str(code.e))
                nerr+=1    
            code.e[j]=prev1    
        code.e[i]=0
        
    print "Failures with 2 errors: "+str(nerr)+"with method "+methodtext[method]
    ##################### 3 ERROR CHAINS #################
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
                    f3.write(str(code.e))
                    nerr+=1    
                code.e[k]=prev2  
            code.e[j]=prev1        
        code.e[i]=0
        
    print "Failures with 3 errors: "+str(nerr)+"with method "+methodtext[method]
    f1.close()
    f2.close()
    f3.close()
    '''