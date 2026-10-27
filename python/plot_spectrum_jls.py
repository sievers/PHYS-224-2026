import numpy as np
from matplotlib import pyplot as plt
import sounddevice as sd
import time
plt.ion()


def get_spec(dat,pad,win=None):
    n=len(dat)
    vec=np.zeros(pad*n)
    if win is None:
        vec[:n]=dat
    else:
        vec[:n]=dat*win
    spec=np.abs(np.fft.rfft(vec))
    ind=np.argmax(spec)
    return spec,ind

fs=44100
tmax=1.5
tcut=0.5
dt=tmax-tcut
nsamp=int(dt*fs)
nsamp_raw=int(tmax*fs)
x=np.linspace(-np.pi,np.pi,nsamp)
win=0.5+0.5*np.cos(x)
pad=8
dnu=1/(dt*pad)

imin=int(tcut*fs)

while True:
    dummy=input('return to record (q to quit): ')
    if len(dummy)>0:
        if dummy[0]=='q':
            break
    myrecording=sd.rec(nsamp_raw,samplerate=fs,channels=1,dtype='float64')
    sd.wait()
    myrecording=np.squeeze(myrecording)[imin:]
    spec,ind=get_spec(myrecording,pad,win)
    nuvec=np.arange(len(spec))*dnu
    fmax=ind*dnu
    print("max freq is: ",fmax)
    plt.clf()
    plt.loglog(nuvec,spec)
    plt.pause(0.01)

