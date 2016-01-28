import csv
import compass

point0 = ()
point1 = ()
with open('full-drifter.csv', 'rt') as csvfile:
    with open('full-drifter-output.csv', 'w') as output:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        writer = csv.writer(output, lineterminator='\n')
        for row in reader:
            try:
                lat = float(row[3])
                lng = float(row[4])
                point1 = (lat, lng)
                if point0:
                    distance = compass.haversine(point0, point1)
                    row.append(distance)
                point0 = point1
            except ValueError as e:
                print(e)

            writer.writerow(row)
