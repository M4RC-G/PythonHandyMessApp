import matplotlib
matplotlib.use('module://garden_matplotlib.backend_kivy')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from garden_matplotlib.backend_kivy import FigureCanvasKivy
from kivy.properties import OptionProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.clock import Clock

class Plot3D(BoxLayout):
    def __init__(self, **kwargs):
        super(Plot3D, self).__init__(**kwargs)
        fig = plt.figure()
        self.ax = fig.gca(projection="3d")
        self.ax.plot([],[],[])
        self.mpl_canvas = fig.canvas
        #plt.axis("off")
        self.add_widget(self.mpl_canvas)

    def plot(self,x ,y ,z):
        self.ax.plot(x, y, z)

        self.ax.plot(x, z,  zdir='y', zs=1.5)
        self.ax.plot(y, z,  zdir='x', zs=-0.5)
        self.ax.plot(x, y,  zdir='z', zs=-1.5)

        self.mpl_canvas.draw()







