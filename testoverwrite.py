#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 17:41:38 2018

@author: pedro
"""

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


nsteps=3
Niter=1000
size=1
p1=.01
p2=.5
method=2

code=ColorCode(1,.08)

P=np.linspace(p1,p2,nsteps)
startime=time.time()
E=np.zeros(nsteps)
Epartial=np.zeros((nsteps,4))#one for each logical error
t=np.zeros(nsteps)
E500=np.zeros(nsteps)
Ep500=np.zeros((nsteps,4))
t500=np.zeros(nsteps)
code=ColorCode(size,P[0])


eold=np.zeros((nsteps,4))
startime=time.time()
for j in range(Niter):
    for i in range(nsteps):
        dt=time.time()
        p=P[i]
        res,loger=code.simulation(p,method)
        E[i]+=res
        for k in range(4):
            Epartial[i,k]+=loger[k]
            Ep500[i,k]+=loger[k]
        t[i]+=time.time()-dt
        E500[i]+=res
        t500[i]+=time.time()-dt
    #50 iterations security save
    if (j+1)%50==0 and j>0:
        totaltime=time.time()-startime
        niter500=50
        niterold=50
        #save current progress
        methodtext=['init0','hard','soft']
        #filename of the temporal progress save
        filen="./results/cctestm"+str(size)+"ns"+str(nsteps)+"p"+str(int(p1*100))+"to"+str(int(p2*100))+methodtext[method]+".txt"
        
        #check if there is an already existing file
        if(os.path.isfile(filen)):
            #if exist, then read the data inside and add it to the statistics            
            f=open(filen)
            z=[]
            x=[]
            y=[]
            y0=[]
            y1=[]
            y2=[]
            y3=[]
            for line in f:
                r=line.split()
                print r
                x.append(float(r[0]))
                y.append(float(r[1]))
                y0.append(float(r[2]))
                y1.append(float(r[3]))
                y2.append(float(r[4]))
                y3.append(float(r[5]))
                z.append(float(r[6]))
            niterold=x[0]
            oldtime=t[0]
            eold1=np.array(y[1:])
            eold[:,0]=np.array(y0[1:])
            eold[:,1]=np.array(y1[1:])
            eold[:,2]=np.array(y2[1:])
            eold[:,3]=np.array(y3[1:])
            told=np.array(z[1:])
            
            #and we add those to the actual results
            niter500+=niterold
            totaltime+=oldtime
            E500+=eold1
            Ep500+=eold
            t500+=told
            f.close()
                
        #save the data
        f=open(filen,"w")    
        f.write(str(niter500)+" "+str(nsteps)+" "+str(0)+" "+str(1)+" "+str(2)+" "+str(3)+" "+str(totaltime)+"\n")
        for i in range(len(P)):
            f.write(str(P[i])+" "+str(E500[i])+" "+str(Ep500[i,0])+" "+str(Ep500[i,1])+" "+str(Ep500[i,2])+" "+str(Ep500[i,3])+" "+str(t500[i])+"\n")
        f.close()
        
        #reset the partial count
        E500=np.zeros(nsteps)
        Ep500=np.zeros((nsteps,4))
        t500=np.zeros(nsteps)
        startime=time.time()

        
E/=Niter
t/=Niter



methodtext=['init0','hard','soft']

filen="./results/cctesttotalm"+str(size)+"Nit"+str(Niter)+"p"+str(int(p1*100))+"to"+str(int(p2*100))+methodtext[method]+".txt"


f=open(filen,"w")
for i in range(len(P)):
    f.write(str(P[i])+" "+str(E[i])+" "+str(Epartial[i,0])+" "+str(Epartial[i,1])+" "+str(Epartial[i,2])+" "+str(Epartial[i,3])+" "+str(t[i])+"\n")
f.close()



