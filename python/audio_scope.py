import numpy as np
import sounddevice as sd
from matplotlib import pyplot as plt

plt.ion()



fs=44100
nu=40
nsamp=int(fs/nu)

info=sd.query_devices(kind='input')
nchan=info['max_input_channels']

tvec=np.arange(nsamp)/fs*1000 #time in milliseconds


last=False

#nchunk=20
#samps=np.zeros([nchunk,nsamp])
#for i in range(nchunk):
#    myrecording = sd.rec(nsamp, samplerate=fs, channels=nchan,dtype='float32')
#    sd.wait()
#    samps[i,:]=np.squeeze(myrecording)
#assert(1==0)


ncut=4000 #it appears sd.rec takes about this many samples to settle in
while True:
    myrecording = sd.rec(2*nsamp+ncut, samplerate=fs, channels=nchan,dtype='float32')
    sd.wait()
    if nchan>1:
        myrecording=np.mean(myrecording,axis=1)
    else:
        myrecording=np.squeeze(myrecording)
    myrecording=myrecording[ncut:]
    #if np.max(np.abs(myrecording)>0.2):
    #    if last:
    #        assert(1==0)
    #    last=True
    #else:
    #    last=False

    mask=(myrecording[1:]>0)&(myrecording[:-1]<0)
    if np.sum(mask)>0:
        ind=np.min(np.where(mask>0)[0])
    if ind<nsamp:
        to_plot=myrecording[ind:ind+nsamp]
    else:
        to_plot=myrecoring[:nsamp]
    plt.clf()
    plt.plot(tvec,to_plot)
    plt.ylim([-0.5,0.5])
    plt.pause(0.0001)
        

