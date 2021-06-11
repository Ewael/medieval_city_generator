#!/usr/bin/env python3

from shapely.geometry import mapping
import fiona

def write_co(c, what):
    if what.components() == [what]: # if only subco is the co itself
        return
    for co in what.components(): # else rec call on each subco
        c.write({
            'geometry': mapping(co._polygon),
            'properties': {'category': co._category.value},
        })
        write_co(c, co)

def json(what, filename):
    schema = {
        'geometry': 'Polygon',
        'properties': {'category': 'int'},
    }
    with fiona.open(filename, 'w', 'GeoJSON', schema) as c:
        write_co(c, what)
