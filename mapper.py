import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
from mpl_toolkits.basemap import Basemap

class Mapper:
    def __init__(self):
        # Great Bay 43.0669N, 70.8686W
        self.m = Basemap(llcrnrlon=-70.96,llcrnrlat=43.,urcrnrlon=-70.55,urcrnrlat=43.2, projection='merc', resolution ='f')
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.m.drawmapboundary(fill_color='#ffffff')
        self.m.readshapefile('./n130', 'n130')
        self.m.fillcontinents(color='#cccccc',lake_color='#ffffff')

        self.patches = []
        for info, shape in zip(self.m.n130_info, self.m.n130):
            self.patches.append(Polygon(np.array(shape), True))
        self.ax.add_collection(PatchCollection(self.patches, facecolor= '#ffffff', edgecolor='#ffffff', linewidths=0., zorder=2))

    def plot(self, pointA, pointB):
        self.m.plot([pointA[1], pointB[1]], [pointA[0], pointB[0]], latlon=True, label='', linewidth=1, color='#666666')

    def trace(self, points):
        for i, value in enumerate(points):
            try:
                self.plot(points[i], points[i+1])
            except (IndexError, ValueError) as e:
                print(e)
        self.m.plot(points[0][1], points[0][0], latlon=True, label='', marker='*', linewidth=.5, color='k')
        self.m.plot(points[i][1], points[i][0], latlon=True, label='', marker='8', linewidth=.5, color='k')

    def display(self, name):
        # draw coastlines, meridians and parallels.
        plt.savefig('.'.join([name, 'pdf']), format='pdf')
