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
    #print(tmp.shape,fitp.shape)
    out=y.copy()
    out[i1-1:i2+2]=pred
    return out





n=1001
nmode=45

#generate a triangle with a smoothed top
xpeak=0.2 #where along the string we pluck
dx=0.01   #how "fat" our finger is
y=get_triangle(xpeak,n)
i1=int((xpeak-dx)*n)
i2=int((xpeak+dx)*n)
ysmooth=spline_chunk(y,i1,i2)

#now find how much of each mode is in our plucked string

amps=np.zeros(nmode)
modes=np.zeros([nmode,n])
x=np.linspace(0,np.pi,n)
for i in range(nmode):
    modes[i,:]=np.sin(x*(i+1))
    amps[i]=2*np.mean(modes[i,:]*ysmooth)
pred=modes.T@amps
plt.clf()
plt.plot(ysmooth)
plt.plot(pred)
plt.show()

tmax=10
fs=44100
t=np.arange(tmax*fs)/fs

nu0=220
tot=0
tau_rel=1/(2+np.arange(nmode))

tau_f =0.7#time constant of fundamental
tau=tau_f*(tau_rel/tau_rel[0])**2
       

for i in range(nmode):
    tot=tot+amps[i]*np.sin(2*np.pi*t*(i+1)*nu0)*np.exp(-t/tau[i])

sd.play(tot/tot.max())
