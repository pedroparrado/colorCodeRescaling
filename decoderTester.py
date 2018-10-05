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
nsteps=8
Niter=800
nsizes=3

P=np.linspace(0.001,0.41,nsteps)
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
E/=Niter
totaltime=time.time()-startime
print "Total time: "+str(totaltime)+"s, "+str(totaltime/60.)+"min, "+str(totaltime/3600.)+"h"

plt.figure(1)
plt.clf()

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



#saving the simulation
filen="ccPsimtom"+str(nsizes)+"p"+str(int(1000*P[0]))+"to"+str(int(1000*P[-1]))
np.save(filen,P)
filen="ccEsimtom"+str(nsizes)+"p"+str(int(1000*P[0]))+"to"+str(int(1000*P[-1]))
np.save(filen,E)

#%%    

#### MONTE CARLO SIMULATION OF THE DECODER WITH 5 DIFFERENT CURVES#######

import numpy as np
import matplotlib.pyplot as plt
import time
from colorCodeh import *

code=ColorCode(1,.01)
nsteps=10
Niter=5000
nsizes=4

P=np.linspace(0.001,0.09,nsteps)
startime=time.time()
E=np.zeros((nsteps,nsizes,5))
codes=[]
for i in range(nsizes):
    codes.append(ColorCode(i+1,P[0]))

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
#saving the simulation
filen="ccPsimtom"+str(nsizes)+"p"+str(int(1000*P[0]))+"to"+str(int(1000*P[-1]))
np.save(filen,P)
filen="ccEsimtom"+str(nsizes)+"p"+str(int(1000*P[0]))+"to"+str(int(1000*P[-1]))
np.save(filen,E)

#%%
nsizes=4
p1=0.001
p2=0.1

#recovering the simulation

filen="ccPsimtom"+str(nsizes)+"p"+str(int(1000*p1))+"to"+str(int(1000*p2))+".npy"
P=np.load(filen)
filen="ccEsimtom"+str(nsizes)+"p"+str(int(1000*p1))+"to"+str(int(1000*p2))+".npy"
E=np.load(filen)
plt.figure(1)
plt.clf()

for k in range(nsizes):
    plt.plot(P,E[:,k],'s-',label="m="+str(k+1))
    
plt.title("Probability of Log Error")
plt.legend()
