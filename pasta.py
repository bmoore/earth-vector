import csv
import mapper

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


for i, value in enumerate(river):
    try:
        mapper.plot(river[i], river[i+1])
    except (IndexError, ValueError) as e:
        print(e)

mapper.display()
