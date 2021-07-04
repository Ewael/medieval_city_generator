#!/usr/bin/env python3

from shapely.geometry import Polygon
import pytest

from medieval_city_generator.area import generate_perimeter

class TestCity:
    def test_generate_perimeter(self):
        peri = generate_perimeter(20)
        assert type(peri) == Polygon


