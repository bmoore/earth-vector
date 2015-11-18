import compass
import csv

boundary = (43.125873, -70.853216)
rows = []

def build_diff(point1, point2):
    line = []
    distance = compass.haversine(point1, point2)
    bearing = compass.bearing(point1, point2)


    # This tests whether the first point is east or west of the boundary
    if (boundary[1] < point1[1]):
        if (bearing < 30 and bearing > 230):
            direction = 'Upstream'
        else:
            direction = 'Downstream'

    else:
        if (bearing < 270 and bearing > 120):
            direction = 'Upstream'
        else:
            direction = 'Downstream'

    if (boundary[1] < point1[1] and boundary[1] > point2[1]):
        direction = 'Upstream'

    if (boundary[1] > point1[1] and boundary[1] < point2[1]):
        direction = 'Downstream'

    line.append(distance)
    line.append(bearing)
    line.append(direction)

    return line


# Read the drifter.csv file into rows.
with open('drifter.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        try:
            # Map the columns to lat lon points
            lat = float(row[2])
            lon = float(row[1])
            rows.append((lat, lon))
        except ValueError as e:
            print e

# Walk the rows and get the distance, bearing, and orientation in regards to the boundary
sheet = []
for i, value in enumerate(rows):
    try:
        line = build_diff(rows[i],rows[i+1])
        sheet.append(','.join(map(str, line)))
    except (IndexError, ValueError) as e:
        print e

# Print the results
print "\n".join(sheet)
