import numpy as np

class Wave2DFixedEndsSolver:
    # IMPLEMENTAR BARREIRAS QUE FAZ FUNCAO VELOCIDADE POR RAMOS
    def __init__(self,t0,t1,dt,x0,x1,y0,y1,dq,v,ux0,ux1,uy0,uy1,ut0):
        self.t0 = t0
        self.t1 = t1
        self.dt = dt
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.ux0 = ux0
        self.ux1 = ux1
        self.uy0 = uy0
        self.uy1 = uy1
        self.dq = dq
        self.v = v
        self.T = int((t1-t0)/dt)
        self.X = int((x1-x0)/dq)
        self.Y = int((y1-y0)/dq)
        self.S = np.zeros((self.T,self.X,self.Y))
        self.ut0 = ut0
        self.stability = dq/(v**2) - dt
        self.r = pow(v*dt/dq,2)


    def Stability(self):
        print("esta estavel", self.stability) if self.stability > 0 else print("NAO esta estavel",self.stability)
        return self.stability


    def FullSolve(self):
        # u(t,0,y) u(t,1,y) 
        self.S[:,0,:] = self.ux0
        self.S[:,self.X-1,:] = self.ux1

        # u(t,x,0) u(t,x,1) 
        self.S[:,:,0] = self.uy0
        self.S[:,:,self.Y-1] = self.uy1

        # u(0,x,y)
        for xj in range(0,self.X):
            for yj in range(0,self.Y):
                self.S[0,xj,yj] = self.ut0(xj*self.dq,yj*self.dq)

        # corrigir algoritmo geral para u(x,t=1)
        for xj in range(1,self.X-1):
            for yj in range(1,self.Y-1):
                self.S[1,xj,yj] = self.S[0,xj,yj] + self.r*(self.S[0,xj-1,yj]-2*self.S[0,xj,yj]+self.S[0,xj+1,yj]+self.S[0,xj,yj-1]-2*self.S[0,xj,yj]+self.S[0,xj,yj+1])/2

        # Algoritmo ao resto da matrix:
        for tj in range(1,self.T-1):
            for xj in range(1,self.X-1):
                for yj in range(1,self.Y-1):
                    self.S[tj+1,xj,yj] = 2*self.S[tj,xj,yj] - self.S[tj-1,xj,yj] + self.r*(self.S[tj,xj-1,yj]-2*self.S[tj,xj,yj]+self.S[tj,xj+1,yj]+self.S[tj,xj,yj-1]-2*self.S[tj,xj,yj]+self.S[tj,xj,yj+1])


    # def AddGaussianPulse(self,line,pulseX,pulseY):
    #     if pulseX > self.x0 and pulseX < self.x1: 
    #         defaultPulse = lambda x: pulseY*np.exp(-(x-pulseX)**2/0.01)
    #         for xj in range(0,self.M):
    #             line[xj] +=  defaultPulse(xj*self.dx)
    #         return line
    #     return line


    def Matrix(self):
        return self.S


    def ForwardSolve(self,preLine,Line):
        forwardLine = preLine
        forwardLine[0,:] = self.ux0
        forwardLine[-1,:] = self.ux1
        forwardLine[:,0] = self.uy0
        forwardLine[:,-1] = self.uy1

        
        for xj in range(1,self.X-1):
            for yj in range(1,self.Y-1):
                forwardLine[xj,yj] = 2*Line[xj,yj] - preLine[xj,yj] + self.r*(Line[xj-1,yj]-2*Line[xj,yj]+Line[xj+1,yj]+Line[xj,yj-1]-2*Line[xj,yj]+Line[xj,yj+1])

        return forwardLine
