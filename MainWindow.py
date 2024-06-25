from PyQt6 import QtCore
import pyqtgraph as pg
import numpy as np
from PyQt6.QtWidgets import QMainWindow
from Wave1DSolver import Wave1DSolver
from functools import partial

class MainWindow(QMainWindow):
    def __init__(self,eq):
        super().__init__()
        self.plot_graph = pg.PlotWidget()
        self.setCentralWidget(self.plot_graph)
        self.eq = eq

        # Set axis labels and plot title
        self.setWindowTitle("Wave Main Window")
        self.plot_graph.getPlotItem().setLabel('left', 'u [m]')
        self.plot_graph.getPlotItem().setLabel('bottom', 'x [m]')
        self.plot_graph.getPlotItem().setTitle("Plot in function of time")


    def plot(self,eq: Wave1DSolver):
        self.eq = eq
        self.plot_graph.setXRange(eq.x0,eq.x1)
        self.plot_graph.setYRange(np.min(eq.Matrix()[0]),np.max(eq.Matrix()[0]))
        self.plot_graph.showGrid(x=True, y=True)
        self.eq.FullSolve()
        self.preLine = self.eq.Matrix()[-2]
        self.Line = self.eq.Matrix()[-1]

    def startSimulation(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(partial(self.updatePlot))
        self.timer.start()

    def stopSimulation(self):
        self.timer.stop()

    def updatePlot(self):
        forwardLine = self.eq.ForwardSolve(self.preLine,self.Line)
        self.plot_graph.plot(np.arange(self.eq.x0, self.eq.x1, self.eq.dx), forwardLine, clear=True)
        self.preLine = self.Line
        self.Line = forwardLine

    def mousePressEvent(self, event):
        # Obter posição na cena
        pos = event.scenePosition()

        # Map the position to the view coordinates (data coordinates)
        if self.plot_graph.sceneBoundingRect().contains(pos):
            mouse_point = self.plot_graph.plotItem.vb.mapSceneToView(pos)
            x = mouse_point.x()
            y = mouse_point.y()
            self.Line = self.eq.AddGaussianPulse(self.Line,x,y)
            self.preLine = self.eq.AddGaussianPulse(self.preLine,x,y)