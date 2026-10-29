import numpy as np
from scipy.special import jn_zeros,jv
from matplotlib import pyplot as plt
import sounddevice as sd
from scipy.interpolate import CubicSpline
import time
def get_modes(x,y,kmax):
    n=len(x)
    nmode=(kmax)**2
    out=np.zeros([n,nmode])
    icur=0
    freqs=np.zeros(nmode)
    for kx in range(1,kmax+1):
        for ky in range(1,kmax+1):
            k=np.sqrt(kx**2+ky**2)
            out[:,icur]=np.sin(np.pi/2*kx*(x+1))*np.sin(np.pi/2*ky*(y+1))
            freqs[icur]=k
            icur=icur+1
    assert(icur==nmode)
    return out,freqs

def vec2mat(vec):
    n=int(np.sqrt(len(vec)))
    return np.reshape(vec,[n,n])

plt.ion()


n=501
vec=np.linspace(-1,1,n)
xx,yy=np.meshgrid(vec,vec)
kmax=15
x=np.ravel(xx)
y=np.ravel(yy)
modes,freqs=get_modes(x,y,kmax)
fwee=np.reshape(modes[:,1*kmax+0],[n,n])

x_0=0.0
y_0=0.0
sig=0.2
zvec=np.exp(-0.5*( (x-x_0)**2+(y-y_0)**2)/sig**2)
fitp=np.linalg.inv(modes.T@modes)@(modes.T@zvec)
pred=modes@fitp
pp=vec2mat(pred)

#generate what we think the sound might be like
f0=100 #pick frequency of fundamental
ff=freqs/freqs.min()*f0
fs=44100
tmax=5
tvec=np.arange(fs*tmax)/fs
tot=0
for i in range(len(freqs)):
    tot=tot+np.abs(fitp[i])*np.sin(2*np.pi*ff[i]*tvec)


tau=1
tot=tot*np.exp(-tvec/tau)
if True:
    sd.play(tot/tot.max(),fs)
    sd.wait()

plt.figure(3)
plt.clf()
plt.plot(freqs,fitp**2,'*')
plt.show()
plt.figure(2)
dt=0.01
for i in range(1000):
    t=dt*i;
    cur_vec=modes@(fitp*np.cos(t*freqs))
    cur=vec2mat(cur_vec)
    #cur[r>1]=np.nan
    
    plt.clf()
    plt.imshow(cur,vmin=-0.5,vmax=0.5,extent=[-1,1,-1,1])
    plt.axis('off')
    #plt.plot(xx,yy,'k')
    plt.pause(0.01)

    

#d2f/dt^2=c^2 d2f/dx^2 - bdf/dt
# A''Y = c^2 Y''A - b A' Y
# A''/A +bA'/A = c^2 Y''/Y
# A''/A + bA'/A = -c^2k^2 = -om^2
# A'' + b A' + om^2 A = 0
# A=exp(wt)
#w^2 + bw + om^2 = 0
#w=-b +/- sqrt(b^2-4om^2)/2
#A=exp(-bt/2)sin/cos(om't), om' = sqrt(om^2-b^2/4)

#A'' + bA'^2 + om^2 A
#A=exp(wt), w^2 exp(wt)+bw^2 exp(2wt) + om^2 exp(wt)=0
#w^2 + bw^2 exp(wt) + om^2 = 0
#exp(wt) ~ 

