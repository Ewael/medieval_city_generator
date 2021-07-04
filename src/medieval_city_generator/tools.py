#!/usr/bin/env python3

import fiona
from shapely.geometry import MultiPolygon, mapping


def write_co(c, what):
    """Recursive function to write sub components of each area."""
    if what.components() == [what]: # if only subco is the co itself
        return
    for co in what.components(): # else rec call on each subco
        if type(co._polygon) == MultiPolygon:
            for p in co._polygon:
                c.write({
                    'geometry': mapping(p),
                    'properties': {'category': co._category.value},
                })
        else:
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
