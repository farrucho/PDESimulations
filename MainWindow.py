from PyQt6 import QtCore
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
from PyQt6.QtWidgets import QMainWindow,QVBoxLayout, QWidget
from functools import partial
from matplotlib import cm
from matplotlib.colors import Normalize

class MainWindow(QMainWindow):
    def __init__(self,eq):
        super().__init__()
        self.eq = eq
        self.setWindowTitle("Wave Main Window")


    def plot2D(self,eq): # eq: Wave1DSolver
        self.plot_graph = pg.PlotWidget()
        self.setCentralWidget(self.plot_graph)
        # Set axis labels and plot title
        self.plot_graph.getPlotItem().setLabel('left', 'u [m]')
        self.plot_graph.getPlotItem().setLabel('bottom', 'x [m]')
        self.plot_graph.getPlotItem().setTitle("Plot in function of time")
        self.eq = eq
        self.plot_graph.setXRange(eq.x0,eq.x1)
        self.plot_graph.setYRange(np.min(eq.Matrix()[0]),np.max(eq.Matrix()[0]))
        self.plot_graph.showGrid(x=True, y=True)
        self.eq.FullSolve()
        self.preLine = self.eq.Matrix()[0]
        self.Line = self.eq.Matrix()[1]

    def plot3D(self,eq): # eq: Wave2DSolver
        self.plot_graph =  gl.GLViewWidget()
        self.setCentralWidget(self.plot_graph)
        self.eq = eq

        ## create three grids, add each to the view
        xgrid = gl.GLGridItem()
        ygrid = gl.GLGridItem()
        zgrid = gl.GLGridItem()
        self.plot_graph.addItem(xgrid)
        self.plot_graph.addItem(ygrid)
        self.plot_graph.addItem(zgrid)

        ## rotate x and y grids to face the correct direction
        xgrid.rotate(90, 0, 1, 0)
        ygrid.rotate(90, 1, 0, 0)

        xgrid.setSize(2,2,2)
        ygrid.setSize(2,2,2)
        zgrid.setSize(2,2,2)


        x = np.linspace(self.eq.x0, self.eq.x1, self.eq.X)
        y = np.linspace(self.eq.y0, self.eq.y1, self.eq.Y)

        X, Y = np.meshgrid(x, y)
        Z = eq.S[0, :, :] 

        X_flat = X.flatten()
        Y_flat = Y.flatten()
        Z_flat = Z.flatten()

        # Combine into points for the GL plot
        pts = np.vstack([X_flat, Y_flat, Z_flat]).T

        # Normalize Z values to [0, 1] for color mapping
        norm = Normalize(vmin=0, vmax=Z_flat.max())
        self.colors = cm.magma(norm(Z_flat))  # https://matplotlib.org/stable/users/explain/colors/colormaps.html


        line = gl.GLLinePlotItem(pos=pts,color=self.colors)
        self.plot_graph.addItem(line)

        self.preLine = self.eq.Matrix()[0]
        self.Line = self.eq.Matrix()[1]



    def startSimulation(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(partial(self.updatePlot))
        self.timer.start()

    def stopSimulation(self):
        self.timer.stop()

    def updatePlot(self):
        if self.eq.S.ndim == 2:
            forwardLine = self.eq.ForwardSolve(self.preLine,self.Line)
            self.plot_graph.plot(np.arange(self.eq.x0, self.eq.x1, self.eq.dx), forwardLine, clear=True)
            self.preLine = self.Line
            self.Line = forwardLine
        else:
            forwardLine = self.eq.ForwardSolve(self.preLine,self.Line)
            x = np.linspace(self.eq.x0, self.eq.x1, self.eq.X)
            y = np.linspace(self.eq.y0, self.eq.y1, self.eq.Y)
            X, Y = np.meshgrid(x, y)
            Z = forwardLine

            X_flat = X.flatten()
            Y_flat = Y.flatten()
            Z_flat = Z.flatten()

            # Combine into points for the GL plot
            pts = np.vstack([X_flat, Y_flat, Z_flat]).T

            line = gl.GLLinePlotItem(pos=pts,color=self.colors)
            
            # apagar previous plottedlines
            for item in self.plot_graph.items:
                if isinstance(item, gl.GLLinePlotItem):
                    self.plot_graph.removeItem(item)

            self.plot_graph.addItem(line)


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
