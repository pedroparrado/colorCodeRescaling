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


import numpy as np
import matplotlib.pyplot as plt
import time
from colorCodeh import *

import copy

import copy
nsteps=15
nmeas=100


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
Ep3=np.zeros(nsteps)
Ep4=np.zeros(nsteps)
Emin=np.zeros(nmeas)

count1=np.zeros(nsteps)
count2=np.zeros(nsteps)
count3=np.zeros(nsteps)
count4=np.zeros(nsteps)
count5=np.zeros(nsteps)
count6=np.zeros(nsteps)

de1=np.zeros(nsteps)
de2=np.zeros(nsteps)
de3=np.zeros(nsteps)
de4=np.zeros(nsteps)
de5=np.zeros(nsteps)
de6=np.zeros(nsteps)




for j in range(nmeas):
    code=ColorCode(m,.05)
    code.noise()
    code.syndrome()
    code2=copy.deepcopy(code)
    code3=copy.deepcopy(code)
    codep=copy.deepcopy(code)
    codep2=copy.deepcopy(code)
    codep3=copy.deepcopy(code)
    codep4=copy.deepcopy(code)
    codemin=copy.deepcopy(code)
    changes=np.zeros(nsteps)

    Emin[j],fs=codemin.fullsplittester()    
        
    #initial condition
    for i in range(len(code3.split)):
        code3.split[i]=0
        codep3.sp[i]=0.75
        if codemin.split[i]==0:
            codep4.sp[i]=.2
            codep4.split[i]=0
        else:
            codep4.sp[i]=.8
            codep4.split[i]=1
    
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
        de1[i]+=code.energy()/Emin[j]/nmeas
            
        if code.energy()==Emin[j]:
            count1[i]+=1./nmeas
        
    changes2=np.zeros(nsteps)  
    #different initialization
    changes3=np.zeros(nsteps)    
    for i in range(nsteps):
        changes3[i],T=code3.resplit()
        E3[i]+=code3.energy()        
        de3[i]+=code3.energy()/Emin[j]/nmeas
        changes2[i],T=code2.resplit()
        E2[i]+=code2.energy()
        de2[i]+=code2.energy()/Emin[j]/nmeas
        if code2.energy()==Emin[j]:
            count2[i]+=1./nmeas
        if code3.energy()==Emin[j]:
            count3[i]+=1./nmeas
        
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
        de4[i]+=codep.energy()/Emin[j]/nmeas
        
        if codep.energy()==Emin[j]:
            count4[i]+=1./nmeas
        
    
        
    changesp2=np.zeros(nsteps)    
    for i in range(nsteps):
        changesp2[i],T=codep2.softresplit()
        Ep2[i]+=codep2.energy()
        de5[i]+=codep2.energy()/Emin[j]/nmeas
        if codep2.energy()==Emin[j]:
            count5[i]+=1./nmeas
    changesp3=np.zeros(nsteps)    
    for i in range(nsteps):
        c,T=codep3.softresplit()
        Ep3[i]+=codep3.energy()
        if i>0:
            c,T=codep4.softresplit()
        Ep4[i]+=codep4.energy()
        de6[i]+=codep3.energy()/Emin[j]/nmeas
        if codep3.energy()==Emin[j]:
            count6[i]+=1./nmeas
    
    chp+=changesp*1./T
    chp2+=changesp2*1./T 
    
    
  
    

ch=ch/nmeas
ch2=ch2/nmeas
ch3=ch3/nmeas
E=E/nmeas
E2=E2/nmeas
E3=E3/nmeas
Ep4=Ep4/nmeas
chp=chp/nmeas
chp2=chp2/nmeas
Ep=Ep/nmeas
Ep2=Ep2/nmeas
Ep3=Ep3/nmeas
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
plt.plot(Ep3,'d-',label="Soft init0")
plt.plot(Ep4,'p-',label="Init at min")



plt.title("Energy after the splittings")
minen=np.mean(Emin)
plt.plot(range(nsteps),np.zeros(nsteps)+minen,'-.', label='Min Energy')
plt.legend()


plt.figure(2)
plt.clf()
plt.plot(count2,'p-',label="Randomized")
plt.plot(count3,'p-',label="Init at 0")
plt.plot(count1,'p-',label="Paralellized")


plt.plot(count5,'d-',label="Soft Randomized")
plt.plot(count4,'d-',label="Soft Paralellized")
plt.plot(count6,'d-',label="Soft init0")



plt.title("Percentage of cases with optimal solution")
plt.legend()

plt.figure(1)
plt.clf()
plt.plot(de2-1,'p-',label="Randomized")
plt.plot(de3-1,'p-',label="Init at 0")
plt.plot(de1-1,'p-',label="Paralellized")


plt.plot(de5-1,'d-',label="Soft Randomized")
plt.plot(de4-1,'d-',label="Soft Paralellized")
plt.plot(de6-1,'d-',label="Soft init0")



plt.title("Energy difference")
plt.legend()


#%%

#dependance with P error


import numpy as np
import matplotlib.pyplot as plt
import time
from colorCodeh import *

import copy

import copy
nsteps=15
nmeas=10000
nps=60
p1=0.01
p2=0.09
P=np.linspace(p1,p2,nps)

nq=32
m=.5*np.log2(nq*1./18.)
E=np.zeros(nps)
E2=np.zeros(nps)
E3=np.zeros(nps)
Ep=np.zeros(nps)
Ep2=np.zeros(nps)
Ep3=np.zeros(nps)
Ep4=np.zeros(nps)
Em=np.zeros(nps)
Emin=np.zeros(nmeas)

count1=np.zeros(nps)
count2=np.zeros(nps)
count3=np.zeros(nps)
count4=np.zeros(nps)
count5=np.zeros(nps)
count6=np.zeros(nps)
count7=np.zeros(nps)

de1=np.zeros(nps)
de2=np.zeros(nps)
de3=np.zeros(nps)
de4=np.zeros(nps)
de5=np.zeros(nps)
de6=np.zeros(nps)
de7=np.zeros(nps)



startime=time.time()

for j in range(nmeas):
    for k in range(nps):
        p=P[k]
        code=ColorCode(m,p)
        code.noise()
        code.syndrome()
        code2=copy.deepcopy(code)
        code3=copy.deepcopy(code)
        codep=copy.deepcopy(code)
        codep2=copy.deepcopy(code)
        codep3=copy.deepcopy(code)
        codep4=copy.deepcopy(code)
        codemin=copy.deepcopy(code)
    
        Emin[j],fs=codemin.fullsplittester() 
        Em[k]+=codemin.energy()   
            
        #initial condition
        for i in range(len(code3.split)):
            code3.split[i]=0
            codep3.sp[i]=0.75
            if codemin.split[i]==0:
                codep4.sp[i]=.2
                codep4.split[i]=0
            else:
                codep4.sp[i]=.8
                codep4.split[i]=1
        #hard splitter parallelized
        for i in range(nsteps):
            c,t=code.resplit(1)
            c,t=code.resplit(2)
            c,t=code.resplit(0)
        E[k]+=code.energy()
        de1[k]+=code.energy()/Emin[j]/nmeas
            
        if code.energy()==Emin[j]:
            count1[k]+=1./nmeas
            
        #different initialization
        for i in range(nsteps):
            c,T=code3.resplit()
            c,T=code2.resplit()
            
        E3[k]+=code3.energy()        
        de3[k]+=code3.energy()/Emin[j]/nmeas
        E2[k]+=code2.energy()
        de2[k]+=code2.energy()/Emin[j]/nmeas
        if code2.energy()==Emin[j]:
            count2[k]+=1./nmeas
        if code3.energy()==Emin[j]:
            count3[k]+=1./nmeas
                   
        
        
        #soft respliting
        #parallelized
        for i in range(nsteps):
            c,t=codep.softresplit(1)
            c,t=codep.softresplit(2)
            c,t=codep.softresplit(0)
        Ep[k]+=codep.energy()
        de4[k]+=codep.energy()/Emin[j]/nmeas
        
        if codep.energy()==Emin[j]:
            count4[k]+=1./nmeas
            
        
        #randomized
        changesp2=np.zeros(nsteps)    
        for i in range(nsteps):
            c,T=codep2.softresplit()
        Ep2[k]+=codep2.energy()
        de5[k]+=codep2.energy()/Emin[j]/nmeas
        if codep2.energy()==Emin[j]:
            count5[k]+=1./nmeas
            
        #different initial conditions
        for i in range(nsteps):
            c,T=codep3.softresplit()
            c,T=codep4.softresplit()
        Ep3[k]+=codep3.energy()
        Ep4[k]+=codep4.energy()
        de6[k]+=codep3.energy()/Emin[j]/nmeas
        de7[k]+=codep4.energy()/Emin[j]/nmeas
        if codep3.energy()==Emin[j]:
            count6[k]+=1./nmeas
        if codep4.energy()==Emin[j]:
            count7[k]+=1./nmeas
    

    if j%10==0:
        dt=time.time()-startime
        currentstep=1.*(j+1.)/nmeas
        print "Iteration "+str(j+1)+", "+str(currentstep)+"% completed"
        print "Time spent: "+str(dt/60.)+"min, "+str(dt/3600.)+"h"
        dt=dt*(1./currentstep)
        timestimates.append(dt)
        print "Total time: "+str(dt/60.)+"min, "+str(dt/3600.)+"h"
        dt=dt*(1.-currentstep)
        print "Time to finish: "+str(dt/60.)+"min, "+str(dt/3600.)+"h"
        print "---------------------------------------------------------"
    
  
    

E=E/nmeas
E2=E2/nmeas
E3=E3/nmeas
Ep4=Ep4/nmeas
Ep=Ep/nmeas
Ep2=Ep2/nmeas
Ep3=Ep3/nmeas
Em=Em/nmeas


plt.figure(5)
plt.clf()
plt.plot(P,E2,'p-',label="Randomized")
plt.plot(P,E3,'p-',label="Init at 0")
plt.plot(P,E,'p-',label="Paralellized")


plt.plot(P,Ep2,'d-',label="Soft Randomized")
plt.plot(P,Ep,'d-',label="Soft Paralellized")
plt.plot(P,Ep3,'d-',label="Soft init0")
plt.plot(P,Ep4,'p-',label="Init at min")
plt.plot(P,Em,'-.',label="Min Energy")

plt.xlabel("Error probability per qubit")
plt.title("Energy after the splittings")
plt.legend()


plt.figure(2)
plt.clf()
plt.plot(P,count2,'p-',label="Randomized")
plt.plot(P,count3,'p-',label="Init at 0")
plt.plot(P,count1,'p-',label="Paralellized")


plt.plot(P,count5,'d-',label="Soft Randomized")
plt.plot(P,count4,'d-',label="Soft Paralellized")
plt.plot(P,count6,'d-',label="Soft init0")
plt.plot(P,count7,'d-',label="Soft init min")


plt.xlabel("Error probability per qubit")

plt.title("Percentage of cases with optimal solution")
plt.legend()

plt.figure(1)
plt.clf()
plt.plot(P,de2-1,'p-',label="Randomized")
plt.plot(P,de3-1,'p-',label="Init at 0")
plt.plot(P,de1-1,'p-',label="Paralellized")


plt.plot(P,de5-1,'d-',label="Soft Randomized")
plt.plot(P,de4-1,'d-',label="Soft Paralellized")
plt.plot(P,de6-1,'d-',label="Soft init0")

plt.plot(P,de7-1,'d-',label="Soft init min")

plt.xlabel("Error probability per qubit")


plt.title("Energy difference")
plt.legend()



