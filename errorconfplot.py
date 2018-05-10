

import numpy as np
import matplotlib.pyplot as plt
import time
from colorCodeh import *

import copy



#plot all states

#plt.figure(0)
#plt.clf()

m=1
code=ColorCode(m,.05)
#code.noise()


er=[2,3]
for i in er:
    code.e[i]=1
code.syndrome()
codehard=copy.deepcopy(code)
codesoft=copy.deepcopy(code)


log,loger=code.hardDecoder(splitmethod=0,plotall=True,fignum=0)
#code.plot(splitting=True)
plt.title("init 0 "+str(loger))

#plt.figure(1)
#plt.clf()
log,loger=codehard.hardDecoder(splitmethod=1,plotall=True,fignum=6)
#codehard.plot(splitting=True)
plt.title("Hard "+str(loger))

#plt.figure(2)
#plt.clf()
log,loger=codesoft.hardDecoder(splitmethod=1,plotall=True,fignum=12)
#codesoft.plot(splitting=True)
plt.title("Soft "+str(loger))


