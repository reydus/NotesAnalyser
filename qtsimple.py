from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from datetime import datetime
import time
import sounddevice as sd
from scipy.fft import fft
'''
app = QtGui.QApplication([])
win = pg.GraphicsWindow(title="My plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')
p1 = win.addPlot(title="plot1")
p2 = win.addPlot(title="plot2")
curve1 = p1.plot(pen='y')
curve2 = p1.plot(pen='r')
curve3 = p2.plot(pen='b')
x = np.linspace(0,10,1000)
x_current = x[0]
#p1.setXRange((5,20), padding=0)
###############################################
'''
class graphing:
    def __init__(self):
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow(title="Live microphone input plotting and fourier transform")
        self.win.resize(1000,600)
        #self.win.setWindowTitle('pyqtgraph example: Plotting')

        self.plot = self.win.addPlot()
        
        self.h1 = self.plot.plot(pen="y")
        self.plot.setLabel("bottom", text="Frequency (Hz)")
        self.plot.setLabel("left", text="Magnitude")
        #self.plot.showLabel("left", show=False)
        #self.plot.getAxis("left").setRange(0,4)


        #self.canvas.nextRow()
        #  line plot
        self.otherplot = self.win.addPlot()
        self.otherplot.setXRange(-4.0,0, padding=0)
        self.otherplot.setLabel("bottom", text="Time-to-current (s)")
        self.otherplot.setLabel("left", text="Amplitude")
        self.h2 = self.otherplot.plot(pen='y')
        self.chunk = 32 #64
        self.fs = 1200
        self.plot.setXRange(0,self.fs//2, padding=0)
        self.plot.autoRange(padding=0)
        #### Set Data  #####################
        self.timespan = 4.0
        self.x = np.linspace(-self.timespan,0, num=(int(self.timespan*self.fs)))
        #self.X,self.Y = np.meshgrid(self.x,self.x)

        self.counter = 0
        self.fps = 0.
        self.lastupdate = time.time()

        #### Start  #####################

        self.ydata = self.x[:] * 0 
        self.inputStream = sd.Stream(blocksize=self.chunk,samplerate=self.fs,channels=1)
        self.inputStream.start()
        self.start = datetime.now().timestamp()

        self.block = self.inputStream.read(self.chunk)
        self.block = np.reshape(self.block[0],(self.chunk,))
        self.ydata[-(self.chunk+1):-1] = self.block
        self.frames = []
        self.fftdata = np.ndarray((self.fs), dtype=np.float32)
        #(np.linspace(0,fs/2,num=self.chunk/2),np.real(fftdata[:self.chunk/2])
        self.maxfft = 0
        self._update()

    def _update(self):

        #self.data = np.sin(self.X/3.+self.counter/9.)*np.cos(self.Y/3.+self.counter/9.)
        self.ydata = np.roll(self.ydata, -self.chunk)
        self.block = self.inputStream.read(self.chunk)
        if self.block[1] == True:
            print("Overflow on stream detected.")
        
        self.ydata[-(self.chunk):] = self.block[0].flatten()
        #self.ydata = np.sin(self.x/3.+ self.counter/9.)
        #self.img.setImage(self.data)
        self.h2.setData(self.x,self.ydata)
        self.fftspan = 1.0
        self.fftdata = fft(self.ydata[-int(self.fftspan*self.fs):]) # retrieve enough samples from the end of the main waveform
        self.fftdata = np.real(self.fftdata[:len(self.fftdata)//2]).flatten() # perform FFT on it, only include the first half of the real part.
        self.fftdata = abs(self.fftdata)
        
        
        if max(self.fftdata) > self.maxfft:
            self.maxfft = max(self.fftdata)

        
        self.h1.setData(self.fftdata)
        now = time.time()
        dt = (now-self.lastupdate)
        if dt <= 0:
            dt = 0.000000000001
        fps2 = 1.0 / dt
        self.lastupdate = now
        self.fps = self.fps * 0.9 + fps2 * 0.1
        tx = 'Mean Frame Rate:  {fps:.3f} FPS'.format(fps=self.fps )
        #self.label.setText(tx)
        QtCore.QTimer.singleShot(1, self._update)
        self.newtime = datetime.now().timestamp() - self.start 
        #print("Stream time      Time measured")
        #print(str(self.inputStream.time)+"      "+str(self.newtime))
        self.counter += 1


if __name__ == '__main__':
    app = graphing()
    QtGui.QApplication.instance().exec_()
    '''
    app = QtGui.QApplication(sys.argv)
    thisapp = App()
    thisapp.show()
    sys.exit(app.exec_())
    '''







'''
for i in range(1,len(x)):
    x_current = np.append(x_current,x[i])
    curve1.setData(x_current,np.sin(x_current))
    curve2.setData(x_current,np.cos(x_current))
    curve3.setData(x_current,np.tan(x_current))
    app.processEvents()

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
'''