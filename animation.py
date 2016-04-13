from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
import csv
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

map = Basemap(llcrnrlon=-70.96,llcrnrlat=43.,urcrnrlon=-70.55,urcrnrlat=43.2, projection='merc', resolution ='l')
fig = plt.figure()
ax = fig.add_subplot(111)
map.drawcoastlines()
map.drawcountries()
map.fillcontinents(color = 'gray')
map.drawmapboundary()
map.drawmeridians(np.arange(0, 360, 30))
map.drawparallels(np.arange(-90, 90, 30))

map.readshapefile('./n130', 'n130')
map.fillcontinents(color='#cccccc',lake_color='#ffffff')

timetext = ax.text(0.5, 50, '')

points = []
with open('pasta.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        try:
            if row[6]:
                points.append((float(row[6]), float(row[7])))
        except ValueError as e:
            print(e)

patches = []
for info, shape in zip(map.n130_info, map.n130):
    patches.append(Polygon(np.array(shape), True))
ax.add_collection(PatchCollection(patches, facecolor= '#ffffff', edgecolor='#ffffff', linewidths=0., zorder=2))

x,y = map(0, 0)
point = map.plot(x, y, 'ro', markersize=5)[0]
line = map.plot([], [], lw=2, color="red")[0]

def init():
    point.set_data([], [])
    line.set_data([], [])
    return point, line,

# animation function.  This is called sequentially
xs, ys = [], []
def animate(i):
    lons = float(points[i][1])
    lats = float(points[i][0])
    x, y = map(lons, lats)
    if (i == 0):
        xs[:] = ys[:] = []
    xs.append(x)
    ys.append(y)
    if (i > 0):
        line.set_data(xs, ys)
    point.set_data(x, y)
    timetext.set_text(i)
    return (point,timetext,line)

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(plt.gcf(), animate, init_func=init,
                               frames=len(points), interval=100, blit=True)

plt.show()
