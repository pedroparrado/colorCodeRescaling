#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 14:20:59 2018

@author: pedro
"""

import numpy as np
import time

start=time.time()
#the lookuptable is a list of sets, one per syndrome
#each set has the combinations of errors that trigger it
#for example, 00010010100 would mean errors in the
#qubits 3, 6 and 8


lut=[]
for i in range(2**9):
    lut.append(set())
    
    
#stabilizers correspondent to each qubit
sq=[
    [  0 , 1  , 3  ],
    [  4 , 1  , 3  ],
    [  4 , 1  , 2  ],
    [  4 , 5  , 2  ],
    [  0 , 5  , 2  ],
    [  0 , 5  , 3  ],
    [  4 , 6  , 3  ],
    [  4 , 6  , 7  ],
    [  4 , 5  , 7  ],
    [  8 , 5  , 7  ],
    [  8 , 5  , 3  ],
    [  8 , 6  , 3  ],
    [  0 , 6  , 7  ],
    [  0 , 1  , 7  ],
    [  8 , 1  , 7  ],
    [  8 , 1  , 2  ],
    [  8 , 6  , 2  ],
    [  0 , 6  , 2  ],   
    ]

    
#now, to generate the lookuptable, we examinate every single possible 
#error distribution, and add them to the correspondent set in lut

for i in range(2**18):
    er=bin(i)[2:]
    er='0'*(18-len(er))+er
    
    syn=[0]*9
    
    for j in range(len(er)):
        if er[j]=='1':
            for s in sq[j]:
                syn[s]=(syn[s]+1)%2
    synb=''
    for j in syn:
        synb+=str(j)
    index=int(synb,2)
    
    lut[index].add(er)
        
print "Computation time/s:", time.time()-start
datafile="lookuptable18"
np.save(datafile,lut)

            
            
            
            