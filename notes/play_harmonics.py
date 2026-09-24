import numpy as np
import sounddevice as sd

tmax=20 #how many seconds of playing
nu0=220 #fundamental will be this frequency
fs=44100 #standard audio sample rate

t=np.arange(tmax*fs)/fs

amps=[0, 0.5, .33, 0.25, 0.2 ,0.16, 0.14] #amplitude of harmonics.  These are the numbers you should play with
#amps=(1.0/np.arange(1,10))**1
#amps[0]=0
#amps[1::2]=0
#amps=[1]

#sum all the harmonics together, with the amplitudes we set.
tot=0
for i in range(len(amps)):
    k=i+1
    if (amps[i]>0):
        print("adding in frequency: ",nu0*k)
        tot=tot+np.sin(t*nu0*2*np.pi*k)*amps[i]

tot=tot/tot.max()

#convert our mono signal into a stereo one
to_play=np.zeros([len(tot),2])
to_play[:,0]=tot
to_play[:,1]=tot
#play what we made!
sd.play(to_play,fs)
