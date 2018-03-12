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

code=ColorCode(1,.1)
plt.figure(1)
plt.clf()
code.noise()
code.syndrome()
code.hardDecoder()
code.plot()
     



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
code=ColorCode(1,.08)
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
ch=np.zeros(nsteps)
ch2=np.zeros(nsteps)
E=np.zeros(nsteps)
E2=np.zeros(nsteps)
chp=np.zeros(nsteps)
chp2=np.zeros(nsteps)
Ep=np.zeros(nsteps)
Ep2=np.zeros(nsteps)
for j in range(nmeas):
    code=ColorCode(1,.05)
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
plt.plot(chp2,'d',label="Soft Randomized")
plt.plot(chp,'d',label="Soft Paralellized")
plt.title("Percentage of splitting changes")
plt.ylim(0,1)
plt.legend()
plt.figure(4)
plt.clf()
plt.title("Percentage of splitting changes, log scale")
plt.plot(np.log(ch2),'p',label="Randomized")
plt.plot(np.log(ch),'p',label="Paralellized")
plt.plot(np.log(chp2),'d',label="Soft Randomized")
plt.plot(np.log(chp),'d',label="Soft Paralellized")
plt.legend()
plt.figure(5)
plt.clf()
plt.plot(E2,'p',label="Randomized")
plt.plot(E,'p',label="Paralellized")
plt.plot(Ep2,'d',label="Soft Randomized")
plt.plot(Ep,'d',label="Soft Paralellized")
plt.title("Energy after the splittings")
plt.legend()

''' 
E=E-min(E)+1e-8
E2=E2-min(E2)+1e-8
plt.figure(6)
plt.clf()
plt.title("Energy, log scale")
plt.plot(np.log(E2),'p',label="Randomized")
plt.plot(np.log(E),'p',label="Paralellized")
plt.legend()
'''
