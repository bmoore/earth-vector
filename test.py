import csv
from drifter import points, build_diff

# Walk the points and get the distance, bearing, and orientation in regards to the boundary
sheet = []
for i, value in enumerate(points):
    try:
        line = build_diff(points[i],points[i+1])
        sheet.append(line)
    except (IndexError, ValueError) as e:
        print(e)

with open("output.csv", "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in sheet:
        writer.writerow(val)

