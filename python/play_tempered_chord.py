import numpy as np
import sounddevice as sd
from scipy.io import wavfile
from matplotlib import pyplot as plt
plt.ion()

def safe_sum(vecs):
    ll=np.min([len(vv) for vv in vecs])
    out=np.zeros(ll)
    for vv in vecs:
        out[:ll]=out[:ll]+vv[:ll]
    return out

def shift_pitch(dat,ratio):
    ratio=1.0/ratio #we work in wavelength but ratio is usually in frequency
    dft=np.fft.rfft(dat)
    n_targ=int(len(dat)*ratio)
    nn=int(len(dft)*ratio)
    out=np.zeros(nn,dtype='complex')
    if ratio>1:
        out[:len(dft)]=dft
    else:
        out[:]=dft[:nn]
    if n_targ%2==1:
        return np.fft.irfft(out,n_targ)
    else:
        out[-1]=np.real(out[-1])
        return np.fft.irfft(out,n_targ)


#fs,sample=wavfile.read('organ_c4.wav');i_start=12500 #because I looked at it
#fs,sample=wavfile.read('organ_c3.wav');i_start=18000 #because I looked at it
fs,sample=wavfile.read('organ_c5.wav');i_start=19000 #because I looked at it



sample=sample[i_start:]
sample=0.8*(1.0*sample)/sample.max()
plt.clf();plt.plot(sample);plt.show()
rat=2**(1/12)
samp2=shift_pitch(sample,rat**7)
#rats=[rat**-4,1,rat**3] #for an equal-tempered major chord
#rats=[4/5,1,6/5] #for an ideal major chord
rats=[1.5**-4*4,1,1.5**-3*4] #for a pythagorean chord


do_minor=False
if do_minor:
    rats=[1/rr for rr in rats]
samps=[shift_pitch(sample,myrat) for myrat in rats]
tot=safe_sum(samps)
tt=tot[:int(len(tot)*0.8)] #we havent been careful about ends so chop off
tt=tt/tt.max()
#sd.play(tt,fs)
