#!/usr/bin/env python3

import random

from area import Category


def generate_outer_category():
    n = random.random()
    if n < 0.2:
        return Category.LAND
    if n < 0.5:
        return Category.FIELD
    if n < 0.75:
        return Category.FARM
    if n < 0.9:
        return Category.FOREST
    else:
        return Category.LAKE


def map_outer_city(outer_city, nb_lands):
    for outer_area in outer_city:
        outer_area.category = generate_outer_category()


"""
Outer:
    LAND = 1
    FIELD = 2
    FOREST = 3
    RIVER = 4
    LAKE = 5
    SEA = 6
    FARM = 15
"""
