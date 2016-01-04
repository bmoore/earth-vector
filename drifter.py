import csv
import math
import time
import compass
import helpers
from tides import tides

def stream_direction(point1, point2, bearing):
    # This tests whether the first point is east or west of the boundary
    boundary = (43.125873, -70.853216)
    if (boundary[1] < point1[1]):
        place = "in river"
        if (bearing < 60 or bearing > 240):
            direction = 'Upstream'
        else:
            direction = 'Downstream'
    else:
        place = "in bay"
        if (bearing < 270 and bearing > 90):
            direction = 'Upstream'
        else:
            direction = 'Downstream'

    if (boundary[1] < point1[1] and boundary[1] > point2[1]):
        direction = 'Upstream'

    if (boundary[1] > point1[1] and boundary[1] < point2[1]):
        direction = 'Downstream'

    return direction, place

@helpers.static_vars(index=0, tide=[], direction='I', t0=[], cycle={})
def tide_at_point(point):
    trial = point[3]
    if trial not in tide_at_point.cycle.keys():
        tide_at_point.cycle.update({trial: {}})
    tide_at_point.tide = tides[tide_at_point.index]
    tide_time = tide_at_point.tide[0]
    point_time = point[2]

    fresh = False
    while point_time > tide_time:
        fresh = True
        tide_at_point.t0 = tide_at_point.tide
        tide_at_point.index += 1
        tide_at_point.tide = tides[tide_at_point.index]
        tide_time = tide_at_point.tide[0]

        if tide_at_point.t0[3] is 'L' and tide_at_point.tide[3] is 'H':
            tide_at_point.direction = 'I'
        else:
            tide_at_point.direction = 'O'

    time_offset = point_time - tide_at_point.t0[0]
    tide_cycle = ''.join([tide_at_point.direction, str(int(math.ceil(time_offset/3600)))])
    if tide_cycle not in tide_at_point.cycle[trial].keys():
        tide_at_point.cycle[trial].update({tide_cycle:0})
    if fresh:
        tide_at_point.cycle[trial][tide_cycle] += 1
    return time_offset, tide_at_point.direction, tide_cycle, '-'.join([tide_cycle, str(tide_at_point.cycle[trial][tide_cycle])])

# Build a list that is the difference between the points
def build_diff(point1, point2):
    trial_1 = point1[3]
    trial_2 = point2[3]
    if (trial_1 is not trial_2):
        return []

    diff = []
    distance = compass.haversine(point1, point2)
    bearing = compass.bearing(point1, point2)
    velocity =  compass.velocity(point1, point2)
    minutes = (point2[2] - point1[2]) / 60
    direction, place = stream_direction(point1, point2, bearing)
    tide_time_offset, tide, tide_offset, tide_offset_lap = tide_at_point(point1)

    if (direction is 'Downstream' ):
        distance = distance * -1
        velocity = velocity * -1

    diff.append(place)
    diff.append(distance)
    diff.append(bearing)
    diff.append(velocity)
    diff.append(direction)
    diff.append(minutes)
    diff.append(point1[4])
    diff.append(tide)
    diff.append(tide_time_offset)
    diff.append(tide_offset)
    diff.append(tide_offset_lap)
    diff.append(point1[3])
    diff.append(point1[0])
    diff.append(point1[1])

    return diff

points = []
# Read the drifter.csv file into points.
with open('drifter.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        try:
            # Map the columns to lat lon points
            lat = float(row[2])
            lon = float(row[1])
            datetime = time.strptime(row[4], '%Y-%m-%d %H:%M:%S')
            timestamp = time.mktime(datetime)
            trial = (row[3])
            points.append((lat, lon, timestamp, trial, row[4]))
        except ValueError as e:
            print(e)

points = sorted(points, key=lambda x: x[2])
