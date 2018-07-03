#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 01:00:32 2018

@author: pedro
"""


import numpy as np
import matplotlib.pyplot as plt
import time
from colorCodeh import *

import copy

#important values

p=0.05
q=1.-p

ps=0.5
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

code=ColorCode(0,p)

prob=code.singlesoftresplit(1)

print "theory",psu
print "program", prob






















