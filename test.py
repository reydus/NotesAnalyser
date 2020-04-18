import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

fs = 44100
chunk = 2048

ln = sd.Stream(samplerate=fs,blocksize=chunk,dtype="float32")

ln.start()

block = ln.read(chunk)
for i in block[0]:
    print(i)

plt.plot(block[0])
plt.show()