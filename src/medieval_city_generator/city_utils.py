#!/usr/bin/env python3

def get_surface(regions):
    """Return total surface of a set of areas."""
    r = sum([region.get_area() for region in regions])
    return r
