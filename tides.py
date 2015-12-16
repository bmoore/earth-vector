import csv
import time

# Read the drifter.csv file into points.
tides = []
with open('tides.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        try:
            datetime = ' '.join([row[1], row[2]])
            datetime = time.strptime(datetime, '%m/%d/%y %I:%M %p')
            tides.append([time.mktime(datetime), datetime, row[3], row[4]])
        except ValueError as e:
            print(e)

tides = sorted(tides, key=lambda x: x[0])
