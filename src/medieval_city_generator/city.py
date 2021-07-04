#!/usr/bin/env python3

import logging
import os

import numpy as np
import shapely
from area import Area, Category, generate_perimeter
from city_splitter import split_city
from city_utils import get_surface
from mapper_inner import map_inner_city
from mapper_outer import map_outer_city
from scipy.spatial import Voronoi, voronoi_plot_2d
from shapely.geometry import LineString, MultiPolygon, Point, Polygon, mapping
from tools import json

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


class City(Area):
    def __init__(self, population, density=10000, has_walls=False, has_castle=False, has_river=False):
        # scale the city size with population
        N = population // 650
        radius = 100

        # generate big area
        logging.info(f"Generating borders for N = {N} and radius = {radius}")
        borders = generate_perimeter(radius)
        super().__init__(borders, Category.COMPOSITE)

        self.population = population
        self.density = density
        self.has_walls = has_walls
        self.has_castle = has_castle
        self.has_river = has_river
        self.districts = []

        generate_city(self, N, radius, borders)

    def empty(self):
        """Clear city areas."""
        self._sub_areas.clear()

    def add_walls(self, inner_city):
        """Add walls around the inner city."""
        inner_polys = [district.polygon for district in inner_city]
        walls = MultiPolygon(inner_polys).buffer(0, join_style=2)
        area_walls = Area(walls, Category.WALL)
        self.add_subco(area_walls)

    def add_streets(self, inner_city):
        """Add streets in the inner city."""
        for district in inner_city:
            poly = MultiPolygon([district.polygon]).buffer(0, join_style=2)
            streets = Area(poly, Category.STREET)
            self.add_subco(streets)


def generate_city(city, N, radius, borders):
    min_surface, nb_small = 3, 8
    while True: # while the generated city is not coherent
        inner_city, outer_city = split_city(city, N, radius, borders, min_surface, nb_small)
        nb_districts, nb_lands = len(inner_city), len(outer_city)
        inner_surface, outer_surface = get_surface(inner_city), get_surface(outer_city)

        # conditions for a realistic city
        if nb_districts > 5 and \
            nb_lands > 8    and \
            inner_surface * 2 <= outer_surface:
            break

        logging.info("Unrealistic city, regenerating...")
        city.empty() # clear city components before generating a new one

    logging.info(f"""Generated city has {nb_districts} districts and {nb_lands} lands
        - inner surface = {inner_surface}
        - outer surface = {outer_surface}""")
    map_outer_city(outer_city, nb_lands) # associate asset to each outer area
    map_inner_city(inner_city, nb_districts, city.has_castle) # associate asset to each inner area

    city.add_streets(inner_city)

    if city.has_walls:
        city.add_walls(inner_city)


if __name__ == "__main__":
    os.system('mkdir -p ../../outfiles')
    city = City(12000, has_walls=True, has_castle=True)
    json(city, '../../outfiles/city.json')
