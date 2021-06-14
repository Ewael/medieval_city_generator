#!/usr/bin/env python3

import random

from area import Category


def generate_outer_category():
    n = random.random()
    if n < 0.3:
        return Category.LAND
    if n < 0.6:
        return Category.FIELD
    if n < 0.8:
        return Category.FARM
    if n < 0.9:
        return Category.FOREST
    else:
        return Category.LAKE


def map_outer_city(outer_city, nb_lands):
    for outer_area in outer_city:
        outer_area.category = generate_outer_category()
