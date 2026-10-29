import numpy as np
from scipy.special import jn_zeros,jv
from matplotlib import pyplot as plt
import sounddevice as sd
from scipy.interpolate import CubicSpline
import time

def setup_splines(nmax):
    xvec=np.linspace(0,100,20001)
    splines=[None]*(nmax+1)
    for i in range(nmax+1):
        yvec=jv(i,xvec)
        splines[i]=CubicSpline(xvec,yvec)
    return splines


def get_modes(n,m,r,th,splines=None):
    nmode=(2*m+1)*(n)
    out=np.zeros([len(r),nmode])
    icur=0
    freqs=np.zeros(nmode)
    phase=np.zeros(nmode) #handy dandy vec so we just have to take cosine
    for nn in range(1,n+1):
        for mm in range(m+1):
            #print('nn,mm are: ',nn,mm)
            lam_vec=jn_zeros(mm,nn+1)
            lam=lam_vec[nn-1]
            if splines is None:
                u=jv(mm,lam*r)
            else:
                u=splines[mm](lam*r)
            out[:,icur]=u*np.cos(mm*th)
            freqs[icur]=lam
            phase[icur]=0
            icur=icur+1
            if mm>0:
                out[:,icur]=u*np.sin(mm*th)
                freqs[icur]=lam
                phase[icur]=-np.pi/2
                icur=icur+1
            #print('nmode and icur are: ',nmode,icur)
    assert(icur==nmode)
    return out,freqs,phase
def vec2mat(vec,mask):
    tmp=np.zeros(len(mask))
    tmp[mask]=vec
    n=int(np.sqrt(len(mask)))
    return np.reshape(tmp,[n,n])

plt.ion()





vec=np.linspace(-1,1,501)
x,y=np.meshgrid(vec,vec)
r=np.sqrt(x**2+y**2)
th=np.arctan2(x,y)
rvec=np.ravel(r)
mask=rvec<=1
rvec=rvec[mask]
thvec=np.ravel(th)[mask]
nmax=15
mmax=15
splines=setup_splines(nmax)

t1=time.time()
modes,freqs,phase=get_modes(nmax,mmax,rvec,thvec,splines)
#modes2,freqs,phase=get_modes(nmax,mmax,rvec,thvec)
t2=time.time()
print('mode time: ',t2-t1)
#assert(1==0)

x_0=0.4
y_0=0.4
sig=0.05
z_init=np.exp(-0.5*( (x-x_0)**2+(y-y_0)**2)/sig**2)
zvec=np.ravel(z_init)[mask]
fitp=np.linalg.inv(modes.T@modes)@(modes.T@zvec)
pred=modes@fitp
pp=vec2mat(pred,mask)

#generate what we think the sound might be like
f0=50 #pick frequency of fundamental
ff=freqs/freqs.min()*f0
fs=44100
tmax=10
tvec=np.arange(fs*tmax)/fs
tot=0
for i in range(len(freqs)):
    tot=tot+np.abs(fitp[i])*np.sin(2*np.pi*ff[i]*tvec)
tau=0.2
tot=tot*np.exp(-tvec/tau)
    
sd.play(tot/tot.max(),fs)


plt.figure(3)
plt.clf()
plt.plot(freqs,fitp**2,'*')
plt.show()
plt.figure(2)
dt=0.01
for i in range(1000):
    t=dt*i;
    cur_vec=modes@(fitp*np.cos(t*freqs-0*phase))
    cur=vec2mat(cur_vec,mask)
    cur[r>1]=np.nan
    
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

