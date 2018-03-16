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

            
            
#%%


s=[]
#there are only 7 independent stabilizers
for i in range(7):
    s.append([])

s[0]=[0,4,5,12,13,17]
s[1]=[0,1,2,13,14,15  ]
s[2]=[2,3,4,15,16,17  ]
s[3]=[0,1,5,6,10,11  ]
s[4]=[1,2,3,6,7,8  ]
s[5]=[3,4,5,8,9,10  ]
s[6]=[6,7,11,12,16,17  ]


lop=[]
#there are 4 logical operators

#although i am not sure they are these
for i in range(4):
    lop.append([])
lop[0]=[0,1,3,4]
lop[1]=[3,8,14,15]
lop[2]=[6,7,9,10]
lop[3]=[0,1,7,12]


#we initialize the empty table
lut4=[]
listofsets=[]
for j in range(2**4):
    listofsets.append(set())
for i in range(2**9):
    lut4.append(list(listofsets))

def applyop(op,state):
    '''
    the operator op is a list of qubits affected,
    state is a string of 01101010, which is 
    going to be modified
    '''
    state2=''
    for i in range(len(state)):
        newq=int(state[i])
        if i in set(op):
            newq=(newq+1)%2
        state2+=str(newq)
    return state2

def applystabilizers(state,s):
    '''
    applies all possible combinations of the stabilizers
    and returns a set with the resultant states
    '''
    sol=set()
    #we have to cover the whole 2**7 combinations
    #print "starting with state "+state
    for i in range(2**7):
        
        #we find the combination of stabilizers
        comb=bin(i)[2:]
        comb='0'*(7-len(comb))+comb
        
        #initializate a state
        news=state
        #print comb
        for j in range(7):
            #and apply the correspondent stab. of that combiantion
            if comb[j]=="1":
                #print s[j]
                news=applyop(s[j],news)
        #print news+"  from "+state
        sol.add(news)
    #print sol
    assert len(sol)==2**7, "we should have 2**7 different states, we have: "+str(len(sol))
    return sol

      

'''
now we go through all positions in the first table
for each, we take one of the error configurations
and we apply the full set of stabilizers to generate
the first set of the 2**4 in lut4.
Then, we apply one combination of logical operators
to generate the starting point of the next set
and then apply again the full set of stabilizers
'''

    
start=time.time()
for i in range(len(lut)):
    #we start with one random choice from the previous table
    if len(lut[i])>0:
            
        state=lut[i].pop()
        #for each position, we find all combinations of L. operators
        for j in range(2**4):
            #we find the combination of Log. Ops.
            comb=bin(j)[2:]
            comb='0'*(4-len(comb))+comb
            if i==0:
                print comb
            newstate=state
            for z in range(4):
                if comb[z]=="1":
                    #print lop[z]
                    newstate=applyop(lop[z],newstate)
            if i==0:
                print newstate
            lut4[i][j]=applystabilizers(newstate,s)

        
print "Computation time for the second method/s:", time.time()-start
datafile="lookuptable18q4lop"
np.save(datafile,lut4)











            
            