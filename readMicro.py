import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import time
from matplotlib import pyplot
from scipy.fftpack import fft

fs=44100
duration = 10  # seconds
#myrecording = sd.rec(duration * fs, samplerate=fs, channels=1,dtype='float64')
streamed = sd.Stream(blocksize=2048,samplerate=fs,channels=1)
streamed.start()
myrecording = streamed.read(fs*duration)
print("Prepare...")
#time.sleep(5)
print("recording audio")
#sd.wait()
print("Audio recording complete , Play Audio")
copy = myrecording[:]
co = 0
'''
for i in range(0, len(myrecording)):
    
    if myrecording[i] == float(0):
        myrecording[i] = np.nextafter(0,1)
        print("Found zero in index "+str(i)+" = "+str(myrecording[i]))
        co += 1
'''
print("replaced zeroes with "+str(np.nextafter(0,1))+" in "+str(co)+" cases")
myrecording = myrecording[0]
myrecording = myrecording.flatten()

x = np.arange(0, duration, 1/fs)
pyplot.subplot(211)
pyplot.plot(x,myrecording)
pyplot.subplot(212)
Pxx, freqs, bins, im = pyplot.specgram(myrecording, Fs=fs, NFFT=1024)
sd.play(myrecording, fs)
sd.wait()
print("Play Audio Complete")
print("end.")
print("post end")
pyplot.draw()
pyplot.show()

print("Drawing fft")
fftdata = fft(myrecording)
pyplot.plot(np.linspace(0,22050,num=220500),np.real(fftdata[:220500]))




print("post draw")
