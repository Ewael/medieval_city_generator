#!/usr/bin/env python3

import logging
import random

import numpy as np
from area import Area, Category, generate_perimeter
from scipy.spatial import Voronoi, voronoi_plot_2d
from shapely.geometry import LineString, MultiPolygon, Point, Polygon, mapping

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def generate_regions(N, radius, limit, min_surface, nb_small):
    """Generate random regions, loop while one region has nb_small areas < min_surface."""
    while True:
        # generation points for voronoi split
        points = np.array([[x,y] for x in np.linspace(-1,1,N) for y in np.linspace(-1,1,N)])
        points *= radius
        points += np.random.random((len(points), 2)) * (radius / 3)

        # build initial regions from generated points
        vor = Voronoi(points)
        regions = [r for r in vor.regions if -1 not in r and len(r) > 0]
        regions = [Polygon([vor.vertices[i] for i in r]) for r in regions]
        regions = [r for r in regions if limit.contains(r)]

        # check surfaces coherence
        n = 0
        for r in regions:
            if r.area < min_surface:
                n += 1
                if n > nb_small:
                    break
        if n < nb_small:
            return regions
        logging.info(f"Regeneration regions, too many small areas")


def split_city(city, N, radius, limit, min_surface, nb_small):
    """Split inner and outer regions of the city."""
    regions = generate_regions(N, radius, limit, min_surface, nb_small)

    # generate walls
    walls = generate_perimeter(radius / 1.9)
    categories = [Category.HOUSE if walls.contains(r) else Category.FARM for r in regions]

    # temporarly associate HOUSE to inner city and FARM to outer city
    inner_city, outer_city = [], []
    for r in regions:
        area = Area(r, Category.HOUSE if walls.contains(r) else Category.FARM)
        city.add_subco(area)
        if area.category == Category.HOUSE: # inner
            inner_city.append(area)
        else: # outer
            outer_city.append(area)

    return inner_city, outer_city
