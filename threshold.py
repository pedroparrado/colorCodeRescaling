#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 19:28:32 2018

@author: pedro
"""


import os
import numpy as np
import matplotlib.pyplot as plt
import time
from colorCodeh import *

nsteps=10
Niter=140
nsizes=3

nmin=[3,7,15,31,63,127,255]

P=np.linspace(0.045,0.075,nsteps)
startime=time.time()
E=np.zeros((nsteps,nsizes,5))
codes=[]
nerrors=[]
for i in range(nsizes):
    codes.append(ColorCode(i+1,P[0]))
    nerrors.append([])

timestimates=[]
for i in range(nsteps):
    p=P[i]
    for j in range(Niter):
        for k in range(nsizes):
            res,loger=codes[k].simulation(p)
            E[i,k,0]+=res
            E[i,k,1]+=loger[0]
            E[i,k,2]+=loger[1]
            E[i,k,3]+=loger[2]
            E[i,k,4]+=loger[3]
            if res==1:
                nerrors[k].append(np.sum(codes[k].e))
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
E/=Niter
totaltime=time.time()-startime
print "Total time: "+str(totaltime)+"s, "+str(totaltime/60.)+"min, "+str(totaltime/3600.)+"h"

plt.figure(1)
plt.clf()

for k in range(nsizes):
    plt.plot(P,E[:,k,0],'s-',label="m="+str(k+1))
    
plt.title("Probability of Log Error")
plt.xlabel("p")
plt.legend()


plt.figure(2)
plt.clf()
plt.title("Different Logical errors")
col=["red","blue","green","yellow","black","orange","teal"]
for k in range(nsizes):
    for lei in range(1,5):
        plt.plot(P,E[:,k,lei],'s-',color=col[k]  ,label="m="+str(k+1))
plt.xlabel("p")


plt.legend()
Emean=np.zeros((nsteps,nsizes))

for k in range(nsizes):
    for lei in range(1,5):
        Emean[:,k]+=E[:,k,lei]/4.
        
plt.figure(3)
plt.clf()
plt.title("Average of each error against any error curve")
plt.xlabel("p")

for k in range(nsizes):
    plt.plot(P,Emean[:,k],'p-',color=col[k] ,label="Mean m="+str(k+1))
    plt.plot(P,E[:,k,0],'s-',color=col[k]  ,label="Any error m="+str(k+1))

plt.legend()

for k in range(nsizes):
        
    plt.figure(4+k)
    plt.hist(nerrors[k])
    plt.title("Histogram of number of unsolved errors, size "+str(k+1)+", min amount:"+str(np.min(nerrors[k])))


#saving the simulation

filen="ccPthreshold"+str(nsizes)+"p"+str(int(1000*P[0]))+"to"+str(int(1000*P[-1]))
if(os.path.isfile(filen)):
    
    filen="ccEthreshold"+str(nsizes)+"p"+str(int(1000*P[0]))+"to"+str(int(1000*P[-1]))
    oldE=np.load(filen)
    
    filen="ccNthreshold"+str(nsizes)+"p"+str(int(1000*P[0]))+"to"+str(int(1000*P[-1]))
    oldN=np.load(filen)
    
    newE=(E*Niter+oldE*oldN)/(Niter+oldN)
    
    filen="ccEthreshold"+str(nsizes)+"p"+str(int(1000*P[0]))+"to"+str(int(1000*P[-1]))
    np.save(filen,newE)
    filen="ccNthreshold"+str(nsizes)+"p"+str(int(1000*P[0]))+"to"+str(int(1000*P[-1]))
    np.save(filen,Niter+oldN)
else:        
    filen="ccPthreshold"+str(nsizes)+"p"+str(int(1000*P[0]))+"to"+str(int(1000*P[-1]))
    np.save(filen,P)
    filen="ccEthreshold"+str(nsizes)+"p"+str(int(1000*P[0]))+"to"+str(int(1000*P[-1]))
    np.save(filen,E)
    filen="ccNthreshold"+str(nsizes)+"p"+str(int(1000*P[0]))+"to"+str(int(1000*P[-1]))
    np.save(filen,Niter)


