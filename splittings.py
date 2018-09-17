#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 14:40:58 2018

@author: pedro
"""


import numpy as np
import matplotlib.pyplot as plt
import time
from colorCodeh import *


import copy

#testing the splitting methods

nps=10
nmeas=10000
m=3

P=np.linspace(.001,.15,nps)

E0=np.zeros(nps)
E2=np.zeros(nps)
E5=np.zeros(nps)
E6=np.zeros(nps)

start=time.time()
tm0=tm2=tm5=tm6=0.0
for jj in range(nmeas):
    
    for k in range(len(P)):
        p=P[k]
        code=ColorCode(m,p)
        code.noise()
        code.syndrome()
        code0=copy.deepcopy(code)#hard
        code2=copy.deepcopy(code)#soft
        code5=copy.deepcopy(code)#hard random choice
        code6=copy.deepcopy(code)#soft coordinate
        
        #   SPLITTING OF SYNDROMES    
        splitsteps=20    
        #initial condition
        for i in range(len(code.split)):
            #init0 condition
            code0.split[i]=0
            code5.split[i]=0
            #soft guess initial condition
            code2.sp[i]=0.5        
        
        t0=time.time()
        for j in range(splitsteps):
            code2.softresplit()    
        t1=time.time()    
        for j in range(splitsteps):
            code0.resplit() 
        t2=time.time()
        code5.randomminsplit(splitsteps)
        t3=time.time()
        code6.softresplitcoordinate(splitsteps)
        t4=time.time()    
        E0[k]+=code0.energy()
        E2[k]+=code2.energy()
        E5[k]+=code5.energy()
        E6[k]+=code6.energy()

    print " "
    print " "
    print "Step: ",jj,nmeas
    print "Time taken/min: ", (time.time()-start)/60.
    tm0+=t2-t1
    tm2+=t1-t0
    tm5+=t3-t2
    tm6+=t4-t3
    
    print "time method 0: ",tm0
    print "time method 2: ",tm2
    print "time method 5: ",tm5
    print "time method 6: ",tm6
    
E0=E0/nmeas
E2=E2/nmeas
E6=E6/nmeas
E5=E5/nmeas


plt.figure(1)
plt.clf()

plt.plot(P,E0,'p-',label="Hard best choice")
plt.plot(P,E5,'p-',label="Hard random choice")
plt.plot(P,E2,'p-',label="Soft random sample")
plt.plot(P,E6,'p-',label="Soft syncronized")

plt.title("Energy after the splittings, m="+str(m))
plt.legend()


#%%

#changes in split with number of iterations
import numpy as np
import matplotlib.pyplot as plt
import time
from colorCodeh import *


import copy


p=0.01
nmeas=1000
nsteps=20

plt.figure(2)
plt.clf()

plt.figure(3)
plt.clf()
for m in range(1,5):
        
    code=ColorCode(m,p)
    code.noise()
    code.syndrome()
    change=code.softresplitcoordinate(nsteps)
    
    
    for k in range(nmeas-1):
        
        code=ColorCode(m,p)
        code.noise()
        code.syndrome()
        change+=code.softresplitcoordinate(nsteps)
    
    change/=nmeas


    
    plt.figure(2)
    plt.plot(change,'p-', label=str(m))
    plt.figure(3)
    plt.plot(np.log(change),'p-', label=str(m))
    




plt.figure(2)
plt.title("Changes in p(split) with every step, p="+str(p))
plt.legend()
plt.figure(3)
plt.title("Changes in p(split) with every step,logscale")
plt.legend()






