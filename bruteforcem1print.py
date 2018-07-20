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


methodtext=['init0','hard','soft','init0corners','heatsplit','hard minexplore', 'softcoordinate']
#1 error configuration
methods=[6]
usecorners=True
softRescale=True
for method in methods:
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
    #for i in range(len(code.p)):
    #    code.e[i]=0
    #    code.c[i]=0
        
    #code=ColorCode(1,.01)
    #code.s=[0]*(code.L**2)
    
    for i in range(70):#len(code.e)):
        code=ColorCode(1,.01)
        code.e[i]=1
        code.syndrome()    
        res,loger=code.hardDecoder(splitmethod=method,cornerupdate=usecorners,softRescaling=softRescale,plotall=False,fignum=27,beta=10)
        if res==1:
            #f1.write(str(code.e))
            texter=" "
            for ki in range(len(code.e)):
                if code.e[ki]==1:
                    texter+=str(ki)+" "
                    
            print "Error found for method "+str(method)+" with corners: "+str(usecorners)
            print "Failure at error: "+texter+"  "+str(sum(code.c))+"\n \n"
            nerr+=1        
        code.e[i]=0
    print "Failures with one error: "+str(nerr)+"with method "+methodtext[method]
    
    
    ##################### TWO ERROR CHAINS #################
    nerr=0
    for i in range(len(code.p)):
        code.e[i]=0
        code.c[i]=0
    code.s=[0]*(code.L**2)
    for i in range(len(code.e)):
        for j in range(i+1,len(code.e)):
            code=ColorCode(1,.01)
            code.e[i]=1
            code.e[j]=1
            
            code.syndrome()    
            res,loger=code.hardDecoder(splitmethod=method,cornerupdate=usecorners,beta=10)
            if res==1:
                #f2.write(str(code.e))
                erchain=[]
                correctionapplied=[]
                for ind in range(len(code.e)):
                    if code.e[ind]==1:
                        erchain.append(ind)
                    if code.c[ind]==1:
                        correctionapplied.append(ind)
                print "Error found for method "+str(method)+" with corners: "+str(usecorners)
                print "Error configuration: "+str(erchain)
                print "corrections: " + str(correctionapplied)
                print " "
                nerr+=1    
            #code.e[j]=prev1    
        #code.e[i]=0
        
    print "Failures with 2 errors: "+str(nerr)+"with method "+methodtext[method]
    ##################### 3 ERROR CHAINS #################
    
    nerr=0
    for i in range(len(code.p)):
        code.e[i]=0
        code.c[i]=0
    code.s=[0]*(code.L**2)
    for i in range(len(code.e)):
        #code.e[i]=1
        for j in range(i+1,len(code.e)):
            #prev1=code.e[j]
            #code.e[j]=1
            for k in range(j+1,len(code.e)):
                #prev2=code.e[k]
                
                code=ColorCode(1,.01)
                code.e[k]=1
                code.e[i]=1
                code.e[j]=1
                
                code.syndrome()    
                res,loger=code.hardDecoder(splitmethod=method,cornerupdate=usecorners,beta=10)
                if res==1:
                    #f3.write(str(code.e))
                    erchain=[]
                    correctionapplied=[]
                    for ind in range(len(code.e)):
                        if code.e[ind]==1:
                            erchain.append(ind)
                        if code.c[ind]==1:
                            correctionapplied.append(ind)
                            
                    print "Error found for method "+str(method)+" with corners: "+str(usecorners)
                    print "Error configuration: "+str(erchain)
                        
                    print "corrections: " + str(correctionapplied)
                    print " "
                    nerr+=1    
                    if nerr>10:
                        print "more than 10 3-error configurations"
                        break
            if nerr>10:
                        break
        if nerr>10:
            break
                #code.e[k]=prev2  
            #code.e[j]=prev1        
        #code.e[i]=0
        
    print "Failures with 3 errors: "+str(nerr)+"with method "+methodtext[method]
    #f1.close()
    #f2.close()
    #f3.close()
    