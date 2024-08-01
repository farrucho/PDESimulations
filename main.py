from Wave1DFreeEndsSolver import Wave1DFreeEndsSolver
from Wave1DFixedEndsSolver import Wave1DFixedEndsSolver
from Wave2DFixedEndsSolver import Wave2DFixedEndsSolver
from Wave2DFreeEndsSolver import Wave2DFreeEndsSolver
from MainWindow import MainWindow
from PyQt6.QtWidgets import QApplication
import numpy as np
import sys

app = QApplication(sys.argv)
# eq = Wave1DFixedEndsSolver(0,1,0.001,0,5,0.02,1,0,0,lambda x: np.exp(-(x-2.5)**2/0.01)) # impulso
# eq = Wave1DFixedEndsSolver(0,1,0.01,0,4,0.001,0.1,0,0,lambda x: np.sin(x*2*math.pi/4)*np.sin(50*x)) # pacote de ondas
# eq = Wave1DFreeEndsSolver(0,3,0.01,0,4,0.001,0.1,lambda x: np.exp(-(x-2)**2/0.01)) # impulso
# eq = Wave1DFixedEndsSolver(0,1,0.01,0,4,0.001,0.1,0,0,lambda x: np.exp(-(x-2)**2/0.01)) # pacote de ondas

# eq = Wave2DFixedEndsSolver(0,0.5,0.01,0,1,0,1,0.005,0.2,0,0,0,0,lambda x, y: np.exp(-((y-0.5)**2/0.001) - ((x-0.5)**2/0.001)))
# eq = Wave2DFixedEndsSolver(0,0.5,0.01,0,1,0,1,0.005,0.2,0,0,0,0,lambda x, y: np.exp(-((y-0.5)**2/0.001) - ((x-0.5)**2/0.001))+np.exp(-((y-0.1)**2/0.001) - ((x-0.1)**2/0.001)))
eq = Wave2DFreeEndsSolver(0,0.5,0.01,0,1,0,1,0.005,0.2,lambda x, y: np.exp(-((y-0.5)**2/0.001) - ((x-0.5)**2/0.001)))

window = MainWindow(eq)

eq.FullSolve()

#2D


#3D
window.plot3D(eq)
# window.startSimulation(10)

window.show()
# app.exec()
