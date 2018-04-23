#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 20:09:23 2018

@author: pedro
"""


import numpy as np
import matplotlib.pyplot as plt
import time
from colorCodeh import *

#####  PLOTTING EXAMPLE #######

code=ColorCode(1,.071)
code.noise()
code.syndrome()
code.hardDecoder(softsplit=False,plotall=True)


   
    
#%%    

#### MONTE CARLO SIMULATION OF THE DECODER #######

code=ColorCode(1,.01)
plt.figure(1)
plt.clf()

nsteps=12
Niter=30000
nsizes=4

P=np.linspace(0.001,0.1,nsteps)
startime=time.time()
E=np.zeros((nsteps,nsizes))
codes=[]
for i in range(nsizes):
    codes.append(ColorCode(i+1,P[0]))

timestimates=[]
for i in range(nsteps):
    p=P[i]
    for j in range(Niter):
        for k in range(nsizes):
            res,loger=codes[k].simulation(p)
            E[i,k]+=res
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
E/=niter
totaltime=time.time()-startime
print "Total time: "+str(totaltime)+"s, "+str(totaltime/60.)+"min, "+str(totaltime/3600.)+"h"
for k in range(nsizes):
    plt.plot(P,E[:,k],'s-',label="m="+str(k+1))
    
plt.title("Probability of Log Error")
plt.legend()

#stimates of total time:

cumulative=np.zeros(len(timestimates))
for i in range(len(cumulative)):
    cumulative[i]=sum(np.array(timestimates)[0:i])/(i+1.)


plt.figure(2)
plt.clf()
plt.title("Time stimates")
plt.plot(timestimates,'.')
plt.plot(cumulative,'.')
plt.plot(totaltime+np.zeros(len(timestimates)))

plt.figure(3)
plt.clf()
plt.title("Time stimates, relative error")
plt.plot(np.abs(np.array(timestimates)/totaltime-1.),'.')
plt.plot(np.abs(np.array(cumulative)/totaltime-1.),'.')
plt.plot(1.+np.zeros(len(timestimates)))






