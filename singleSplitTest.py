#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 01:00:32 2018

@author: pedro
"""

#case 1: no errors

import numpy as np
import matplotlib.pyplot as plt
import time
from colorCodeh import *

import copy

#important values

p=0.05
q=1.-p

ps=0.97602226
qs=1.-ps



#first, we compute the theoretical probability

#probabilities of cells p(s0,s1,s2)
pc0=q**4+p**3*q
pc1=p**2*q**2+p**3*q
pc2=p*q**3+p**2*q**2
pc3=p*q**3+p**4


#conditional probabilities p(0|s1,s2)
p20=pc0/(pc0+pc1)
p21=pc1/(pc1+pc2)
p22=pc2/(pc2+pc3)

#final probability

p0=ps**2*p20+2*ps*qs*p21+qs**2*p22

psu=p0**2/(p0**2+(1.-p0)**2)






#Second, we need to generate the code

code=ColorCode(1,p)
code.e[0]=1
code.syndrome()
code.sp=code.sp*0.0+ps
prob=code.singlesoftresplit(1)
#code.hardDecoder(splitmethod=2)
print "theory ",psu
print "program", prob






#%%

#case 2: 2 errors in one of the cells

#first, probability of error of the qubits, including corner qubits
p=0.01
pc=0.16678000217679634
pnc=0.00050947631771845866

q=1.-p
qc=1.-pc
qnc=1.-pnc

#probabilities of cells p(s1,s2,s3)

p10=q*qnc*qnc*qc+pc*pnc*pnc*q
p11=p*pc*qnc*qnc+pnc*pnc*p*qc
p20=q*qnc**3+pnc**3*q
p21=p*pnc*qnc*qnc+pnc**2*p*qnc

#conditional probabilities p(+-|++)

p1P=p10/(p11+p10)
p1m=1.-p1P

p2m=p21/(p21+p20)
p2P=1.-p2m

#final probability:
pPm=p1P*p2m/(p1P*p2m+p1m*p2P)

print pPm,1.-pPm

#%%
#following the evolution of splitting values

code2=ColorCode(1,.01)
code3=ColorCode(1,.01)

code2.e[0]=1
code2.e[1]=1

code3.e[0]=1
code3.e[1]=1
code3.e[18]=1
code2.syndrome()
code3.syndrome()
nsteps=35
p2=np.zeros((nsteps,5))
p3=np.zeros((nsteps,5))

for i in range(nsteps):
    code2.softresplitcoordinate(i)
    code3.softresplitcoordinate(i)
    
    p2[i,:]=code2.sp[[1,6,7,8,13]]
    p3[i,:]=code3.sp[[1,6,7,8,13]]

for i in range(5):
        
    
    plt.figure(i)
    plt.clf()
    plt.plot(p2[:,i],'r-',label='2er side '+str(i))
    plt.plot(p3[:,i],'y-.',label='3er side '+str(i))
    
    plt.legend()
    
plt.figure(2)
plt.clf()
plt.plot(p2[:,2],'g-',label='2er central')
plt.plot(p3[:,2],'b-.',label='3er central')
plt.legend()

#%%
#the examples itselves

code3=ColorCode(1,.01)
code3.e[0]=1
code3.e[1]=1
code3.e[18]=1
code3.syndrome()
print code3.hardDecoder(plotall=True,fignum=20,splitsteps=15)
code2=ColorCode(1,.01)
code3=ColorCode(1,.01)
code2.e[0]=1
code2.e[1]=1
code3.e[0]=1
code3.e[1]=1
code3.e[18]=1

code2.syndrome()
code3.syndrome()
print code2.hardDecoder(plotall=True,fignum=10)
print code3.hardDecoder(plotall=True,fignum=25,splitsteps=14)




#%%

import numpy as np
import matplotlib.pyplot as plt
import time
from colorCodeh import *


code=ColorCode(1,.01)
code.e[0]=1
code.e[5]=1
code.e[10]=1
code.syndrome()
print code.hardDecoder(plotall=True,fignum=0,splitsteps=15)
print code.sp[7]


code=ColorCode(1,.01)
code.e[0]=1
code.e[5]=1
code.e[10]=1
code.syndrome()
print code.hardDecoder(plotall=True,fignum=10,splitsteps=16)
print code.sp[7]



code=ColorCode(1,.01)
code.e[0]=1
code.e[5]=1
code.e[10]=1
code.syndrome()
print code.hardDecoder(plotall=True,fignum=20,splitsteps=17)
print code.sp[7]



code=ColorCode(1,.01)
code.e[0]=1
code.e[5]=1
code.e[10]=1
code.syndrome()
print code.hardDecoder(plotall=True,fignum=30,splitsteps=18)
print code.sp[7]





