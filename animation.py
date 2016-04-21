from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
import csv
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

map = Basemap(llcrnrlon=-70.96,llcrnrlat=43.,urcrnrlon=-70.55,urcrnrlat=43.2, projection='merc', resolution ='f')
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

points = []
with open('drifter.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        try:
            if row[2] and row[3] == 'LB52':
                lat, lon = float(row[2]), float(row[1])
                if lat > 10 and lon < 10:
                    points.append((float(row[2]), float(row[1]), row[3], row[4]))
        except ValueError as e:
            print(e)

other_points = []
river = []
lb = []
ub = []
with open('pasta.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        try:
            if row[0]:
                river.append((float(row[0]), float(row[1])))
            if row[3]:
                lb.append((float(row[3]), float(row[4])))
            if row[6]:
                ub.append((float(row[6]), float(row[7])))
        except ValueError as e:
            print(e)

other_points = river + lb + ub

patches = []
for info, shape in zip(map.n130_info, map.n130):
    patches.append(Polygon(np.array(shape), True))
ax.add_collection(PatchCollection(patches, facecolor= '#ffffff', edgecolor='#ffffff', linewidths=1., zorder=2))

x,y = map(0, 0)
line = map.plot([], [], 'r', lw=2, zorder=5)[0]
point = map.plot(x, y, 'bo', markersize=5, zorder=10)[0]
font = {'family': 'sans-serif',
        'color': 'black',
        'weight': 'bold',
        'size': 24,
        }
runtext = ax.text(4000, 2000, '', fontdict=font)

start = map.plot(x, y, 'bo', markersize=5, zorder=10)[0]
end = map.plot(x, y, 'bo', markersize=5, zorder=10)[0]

def init():
    point.set_data([], [])
    line.set_data([], [])
    return line, point,

xs, ys = [], []
runs = []
# This animation function is for the drifter.csv tracks
#def animate(i):
#    lons = float(points[i][1])
#    lats = float(points[i][0])
#    x, y = map(lons, lats)
#    if (points[i][2] not in runs):
#        runs[:] = []
#        runs.append(points[i][2])
#        xs[:] = ys[:] = []
#    xs.append(x)
#    ys.append(y)
#    if (i > 0):
#        line.set_data(xs, ys)
#    point.set_data(x, y)
#    runtext.set_text(points[i][2])
#    return (runtext,line,point)

# This animation function is for the pasta.csv tracks
def animate(i):
    lons = float(river[i][1])
    lats = float(river[i][0])
    x, y = map(lons, lats)
    if not i:
        xs[:] = ys[:] = []
    xs.append(x)
    ys.append(y)
    if (i > 0):
        line.set_data(xs, ys)
    point.set_data(x, y)
    runtext.set_text('River')
    return (runtext,line,point)

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(plt.gcf(), animate, init_func=init,
                               frames=len(river), interval=50, blit=True)

anim.save('animation.gif',writer='imagemagick',fps=30)
#plt.show()
