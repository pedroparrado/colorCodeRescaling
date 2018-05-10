#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 13:03:29 2018

@author: pedro
"""

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


nsteps=15
nmeas=5000
nps=20
p1=0.001
p2=0.09
P=np.linspace(p1,p2,nps)

nq=32
m=.5*np.log2(nq*1./18.)
Emin=np.zeros(nmeas)

Em=np.zeros(nps)

startime=time.time()


filen="./results/toyerrors1.txt"
f1=open(filen,"w")    
filen="./results/toyerrors2.txt"
f2=open(filen,"w")    
filen="./results/toyerrors3.txt"
f3=open(filen,"w")    
for j in range(nmeas):
    for k in range(nps):
        p=P[k]
        code=ColorCode(m,p)
        code.noise()
        code.syndrome()
        code2=copy.deepcopy(code)
        code3=copy.deepcopy(code)
        codemin=copy.deepcopy(code)
    
        Emin[j],fs=codemin.fullsplittester() 
        Em[k]+=codemin.energy()   
            
        #initial condition
        for i in range(len(code.split)):
            code.split[i]=0
            code2.split[i]=np.random.randint(0,2)
            code3.sp[i]=0.5
            
        #different initialization
        for i in range(nsteps):
            c,T=code.resplit()
            c,T=code2.resplit()
            c,T=code3.softresplit()
            
        if code.energy()==Emin[j]:
            f1.write(str(code.e))
        if code2.energy()==Emin[j]:
            f2.write(str(code2.e))
        if code3.energy()==Emin[j]:
            f3.write(str(code3.e))       
    
f1.close()
f2.close()
f3.close()



