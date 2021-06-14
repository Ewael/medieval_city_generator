#!/usr/bin/env python3

import random
import logging

from area import Category

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def generate_inner_category():
    n = random.random()


def get_unique_assets():
    assets = [
            #Category.MARKET,
            #Category.TOWNHALL,
            #Category.UNIVERSITY,
            #Category.CHURCH,
            Category.CATHEDRAL,
            #Category.MONASTRY,
            #Category.FORT,
            Category.CASTLE
            ]
    return assets

def get_random_asset():
    assets = [
            [(Category.MANSION, 0.7), (Category.GARDEN, 0.3)],
            #[(Category.HOUSE, 0.3), (Category.HOUSE, 0.3), (Category.HOUSE, 0.4)]
            ]
    return random.choice(assets)


def associate_asset(inner_city, i, asset):
    curr_area = inner_city[i]
    curr_area.category = asset[-1][0] # set the area category to the last one
    for i in range(len(asset) - 1):
        category, p = asset[i]
        direction = random.randint(0, 360)
        logging.info(f"direction = {direction}")
        logging.info(f"curr_area = {curr_area}")
        curr_area = curr_area.split(p, direction, new_category=category)[1]


def map_inner_city(inner_city, nb_districts):
    unique_assets = get_unique_assets()
    for unique_asset in unique_assets:
        inner_city[0].category = unique_asset
        inner_city.pop(0)

    for i in range(len(inner_city)):
        asset = get_random_asset()
        logging.info(f"Disctrict {i} -> asset = {asset}")
        associate_asset(inner_city, i, asset)


"""
example for asset and split usage:
    residential_city = Area(Polygon([(0,0), (-40,0), (-40,-40), (0,-40)]), Category.HOUSE)
    h1, h2 = residential_city.split(0.6, Dir.EAST, new_category=Category.HOUSE)
    h2, s1 = h2.split(0.2, Dir.WEST, new_category=Category.STREET)
    h1, g1 = h1.split(0.3, Dir.NORTH, new_category=Category.GARDEN)

Inner:
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
    PARK = 7
    GARDEN = 8
"""
