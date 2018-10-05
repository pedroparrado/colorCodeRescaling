#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 17:51:08 2018

@author: pedro
"""

import numpy as np
import matplotlib.pyplot as plt
import time
from colorCodeh import *



code=ColorCode(1,.071)
code.noise()
code.syndrome()
code.hardDecoder(softsplit=True,plotall=True)

        
   
    
#%%    
p=.07
#code=ColorCode(2,p)
plt.figure(1)
plt.clf()
code.simulation(p,plotall=True)
     



#%%

code=ColorCode(4,.08)
plt.figure(1)
#plt.clf()
code.noise()
code.syndrome()
#code.plot(splitting=True,cells=True)

#%%
'''
print code.resplit()
code.plot(lattice=False,syndrome=False,splitting=True,cells=True)
'''

#%%
import copy

nsteps=15

nq=32
m=.5*np.log2(nq*1./18.)
code=ColorCode(m,.08)
code.noise()
code.syndrome()
plt.figure(1)
#plt.clf()
code.noise()
code.syndrome()
code2=copy.deepcopy(code)
changes=np.zeros(nsteps)
for i in range(nsteps):
    T=0
    c,t=code.resplit(1)
    changes[i]+=c
    T+=t
    c,t=code.resplit(2)
    changes[i]+=c
    T+=t
    c,t=code.resplit(0)
    changes[i]+=c
    T+=t
changes2=np.zeros(nsteps)
minen=code.fullsplittester()
for i in range(nsteps):
    changes2[i],T=code2.resplit()
plt.figure(2)
plt.clf()
plt.plot(changes2*1./float(T),'p',label="Randomized")
plt.plot(changes*1./float(T),'p',label="Paralellized")
plt.plot(range(nsteps),np.zeros(nsteps)+minen, '-.', label='Min Energy')
plt.ylim(0,1)
plt.legend()

#%%

#average number of splitting changes per step


import copy
nsteps=40
nmeas=100

nq=32
m=.5*np.log2(nq*1./18.)
ch=np.zeros(nsteps)
ch2=np.zeros(nsteps)
E=np.zeros(nsteps)
E2=np.zeros(nsteps)
chp=np.zeros(nsteps)
chp2=np.zeros(nsteps)
Ep=np.zeros(nsteps)
Ep2=np.zeros(nsteps)
for j in range(nmeas):
    code=ColorCode(m,.05)
    code.noise()
    code.syndrome()
    code2=copy.deepcopy(code)
    codep=copy.deepcopy(code)
    codep2=copy.deepcopy(code)
    changes=np.zeros(nsteps)
    for i in range(nsteps):
        T=0
        c,t=code.resplit(1)
        changes[i]+=c
        T+=t
        c,t=code.resplit(2)
        changes[i]+=c
        T+=t
        c,t=code.resplit(0)
        changes[i]+=c
        T+=t
        E[i]+=code.energy()
        
    changes2=np.zeros(nsteps)    
    for i in range(nsteps):
        changes2[i],T=code2.resplit()
        E2[i]+=code2.energy()
    ch+=changes*1./T
    ch2+=changes2*1./T 
    
    '''
    #soft respliting
    changesp=np.zeros(nsteps)
    for i in range(nsteps):
        T=0
        c,t=codep.softresplit(1)
        changesp[i]+=c
        T+=t
        c,t=codep.softresplit(2)
        changesp[i]+=c
        T+=t
        c,t=codep.softresplit(0)
        changesp[i]+=c
        T+=t
        Ep[i]+=codep.energy()
        
        
    changesp2=np.zeros(nsteps)    
    for i in range(nsteps):
        changesp2[i],T=codep2.softresplit()
        Ep2[i]+=codep2.energy()
    chp+=changesp*1./T
    chp2+=changesp2*1./T 
    '''

ch=ch/nmeas
ch2=ch2/nmeas
E=E/nmeas
E2=E2/nmeas
chp=chp/nmeas
chp2=chp2/nmeas
Ep=Ep/nmeas
Ep2=Ep2/nmeas
plt.figure(3)
plt.clf()
plt.plot(ch2,'p',label="Randomized")
plt.plot(ch,'p',label="Paralellized")

'''
plt.plot(chp2,'d',label="Soft Randomized")
plt.plot(chp,'d',label="Soft Paralellized")
'''

plt.title("Percentage of splitting changes")
plt.ylim(0,1)
plt.legend()
plt.figure(4)
plt.clf()
plt.title("Percentage of splitting changes, log scale")
plt.plot(np.log(ch2),'p',label="Randomized")
plt.plot(np.log(ch),'p',label="Paralellized")
'''
plt.plot(np.log(chp2),'d',label="Soft Randomized")
plt.plot(np.log(chp),'d',label="Soft Paralellized")
'''
plt.legend()
plt.figure(5)
plt.clf()
plt.plot(E2,'p',label="Randomized")
plt.plot(E,'p',label="Paralellized")
'''
plt.plot(Ep2,'d',label="Soft Randomized")
plt.plot(Ep,'d',label="Soft Paralellized")
'''
plt.title("Energy after the splittings")
plt.legend()


#%%



import numpy as np
import matplotlib.pyplot as plt
import time
from colorCodeh import *

code=ColorCode(0,.15)
code.noise()
code.syndrome()
lut18=np.load("lookuptable18.npy")
lut18lop=np.load("lookuptable18q4lop.npy")

code2=copy.deepcopy(code)

code.decode0()
ehmax,hmax=code2.decode0lop()

plt.figure(0)
plt.clf()
code.plot()
plt.title("MLE decoder")
plt.figure(1)
plt.clf()
code2.plot()
plt.title("MLH decoder")

def check18(code,printall=False):
        
    
    epc=""    
    for i in range(18):
        new=0
        if code.e[i]==1:
            new+=1
        if code.c[i]==1:
            new+=1
        epc+=str(new%2)
    if printall:
            
        print "Error correction status:"
        if epc in lut18lop[0][3]:
            print "Error solved for MLE Case"
        else:
            print "Logical error induced"

    if epc in lut18lop[0][3]:
        return 0
    else:
        return 1

check18(code,True)
check18(code2,True)
#lut18=np.load("lookuptable18.npy")
#lut18lop=np.load("lookuptable18q4lop.npy")



#%%

#Monte carlo for 18 qubit code


import numpy as np
import matplotlib.pyplot as plt
import time
from colorCodeh import *


lut18=np.load("lookuptable18.npy")
lut18lop=np.load("lookuptable18q4lop.npy")

niter=500
nsteps=15
pvar=0.00#percentage of the variation in the error probabilities
P=np.linspace(0.0002,0.03,nsteps)

peMLE=np.zeros(nsteps)
peMLH=np.zeros(nsteps)

timecreate=0.
timenoise=0.
timecopy=0.
timedecode1=0.
timedecode2=0.
timecheck=0.
def addtime(timecount,start):
    timecount+=time.time()-start
    start=time.time()
    return timecount,start

start0=time.time()
for j in range(nsteps):
    p=P[j]
    if j>0:            
        timetonow=time.time()-start0
        totaltimestimate=timetonow/j*nsteps
        print "Step: ",j,"Current time: ",timetonow
        print "Stimated time to finish: ",totaltimestimate-timetonow
        print "Stimated total time: ",totaltimestimate
    for i in range(niter):
        start=time.time()   
        
        code=ColorCode(0,p)    
        for k in range(18):
            r=np.random.rand()-.5
            code.p[k]=code.p[k]*(1.+r*pvar)
        timecreate,start=addtime(timecreate,start)
        
        code.noise()
        code.syndrome()        
        timenoise,start=addtime(timenoise,start)
        
        code2=copy.deepcopy(code)
        timecopy,start=addtime(timecopy,start)
        
        code.decode0()
        timedecode1,start=addtime(timedecode1,start)
        
        code2.decode0lop()
        timedecode2,start=addtime(timedecode2,start)
        
        peMLE[j]+=check18(code)
        peMLH[j]+=check18(code2)
                
        timecheck,start=addtime(timecheck,start)


print "timers:"


print timecreate/60., " min for creating ColorCode"
print timenoise/60., " min for generating noise"
print timecopy/60., " min for copying the code"
print timedecode1/60., " min for decoding MLE"
print timedecode2/60., " min for decoding MLH"
print timecheck/60., " min for checking logical error"



peMLE=peMLE/niter
peMLH=peMLH/niter


plt.figure(4)
plt.clf()
plt.plot(P,peMLE,'p-',label="MLE")
plt.plot(P,peMLH,'p-',label="MLH")
plt.legend()
plt.title("Probability of Logical Error")
plt.xlabel("p")











