import numpy as np
from matplotlib import pyplot as plt
plt.ion()


xmax=20
lamda=1
k=2*np.pi/lamda

xvec=np.linspace(-xmax,xmax,1001)
xmat,ymat=np.meshgrid(xvec,xvec)

v=1
dt=0.1
omega=v*k


#pos=[[0,0]] #this line gives you a single source at the origin

pos=[[2,0],[-2,0,0.0]] #this line gives you two sources, but radiating in-phase
#pos=[[0,-0.1,0],[0,0.1,0.0]] #this line gives you two very close sources.  in vs out of phase will look quite different
#pos=[[0,0,0],[0,0,0],[0.1,0,0.5],[-0.1,0,0.5]] #gives a brighter central source, with two close neighbor.  Behavior again is very different if in-phase or out-of-phase
#pos=[[-2,0,0],[-1.5,0,0],[-1,0,0],[-0.5,0,0],[0,0,0],[0.5,0,0],[1,0,0],[1.5,0,0],[2,0,0]]

#xx=np.linspace(-6,6,21);pos=[[xxx,0,0] for xxx in xx] #gives you a source at every point in xx


nsrc=len(pos)
out=0
plt.clf()
t=0
rmat=[None]*len(pos)
for i in range(nsrc):
    dx=xmat-pos[i][0]
    dy=ymat-pos[i][1]
        
    rmat[i]=np.sqrt(dx**2+dy**2)
    
while True:
    tot=0
    for i in range(nsrc):
        phi=0 #this is in wavelengths, not radians
        if len(pos[i])>2:
            phi=pos[i][2]

        tot=tot+np.sin(k*rmat[i]-omega*t+2*np.pi*phi)
    t=t+dt
    plt.clf();
    plt.imshow(tot,extent=[xvec[0],xvec[-1],xvec[-1],xvec[0]],vmin=-nsrc,vmax=nsrc)
    #plt.imshow(tot,extent=[xvec[0],xvec[-1],xvec[-1],xvec[0]])
    for i in range(nsrc):
        plt.plot(pos[i][0],pos[i][1],'r*')
    plt.pause(0.01)
    
    
