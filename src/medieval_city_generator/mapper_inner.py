#!/usr/bin/env python3

import random
import logging

from area import Category, Area

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def get_unique_assets(has_castle):
    """Return a list of unique assets."""
    assets = [
            # possible unique assets but we only use 2

            #Category.MARKET,
            #Category.TOWNHALL,
            #Category.UNIVERSITY,
            #Category.CHURCH,
            Category.CATHEDRAL,
            #Category.MONASTRY,
            #Category.FORT,
            ]
    if has_castle:
        assets.append(Category.CASTLE)
    return assets

def get_random_asset():
    """Return a non-unique random asset for inner city areas."""
    assets = [
            [(Category.MANSION, 0.7), (Category.MANSION, 0.5), (Category.PARK, 0.3)],
            [(Category.HOUSE, 0.7), (Category.HOUSE, 0.5), (Category.HOUSE, 0.3)],
            [(Category.HOUSE, 0.7), (Category.HOUSE, 0.5), (Category.HOUSE, 0.3)],
            [(Category.HOUSE, 0.7), (Category.HOUSE, 0.5), (Category.HOUSE, 0.3)],
            [(Category.HOUSE, 0.7), (Category.HOUSE, 0.5), (Category.HOUSE, 0.3)],
            [(Category.MARKET, 0.6), (Category.HOUSE, 0.2)]
            ]
    return random.choice(assets)


def associate_asset(inner_city, i, asset):
    """Associate asset to an inner city area."""
    curr_area = inner_city[i]
    curr_area.category = asset[-1][0] # set the area category to the last one
    direction = random.randint(0, 3) * 90 # random dir beyond four cardinal points
    for i in range(len(asset) - 1):
        category, p = asset[i]
        curr_area = curr_area.split(p, direction, new_category=category)
        curr_area = curr_area[1] # we split the new category
        direction += 90 # we change split direction so it's never parallel


def map_inner_city(inner_city, nb_districts, has_castle):
    """Associate coherent categories to inner city areas."""
    logging.info(f"Generating assets for inner city")

    # associate unique assets first (which means unique buildings like castle)
    unique_assets = get_unique_assets(has_castle)
    unique_buildings = []
    for unique_asset in unique_assets:
        inner_city[0].category = unique_asset # this is where we associate it
        unique_buildings.append(inner_city.pop(0))

    # loop on remaining districts and split them with realistic assets
    for i in range(len(inner_city)):
        asset = get_random_asset()
        associate_asset(inner_city, i, asset)
        inner_city[i].category = Category.COMPOSITE # dont print parent
        old_dis = inner_city[i]
        while len(old_dis.sub_areas) > 1: # append new splitted areas to inner city
            inner_city.append(old_dis.sub_areas[0])
            old_dis = old_dis.sub_areas[1]

    for building in unique_buildings: # add saved unique buildings
        inner_city.append(building)
