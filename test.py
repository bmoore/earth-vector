import compass
import mapper
import csv

boundary = (43.125873, -70.853216)
points = []

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

    # This tests whether the first point is east or west of the boundary
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

    if (direction is 'Downstream' ):
        distance = distance * -1
        velocity = velocity * -1

    diff.append(place)
    diff.append(distance)
    diff.append(bearing)
    diff.append(velocity)
    diff.append(direction)
    diff.append(minutes)
    diff.append(point1[3])
    diff.append(point1[0])
    diff.append(point1[1])

    mapper.plot(point1, point2)

    return diff


# Read the drifter.csv file into points.
with open('drifterfinal.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        try:
            # Map the columns to lat lon points
            lat = float(row[2])
            lon = float(row[1])
            timestamp = int(row[4])
            trial = (row[3])
            points.append((lat, lon, timestamp, trial))
        except ValueError as e:
            print e

# Walk the points and get the distance, bearing, and orientation in regards to the boundary
sheet = []
for i, value in enumerate(points):
    try:
        line = build_diff(points[i],points[i+1])
        sheet.append(line)
    except (IndexError, ValueError) as e:
        print e

with open("output.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in sheet:
        writer.writerow(val)

mapper.display()
