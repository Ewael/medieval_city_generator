#!/usr/bin/env python3

from shapely.geometry import Polygon
import pytest

from medieval_city_generator.area import Category, generate_perimeter, Area
from medieval_city_generator.city_utils import get_surface
from medieval_city_generator.city_splitter import generate_regions, split_city
from medieval_city_generator.mapper_inner import get_unique_assets, get_random_asset
from medieval_city_generator.mapper_outer import generate_outer_category


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

    def test_get_surface(self):
        limit = generate_perimeter(20)
        regions = generate_regions(12, 20, limit, 3, 8)
        regions = [Area(region, category=Category.HOUSE) for region in regions]
        surface = get_surface(regions)
        assert surface > 0

    def test_getter(self):
        limit = generate_perimeter(20)
        regions = generate_regions(12, 20, limit, 3, 8)
        regions = [Area(region, category=Category.HOUSE) for region in regions]
        assert regions[0].category == Category.HOUSE

    def test_generate_outer_category(self):
        assert generate_outer_category() in [Category.LAND,
                Category.FIELD, Category.FARM, Category.FOREST, Category.LAKE]
