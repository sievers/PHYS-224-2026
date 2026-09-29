import numpy as np
import sounddevice as sd

tmax=3 #how many seconds of playing

fs=44100 #standard audio sample rate

t=np.arange(tmax*fs)/fs

nu0=220*(1+np.random.rand())
updown=(2*(np.random.rand()>0.5)-1)
print('updown is: ',updown)
cents=1  #percent of a halfstep to move
rat=(2**(1/12)-1)*cents/100
print('ratio is: ',rat)
nu1=nu0*(1+updown*rat)

freqs=[nu0,nu1]

n=fs*tmax
phase1=2*np.pi*np.arange(n)/fs*nu0
phase2=2*np.pi*np.arange(n)/fs*nu1
phase2=phase2+phase1[-1]+(phase1[-1]-phase1[-2])
phases=np.hstack([phase1,phase2])
tot2=np.sin(phases)

print('freqs are ',nu0,nu1)


freqs=[nu0,nu1]
#amps=[1, 1]

bits=[np.sin(t*freq*2*np.pi) for freq in freqs]
tot=np.hstack(bits)
sd.play(tot2*0.8,fs)
