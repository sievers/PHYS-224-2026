import numpy as np
from matplotlib import pyplot as plt
import sounddevice as sd
plt.ion()

def get_modes_half(n,nmode):
    modes=np.zeros([n,nmode])
    k=np.zeros(nmode)
    x=np.linspace(0,np.pi,n)
    for i in range(nmode):
        k[i]=i+1
        modes[:,i]=np.sin(k[i]*x)
    return modes,k

def get_triangle(x,n):
    out=np.zeros(n)
    ii=int(x*n)
    out[:ii]=np.linspace(0,1,ii)
    out[ii:]=np.linspace(1,0,n-ii)
    return out

def spline_chunk(y,i1,i2):
    x=np.arange(i1-1,i2+2)
    xx=np.asarray([i1-1,i1,i2,i2+1])
    yy=np.asarray(y[xx])
    mat=np.zeros([4,4])
    mat[:,0]=1
    mat[:,1]=xx
    mat[:,2]=xx**2
    mat[:,3]=xx**3
    fitp=np.linalg.inv(mat)@yy
    tmp=np.zeros([len(x),4])
    tmp[:,0]=1
    tmp[:,1]=x
    tmp[:,2]=x**2
    tmp[:,3]=x**3
    pred=tmp@fitp
    print(tmp.shape,fitp.shape)
    out=y.copy()
    out[i1-1:i2+2]=pred
    return out

n=1001
nmode=25
xpeak=0.2
y=get_triangle(xpeak,n)
dx=0.1
i1=int((xpeak-dx)*n)
i2=int((xpeak+dx)*n)
ysmooth=spline_chunk(y,i1,i2)


modes,k=get_modes_half(n,nmode)
amps=np.linalg.inv(modes.T@modes)@(modes.T@y)
amps2=np.linalg.inv(modes.T@modes)@(modes.T@ysmooth)
plt.clf()
plt.semilogy(k,amps**2,'r*')
plt.plot(k,amps2**2,'bo')
plt.legend(['Triangle','Smoothed'])
plt.pause(0.01)

y=ysmooth
amps=amps2

tmax=10
fs=44100
t=np.arange(tmax*fs)/fs
tot=0
nu0=220 #frequency of fundamental
for i in range(nmode):
    freq=nu0*k[i]
    tot=tot+np.sin(2*np.pi*freq*t)*amps2[i]
tot=tot/tot.max()*0.5
    
if True:
    sd.play(tot,fs)    
    sd.wait()
if True:
    for i in range(1,nmode):
        pred=modes[:,:i]@amps[:i]
        plt.clf()
        plt.plot(y)
        plt.plot(pred)
        plt.plot(modes[:,i-1]*amps[i-1])
        plt.pause(2)

if True:
    dt=0.01
    for i in np.arange(1000):
        t=dt*i
        vec=amps*np.cos(t*k)
        cur=modes@vec
        plt.clf()
        plt.plot(cur)
        plt.ylim(-1,1)
        plt.pause(0.01)
