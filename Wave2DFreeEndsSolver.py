import numpy as np

class Wave2DFreeEndsSolver:
    # IMPLEMENTAR BARREIRAS QUE FAZ FUNCAO VELOCIDADE POR RAMOS
    def __init__(self,t0,t1,dt,x0,x1,y0,y1,dq,v,ut0):
        self.t0 = t0
        self.t1 = t1
        self.dt = dt
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
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
        # u(x,0)
        for xj in range(0,self.X):
            for yj in range(0,self.Y):
                self.S[0,xj,yj] = self.ut0(xj*self.dq,yj*self.dq)

        # free ends em t=1
        for xj in range(0,self.X):
            for yj in range(0,self.Y):
                u_x_y_0 = self.S[0,xj,yj]
                try:
                    u_xmenos1_y_0 = self.S[0,xj-1,yj]
                except:
                    u_xmenos1_y_0 = self.S[0,xj+1,yj]
                try:
                    u_xmais1_y_0 = self.S[0,xj+1,yj]
                except:
                    u_xmais1_y_0 = self.S[0,xj-1,yj]
                try:
                    u_x_ymenos1_0 = self.S[0,xj,yj-1]
                except:
                    u_x_ymenos1_0 = self.S[0,xj,yj+1]
                try:
                    u_x_ymais1_0 = self.S[0,xj,yj+1]
                except:
                    u_x_ymais1_0 = self.S[0,xj,yj-1]

                self.S[1,xj,yj] = u_x_y_0 + self.r*0.5*(u_xmenos1_y_0-4*u_x_y_0+u_xmais1_y_0+u_x_ymenos1_0+u_x_ymais1_0)


        # Algoritmo ao resto da matrix:
        for tj in range(1,self.T-1):
            for xj in range(0,self.X):
                for yj in range(0,self.Y):
                    # derivada nos boundaries é 0, loop geral com try except previne erro
                    u_x_y_0 = self.S[tj,xj,yj]
                    try:
                        u_xmenos1_y_0 = self.S[tj,xj-1,yj]
                    except:
                        u_xmenos1_y_0 = self.S[tj,xj+1,yj]
                    try:
                        u_xmais1_y_0 = self.S[tj,xj+1,yj]
                    except:
                        u_xmais1_y_0 = self.S[tj,xj-1,yj]
                    try:
                        u_x_ymenos1_0 = self.S[tj,xj,yj-1]
                    except:
                        u_x_ymenos1_0 = self.S[tj,xj,yj+1]
                    try:
                        u_x_ymais1_0 = self.S[tj,xj,yj+1]
                    except:
                        u_x_ymais1_0 = self.S[tj,xj,yj-1]

                    self.S[tj+1,xj,yj] = 2*u_x_y_0 - self.S[tj-1,xj,yj] + self.r*(u_xmenos1_y_0-4*u_x_y_0+u_xmais1_y_0+u_x_ymenos1_0+u_x_ymais1_0)



    def Matrix(self):
        return self.S


    def ForwardSolve(self,preLine,Line):
        forwardLine = preLine
        
        for xj in range(0,self.X):
            for yj in range(0,self.Y):
                # derivada nos boundaries é 0, loop geral com try except previne erro
                u_x_y_0 = Line[xj,yj]
                try:
                    u_xmenos1_y_0 = Line[xj-1,yj]
                except:
                    u_xmenos1_y_0 = Line[xj+1,yj]
                try:
                    u_xmais1_y_0 = Line[xj+1,yj]
                except:
                    u_xmais1_y_0 = Line[xj-1,yj]
                try:
                    u_x_ymenos1_0 = Line[xj,yj-1]
                except:
                    u_x_ymenos1_0 = Line[xj,yj+1]
                try:
                    u_x_ymais1_0 = Line[xj,yj+1]
                except:
                    u_x_ymais1_0 = Line[xj,yj-1]

                forwardLine[xj,yj] = 2*u_x_y_0 - preLine[xj,yj] + self.r*(u_xmenos1_y_0-4*u_x_y_0+u_xmais1_y_0+u_x_ymenos1_0+u_x_ymais1_0)

        return forwardLine
