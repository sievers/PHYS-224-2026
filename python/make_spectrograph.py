import numpy as np
import sounddevice as sd
from matplotlib import pyplot as plt
plt.ion()


info=sd.query_devices(kind='input')
nchan=info['max_input_channels']

fs=44100
dt=0.25

nsamp=int(fs*dt)

f0=220/4
freqs=f0*(2**(np.arange(88)/12))
edges=f0*(2**((np.arange(89)-0.5)/12))
dnu=1/dt
iedge=np.asarray(edges/dnu,dtype='int')

inds=np.arange(len(freqs))
mask=np.zeros(len(freqs),dtype='bool')
mask[inds%12==1]=True
mask[inds%12==4]=True
mask[inds%12==6]=True
mask[inds%12==9]=True
mask[inds%12==11]=True
mask2=np.logical_not(mask)



while True:
    myrecording = sd.rec(nsamp, samplerate=fs, channels=nchan,dtype='float32')
    sd.wait()
    myft=np.fft.rfft(np.squeeze(myrecording))
    mypow=np.abs(myft)**2
    spec=np.zeros(len(iedge)-1)
    for i in range(len(iedge)-1):
        spec[i]=np.mean(mypow[iedge[i]:iedge[i+1]])
    plt.clf()
    #plt.bar(spec,0.8)
    plt.bar(inds[mask2],np.log10(spec[mask2])+3)
    plt.bar(inds[mask],np.log10(spec[mask])+3)

    plt.ylim(0,10)
    plt.pause(0.001)
    
    


