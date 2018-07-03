
import numpy as np
import matplotlib.pyplot as plt
import time
from colorCodeh import *

import copy



#plot all states

#plt.figure(0)
#plt.clf()

m=1
code=ColorCode(m,.01)
#code.noise()


log=0
attempts =0
while log == 0 and attempts <150:
    attempts+=1
    m=1
    code=ColorCode(m,.01)
    er=[0,19,39] # init 0 with corners
    #er=[40,41,64] #method 3
    #er=[7, 18, 43]#method 0
    #er=[1, 27, 61]#method 3
    #er=[0,3,4]#method 4
    #er=[0,13]#method 2 no corners
    er=[0,15]#method 2 corners
    #er=[0,4,7]#method 0 corners
    #er=[3,38]
    for i in er:
        code.e[i]=1
    code.syndrome()        
    log,loger=code.hardDecoder(splitmethod=2,cornerupdate=True,plotall=True,fignum=0,beta=10)
    #code.plot(splitting=True)
    print log, loger
    #if sum(code.c)>2:
    #    log=1
plt.title("Errors: "+str(loger))

#plt.figure(1)
#plt.clf()
#log,loger=codehard.hardDecoder(splitmethod=1,plotall=True,fignum=6)
#codehard.plot(splitting=True)
#plt.title("Hard "+str(loger))

#plt.figure(2)
#plt.clf()
#log,loger=codesoft.hardDecoder(splitmethod=1,plotall=True,fignum=12)
#codesoft.plot(splitting=True)
#plt.title("Soft "+str(loger))


