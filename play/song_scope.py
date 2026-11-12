import numpy as np
import audioread
import sounddevice as sd
import subprocess
from read_song import read_song
from matplotlib import pyplot as plt
from threading import Thread
import os
import time
plt.ion()

def escape_string(mystr):
    out=''
    for myc in mystr:
        if myc in [' ',',']:
            out=out+'\\'+myc
        elif myc in ['\'']:
            out=out+'\\\\\''
        else:
            out=out+myc
    return out


#def play_wscope(dat,fsamp=44100,dt=0.5):
def play_wscope(fname,dt=0.5):
    dat,fsamp=read_song(fname)
    n=int(fsamp*dt)
    x=np.linspace(-np.pi,np.pi,n)
    win=(np.cos(x)+1)*0.5
    nchunk=int(np.floor(dat.shape[0]/fsamp/dt))-2
    time.sleep(0.5)  #it looks like it takes ~half a second to get going
    t0=time.time()
    
    #sd.play(dat,fsamp)
    #thread = Thread(target = sd.play, args = (dat,fsamp, ))
    #thread.start()
    os.system('open '+fname)
    dnu=1/dt
        
    for i in range(nchunk):
        ttarg=i*dt+dt/2
        t=time.time()-t0
        if (ttarg-t>0):
            time.sleep(ttarg-t)
        i0=int(ttarg*fsamp-n/2)
        i1=i0+n
        ftl=np.fft.rfft(win*dat[i0:i1,0])
        ftr=np.fft.rfft(win*dat[i0:i1,1])
        nuvec=np.arange(len(ftl))*dnu
        plt.clf()
        plt.loglog(nuvec,np.abs(ftl))
        plt.loglog(nuvec,np.abs(ftr))
        plt.xlim([20,20000])
        plt.ylim([1,1e7])
        plt.pause(0.01)

#fname='Copland_Fanfare_For_The_Common_Man.m4a'
#fname='/Users/sievers/Music/iTunes/iTunes\ Media/Music/Compilations/Die\ Walküre_\ Levine_MET\ disc\ 4/4-01\ Die\ Walküre\,\ Act3\ Sc1.m4a'

#fname="/Users/sievers/Music/iTunes/iTunes\ Media/Music/Matthew\ Morley\,\ Robert\ Jones\;\ St.\ Bride\'s\ Church\ Choir/Bruckner_\ Motets/01\ Bruckner_\ Os\ Justi\,\ Wab\ 30.m4a"
#fname="01\ Bruckner_\ Os\ Justi,\ Wab\ 30.m4a"
#fname="/Users/sievers/Music/iTunes/iTunes\ Media/Music/Compilations/Chopin_\ Etudes/24\ Chopin_\ Etude\ \#12\ In\ C\ Minor\,\ Op.\ 25.m4a"
fname="/Users/sievers/Music/iTunes/iTunes\ Media/Music/Canadian\ Brass/Bach_\ Art\ of\ the\ Fugue/17\ Bach_\ Chorale\ Prelude\ -\ _Vor\ deinen\ Thron\ tret\\'\ ich\ hiermit_.m4a"
#dat,fsamp=read_song(fname)
fname="/Users/sievers/Music/iTunes/iTunes Media/Music/Canadian Brass/Bach_ Art of the Fugue/01 Bach_ The Art of the Fugue - Contrapunctus 1 - Andante sostenuto.m4a";fname=escape_string(fname)



play_wscope(fname,dt=0.25)
