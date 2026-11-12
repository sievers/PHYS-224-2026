import numpy as np
from read_song import read_song
from scipy.interpolate import CubicSpline


attenuations=np.loadtxt('attenuation.txt')

rh=10
col=(rh//10)
nu=attenuations[:,0]
db=attenuations[:,col]
nu=np.hstack([0,nu])
db=np.hstack([0,db])

#fname="/Users/sievers/Music/iTunes/iTunes\ Media/Music/Canadian\ Brass/Bach_\ Art\ of\ the\ Fugue/17\ Bach_\ Chorale\ Prelude\ -\ _Vor\ deinen\ Thron\ tret\\'\ ich\ hiermit_.m4a"
#fname="/Users/sievers/julian/music/31\ Tuned\ Percussion.aiff"
#fname2="/Users/sievers/julian/music/31 Tuned Percussion.aiff"
#fname='hebrides.aiff'
#fname='concerto_for_orchestra.aiff'
fname='magic_flute.aiff'  #this demonstrates pretty well
song,fs=read_song(fname)



songft=np.fft.rfft(song,axis=0)
tmax=song.shape[0]/fs
dnu=1/tmax
nuvec=np.arange(len(songft))*dnu
spl=CubicSpline(nu*1000,db)
mydb=spl(nuvec)
dist=1.0 #in km

atten=10**(-dist*mydb/10)
songft[:,0]=songft[:,0]*atten
songft[:,1]=songft[:,1]*atten
song_atten=np.fft.irfft(songft,song.shape[0],axis=0)
song_atten=np.asarray(song_atten,dtype='int16')

