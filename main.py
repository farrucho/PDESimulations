from Wave1DFreeEndsSolver import Wave1DFreeEndsSolver
from Wave1DFixedEndsSolver import Wave1DFixedEndsSolver
from MainWindow import MainWindow
from PyQt6.QtWidgets import QApplication
import numpy as np
import sys

app = QApplication(sys.argv)
#eq = Wave1DFixedEndsSolver(0,1,0.001,0,5,0.02,1,0,0,lambda x: np.exp(-(x-2.5)**2/0.01)) # impulso
# eq = Wave1DFixedEndsSolver(0,1,0.01,0,4,0.001,0.1,0,0,lambda x: np.sin(x*2*math.pi/4)*np.sin(50*x)) # pacote de ondas
eq = Wave1DFreeEndsSolver(0,3,0.01,0,4,0.001,0.1,lambda x: np.exp(-(x-2)**2/0.01)) # impulso

window = MainWindow(eq)

window.plot(eq)
# window.startSimulation()


window.show()
# app.exec()
