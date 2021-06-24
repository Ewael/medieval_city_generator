#!/usr/bin/env python3

from shapely.geometry import mapping, Polygon, Point, LineString, MultiPolygon
from scipy.spatial import Voronoi, voronoi_plot_2d

import numpy as np
import shapely
import logging

from area import Area, Category, generate_perimeter
from city_splitter import split_city
from mapper_outer import map_outer_city
from mapper_inner import map_inner_city
from city_utils import get_surface

import tools

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


class City(Area):
    def __init__(self, population, density=10000, has_walls=False, has_castle=False, has_river=False):
        N, radius = 8, 10 # TODO: scale it with density
        logging.info(f"Generating borders for N = {N} and radius = {radius}")
        borders = generate_perimeter(radius)
        super().__init__(borders, Category.COMPOSITE)

        self.population = population
        # 10 000 ha/km2 by default, between 2000 ha/km2 with the fields and 30000 ha/km2
        self.density = density
        self.has_walls = has_walls
        self.has_castle = has_castle
        self.has_river = has_river
        self.districts = []

        generate_city(self, N, radius, borders)

    def empty(self):
        self._sub_areas.clear()

    def add_walls(self, inner_city):
        inner_polys = [district.polygon for district in inner_city]
        walls = MultiPolygon(inner_polys).buffer(0, join_style=2)
        area_walls = Area(walls, Category.WALL)
        self.add_subco(area_walls)


def generate_city(city, N, radius, borders):
    min_surface, nb_small = 3, 8
    while True:
        inner_city, outer_city = split_city(city, N, radius, borders, min_surface, nb_small)
        nb_districts, nb_lands = len(inner_city), len(outer_city)
        inner_surface, outer_surface = get_surface(inner_city), get_surface(outer_city)

        #TODO: scale it with density
        if nb_districts > 5 and \
            nb_lands > 8    and \
            inner_surface * 2 <= outer_surface:
            break

        logging.info("Unrealistic city, regenerating...")
        city.empty() # clear city components before generating a new one

    logging.info(f"""Generated city has {nb_districts} districts and {nb_lands} lands
        - inner surface = {inner_surface}
        - outer surface = {outer_surface}""")
    map_outer_city(outer_city, nb_lands)
    map_inner_city(inner_city, nb_districts)

    if city.has_walls:
        city.add_walls(inner_city)


if __name__ == "__main__":
    city = City(5000, has_walls=True)
    tools.json(city, '../outfiles/city.json')


'''
TODO: STREETS
on plot les rues avant les walls en blanc avec 0 buffer
puis on ploot les walls pour overwqrite les streets exterieures

TODO: changer les couleurs trop claires et eviter le rose fuchsia
'''
