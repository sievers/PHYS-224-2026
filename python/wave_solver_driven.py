import numpy as np
from matplotlib import pyplot as plt
plt.ion()

def bcs_tied(mystring):
    mystring.ypad[1:-1]=mystring.y
    mystring.ypad[0]=0
    mystring.ypad[-1]=0
    mystring.vpad[1:-1]=mystring.v
    mystring.vpad[0]=0
    mystring.vpad[-1]=0
def bcs_driven(mystring,om=0.009): #0.0185 does pretty well at 3rd mode,  0.006 looks to be fundamental
    mystring.ypad[1:-1]=mystring.y
    mystring.ypad[0]=0.2*np.sin(mystring.time*om)
    mystring.ypad[-1]=0
    mystring.vpad[1:-1]=mystring.v
    mystring.vpad[0]=0
    mystring.vpad[-1]=0
def bcs_random(mystring,dy=0.001,tau=0.99999): #0.0185 does pretty well at 3rd mode,  0.006 looks to be fundamental
    mystring.ypad[1:-1]=mystring.y
    #mystring.ypad[0]=0.2*np.sin(mystring.time*om)
    mystring.ypad[0]=(mystring.ypad[0]+dy*np.random.randn())*tau
    mystring.ypad[-1]=0
    mystring.vpad[1:-1]=mystring.v
    mystring.vpad[0]=0
    mystring.vpad[-1]=0

    

class String:
    def __init__(self,y,v=None,T=None,M=None,bcs=bcs_tied,dx=1):
        self.n=len(y)
        self.dx=dx #assume all points equally spaced
        self.bcs=bcs
        self.y=y.copy()
        self.ypad=np.zeros(self.n+2)
        self.time=0
        if v is None:
            self.v=np.zeros(self.n)
        else:
            self.v=v.copy()
        self.vpad=np.zeros(self.n+2)

            
        if T is None:
            self.T=np.ones(self.n)
        else:
            if np.isscalar(T):
                self.T=np.zeros(self.n)+T
            else:
                self.T=T.copy()
            
        if M is None:
            self.M=np.ones(self.n)
        else:
            if np.isscalar(M):
                self.M=np.zeros(self.n)+M
            else:
                self.M=M.copy()
        self.F=np.zeros(self.n)
    def get_forces(self):
        self.bcs(self) #get the boundary conditions
        curve=self.ypad[1:-1]-0.5*(self.ypad[:-2]+self.ypad[2:])
        self.F[:]=self.T*curve/self.dx**2
    def update(self,dt=0.01):
        self.time=self.time+dt
        self.get_forces()
        a=self.F/self.M
        
        self.y=self.y+self.v*dt
        self.v=self.v+a*dt
        self.y[-1]=0
        self.v[-1]=0
    def update_lax(self,alpha=1,dt=0.01):
        self.time=self.time+dt
        self.get_forces()
        a=self.F/self.M
        y0=(1-alpha)*self.y+0.5*alpha*(self.ypad[:-2]+self.ypad[2:])
        
        self.y=y0+self.v*dt
        v0=(1-alpha)*self.v+0.5*alpha*(self.vpad[:-2]+self.vpad[2:])
        
        self.v=v0-a*dt
        self.v[-1]=0
        self.y[-1]=0
        

x=np.arange(1024)[1:-1]
dx=(x[1]-x[0])*512/(len(x)+2)
M=dx
y=np.sin(x/len(x)*2*np.pi)
xx=x*dx
y=np.exp(-0.5*(xx-400)**2/20**2)

string=String(0*y,M=M,dx=dx,bcs=bcs_driven)
dt=0.01
nstep=100
plt.clf()
plt.plot(string.y)
plt.pause(0.01)
for i in range(10000):
    for j in range(nstep):
        string.update_lax(dt=dt,alpha=0.05*dt)
        #string.update(dt)
    plt.clf()
    plt.plot(string.y)
    plt.ylim([-1,1])
    plt.pause(0.01)
