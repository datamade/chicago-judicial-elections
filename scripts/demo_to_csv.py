import json
import sys
import csv

geojson = json.load(sys.stdin)
writer = csv.DictWriter(sys.stdout,
                        fieldnames=('ward',
                                    'Total Population',
                                    'Not Hispanic or Latino Origin, Whites',
                                    'Not Hispanic or Latino Origin, Blacks',
                                    'Not Hispanic or Latino Origin, Asians',
                                    'Hispanic or Latino Origin',
                                    'Aggregate household income in the past 12 months',
                                    'Total households',
                                    'mean household income',
                                    'number of tracts'),
                        extrasaction='ignore')
writer.writeheader()

for feature in geojson['features']:
    properties = feature['properties']
    writer.writerow(properties)
    