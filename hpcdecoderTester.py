#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 15:48:23 2018

@author: pedro
"""


import numpy as np
import matplotlib.pyplot as plt
import time
from colorCodeh import *
import sys
import os


nsteps=int(sys.argv[1])
Niter=int(sys.argv[2])
size=int(sys.argv[3])
p1=float(sys.argv[4])
p2=float(sys.argv[5])

code=ColorCode(1,.08)

P=np.linspace(p1,p2,nsteps)
startime=time.time()
E=np.zeros(nsteps)
t=np.zeros(nsteps)
E500=np.zeros(nsteps)
t500=np.zeros(nsteps)
code=ColorCode(size,P[0])

startime=time.time()
for j in range(Niter):
    for i in range(nsteps):
        dt=time.time()
        p=P[i]
        res,loger=code.simulation(p)
        E[i]+=res
        t[i]+=time.time()-dt
        E500[i]+=res
        t500[i]+=time.time()-dt
        '''
        if j%10==0:
            dt=time.time()-startime
            currentstep=1.*(j+1.)/Niter*(i+1)/nsteps
            print "Iteration "+str(j+1)+", "+str(currentstep)+"% completed"
            print "Time spent: "+str(dt/60.)+"min, "+str(dt/3600.)+"h"
            dt=dt*(1./currentstep)
            timestimates.append(dt)
            print "Total time: "+str(dt/60.)+"min, "+str(dt/3600.)+"h"
            dt=dt*(1.-currentstep)
            print "Time to finish: "+str(dt/60.)+"min, "+str(dt/3600.)+"h"
            print "---------------------------------------------------------"
        '''
    #500 iterations security save
    if (j+1)%500==0 and j>0:
        totaltime=time.time()-startime
        niter500=500
        niterold=500
        #save current progress
        
        #filename of the temporal progress save
        filen="./results/ccsavem"+str(size)+"ns"+str(nsteps)+"p"+str(int(p1*100))+"to"+str(int(p2*100))+".txt"
        
        #check if there is an already existing file
        if(os.path.isfile(filen)):
            #if exist, then read the data inside and add it to the statistics            
            f=open(filen)
            z=[]
            x=[]
            y=[]
            for line in f:
                r=line.split()
                x.append(float(r[0]))
                y.append(float(r[1]))
                z.append(float(r[2]))
            niterold=x[0]
            oldtime=t[0]
            eold=np.array(y[1:])
            told=np.array(z[1:])
            
            #and we add those to the actual results
            niter500+=niterold
            totaltime+=oldtime
            E500+=eold
            t500+=told
            f.close()
                
        #save the data
        f=open(filen,"w")    
        f.write(str(niterold)+" "+str(nsteps)+" "+str(totaltime)+"\n")
        for i in range(len(P)):
            f.write(str(P[i])+" "+str(E500[i])+" "+str(t500[i])+"\n")
        f.close()
        
        #reset the partial count
        E500=np.zeros(nsteps)
        t500=np.zeros(nsteps)
        startime=time.time()

        
E/=Niter
t/=Niter




filen="./results/ccm"+str(size)+"Nit"+str(Niter)+"p"+str(int(p1*100))+"to"+str(int(p2*100))+".txt"


f=open(filen,"w")
for i in range(len(P)):
    f.write(str(P[i])+" "+str(E[i])+" "+str(t[i])+"\n")
f.close()




