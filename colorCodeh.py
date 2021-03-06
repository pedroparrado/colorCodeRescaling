#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 17:17:54 2018

@author: pedro
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import math

#lookuptable for a 18 qubit basic code
lut18=np.load("lookuptable18.npy")
lut18lop=np.load("lookuptable18q4lop.npy")


#lookup table for a 4 qubit cell
lookuptable4=[]                               #s0s1s2
lookuptable4.append([    [0,0,0,0],[1,0,1,1]  ])#000
lookuptable4.append([    [1,1,0,0],[0,1,1,1]  ])#001
lookuptable4.append([    [0,1,1,0],[1,1,0,1]  ])#010
lookuptable4.append([    [0,0,0,1],[1,0,1,0]  ])#011
lookuptable4.append([    [0,1,0,1],[1,1,1,0]  ])#100
lookuptable4.append([    [0,0,1,0],[1,0,0,1]  ])#101
lookuptable4.append([    [1,0,0,0],[0,0,1,1]  ])#110
lookuptable4.append([    [0,1,0,0],[1,1,1,1]  ])#111

def lut4(s0,s1,s2):
    global lookuptable4
    ind=s2+2*s1+4*s0#binary
    return lookuptable4[ind]


class Cell:
    def __init__(self,i,L):
        
        x0=[0,0,1,0]
        y0=[0,0,0,1]
        z0=[0,1,0,0]
        x1=[1,1,0,1]
        y1=[1,1,1,0]
        z1=[1,0,1,1]
        self.i=i
        x=(i%L-i%2)#*2
        y=2*(i/L)#*2
        z=i%2
        self.x=x
        self.y=y

        self.z=z
        
        #probability of error of the cell after renormalization
        self.pe=0.5#random initial value
        
        #indexes of the qubits  in the cell
        self.q=[]
        for j in range(len(x0)):
            if z==0:
                xq=(x+x0[j])#%(L/2)
                yq=(y+y0[j])#%(L/2)
                zq=z0[j]
                indq=2*xq+2*L*yq+zq
                self.q.append(indq)
            if z==1:
                xq=(x+x1[j])#%(L/2)
                yq=(y+y1[j])#%(L/2)
                zq=z1[j]
                indq=2*xq+2*L*yq+zq
                self.q.append(indq)
        self.qp=np.zeros(4)
        self.corr=np.zeros(4)
        
        
        #indexes of the syndromes of the boundaries
        self.s=[]
        x0=[1,0,1]
        y0=[0,1,1]
        x1=[1,2,1]
        y1=[2,1,1]
        
        for j in range(len(x0)):
            if z==0:
                xq=(x+x0[j])%(L)
                yq=(y+y0[j])%(L)
                indq=xq+L*yq
                self.s.append(indq)
            if z==1:
                xq=(x+x1[j])%(L)
                yq=(y+y1[j])%(L)
                indq=xq+L*yq
                self.s.append(indq)
                

class ColorCode:
    def __init__(self, m,p=.1):
        self.m=m
        #number of qubits
        self.N=18*2**(2*m)
        if type(self.N!=int):
            #print "System size: ",self.N,int(self.N)
            self.N=int(self.N)
        #probability of error of each qubit
        self.p=[p]*self.N #initialized all equal
        #state of error
        self.e=[0]*self.N
        #correction
        self.c=[0]*self.N
        
        L=int(np.sqrt(self.N/2))
        self.L=L
        #syndromes (starts at 0)
        self.s=[0]*(L**2)
        #splittings index(1 or 0)
        self.split=[0]*(L**2)
        #table of splitting values
        self.spt=[[[0,0],[1,1]],[[1,0],[0,1]]]
        #spt[syndrome value][split value][qubit.z]
        
        #initial splitting
        for i in range(L**2):
            self.split[i]=np.random.randint(0,2)
        
        
        #cells
        self.cells=[]
        ncells=self.N/4
        if m>0:
            for i in range(ncells):
                self.cells.append(Cell(i,L))
        
        
        #probability of each splitting (for soft splitting)
        self.sp=np.zeros(L**2)+.5
        
        
        #list of syndromes in the boundaries of the cells
        
        self.s0s=[]
        self.s1s=[]
        self.s2s=[]
        for i in range(L**2):
            x=i%L
            y=i/L
            if (x%2==1 and y%2==0):
                self.s0s.append(i)
            if (x%2==0 and y%2==1):
                self.s1s.append(i)
            if (x%2==1 and y%2==1):
                self.s2s.append(i)
            
        #logical operators
        self.logic=[]
        
        redhorizontal=[]
        bluehorizontal=[]
        for i in range(self.L*2):
            if i%3!=2:
                redhorizontal.append(i)
                bluehorizontal.append(i+4*self.L)
        redvertical=[]
        bluevertical=[]
        verticallist=[]
        for i in range(self.L):
            ind=2*self.L*i
            verticallist.append(ind)
            verticallist.append(ind+1)
        assert len(verticallist)==2*self.L, "The list is incomplete"
        for i in range(len(verticallist)):
            if i%3!=2:
                redvertical.append(verticallist[i])
                bluevertical.append(verticallist[i]+2)
        self.logic.append(redhorizontal)
        self.logic.append(bluehorizontal)
        self.logic.append(redvertical)
        self.logic.append(bluevertical)    
        
        
        #tables of soft rescaling
        self.psoft=[]
        self.ssoft=[]
        
        
        if m>0:
            self.newcode=ColorCode(max(m-1,0),0.)
        
        
    def checkLogError(self):
        loger=[0,0,0,0]
        for j in range(len(self.logic)):
            for i in self.logic[j]:
                loger[j]+=self.e[i]
                loger[j]+=self.c[i]
            loger[j]=loger[j]%2
        finalres=min(1,sum(loger))
        return finalres,loger
                
        
        
    def noise(self):
        #generates errors in the qubits
        for i in range(self.N):
            r=np.random.rand()
            if r<self.p[i]:
                self.e[i]=1
    def syndrome(self,withc=False):
        #coordinates of the neighbors
        nx=[0,-1,-1,-1, 0, 0]
        ny=[0, 0, 0,-1,-1,-1]
        nz=[0, 0, 1, 1, 1, 0]
        L=self.L
        for i in range(len(self.s)):
            xs=i%L
            ys=i/L
            val=0
            for j in range(len(nx)):
                x=(xs+nx[j])%L
                y=(ys+ny[j])%L
                z=nz[j]
                iq=x*2+y*2*L+z
                val+=self.e[iq]
                if withc:
                    val+=self.c[iq]
            self.s[i]=val%2
    def stabilizerneighbors(self,i):
        #coordinates of the neighbors
        nx=[0,-1,-1,-1, 0, 0]
        ny=[0, 0, 0,-1,-1,-1]
        nz=[0, 0, 1, 1, 1, 0]
        L=self.L
        sol=[]
        
        xs=i%L
        ys=i/L
        for j in range(len(nx)):
            x=(xs+nx[j])%L
            y=(ys+ny[j])%L
            z=nz[j]
            iq=x*2+y*2*L+z
            sol.append(iq)
        return sol
    
    def cornerpe(self,cind,normal):
        #computes pe for every qubit involved in this corner stabilizer
        #and updates the corner probabilities
        
        qubits=self.stabilizerneighbors(cind)
        pes=np.zeros(6)
        s=self.s[cind]
        for qubitind in range(6):
            qubit=qubits[qubitind]
            externals=set(qubits)
            externals.remove(qubit)
            pe=(-1.)**s*.5
            for q in externals:
                pe*=(1.-2.*self.p[q])
            pe=.5-pe
            pes[qubitind]=pe
            if not normal:
                pes[qubitind]=0.9+.2*s
        
        #now we update the 
        for qubitind in range(6):
            qubit=qubits[qubitind]
            pi=self.p[qubit]
            pe=pes[qubitind]
            if normal:
                self.p[qubit]=pi*pe/(pi*pe+(1.-pi)*(1.-pe))
            else:
                self.p[qubit]=pi*pe
        return
    def updateCornerP(self,normal=True):
        #updates the probability of error of the corner qubits
        L=self.L
        #we explore all the stabilizers
        for i in range(len(self.s)):
            #and we update the values of the qubits
            xs=i%L
            ys=i/L
            #only for the corner stabilizers
            if (xs%2==0 and ys%2==0):
                self.cornerpe(i,normal)
        return
        
    #utility: find neighboring cells of a syndrome:
    def neighboringcells(self,synind):
        
        L=self.L        
        #first, we compute the coordinates of the syndrome
        x=synind%L        
        y=synind/L
        
        #now we compute if it is an horizontal, vertical or diagonal splitting
        assert x%2!=0 or y%2!=0, "corner syndrome"
        if x%2==1 and y%2==0:
            #coordinates of the cells
            xu=x-1
            yu=y
            xd=x-1
            yd=(y-2)%L
            
        if x%2==0 and y%2==1:
            #coordinates of the cells
            xu=x
            yu=y-1
            xd=(x-2)%L
            yd=(y-1)%L
            
        if x%2==1 and y%2==1:
            #coordinates of the cells
            xu=x-1
            yu=y-1
            xd=x-1
            yd=y-1
            
        #index of the neighboring cells    
        
        icu=xu+L*yu/2  #cell  up  always has z=0
        icd=xd+L*yd/2+1#cell down always has z=1
        return icu,icd
    
            
    def resplit(self,l=3):
        if l==0:
            sptoupdate=self.s0s
        if l==1:
            sptoupdate=self.s1s
        if l==2:
            sptoupdate=self.s2s
        if l>2:
            sptoupdate=self.s0s+self.s1s+self.s2s
        nchanges=0
        #random updates
        if l==3:
            for i in range(len(sptoupdate)):
                s=sptoupdate[np.random.randint(0,len(sptoupdate))]
                prob=self.ps(s)
                old=self.split[s]
                '''
                #CHECK ENERGY
                E1=self.energy()
                #CHECK ENERGY
                '''
                if prob<0.5:
                    self.split[s]=1
                if prob>0.5:
                    self.split[s]=0
                if prob>0.499 and prob <0.501:
                #if prob==0.5:
                    self.split[s]=np.random.randint(0,2)
                if self.split[s]!=old:
                    nchanges+=1
                '''   
                #CHECK ENERGY
                E2=self.energy()
                assert E2<=E1+1e-7, "Bad step in hard split r, "+str(s)+", prob:"+str(prob)+"\n"+   \
                    "From "+str(old)+" to "+str(self.split[s])+"\n"+    \
                    "From "+str(E1)+" to "+str(E2)+"\n"+    \
                    str(plt.figure(10))+str(plt.clf())+self.plot(splitting=True,indexs=True)
                #CHECK ENERGY
                ''' 
                    
            return nchanges, len(sptoupdate)

        #ordered updates               
        for s in sptoupdate:
            prob=self.ps(s)
            old=self.split[s]
            '''
            #CHECK ENERGY
            E1=self.energy()
            #CHECK ENERGY
            '''
            if prob<0.5:
                self.split[s]=1
            if prob>0.5:
                self.split[s]=0
            #if prob==0.5:
            if prob>0.499 and prob <0.501:
                self.split[s]=np.random.randint(0,2)
            if self.split[s]!=old:
                nchanges+=1
            
            '''
            #CHECK ENERGY
            E2=self.energy()
            assert E2<=E1+1e-7, "Bad step in hard split s, "+str(s)+", prob:"+str(prob)+"\n"+        \
                    "From "+str(old)+" to "+str(self.split[s])+"\n"+    \
                    "From "+str(E1)+" to "+str(E2)+"\n"+    \
                    str(plt.figure(10))+str(plt.clf())+self.plot(splitting=True,indexs=True)
            #CHECK ENERGY
            '''
        return nchanges, len(sptoupdate)
            
            
    def heatresplit(self,beta=100.):
        nchanges=0
        sptoupdate=self.s0s+self.s1s+self.s2s
        #random updates
        for i in range(len(sptoupdate)):
            s=sptoupdate[np.random.randint(0,len(sptoupdate))]
            prob=self.ps(s)
            old=self.split[s]
            
            if old==0:
                #if prob<0.5, we change it:
                if prob<0.5:
                    self.split[s]=1
                    nchanges+=1
                else:
                    r=np.random.rand()
                    pacc=np.log(prob/(1.-prob))
                    pacc=np.exp(-beta*pacc)
                    assert pacc<=1 and pacc>=0, "acceptance probability wrong"
                    if r<pacc:
                        self.split[s]=1
                        nchanges+=1
            else:
                #if prob<0.5, we change it:
                if prob>0.5:
                    self.split[s]=0
                    nchanges+=1
                else:
                    r=np.random.rand()
                    pacc=np.log((1.-prob)/prob)
                    pacc=np.exp(-beta*pacc)
                    assert pacc<=1 and pacc>=0, "acceptance probability wrong"
                    if r<pacc:
                        self.split[s]=0
                        nchanges+=1           
                
                
        return nchanges, len(sptoupdate)

    def randomminsplit(self,nsteps=20):
        
        sptoupdate=self.s0s+self.s1s+self.s2s
        
        minenergy=1e9
        minsetup=np.array(self.split)
        minstep=0
        
        for k in range(nsteps):
                
            #random updates
            for i in range(len(sptoupdate)):
                s=sptoupdate[np.random.randint(0,len(sptoupdate))]
                prob=self.ps(s)
                #old=self.split[s]            
                r=np.random.rand()
                if r<prob:
                    self.split[s]=0
                else:
                    self.split[s]=1
            energy=self.energy()
            if energy<minenergy:
                minsetup=np.array(self.split)
                minstep=k
                minenergy=energy
        
        self.split=minsetup            
                
                
        return minstep

            
    def softresplit(self,l=3):
        #print "Entering Softresplit"
        if l==0:
            sptoupdate=self.s0s
        if l==1:
            sptoupdate=self.s1s
        if l==2:
            sptoupdate=self.s2s
        if l>2:
            sptoupdate=self.s0s+self.s1s+self.s2s
        nchanges=0
        #random updates
        if l==3:
            for i in range(len(sptoupdate)):
                s=sptoupdate[np.random.randint(0,len(sptoupdate))]
                self.sp[s]=self.pupdate(s)#splitprobability
                prob=self.sp[s]
                old=self.split[s]
                '''
                #CHECK ENERGY
                E1=self.energy()
                #CHECK ENERGY
                '''
                if prob>0.5:
                    self.split[s]=1
                if prob<0.5:
                    self.split[s]=0
                #if prob==0.5:
                if prob>0.499 and prob <0.501:
                    self.split[s]=np.random.randint(0,2)
                if self.split[s]!=old:
                    nchanges+=1
                '''    
                #CHECK ENERGY
                E2=self.energy()
                assert E2<=E1+1e-7, "Bad step in soft split r, "+str(s)+"\n"+\
                    "From "+str(old)+" to "+str(self.split[s])+"\n"+\
                    "From "+str(E1)+" to "+str(E2)+"\n"+    \
                    str(plt.figure(10))+str(plt.clf())+self.plot(splitting=True,indexs=True)
                #CHECK ENERGY
                '''
            return nchanges, len(sptoupdate)

        #ordered updates               
        for s in sptoupdate:
            self.sp[s]=self.pupdate(s)#splitprobability
            prob=self.sp[s]
            old=self.split[s]
            '''
            #CHECK ENERGY
            E1=self.energy()
            #CHECK ENERGY
            '''
            if prob>0.5:
                self.split[s]=0
            if prob<0.5:
                self.split[s]=1
            #if prob==0.5:
            if prob>0.499 and prob <0.501:
                self.split[s]=np.random.randint(0,2)
            if self.split[s]!=old:
                nchanges+=1
            '''
            #CHECK ENERGY
            E2=self.energy()
            assert E2<=E1+1e-7, "Bad step in soft split s,"+str(s)+"\n"+\
                    "From "+str(old)+" to "+str(self.split[s])+"\n"+\
                    "From "+str(E1)+" to "+str(E2)+"\n"+    \
                    str(plt.figure(10))+str(plt.clf())+self.plot(splitting=True,indexs=True)
            #CHECK ENERGY
            '''
        return nchanges, len(sptoupdate)   
    
    
    
    
    def softresplitcoordinate(self, nsteps=8,meanvalue=True,double=2):
        #print "Entering Softresplit coordinate"
        
        #setting up the initial values
        
        sptoupdate=self.s0s+self.s1s+self.s2s
        for s in sptoupdate:
            icu,icd=self.neighboringcells(s)
            #we check the qubits in the "support" of the stabilizer
            if s in set(self.s0s):
                ind1,ind2,ind3=0,1,2
            if s in set(self.s1s):
                ind1,ind2,ind3=0,1,3
            if s in set(self.s2s):
                ind1,ind2,ind3=1,2,3           
            #upper cell
            p1=self.p[self.cells[icu].q[ind1]]
            p2=self.p[self.cells[icu].q[ind2]]
            p3=self.p[self.cells[icu].q[ind3]]
            q1=1.-p1
            q2=1.-p2
            q3=1.-p3
            pu=p1*q2*q3+q1*p2*q3+q1*q2*p3+p1*p2*p3
            qu=1.-pu
            #lower cell
            p1=self.p[self.cells[icd].q[ind1]]
            p2=self.p[self.cells[icd].q[ind2]]
            p3=self.p[self.cells[icd].q[ind3]]
            q1=1.-p1
            q2=1.-p2
            q3=1.-p3
            pl=p1*q2*q3+q1*p2*q3+q1*q2*p3+p1*p2*p3
            ql=1.-pl
            
            #now, we compute the initial probability of 
            #the splitting according to the syndrome
            if self.s[s]==0:
                self.sp[s]=qu*ql/(qu*ql+pu*pl)
            if self.s[s]==1:
                self.sp[s]=pu*ql/(pu*ql+pu*ql)
            
        
        
        #soft splitting procedure
        
        pchanges=np.zeros(nsteps)
        maxchanges=np.zeros(nsteps)
        spcopy= np.array(self.sp)
        if double>1:                
            pchanges=np.zeros(nsteps*double)
            maxchanges=np.zeros(nsteps*double)
        for kd in range(double):
                
            for k in range(nsteps):
                spcopy= np.array(self.sp)
                #ordered updates  
                maxnow=0.             
                for s in sptoupdate:
                    spcopy[s]=self.pupdate(s)#splitprobability
                    change=np.abs(spcopy[s]-self.sp[s])
                    pchanges[k+kd*nsteps]+=change
                    if change>maxnow:
                        maxnow=change
                    
                    if meanvalue and k==(nsteps-1):
                        spcopy[s]=(spcopy[s]+self.sp[s])/2.
                
                for s in sptoupdate:
                    self.sp[s]=spcopy[s] 
                
                maxchanges[k+kd*nsteps]=maxnow
        
        '''
        if double is active, we repeat the whole splitting update
        '''
            
            
        #splitting assignment                
        for s in sptoupdate:
            self.sp[s]=spcopy[s]
            prob=spcopy[s]
            if prob>0.5:
                self.split[s]=0
            if prob<0.5:
                self.split[s]=1
            #if prob==0.5:
            if prob>0.499 and prob <0.501:
                self.split[s]=np.random.randint(0,2)
            
        return pchanges,maxchanges  
    
    
    def singlesoftresplit(self,s):
        
        self.sp[s]=self.pupdate(s)#splitprobability
        prob=self.sp[s]
        
        if prob>0.5:
            self.split[s]=1
        if prob<0.5:
            self.split[s]=0
        #if prob==0.5:
        if prob>0.499 and prob <0.501:
            self.split[s]=np.random.randint(0,2)
            
        return prob

    def energy(self,info=False):
        E=0.
        for i in range(len(self.cells)):
            #indexes of the syndromes
            s=self.cells[i].s
            s0=self.spt[self.s[s[0]]][self.split[s[0]]][i%2]
            s1=self.spt[self.s[s[1]]][self.split[s[1]]][i%2]
            s2=self.spt[self.s[s[2]]][self.split[s[2]]][i%2]
            if info:
                print " "
                print "Cell ",i
                print s
                print s0,s1,s2
                print self.p3(self.cells[i],s0,s1,s2)
            E-=np.log(self.p3(self.cells[i],s0,s1,s2))
        return E/self.N
    
    def entropyofp(self):
        S=0.
        splits=self.s0s+self.s1s+self.s2s
        for i in splits:
            S+=-np.log(self.sp[i])*self.sp[i]
            
        return S/len(splits)
    def helpsplitmethods(self):
        print "splitmethods:"
        print "0 init0 hard splitting"
        print "1 randomized start hard splitting"
        print "2 soft splitting"
        print "3 init0 hard splitting twice: first without cornerupdate, then with corner update"
        print "4 init0 heatsplit"
        print "5 hard decoder random choice"
        print "6 soft decoder coordinate"
        
    def cellCorrectionAndRescaleProb(self,softRescProb=True, plotall=False):
        
        
        for i in range(len(self.cells)):
            #for each cell
            
            #recover the probabilities of each qubit
            
            qs=self.cells[i].q
            p=np.zeros(4)
            q=np.zeros(4)
            for j in range(len(qs)):
                p[j]=self.p[qs[j]]
                q[j]=1.-p[j]
            
            #recover the half syndromes
            
            ss=self.cells[i].s
            s0=self.spt[self.s[ss[0]]][self.split[ss[0]]][self.cells[i].z]
            s1=self.spt[self.s[ss[1]]][self.split[ss[1]]][self.cells[i].z]
            s2=self.spt[self.s[ss[2]]][self.split[ss[2]]][self.cells[i].z]
            
            #find the 2 possibilities from the lookuptable
            
            options=lut4(s0,s1,s2)
            
            #compute each probability
            p0=1.#p**np.array(options[0])*q**np.array(1-options[0])
            p1=1.#p**np.array(options[1])*q**np.array(1-options[1])
            for j in range(4):
                p0*=p[j]**options[0][j]*q[j]**(1-options[0][j])
                p1*=p[j]**options[1][j]*q[j]**(1-options[1][j])
            
            #apply the best option
            if p0>p1:
                self.cells[i].corr=list(options[0])
                if not softRescProb:
                    self.cells[i].pe=p1/(p0+p1)
            else:
                self.cells[i].corr=list(options[1])
                if not softRescProb:
                    self.cells[i].pe=p0/(p0+p1)
                
            if softRescProb:
                self.cells[i].pe=self.cellSoftRescale(self.cells[i].corr,i,plotall)
            
            #translate the correction to the code
            for j in range(4):
                qubit=self.cells[i].q[j]
                self.c[qubit]=int((self.c[qubit]+self.cells[i].corr[j])%2) 
        return
    
    
    def cellSoftRescale(self,correction, cellid,plotall=False):
        
        #first we find the data we need
        
        #we put the correction in the correct notation
        cor=np.zeros(4)
        cor[0]=correction[0]
        cor[1]=correction[2]
        cor[2]=correction[3]
        cor[3]=correction[1]
        #and we save the x operator
        xop=np.array([1,1,1,0])
        
        #the error probabilities of the qubits:  
        
        pqs=np.zeros((4,2))
        #note the change in notation
        #the max( * ,1e-10) are there to secure there are no 0's 
        pqs[0,0]=max(1.-max(self.p[self.cells[cellid].q[0]],1e-10),1e-10)
        pqs[1,0]=max(1.-max(self.p[self.cells[cellid].q[2]],1e-10),1e-10)
        pqs[2,0]=max(1.-max(self.p[self.cells[cellid].q[3]],1e-10),1e-10)
        pqs[3,0]=max(1.-max(self.p[self.cells[cellid].q[1]],1e-10),1e-10)
        for i in range(4):
            pqs[i,1]=max(1.-max(pqs[i,0],1e-10),1e-10)
        if plotall:
            print pqs
        
        #the splitting probabilities
        
        ps=np.zeros((3,2))
        for i in range(3):
            if (self.split[self.cells[cellid].s[i]]==0):
                ps[i,0]=self.sp[self.cells[cellid].s[i]]
                ps[i,1]=1.-self.sp[self.cells[cellid].s[i]]
            else:
                ps[i,1]=self.sp[self.cells[cellid].s[i]]
                ps[i,0]=1.-self.sp[self.cells[cellid].s[i]]
                
        if plotall:
            print ps
        #the table of equivalencies
        if len(self.psoft)==0:
                
            self.psoft=[np.array([1,1,1,0]),
               np.array([1,0,0,1]),
               np.array([0,1,0,1]),
               np.array([0,0,1,1]),
               np.array([1,0,0,0]),
               np.array([0,1,0,0]),
               np.array([0,0,1,0]),
               np.array([1,1,1,1]) 
                    ]
            self.ssoft=[np.array([0,0,0]),
               np.array([0,0,1]),
               np.array([0,1,0]),
               np.array([1,0,0]),
               np.array([1,1,0]),
               np.array([1,0,1]),
               np.array([0,1,1]),
               np.array([1,1,1]),         
               ]
        #now that we have everything we need, we proceed to compute the rescaling probability
        #which consists on 8 terms
        presc=0.0
        for iterm in range(8):
            
            #each term has a factor due to the error prob on the qubits.
            #a factor due to the splitting probabilities,
            #and a denominator, consisting in the first factor plus X
            
            #let us compute the numerator (correction+table):
            combination=(self.psoft[iterm]+cor)%2
            combinationX=(combination+xop)%2
            num=1.
            den=1.
            for i in range(4):
                num*=pqs[i,int(combination[i])]
                den*=pqs[i,int(combinationX[i])]
            den=num+den
            
            #lets compute now the factor due to the splitting prob
            
            splitf=1.
            for i in range(3):
                splitf*=ps[i,int(self.ssoft[iterm][i])]
                
            #now, we just need to multiply the factors:
            
            presc+=num*splitf/den
            if plotall:
                print "Combination, combinationX"
                print combination,combinationX
                print num, den
                print num/den
                print "splittings"
                print splitf
                print "total term"
                print num*splitf/den
                
    
        if np.any(math.isnan(presc))and plotall==False:
            print "  "
            print "NaN found" 
            print "  "
            
            self.cellSoftRescale(correction, cellid,plotall=True)
        #after adding the 8 factors, we have the probability of the rescaled cell
        return presc
            
                
                
                
    def hardDecoder(self,splitmethod=6,softsplit=False,cornerupdate=True,softRescaling=True,plotall=False,fignum=0,beta=50,splitsteps=7,double=3):
        '''
        splitmethods:
        0 init0 hard splitting
        1 randomized start hard splitting
        2 soft splitting
        3 init0 hard splitting twice: first without cornerupdate, then with corner update
        4 init0 heatsplit
        5 hard decoder random choice
        6 soft decoder coordinate
            
        '''
        
        #if m==0, apply the lookuptable decoder
        if plotall:
            print "Starting decoder of level ", self.m
        if self.m==0:
            self.decode0()
                
            if plotall:
                plt.figure(self.m+fignum)
                plt.clf()
                self.plot(splitting=False, cells=False,indexs=True)
                plt.title("Correction of the 18q decoder")
            return self.c
        #if m>0, apply the rescaling procedure
        
        
        #   RESCALING DECODER
        
        
        # CORNER PROBABILITY UPDATE
        
        if cornerupdate and splitmethod!=3:
            self.updateCornerP()
        
        
        #   SPLITTING OF SYNDROMES
        #first, do the splitting
        
        nchanges=25
        
        #initial condition
        for i in range(len(self.split)):
            #init0 condition
            if splitmethod==0 or splitmethod==3 or splitmethod==4 or splitmethod==5:
                self.split[i]=0
            #random init condition
            if splitmethod==1:
                self.split[i]=np.random.randint(0,2)
            #soft guess initial condition
            if splitmethod==2:
                if self.s[i]==0:
                    self.sp[i]=0.7
                else:
                    self.sp[i]=0.5
                    
        #splitting process            
        if plotall:
            print "Starting splitting process"
            
        i=0
        if splitmethod <5:                
            while i<splitsteps and nchanges>0:
                i+=1
                '''
                c0,t=self.resplit(0)
                c1,t=self.resplit(1)
                c2,t=self.resplit(2)
                nchanges=c1+c2+c0
                '''
                nchanges=0
                for j in range(17):
                    if softsplit or splitmethod==2:
                        print "Calling softresplit"
                        changes,t=self.softresplit()
                    elif splitmethod==4:
                        changes,t=self.heatresplit()
                    else:
                        changes,t=self.resplit()
                    nchanges+=changes
                beta+=10
        if splitmethod==3:
            #we do the corner update and repeat the splitting
            self.updateCornerP()
                
            i=0
            nchanges=25
            while i<splitsteps and nchanges>0:
                i+=1
                if plotall:
                    print "Splitting step part 2",i
                nchanges=0
                for j in range(17):
                    changes,t=self.resplit()
                    nchanges+=changes
                    
        if splitmethod==5:
            self.randomminsplit(splitsteps)
            
        if splitmethod==6:
            self.softresplitcoordinate(splitsteps,double)
            
    
            #   DECODING EACH CELL
        #now the decoding of each cell is independent
        self.cellCorrectionAndRescaleProb(softRescaling,plotall=False)
        '''
        for i in range(len(self.cells)):
            #for each cell
            
            #recover the probabilities of each qubit
            
            qs=self.cells[i].q
            p=np.zeros(4)
            q=np.zeros(4)
            for j in range(len(qs)):
                p[j]=self.p[qs[j]]
                q[j]=1.-p[j]
            
            #recover the half syndromes
            
            ss=self.cells[i].s
            s0=self.spt[self.s[ss[0]]][self.split[ss[0]]][self.cells[i].z]
            s1=self.spt[self.s[ss[1]]][self.split[ss[1]]][self.cells[i].z]
            s2=self.spt[self.s[ss[2]]][self.split[ss[2]]][self.cells[i].z]
            
            #find the 2 possibilities from the lookuptable
            
            options=lut4(s0,s1,s2)
            
            #compute each probability
            p0=1.#p**np.array(options[0])*q**np.array(1-options[0])
            p1=1.#p**np.array(options[1])*q**np.array(1-options[1])
            for j in range(4):
                p0*=p[j]**options[0][j]*q[j]**(1-options[0][j])
                p1*=p[j]**options[1][j]*q[j]**(1-options[1][j])
            
            #apply the best option
            if p0>p1:
                self.cells[i].corr=list(options[0])
                self.cells[i].pe=p1/(p0+p1)
            else:
                self.cells[i].corr=list(options[1])
                self.cells[i].pe=p0/(p0+p1)
            
            #translate the correction to the code
            for j in range(4):
                qubit=self.cells[i].q[j]
                self.c[qubit]=int((self.c[qubit]+self.cells[i].corr[j])%2)
        '''
        # CREATING THE RENORMALIZED CODE
        
        assert len(self.cells)==len(self.newcode.p), 'Wrong match between rescaling'
        for i in range(len(self.cells)):
            #for each cell in the new code we have a new probability
            self.newcode.p[i]=self.cells[i].pe
        if plotall:
                
            print "error probabilities in the new code:"
            print self.newcode.p
            
        
        #we also need to pass on the syndromes of the corners
        for i in range(self.newcode.L**2):
            #we compute the coordinates in the new code
            x=i%self.newcode.L
            y=i/self.newcode.L
            #then find the index of the equivalent from the original
            newi=2*x+2*y*self.L
            #and store it
            self.newcode.s[i]=self.s[newi]
            
            
            
        #we need to change the corner syndromes according to the correction
        nL=self.newcode.L
        
        nsx0=[0,1,0]
        nsy0=[0,0,1]
        nq=[0,2,3]
        nsx1=[1,0,1]
        nsy1=[1,1,0]
        
        
        for i in range(len(self.cells)):
            x=(i/2)%nL
            y=(i/2)/nL
            z=i%2
            
            for j in range(len(nq)):
                    
                if z==0:
                    xn=(x+nsx0[j])%nL
                    yn=(y+nsy0[j])%nL
                if z==1:
                    xn=(x+nsx1[j])%nL
                    yn=(y+nsy1[j])%nL
                ins=xn+yn*nL    
                self.newcode.s[ins]=(self.newcode.s[ins]+self.cells[i].corr[nq[j]])%2
                    
                    
        
        # DECODING THE NEW CELL
        #now that we have all the data in the new code, apply its decoder
        if plotall:
            plt.figure(self.m+fignum)
            plt.clf()
            self.plot(splitting=True, cells=False)
            plt.title("Correction at this level before rescaling")
            
            
        self.newcode.hardDecoder(plotall=plotall,fignum=fignum)
        
        # TRANSLATING THE CORRECTION TO OUR CODE
        for i in range(len(self.newcode.c)):
            #if there is a correction in the qubit i in the 
            #rescaled version
            if self.newcode.c[i]==1:
                #then we apply a logical operator to the corresponding cell
                inds=self.cells[i].q
                self.c[inds[0]]=(self.c[inds[0]]+1)%2
                self.c[inds[2]]=(self.c[inds[2]]+1)%2
                self.c[inds[3]]=(self.c[inds[3]]+1)%2
        res,loger=self.checkLogError()
        if plotall:
            plt.figure(-self.m+fignum)
            plt.clf()
            self.syndrome(True)
            for iq in range(len(self.e)):
                if self.e[iq]==1 and self.c[iq]==1:
                    self.e[iq]=0
                    self.c[iq]=0
            self.plot(splitting=True, cells=False)
            if res==0:
                resulttext="Success: "+str(loger)
            if res==1:
                resulttext="Log. Error: "+str(loger)
            assert res==0 or res==1, "check Log Error is doing something wrong: "+str(res)
            plt.title("Final correction at this level \n"+str(resulttext))
            
        #and we have finished, all the information of the correction is
        #stored in the variable self.c
        return res,loger
                
            
            
        
        
    
    def decode0(self):
        global lut18
        
        assert self.m==0 and self.N==18, "Only for 18 qubit codes"
        
        #first, we find the index for the lutable
        synb=''
        for j in self.s:
            synb+=str(int(j))
        index=int(synb,2)
        p=np.array(self.p)
        q=1-p
        pmax=-12.#initialize a lowvalue
        emax=[]
        #we want to find the most probable correction
        #print lut18[index]
        for er in lut18[index]:
            pc=1.
            
            for i in range(len(er)):
                if er[i]=='0':
                    pc*=q[i]
                if er[i]=='1':
                    pc*=p[i]
            #print er, pc
            if pc==pmax:
                emax.append(er)
                #print emax
            
            if pc>pmax:
                pmax=pc
                emax=[er]
        if len(emax)==0:
            plt.figure(10)
            plt.clf()
            self.plot()
            plt.title("Invalid Syndrome")
            assert len(emax)>0, 'Invalid syndrome, '+str(self.e)
        cor=emax[0]
        if len(emax)>1:
            cor=emax[np.random.randint(len(emax))]
        for i in range(len(cor)):
            self.c[i]=+int(cor[i])
        
        return emax
        
        
    
    def decode0lop(self):
        global lut18lop
        
        assert self.m==0 and self.N==18, "Only for 18 qubit codes"
        
        #first, we find the index for the lutable
        synb=''
        for j in self.s:
            synb+=str(int(j))
        index=int(synb,2)
        p=np.array(self.p)
        q=1-p
        pmax=-12.#initialize a lowvalue
        phmax=-12.
        emax=[]
        ehmax=[]
        hmax=[]
        
        explored=set()
        count=0
        case=0
        #we want to find the most probable correction
        for j in range(len(lut18lop[index])):
            ph=0.    
            for er in lut18lop[index][j]:
                pc=1.
                
                if er in explored:
                    print "Explored state! ",er
                    count+=1
                    print count, len(lut18lop[index][j])
                explored.add(er)
                
                for i in range(len(er)):
                    if er[i]=='0':
                        pc*=q[i]
                    if er[i]=='1':
                        pc*=p[i]
                
                ph+=pc
                if pc==pmax:
                    emax.append(er)
                    #print emax
                
                if pc>pmax:
                    pmax=pc
                    emax=[er]
            #print ph  
            if ph==phmax:
                ehmax.append(emax)
                hmax.append(j)
                case=1
                                  
            if ph>phmax:
                phmax=ph
                ehmax=list(emax)
                hmax=[j]
                case=2
        
        #checking that we have a solution
        if len(ehmax)==0:
            plt.figure(10)
            plt.clf()
            self.plot()
            plt.title("Invalid Syndrome")
            assert len(emax)>0, 'Invalid syndrome'
            
            
        cor=ehmax
        if len(emax)>1:
            cor=emax[np.random.randint(len(emax))]
        while type(cor)==list:
                
            if len(cor)>1:
                cor=cor[np.random.randint(len(cor))]
            else:
                cor=cor[0]
        assert len(cor)==18, "the correction needs to have 18 digits, now has "+str(len(cor))+", case: "+str(case)
        
        for i in range(len(cor)):
            self.c[i]=int(cor[i])
        
        return ehmax,hmax
            
                
    ############################################################        
        
    
    def pupdate(self,synind,printthings=False):
        L=self.L        
        #first, we compute the coordinates of the syndrome
        x=synind%L        
        y=synind/L
        
        #now we compute if it is an horizontal, vertical or diagonal splitting
        assert x%2!=0 or y%2!=0, "corner syndrome"
        if x%2==1 and y%2==0:
            #horizontal syndrome
            st=0
            #s1 and s2
            s1=1
            s2=2
            #coordinates of the cells
            xu=x-1
            yu=y
            xd=x-1
            yd=(y-2)%L
            
        if x%2==0 and y%2==1:
            #vertical syndrome
            st=1
            #s1 and s2
            s1=0
            s2=2
            #coordinates of the cells
            xu=x
            yu=y-1
            xd=(x-2)%L
            yd=(y-1)%L
            
        if x%2==1 and y%2==1:
            #diagonal syndrome
            st=2
            #s1 and s2
            s1=0
            s2=1
            #coordinates of the cells
            xu=x-1
            yu=y-1
            xd=x-1
            yd=y-1
            
        #index of the neighboring cells    
        
        icu=xu+L*yu/2  #cell  up  always has z=0
        icd=xd+L*yd/2+1#cell down always has z=1
#        
#        print 'syndrome: ',synind
#        print 'indexes: ',icu,icd
#        print 's1, s2: ',s1,s2
#        print xu,yu,xd,yd
        #index of the related splittings
        is1=self.cells[icu].s[s1]
        is2=self.cells[icu].s[s2]
        is1p=self.cells[icd].s[s1]
        is2p=self.cells[icd].s[s2]
        
        
        #the factors p(s1), p(s2),p(s1'),p(s2')
        p=min(max(self.sp[is1],1e-10),1.-1e-10)
        assert p<=1.001 and p>=0, 'incorrect value of p '+str(p)+' '+str(is1)
        ps1=np.array(  [p,  p,1-p,1-p])
        p=min(max(self.sp[is2],1e-10)  ,1.-1e-10)  
        assert p<=1.001 and p>=0, 'incorrect value of p '+str(p)+' '+str(is2)
        ps2=np.array(  [p,1-p,  p,1-p])
        p=min(max(self.sp[is1p],1e-10),1.-1e-10)
        ps1p=np.array( [p,  p,1-p,1-p])
        p=min(max(self.sp[is2p],1e-10),1.-1e-10)
        ps2p=np.array( [p,1-p,  p,1-p])
                        
        psu3=np.zeros(4)
        psd3=np.zeros(4)
        psu03=np.zeros(4)
        psd03=np.zeros(4)
        psu13=np.zeros(4)
        psd13=np.zeros(4)
        
        
        #splitting for [syndrome value][0, as that contributes with p(s1)][z of cell]
        su=  self.spt[self.s[synind]][0][0]
        sd=  self.spt[self.s[synind]][0][1]
        sv1= self.spt[self.s[is1]][0][0]   
        sv2= self.spt[self.s[is2]][0][0]   
        sv1p=self.spt[self.s[is1p]][0][1]  
        sv2p=self.spt[self.s[is2p]][0][1]  
        
        sv=[0,0,0]#initialization
        
        #changes in s1 and s2 for the loop
        cs1=[0,0,1,1]
        cs2=[0,1,0,1]
        
        
        #terms for the sum over s1 and s2
        for j in range(4):
            sv[s1]=(sv1+cs1[j])%2
            sv[s2]=(sv2+cs2[j])%2     
            
            sv[st]=su#value for which we have p(s0)
            psu3[j] =min(max(  self.p3(self.cells[icu],sv[0],sv[1],sv[2]) ,1e-10),1.-1e-10)
            if printthings:
                print "j ",j
                print s1,s2,st
                print sv
            sv[st]=1#always one
            psu13[j]=min(max(  self.p3(self.cells[icu],sv[0],sv[1],sv[2]),1e-10),1.-1e-10)
            sv[st]=0#always 0
            psu03[j]=min(max(  self.p3(self.cells[icu],sv[0],sv[1],sv[2]),1e-10),1.-1e-10)
            #same for the probability in the other cell
            sv[s1]=(sv1p+cs1[j])%2
            sv[s2]=(sv2p+cs2[j])%2     
            
            sv[st]=sd
            psd3[j] =min(max(  self.p3(self.cells[icd],sv[0],sv[1],sv[2]),1e-10),1.-1e-10)
            if printthings:
                print sv
            sv[st]=1
            psd13[j]=min(max(  self.p3(self.cells[icd],sv[0],sv[1],sv[2]),1e-10),1.-1e-10)
            sv[st]=0
            psd03[j]=min(max(  self.p3(self.cells[icd],sv[0],sv[1],sv[2]),1e-10),1.-1e-10)
        
        psu=np.sum(psu3*ps1 *ps2 /(psu13+psu03))        
        psd=np.sum(psd3*ps1p*ps2p/(psd13+psd03))
        
        newp=psu*psd/(psu*psd+(1.-psu)*(1.-psd))
        
        
        assert psu>=0 and psu<=1.0001, 'incorrect value of psu: '+str(psu)
        assert newp>=0 and newp<=1.0001, 'incorrect value of newp: '+str(newp)+' '+str(synind)
        return newp
    
    
    def pq(self,p,s):
        if s==1:
            return p
        else:
            return 1-p
    #probability p(s0s1s2)
    def p3(self,cell,s0,s1,s2):
        qubits=cell.q       #indexes of the qubits in the cell
        sol=lut4(s0,s1,s2)  #configurations compatible with syndrome        
        p1=1.
        p2=1.
        for i in range(4):  #we compute p(s0s1s2)
            p1*=min(max(self.pq(self.p[qubits[i]],sol[0][i]),1e-10),1-1e-10)
            p2*=min(max(self.pq(self.p[qubits[i]],sol[1][i]),1e-10),1-1e-10)
        return p1+p2
    
    #probability p(s0 | s1s2)  #the ind choose which one is in the front
    def pc3(self,cell,s0,s1,s2,ind):
        s=list([s0,s1,s2])
        s[ind]=(s[ind]+1)%2
        return self.p3(cell,s0,s1,s2)/(self.p3(cell,s0,s1,s2)+self.p3(cell,s[0],s[1],s[2]))        
    
    
    def ps(self,sind):#finds the probability of a splitting
        L=self.L
        #first we find which kind of syndrome it is
        #meaning, know if it is s0,s1 or s2
        xs=sind%L
        ys=sind/L
        #assuming it is one of the boundary qubits and not a corner one
        if ys%2==0:
            inds=0
        else:
            if xs%2==0:
                inds=1
            else:
                inds=2
        if xs%2==0 and ys%2==0:
            inds=4
        assert inds<3, "Trying to split corner syndrome"
        
        #now we find the index of the neighbouring cells, depending 
        #of inds (check picture on paper)
        if inds==0:
            xcu=xs-1
            ycu=ys
            xcd=xcu
            ycd=(ys-2)%L
        if inds==1:
            xcu=xs
            ycu=ys-1
            xcd=(xcu-2)%L
            ycd=ycu
        if inds==2:
            xcu=xs-1
            ycu=ys-1
            xcd=xcu
            ycd=ycu
        #these are always 0 and 1
        zcu=0
        zcd=1
        #find the index for the cells
        #indcu=xcu/2+L*ycu/2+zcu
        #indcd=xcd/2+L*ycd/2+zcd
        indcu=xcu+L*ycu/2+zcu
        indcd=xcd+L*ycd/2+zcd
        #then the cells themselves from the list
        cellu=self.cells[indcu]
        celld=self.cells[indcd]
        
        #then the syndromes involved
        #syndrome indexes
        siu=list(cellu.s)
        sid=list(celld.s)
        #initialization of the values of the half syndromes
        #syndrome values
        svu=list(siu)
        svd=list(siu)
        
        #splittings index(1 or 0)
        #   self.split=[0]*(L**2)
        #table of splitting values
        #   self.spt=[[[0,0],[1,1]],[[1,0],[0,1]]]
        #       spt[syndrome value][split][qubit]
        #       spt[0 or 1 for +1,-1][0 or 1][z=0 or 1]
        
        #using that:
        #value of the halfsyndrome
        for i in range(3):
            #value=split[syndrome[Sindex][splitChoice][cell up/down]
            svu[i]=self.spt[self.s[siu[i]]][self.split[siu[i]]][0]
            svd[i]=self.spt[self.s[sid[i]]][self.split[sid[i]]][1]    
            if i==inds:
                #for the common syndrome we compute the first option
                #because the probability of the second is 1-p
                
                #we also forget about the previous splitting
                svu[i]=self.spt[self.s[siu[i]]][0][0]
                svd[i]=self.spt[self.s[sid[i]]][0][1]  
            
        #once we have all the indexes, we compute the conditional probabilities    
        pu=self.pc3(cellu,svu[0],svu[1],svu[2],inds)
        pd=self.pc3(celld,svd[0],svd[1],svd[2],inds)
          
        #then the final probability is:
        return min(max(pu*pd/(pu*pd+ (1-pu)*(1-pd)),1e-10),1-1e-10)
            
                
    
    def fullsplittester(self,printon=False):
        assert self.m<2, "size too big"
        sptoupdate=self.s0s+self.s1s+self.s2s
        nst=2**len(sptoupdate)
        enmin=1e10
        splitmin=[]
        if printon:
            print len(sptoupdate),nst
        
        i=-1
        start=time.time()
        while i<nst:
            i+=1
            er=bin(i)[2:]
            er='0'*(len(sptoupdate)-len(er))+er
            for j in range(len(sptoupdate)):
                self.split[sptoupdate[j]]=int(er[j])
            if printon and i%100000==0:
                print i,nst,1.*i/nst,"%"
                print time.time()-start
                print "Expected total time", (1.*nst/i*(time.time()-start)-(time.time()-start))/3600., "hours"
                print "Expected total time", 1.*nst/i*(time.time()-start)/3600., "hours"
            en=self.energy()
            if en<enmin:
                enmin=en
                splitmin=er
        er=splitmin
        assert len(sptoupdate)==len(er), "something went wrong in here"
        for j in range(len(sptoupdate)):
            self.split[sptoupdate[j]]=int(er[j])
        
        if printon:
            print splitmin
            print time.time()-start
            self.plot(splitting=True)
        return enmin,splitmin
            
        
    
    def plot(self,lattice=True,qubits=False,syndrome=True,indexs=False,logicops=False,
             correction=True, cells=False, error=True, splitting=False,coll='k'):
        L=int(np.sqrt(self.N/2))
        colors=["r","b","g"]
        #lattice plotter
        if lattice:
                
            for n in range(L+1):
                #        x1,x2,y1,y2
                plt.plot([0,L],[n,n],coll)#horizontal
                plt.plot([n,n],[0,L],coll)#vertical
                plt.plot([n,0],[0,n],coll)#diagonalbottom
                plt.plot([L,n],[n,L],coll)#diagonaltop
        
        #stabilizer plotter
    
        if (syndrome):
            for i in range(L**2):                
                x=[i%L]
                y=[i/L]
                col=colors[(x[0]-y[0])%3]
                if (x[0]==0): 
                    x.append(x[0]+L)
                    y.append(y[0])
                if (y[0]==0):
                    x.append(x[0])
                    y.append(y[0]+L)
                if (y[0]==0 and x[0]==0):
                    x.append(x[0]+L)
                    y.append(y[0]+L)
                
                plt.plot(x,y,'.',color=col,marker="o",markersize=10)
                if indexs:                        
                    plt.plot(x,y,'.',color="black",marker="$"+str(i)+"$",markersize=13)
                    plt.plot(x,y,'.',color="yellow",marker="$"+str(i)+"$",markersize=10)
                    
                #syndrome plotter
                if (self.s[i]==1):
                    plt.plot(x,y,'.',color="black",marker="$o$",markersize=17)
                    plt.plot(x,y,'.',color="black",marker="$o$",markersize=11)
                    plt.plot(x,y,'.',color="yellow",marker="$o$",markersize=14)
               
        #qubit plotter
        
        if qubits:
            for i in range(self.N):
                x=(i/2)%L
                y=(i/2)/L
                z=i%2
                x+=.3+z*.4
                y+=.3+z*.4
            
                plt.plot(x,y,'.',color="yellow",marker="$q$",markersize=14)
        
        if logicops:
            for i in self.logic[0]:
                x=(i/2)%L
                y=(i/2)/L
                z=i%2
                x+=.25+z*.4
                y+=.3+z*.4            
                plt.plot(x,y,'.',color="red",marker="$H$",markersize=14)
            for i in self.logic[1]:
                x=(i/2)%L
                y=(i/2)/L
                z=i%2
                x+=.35+z*.4
                y+=.3+z*.4            
                plt.plot(x,y,'.',color="blue",marker="$H$",markersize=14)
            for i in self.logic[2]:
                x=(i/2)%L
                y=(i/2)/L
                z=i%2
                x+=.25+z*.4
                y+=.3+z*.4            
                plt.plot(x,y,'.',color="red",marker="$V$",markersize=14)
            for i in self.logic[3]:
                x=(i/2)%L
                y=(i/2)/L
                z=i%2
                x+=.35+z*.4
                y+=.3+z*.4            
                plt.plot(x,y,'.',color="blue",marker="$V$",markersize=14)
        
        
        
        #cell plotter
        if cells:
            
            '''    
            for i in range(self.N/4):
                nx=[0,0,1,0]
                ny=[0,0,0,1]
                nz=[0,1,0,0]
                if i%2==0:
                    x=(i%L)-i%2
                    y=(i/L)*2
                    for j in range(len(nx)):
                        xc=x+nx[j]+.3+nz[j]*.4
                        yc=y+ny[j]+.3+nz[j]*.4
                        plt.plot(xc,yc,'.',color="black",marker="$CELL$",markersize=15)
                nx=[1,1,1,0]
                ny=[1,1,0,1]
                nz=[0,1,1,1]
                if i%2==1:
                    x=(i%L)-i%2
                    y=(i/L)*2
                    for j in range(len(nx)):
                        xc=x+nx[j]+.3+nz[j]*.4
                        yc=y+ny[j]+.3+nz[j]*.4
                        plt.plot(xc,yc,'.',color="red",marker="$CELL$",markersize=15)
            '''            
            for i in range(len(self.cells)):
                if i%2==0:
                    colorcell="black"
                if i%2==1:
                    colorcell="red"
                
                for j in range(len(self.cells[i].q)):
                    ind=self.cells[i].q[j]    
                    xc=(ind/2)%self.L +.3+(ind%2)*.4   
                    yc=(ind/2)/self.L+.3+(ind%2)*.4
                    
                    plt.plot(xc,yc,'.',color=colorcell,marker="$CELL$",markersize=15)
                for j in range(len(self.cells[i].s)):
                    ind=self.cells[i].s[j]    
                    xc=(ind)%self.L+(i%2)*.052   
                    yc=(ind)/self.L+(i%2)*.052
                    
                    plt.plot(xc,yc,'.',color=colorcell,marker="$S$",markersize=15)
        
                    
        #error plotter 
        if error:
                
            for i in range(self.N):  
                if self.e[i]==1:  
                    x=(i/2)%(L)+.3+.4*(i%2)
                    y=(i/2)/(L)+.3+.4*(i%2)
                    col="r"
                    plt.plot(x,y,color=col,marker="$X$",markersize=10)
                    
        #correction plotter 
        if correction:
                
            for i in range(self.N):  
                if self.c[i]==1:  
                    x=(i/2)%(L)+.3+.4*(i%2)
                    y=(i/2)/(L)+.3+.4*(i%2)
                    col="r"
                    plt.plot(x+.15,y,color='blue',marker="$C$",markersize=10)
        
        #splitting plotter
        if splitting:
            
            mark=["$+$","$-$"]
            for i in self.s0s:
                x=i%self.L
                y=i/self.L
                if self.split[i]==0:
                    plt.plot(x-.1,y+0.1,color="black",marker="$U$", markersize=10)
                    plt.plot(x-.1,y+0.11,color="black",marker="$U$", markersize=6)
                    plt.plot(x-.1,y+0.1,color="yellow",marker="$U$", markersize=8)
                if self.split[i]==1:
                    plt.plot(x-.1,y-0.1,color="black",marker="$D$", markersize=10)
                    plt.plot(x-.1,y-0.1,color="black",marker="$D$", markersize=6)
                    plt.plot(x-.1,y-0.1,color="yellow",marker="$D$", markersize=8)
                
                mu=mark[self.spt[self.s[i]][self.split[i]][0]]
                md=mark[self.spt[self.s[i]][self.split[i]][1]]
                    
                plt.plot(x+.1,y+0.1,color="black",marker=mu, markersize=10)
                plt.plot(x+.1,y+0.1,color="black",marker=mu, markersize=6)
                plt.plot(x+.1,y+0.1,color="yellow",marker=mu, markersize=8)
                
                plt.plot(x+.1,y-0.1,color="black",marker=md, markersize=10)
                plt.plot(x+.1,y-0.1,color="black",marker=md, markersize=6)
                plt.plot(x+.1,y-0.1,color="yellow",marker=md, markersize=8)
            for i in self.s1s:
                x=i%self.L
                y=i/self.L
                if self.split[i]==0:
                    plt.plot(x-.1,y+0.1,color="black",marker="$U$", markersize=10)
                    plt.plot(x-.1,y+0.1,color="black",marker="$U$", markersize=6)
                    plt.plot(x-.1,y+0.1,color="yellow",marker="$U$", markersize=8)
                if self.split[i]==1:
                    plt.plot(x+.1,y+0.1,color="black",marker="$D$", markersize=10)
                    plt.plot(x+.1,y+0.1,color="black",marker="$D$", markersize=6)
                    plt.plot(x+.1,y+0.1,color="yellow",marker="$D$", markersize=8)
                
                mu=mark[self.spt[self.s[i]][self.split[i]][0]]
                md=mark[self.spt[self.s[i]][self.split[i]][1]]
                    
                plt.plot(x+.1,y-0.1,color="black",marker=mu, markersize=10)
                plt.plot(x+.1,y-0.1,color="black",marker=mu, markersize=6)
                plt.plot(x+.1,y-0.1,color="yellow",marker=mu, markersize=8)
                
                plt.plot(x-.1,y-0.1,color="black",marker=md, markersize=10)
                plt.plot(x-.1,y-0.1,color="black",marker=md, markersize=6)
                plt.plot(x-.1,y-0.1,color="yellow",marker=md, markersize=8)
            for i in self.s2s:
                x=i%self.L
                y=i/self.L
                if self.split[i]==0:
                    plt.plot(x-.15,y,color="black",marker="$U$", markersize=10)
                    plt.plot(x-.15,y,color="black",marker="$U$", markersize=6)
                    plt.plot(x-.15,y,color="yellow",marker="$U$", markersize=8)
                if self.split[i]==1:
                    plt.plot(x,y+.15,color="black",marker="$D$", markersize=10)
                    plt.plot(x,y+.15,color="black",marker="$D$", markersize=6)
                    plt.plot(x,y+.15,color="yellow",marker="$D$", markersize=8)
                
                mu=mark[self.spt[self.s[i]][self.split[i]][0]]
                md=mark[self.spt[self.s[i]][self.split[i]][1]]
                    
                plt.plot(x,y-0.15,color="black",marker=mu, markersize=10)
                plt.plot(x,y-0.15,color="black",marker=mu, markersize=6)
                plt.plot(x,y-0.15,color="yellow",marker=mu, markersize=8)
            
                plt.plot(x+.15,y,color="black",marker=md, markersize=10)
                plt.plot(x+.15,y,color="black",marker=md, markersize=6)
                plt.plot(x+.15,y,color="yellow",marker=md, markersize=8)
        return ""
    def clearcode(self,per):
        
        #initialization again
        for i in range(len(self.p)):
            self.p[i]=per
            self.e[i]=0
            self.c[i]=0
        self.s=[0]*(self.L**2)
        
        if self.m>0:
            self.newcode.clearcode(per)
        
    def simulation(self,per=-1,method=6,corners=True,softRescale=True,plotall=False):
        if per==-1:
            per=self.p[0]
        
        #initialization again
        self.clearcode(per)
            
        #noise
        self.noise()
        #syndrome]
        self.syndrome()
        
        #decoder
        return self.hardDecoder(splitmethod=method,cornerupdate=corners,softRescaling=softRescale,plotall=plotall)
        

    def simulationMulti(self,per=-1,method=6,corners=True,softRescale=True,plotall=False):
        '''
        This function simulates an error event and applies the decoder, then checks
        if the error was solved. The difference between this function and simulation() is:
        for each error set in the code, we are going to apply the decoder using multiple grids
        we decide which correction is best by counting the number of single qubit corrections
        applied. This method of choice is bad, because it does not take into account the 
        fact that stabilizers here count as 6 errors but have no effect in the code.
        Further improvement has to be done to find the best correction.
        '''
        if per==-1:
            per=self.p[0]
        
        #initialization again
        self.clearcode(per)
            
        #noise
        self.noise()
        
        error=[]
        for i in range(len(self.e)):
            if self.e[i]==1:
                error.append(i)
        L=self.L*2
        #8 types of change for the 8 positions in the cells
        change=[0,2,4,6,L,L+2,L+4,L+6,2*L,2*L+2,2*L+4,2*L+6,3*L,3*L+2,3*L+4,3*L+6]
        
        solved=np.zeros(len(change))
        ncorr=np.zeros(len(change))
        #we will run the decoder for every option
        mincor=self.N
        anysolved=1
        bestcl=[]
        for k in range(len(change)):
            self.clearcode(per)
            #first we setup the errors
            for er in error:
                self.e[(er+change[k])%self.N]=1
            #then proceed with the decoding process as usual
            self.syndrome()
            solved[k],loger=self.hardDecoder(splitmethod=method,cornerupdate=corners,softRescaling=softRescale,plotall=plotall)
            ncorr[k]=sum(self.c)
            #if there is more than one case with the same amount of corrections
            if ncorr[k]==mincor:
                bestcl.append(solved[k])
            
            if ncorr[k]<mincor:
                mincor=ncorr[k]
                bestcl=[solved[k]]
            
        #final output
        #average of the best
        bestc=sum(bestcl)*1./len(bestcl)
        #best result
        anysolved=min(solved)        
        #normal: result from the using 1 method         
        normal=solved[0]
        
        return bestc,anysolved,normal,ncorr,solved,bestcl
        

            