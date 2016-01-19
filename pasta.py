import csv
from mapper import Mapper

river = []
lower = []
upper = []

with open('pasta.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        try:
            if row[0]:
                river.append((float(row[0]), float(row[1])))
            if row[3]:
                lower.append((float(row[3]), float(row[4])))
            if row[6]:
                upper.append((float(row[6]), float(row[7])))
        except ValueError as e:
            print(e)

river_map = Mapper()
river_map.trace(river)
river_map.display('river')

lower_map = Mapper()
lower_map.trace(lower)
lower_map.display('lower')

upper_map = Mapper()
upper_map.trace(upper)
upper_map.display('upper')
