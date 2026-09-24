import numpy as np
import sounddevice as sd

tmax=20 #how many seconds of playing
nu0=220 #fundamental will be this frequency
fs=44100 #standard audio sample rate

t=np.arange(tmax*fs)/fs

amps=[1, 0, 1, 0, 1 ,0, 0.5] #amplitude of harmonics.  These are the numbers you should play with
#amps=[1]

#sum all the harmonics together, with the amplitudes we set.
tot=0
for i in range(len(amps)):
    k=i+1
    tot=tot+np.sin(t*nu0*2*np.pi*k)*amps[i]

tot=tot/tot.max()

#convert our mono signal into a stereo one
to_play=np.zeros([len(tot),2])
to_play[:,0]=tot
to_play[:,1]=tot
#play what we made!
sd.play(to_play,fs)
