#!/usr/bin/env python3

def get_surface(regions):
    r = sum([region.get_area() for region in regions])
    return r
