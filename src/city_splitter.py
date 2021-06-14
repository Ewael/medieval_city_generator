#!/usr/bin/env python3

from shapely.geometry import mapping, Polygon, Point, LineString, MultiPolygon
from scipy.spatial import Voronoi, voronoi_plot_2d

import numpy as np
import random
import logging

from area import Category, Area, generate_perimeter

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def generate_regions(N, radius, limit, min_surface):
    """
    Generate random regions, loop while one region has an area < min_surface.
    """
    while True:
        points = np.array([[x,y] for x in np.linspace(-1,1,N) for y in np.linspace(-1,1,N)])
        points *= radius
        points += np.random.random((len(points), 2)) * (radius / 3)

        # build initial regions from generated points
        vor = Voronoi(points)
        regions = [r for r in vor.regions if -1 not in r and len(r) > 0]
        regions = [Polygon([vor.vertices[i] for i in r]) for r in regions]
        regions = [r for r in regions if limit.contains(r)]

        # check surfaces
        isgood = True
        for r in regions:
            if r.area < min_surface:
                logging.info(f"Regenerating, area is too small: {r.area}")
                isgood = False
                break
        if isgood:
            return regions


def split_city(city, N, radius, limit, min_surface):
    """
    Split inner and outer regions of the city.
    """
    regions = generate_regions(N, radius, limit, min_surface)

    walls = generate_perimeter(radius / 1.9)
    categories = [Category.HOUSE if walls.contains(r) else Category.FARM for r in regions]

    inner_city, outer_city = [], []
    for r in regions:
        area = Area(r, Category.HOUSE if walls.contains(r) else Category.FARM)
        city.add_subco(area)
        if area.category == Category.HOUSE:
            inner_city.append(area)
        else: # FARM
            outer_city.append(area)

    return inner_city, outer_city


"""
Buildings:
    HOUSE = 10
    MANSION = 11
    MARKET = 12
    TOWNHALL = 13
    UNIVERSITY = 14
    CHURCH = 20
    CATHEDRAL = 21
    MONASTRY = 22
    FORT = 31
    CASTLE = 32
    CHATEAU = 33
    STREET = 50
    BRIDGE = 51
Nature:
    LAND = 1
    FIELD = 2
    FOREST = 3
    RIVER = 4
    LAKE = 5
    SEA = 6
    PARK = 7
    GARDEN = 8
    FARM = 15
"""
