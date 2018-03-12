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

plt.clf()

nq=32
m=.5*np.log2(nq*1./18.)
code=ColorCode(m,.05)
code.noise()
code.syndrome()
code.plot(splitting=True)
