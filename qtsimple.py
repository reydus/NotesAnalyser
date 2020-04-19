from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from datetime import datetime
import time
import sounddevice as sd
from scipy.fft import fft

class graphing:
    def __init__(self):
        # Initialise Qt window/app
        self.app = QtGui.QApplication([])
        self.win = pg.GraphicsWindow(title="Live microphone input plotting and fourier transform")
        self.win.resize(1000,600)
        self.counter = 0
        self.fps = 0.
        self.lastupdate = time.time()
        self.label = QtGui.QLabel()
        self.win.setLayout(QtGui.QVBoxLayout())
        self.win.layout().addWidget(self.label)

        # Initialise audio stream
        self.chunk = 32 
        self.fs = 1200  # If we are interested in a frequency domain of 0 <= omega <= 600hz; Nyquist ratio rules a minimum of omega*2 sampling freq.
        self.inputStream = sd.Stream(blocksize=self.chunk,samplerate=self.fs,channels=1)
        self.inputStream.start()


        # Fourier transform (Frequency domain) plot
        self.fourierPlot = self.win.addPlot()
        self.h1 = self.fourierPlot.plot(pen="y")
        self.fourierPlot.setLabel("bottom", text="Frequency (Hz)")
        self.fourierPlot.setLabel("left", text="Magnitude")
        self.fourierPlot.setXRange(0,self.fs//2, padding=0)
        self.fourierPlot.autoRange(padding=0)
        self.fftspan = 1.0 #interval of time for FFT computation

        #  Waveform (Time domain) plot
        self.wavePlot = self.win.addPlot()
        self.wavePlot.setXRange(-4.0,0, padding=0)
        self.wavePlot.setLabel("bottom", text="Time-to-current (s)")
        self.wavePlot.setLabel("left", text="Amplitude")
        self.h2 = self.wavePlot.plot(pen='y')
        self.timespan = 4.0
        self.x = np.linspace(-self.timespan,0, num=(int(self.timespan*self.fs)))
        self.ydata = self.x[:] * 0 

        self._update()

    def _update(self):

        # modify ydata for waveform plot
        self.ydata = np.roll(self.ydata, -self.chunk)
        self.block = self.inputStream.read(self.chunk)
        if self.block[1] == True:
            print("Overflow on stream detected.")
        self.ydata[-(self.chunk):] = self.block[0].flatten()
        self.h2.setData(self.x,self.ydata)


        # modify fft data for frequency plot
        self.fftdata = fft(self.ydata[-int(self.fftspan*self.fs):]) # retrieve enough samples from the end of the main waveform
        self.fftdata = np.real(self.fftdata[:len(self.fftdata)//2]).flatten() # perform FFT on it, only include the first half of the real part.
        self.fftdata = abs(self.fftdata)
        self.h1.setData(self.fftdata)
        self.maxfft = max(self.fftdata)
        self.fourierPlot.setYRange(0,self.maxfft, padding=0)

        
        # FPS counter
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
        self.counter += 1


if __name__ == '__main__':
    app = graphing()
    QtGui.QApplication.instance().exec_()
