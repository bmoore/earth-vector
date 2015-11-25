import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
from mpl_toolkits.basemap import Basemap

# Great Bay 43.0669N, 70.8686W
m = Basemap(llcrnrlon=-70.96,llcrnrlat=43.,urcrnrlon=-70.55,urcrnrlat=43.2,
            projection='merc', resolution ='c')
fig = plt.figure()
ax = fig.add_subplot(111)
m.drawcoastlines()
m.drawmapboundary(fill_color='#99ffff')
m.readshapefile('./n130', 'n130')
m.fillcontinents(color='#cc9966',lake_color='#99ffff')
patches = []
for info, shape in zip(m.n130_info, m.n130):
    patches.append(Polygon(np.array(shape), True))
ax.add_collection(PatchCollection(patches, facecolor= '#99ffff', edgecolor='k', linewidths=0., zorder=2))

def plot(pointA, pointB):
    m.plot([pointA[1], pointB[1]], [pointA[0], pointB[0]], latlon=True, label='', linewidth=1.5, color='k')

def display():
    # draw coastlines, meridians and parallels.
    plt.title('Drifter Tracks (In Piscataqua River and Great Bay)')
    plt.show()