import numpy as np

class Wave1DFixedEndsSolver:
    def __init__(self,t0,t1,dt,x0,x1,dx,v,ux0,ux1,ut0):
        self.t0 = t0
        self.t1 = t1
        self.dt = dt
        self.x0 = x0
        self.x1 = x1
        self.dx = dx
        self.v = v
        self.ux0 = ux0
        self.ux1 = ux1
        self.ut0 = ut0
        self.stability = dx/(v**2) - dt
        self.N = int((t1-t0)/dt)
        self.M = int((x1-x0)/dx)
        self.S = np.zeros((self.N,self.M))
        self.r = pow(v*dt/dx,2)


    def Stability(self):
        print("esta estavel", self.stability) if self.stability > 0 else print("NAO esta estavel",self.stability)
        return self.stability


    def AddGaussianPulse(self,line,pulseX,pulseY):
        if pulseX > self.x0 and pulseX < self.x1: 
            defaultPulse = lambda x: pulseY*np.exp(-(x-pulseX)**2/0.01)
            for xj in range(0,self.M):
                line[xj] +=  defaultPulse(xj*self.dx)
            return line
        return line


    def Matrix(self):
        return self.S


    def FullSolve(self):
        # u(0,t) u(1,t) 
        self.S[:,0] = self.ux0
        self.S[:,self.M-1] = self.ux1

        # u(x,0)
        for xj in range(0,self.M):
            self.S[0,xj] =  self.ut0(xj*self.dx)

        # du(x,0)/dt = 0 ta em repouso a corda
        # corrigir algoritmo geral para u(x,t=1)
        for xj in range (1,self.M-1):
            self.S[1,xj] = self.r*(self.S[0,xj-1]-2*self.S[0,xj]+self.S[0,xj+1])/2 + self.S[0,xj]

        # Algoritmo ao resto da matrix:
        for tj in range (1,self.N-1):
            for xj in range(1,self.M-1):
                self.S[tj+1,xj] = self.r*(self.S[tj,xj-1]-2*self.S[tj,xj]+self.S[tj,xj+1]) + 2*self.S[tj,xj] - self.S[tj-1,xj]

    def ForwardSolve(self,preLine,Line):
        forwardLine = preLine
        forwardLine[0] = self.ux0
        forwardLine[-1] = self.ux1

        for xj in range(1,self.M-1):
            forwardLine[xj] = self.r*(Line[xj-1]-2*Line[xj]+Line[xj+1]) + 2*Line[xj] - preLine[xj]
        
        return forwardLine
