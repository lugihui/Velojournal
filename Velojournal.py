import csv

with open('Journal.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    kilometer_total = 0.0
    aufstieg_total = 0
    abstieg_total = 0

    for line in csv_reader:
        kilometer_total = kilometer_total + float(line['Kilometer'])
        aufstieg_total = aufstieg_total + int(line['Aufstieg'])
        abstieg_total = abstieg_total + int(line['Abstieg'])

    print(f"Gefahrene Strecke in Kilometer: {kilometer_total}")
    print(f"Aufstieg in Höhenmeter: \t{aufstieg_total}")
    print(f"Abstieg in Höhenmeter: \t\t{abstieg_total}")
