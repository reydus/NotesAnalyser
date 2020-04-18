import sys
import time
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import pyqtgraph as pg
import sounddevice as sd
from datetime import datetime
from scipy.fft import fft
class App(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(App, self).__init__(parent)

        #### Create Gui Elements ###########
        self.mainbox = QtGui.QWidget()
        self.setCentralWidget(self.mainbox)
        self.mainbox.setLayout(QtGui.QVBoxLayout())

        self.canvas = pg.GraphicsLayoutWidget()
        self.mainbox.layout().addWidget(self.canvas)

        self.label = QtGui.QLabel()
        self.mainbox.layout().addWidget(self.label)
        '''
        self.view = self.canvas.addViewBox()
        self.view.setAspectLocked(True)
        self.view.setRange(QtCore.QRectF(0,0, 100, 100))

        #  image plot
        self.img = pg.ImageItem(border='w')
        self.view.addItem(self.img)
        '''
        self.plot = self.canvas.addPlot()
        self.h1 = self.plot.plot(pen="y")
        self.plot.setLabel("bottom", text="Frequency (Hz)")
        self.plot.showLabel("left", show=False)
        self.plot.getAxis("left").setRange(0,4)


        #self.canvas.nextRow()
        #  line plot
        self.otherplot = self.canvas.addPlot()
        self.h2 = self.otherplot.plot(pen='y')
        self.chunk = 32 #64
        self.fs = 1200

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
        self.h2.setData(self.ydata)
        self.fftspan = 1.0
        self.fftdata = fft(self.ydata[-int(self.fftspan*self.fs):]) # retrieve enough samples from the end of the main waveform
        self.fftdata = np.real(self.fftdata[:len(self.fftdata)//2]).flatten() # perform FFT on it, only include the first half of the real part.
        self.h1.setData(self.fftdata)
        now = time.time()
        dt = (now-self.lastupdate)
        if dt <= 0:
            dt = 0.000000000001
        fps2 = 1.0 / dt
        self.lastupdate = now
        self.fps = self.fps * 0.9 + fps2 * 0.1
        tx = 'Mean Frame Rate:  {fps:.3f} FPS'.format(fps=self.fps )
        self.label.setText(tx)
        QtCore.QTimer.singleShot(1, self._update)
        self.newtime = datetime.now().timestamp() - self.start 
        #print("Stream time      Time measured")
        #print(str(self.inputStream.time)+"      "+str(self.newtime))
        self.counter += 1


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    thisapp = App()
    thisapp.show()
    sys.exit(app.exec_())