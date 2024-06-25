from Wave1DSolver import Wave1DSolver
from MainWindow import MainWindow
from PyQt6.QtWidgets import QApplication
import numpy as np
import sys

app = QApplication(sys.argv)
eq = Wave1DSolver(0,1,0.001,0,5,0.02,1,0,0,lambda x: np.exp(-(x-2.5)**2/0.01)) # impulso
window = MainWindow(eq)

window.plot(eq)
# window.startSimulation()


window.show()
# app.exec()
