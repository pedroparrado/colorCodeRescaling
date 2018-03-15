#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 17:46:26 2018

@author: pedro
"""


import numpy as np
import matplotlib.pyplot as plt
import time
from colorCodeh import *

import copy



#plot all states

plt.figure(0)
plt.clf()

nq=32
m=.5*np.log2(nq*1./18.)
code=ColorCode(m,.05)
code.noise()
code.syndrome()
code.plot(splitting=True,indexs=True)
plt.title("initial state, "+str(code.energy()))

codesoft=copy.deepcopy(code)
plt.figure(1)
plt.clf()
for i in range(15):
    code.resplit()
code.plot(splitting=True)
plt.title("normal splitting, "+str(code.energy()))
print code.split, "normal"

plt.figure(2)
plt.clf()
for i in range(15):
    codesoft.softresplit()
codesoft.plot(splitting=True)
plt.title("soft splitting, "+str(codesoft.energy()))
print codesoft.split, "soft"


plt.figure(3)
plt.clf()
code.fullsplittester()
code.plot(splitting=True)
plt.title("perfect splitting, "+str(code.energy(True)))
print code.split, "perfect, or so it claims"

plt.figure(4)
plt.clf()
for i in range(len(code.split)):
    code.split[i]=0
for i in range(35):
    code.resplit()
for i in range(3):
    code.resplit(1)
    code.resplit(2)
    code.resplit(0)
code.plot(splitting=True)
plt.title("different initialization, "+str(code.energy()))
print code.split, "init at 0"

plt.figure(5)
plt.clf()
for i in range(len(code.split)):
    code.split[i]=0
    code.sp[i]=0.75
for i in range(35):
    code.softresplit()
code.plot(splitting=True)
plt.title("different initialization soft, "+str(code.energy()))
print code.split, "init at 0, soft"
print code.sp, "init at 0, soft"




#%%

#average number of splitting changes per step


import copy
nsteps=15
nmeas=1000


nq=32
m=.5*np.log2(nq*1./18.)
ch=np.zeros(nsteps)
ch2=np.zeros(nsteps)
ch3=np.zeros(nsteps)
E=np.zeros(nsteps)
E2=np.zeros(nsteps)
E3=np.zeros(nsteps)
chp=np.zeros(nsteps)
chp2=np.zeros(nsteps)
Ep=np.zeros(nsteps)
Ep2=np.zeros(nsteps)
Emin=np.zeros(nmeas)
for j in range(nmeas):
    code=ColorCode(m,.05)
    code.noise()
    code.syndrome()
    code2=copy.deepcopy(code)
    code3=copy.deepcopy(code)
    codep=copy.deepcopy(code)
    codep2=copy.deepcopy(code)
    changes=np.zeros(nsteps)
    for i in range(len(code3.split)):
        code3.split[i]=0
        
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
    #different initialization
    changes3=np.zeros(nsteps)    
    for i in range(nsteps):
        changes2[i],T=code2.resplit()
        E2[i]+=code2.energy()
        changes3[i],T=code3.resplit()
        E3[i]+=code3.energy()
    c=0        
    for i in range(3):
        c1,t=code.resplit(1)
        c2,t=code.resplit(2)
        c3,t=code.resplit(0)
        c+=c1+c2+c3
    ch3[-1]+=c
    ch+=changes*1./T
    ch2+=changes2*1./T 
    ch3+=changes3*1./T 
    
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
    Emin[j],fs=code.fullsplittester()    
    
    chp+=changesp*1./T
    chp2+=changesp2*1./T 

ch=ch/nmeas
ch2=ch2/nmeas
ch3=ch3/nmeas
E=E/nmeas
E2=E2/nmeas
E3=E3/nmeas
chp=chp/nmeas
chp2=chp2/nmeas
Ep=Ep/nmeas
Ep2=Ep2/nmeas
plt.figure(3)
plt.clf()
plt.plot(ch2,'p-',label="Randomized")
plt.plot(ch3,'p-',label="Init at 0")
plt.plot(ch,'p-',label="Paralellized")
plt.plot(chp2,'d-',label="Soft Randomized")
plt.plot(chp,'d-',label="Soft Paralellized")
plt.title("Percentage of splitting changes")
plt.ylim(0,1)
plt.legend()
plt.figure(4)
plt.clf()
plt.title("Percentage of splitting changes, log scale")
plt.plot(np.log(ch2),'p-',label="Randomized")
plt.plot(np.log(ch3),'p-',label="Init at 0")
plt.plot(np.log(ch),'p-',label="Paralellized")
plt.plot(np.log(chp2),'d-',label="Soft Randomized")
plt.plot(np.log(chp),'d-',label="Soft Paralellized")
plt.legend()
plt.figure(5)
plt.clf()
plt.plot(E2,'p-',label="Randomized")
plt.plot(E3,'p-',label="Init at 0")
plt.plot(E,'p-',label="Paralellized")
plt.plot(Ep2,'d-',label="Soft Randomized")
plt.plot(Ep,'d-',label="Soft Paralellized")
plt.title("Energy after the splittings")
minen=np.mean(Emin)
plt.plot(range(nsteps),np.zeros(nsteps)+minen,'-.', label='Min Energy')
plt.legend()



