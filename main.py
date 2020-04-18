import sounddevice as sd
import numpy as np
from datetime import datetime
import time
import math
import matplotlib.pyplot as plt

def live_plotter(x_vec,y1_data,line1,identifier='',pause_time=0.1):
    if line1==[]:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(13,6))
        ax = fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line1, = ax.plot(x_vec,y1_data,alpha=0.8)        
        #update plot label/title
        plt.ylabel('Y Label')
        plt.title('Title: {}'.format(identifier))
        plt.show()
    
    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_ydata(y1_data)
    # adjust limits if new data goes beyond bounds
    if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)
    
    # return line so we can update it again in the next iteration
    return line1

streamed = sd.Stream(blocksize=2048,samplerate=44100,channels=1)

print("Started stream at "+str(datetime.now().time()))
streamed.start()
aa = streamed.read(2048)
if aa[1] == True:
    print("Overflow!")

y = aa[0]
x = np.arange(-(2048/44100),0,1/44100)
line1 = live_plotter(x,y,[])

while True:
    aa = streamed.read(2048)
    if aa[1] == True:
        print("Overflow!")

    y = aa[0]
    x = np.arange(-1,0,1/44100)
    line1 = live_plotter(x,y,line1,pause_time=0.0005)


'''
while True:
    aa = streamed.read(44100)
    #print(aa[1])
    sd.play(aa[0])
    #time.sleep(3)
'''
if streamed.active == True:
    print("Success")
