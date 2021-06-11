#!/usr/bin/env python3

from shapely.geometry import mapping, Polygon, LineString, Point

import geopandas as gpd
import matplotlib.pyplot as plt

import shapely
import fiona
import json

schema = {
    'geometry': 'Polygon',
    'properties': {'id': 'int'},
}

poly1 = Polygon([(0, 0), (0.1, 1), (1, 2), (0, 0)])
poly2 = Polygon([(0, 0), (2, 0), (1, 2), (0, 0)])

with fiona.open('../outfiles/my_shp2.json', 'w', 'GeoJSON', schema) as c:
    c.write({
        'geometry': mapping(poly1),
        'properties': {'id': 1},
    })
    c.write({
        'geometry': mapping(poly2),
        'properties': {'id': 2},
    })

with open('../outfiles/my_shp2.json') as f:
    data = json.load(f)
#print(json.dumps(data, indent=2))

shapes = gpd.read_file('../outfiles/my_shp2.json')
shapes.plot(column='id')
#plt.show()

print(shapes['geometry'])       # shapes[column] gives all lines of a column
display(shapes['geometry'][0])  # shapes[column][line]
