import numpy as np
import sounddevice as sd

tmax=10 #10 seconds of playing
nu0=220 #fundamental will be this frequency
fs=44100 #standard audio sample rate

t=np.arange(tmax*fs)/fs

amps=[1, 1, 1, 1., 0.5] #amplitude of harmonics

tot=0
for i in range(len(amps)):
    k=i+1
    tot=tot+np.sin(t*nu0*2*np.pi*k)*amps[i]

tot=tot/tot.max()
sd.play(tot,fs)
