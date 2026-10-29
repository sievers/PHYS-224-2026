import numpy as np
from scipy.special import jn_zeros,jv
from matplotlib import pyplot as plt
plt.ion()


vec=np.linspace(-1,1,1001)
x,y=np.meshgrid(vec,vec)
r=np.sqrt(x**2+y**2)
th=np.arctan2(x,y)

n=3
m=5
lam_vec=jn_zeros(m,n+1)
lam=lam_vec[n-1]
u=jv(m,lam*r)*np.cos(m*th)
u[r>1]=np.nan
plt.ion()
plt.clf()
plt.imshow(u,vmin=-1,vmax=1)
plt.show()
print('lamda is: ',lam)
dt=0.01
th=np.linspace(0,2*np.pi,101)
xx=np.cos(th)
yy=np.sin(th)
for i in range(1000):
    t=dt*i;
    plt.clf()
    plt.imshow(u*np.cos(t*lam),vmin=-1,vmax=1,extent=[-1,1,-1,1])
    #plt.plot(xx,yy,'k')
    plt.pause(0.01)
    
