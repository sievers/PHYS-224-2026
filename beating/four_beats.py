import numpy as np
import sounddevice as sd
from scipy.io import wavfile

nu0=220.  #reference frequency.

dnu=0.8  #1/this should be roughly how long a cycle takes.  
nnu=2   #this should set roughly how sharp in time a beat is.  larger=shorter in time

tmax=40  #how long to run.  if this is much larger than 1/dnu, you will get many repeats
fs=44100 #probably don't want to change this...
t=np.arange(fs*tmax)/fs  #time vector so we can evaluate our sine waves




tot=0.0

#steps=[0,2,4,5,7,9,11,12, 14, 16, 17, 19,21,23,24]#notes in a two-octave major scale
#steps=[0,2,4,5,7,9,11,12]#notes in a major scale
steps=[0,2,4,0,0,2,4,0,4,5,7,7,4,5,7,7] #possibly familiar sounding
#steps=[0] #a single note so we can hear typical beating

spacing=2**(1/12) #the standard spacing of half-steps, assuming equal tempering
freqs=nu0*(spacing**(np.asarray(steps))) #turn our notes into actual frequencies

#outname='beats_'+repr(len(steps))+'_notes'

#phase_noise=1;outname=outname+'_random' #1 for random phases, 0 for no phase noise.
#phase_shift=0;outname=outname+'_nophase' #1 for random phases, 0 for no phase noise.
phase_shifts=[0,0.0,0,0]


for j in range(nnu):
    jj=j+1
    nu=nu0+jj*dnu
    tot=tot+np.cos(2*np.pi*(t*nu+phase_shifts[j]))
    nu=nu0-jj*dnu
    tot=tot+np.cos(2*np.pi*(t*nu+phase_shifts[j]))
    

tot=tot/np.abs(tot).max()
sd.play(tot,fs)
#wavfile.write(outname+'.wav',fs,(2**15*tot/np.abs(tot).max()).astype('int16'))
