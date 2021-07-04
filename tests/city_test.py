#!/usr/bin/env python3

from shapely.geometry import Polygon
import pytest

from medieval_city_generator.area import Category, generate_perimeter
from medieval_city_generator.city_splitter import generate_regions
from medieval_city_generator.mapper_inner import get_unique_assets


class TestCity:
    def test_generate_perimeter(self):
        peri = generate_perimeter(20)
        assert type(peri) == Polygon

    def test_generate_regions(self):
        limit = generate_perimeter(20)
        regions = generate_regions(12, 20, limit, 3, 8)
        assert len(regions) > 10

    def test_get_unique_assets_with_castle(self):
        assets = get_unique_assets(True)
        assert assets == [Category.CATHEDRAL, Category.CASTLE]

    def test_get_unique_assets_without_castle(self):
        assets = get_unique_assets(False)
        assert assets == [Category.CATHEDRAL]

    def test_get_random_asset(self):
        asset = get_random_asset()
        assert len(asset) >= 2
