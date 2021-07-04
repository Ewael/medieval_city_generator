#!/usr/bin/env python3

import random

from .area import Category


def generate_outer_category():
    """Return a random categoy following coherent probabilities for outer city areas."""
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
    """Associate coherent categories to outer city areas."""
    for outer_area in outer_city:
        outer_area.category = generate_outer_category()
