#!/usr/bin/env python3

from shapely.geometry import mapping, Polygon, Point, LineString, MultiPolygon
from scipy.spatial import Voronoi, voronoi_plot_2d

import numpy as np
import shapely

from area import Area, Category, generate_perimeter

import tools


class City(Area):
    def __init__(self, population, density=10000, has_walls=False, has_castel=False, has_river=False):
        N, radius = 8, 8 # TODO: scale it with density
        limit = generate_perimeter(radius)
        super().__init__(limit, Category.COMPOSITE)

        self.population = population
        # 10 000 ha/km2 by default, between 2000 ha/km2 with the fields and 30000 ha/km2
        self.density = density
        self.has_walls = has_walls
        self.has_castel = has_castel
        self.has_river = has_river
        self.districts = []

        generate_city(self, N, radius, limit)


def generate_city(city: City, N, radius, limit: Polygon):
    points = np.array([[x,y] for x in np.linspace(-1,1,N) for y in np.linspace(-1,1,N)])
    points *= radius
    points += np.random.random((len(points), 2)) * (radius / 3)

    # build initial regions from generated points
    vor = Voronoi(points)
    regions = [r for r in vor.regions if -1 not in r and len(r) > 0]
    regions = [Polygon([vor.vertices[i] for i in r]) for r in regions]
    regions = [r for r in regions if limit.contains(r)]

    walls = generate_perimeter(radius / 2)
    categories = [Category.HOUSE if walls.contains(r) else Category.FARM for r in regions]

    for i in range(len(regions)):
        area = Area(regions[i], categories[i])
        city.add_subco(area)

    # spliting city and land
    inner_city, land = [], []
    for area in city.components():
        if area._category == Category.HOUSE:
            inner_city.append(area)
        else: # FARM
            land.append(area)
    nb_districts = len(inner_city)
    nb_lands = len(land)


if __name__ == "__main__":
    city = City(5000)
    tools.json(city, '../outfiles/city.json')

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

Une fois qu'on a split farm et city
on associe chaque batiment unique à une case
-> on s'occupe des presets uniques d'abord pour remplir la ville
puis on colorie le reste en piochant de maniere random dans un liste de presets
plus génériques
adapter la taille du split en fonction de si on est dans la city ou en dehors
-> on peut donner nous-meme la taille en parametre

example for asset and split usage:
    residential_city = Area(Polygon([(0,0), (-40,0), (-40,-40), (0,-40)]), Category.HOUSE)
    h1, h2 = residential_city.split(0.6, Dir.EAST, new_category=Category.HOUSE)
    h2, s1 = h2.split(0.2, Dir.WEST, new_category=Category.STREET)
    h1, g1 = h1.split(0.3, Dir.NORTH, new_category=Category.GARDEN)
"""
