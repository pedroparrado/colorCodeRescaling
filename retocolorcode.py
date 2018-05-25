

import numpy as np
import matplotlib.pyplot as plt
import time
from colorCodeh import *

import copy



#plot all states
import matplotlib.pyplot as plt

def callback(event):
    print "callback1"
    print event.x, event.y,3
    x,y= event.x, event.y
    x=(x-100.)/450.*6
    y=(y-70.)/330.*6
    print x,y


fig, ax = plt.subplots()
plt.clf()

m=1
code=ColorCode(m,.05)
code.noise()
code.syndrome()
code.plot(error=False)
plt.title("Find the error")
'''
plt.figure(1)
plt.clf()
code.plot()
plt.title("Solution")
'''

fig.canvas.callbacks.connect('button_press_event', callback)
def callback(event):
    print "callback2"
    print event.xdata,event.ydata,3
    x,y= event.xdata, event.ydata
    x=(x-100.)/450.*6
    y=(y-70.)/330.*6
    print x,y
