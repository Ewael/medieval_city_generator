#!/usr/bin/env python3

from shapely.geometry import mapping, Polygon, Point, LineString, MultiPolygon
from enum import IntEnum
from shapely import ops

import numpy as np
import sys


class Dir(IntEnum):
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 270


class Category(IntEnum):
    # outer city
    UNDEFINED = 0
    LAND = 1
    FIELD = 2
    FOREST = 3
    RIVER = 4
    LAKE = 5
    SEA = 6
    PARK = 7
    GARDEN = 8
    FARM = 9
    # inner city
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
    STREET = 50
    BRIDGE = 51
    WALL = 52
    # union of Areas
    COMPOSITE = 90


class Area():
    _last_id = 0
    members = []

    @staticmethod
    def get_id():
        Area._last_id +=1
        return Area._last_id

    def __init__(self, polygon, category, sub_areas = []):
        """
        The Area is the most basic class, however it has all that's needed to
        plot the map.

        Args:
            polygon: Polygon - countour of the area
            category: Category - type of area
            sub_areas: list - list of sub areas if any
        """
        self._polygon = polygon
        self._category = category
        self._sub_areas = [self] + sub_areas
        self._id = self.get_id()
        Area.members.append(self)

    def __del__(self):
        Area.members.remove(self)

    def __repr__(self):
        return str(self._category) + ":" +  self._polygon.wkt

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        self._category = new_category

    @property
    def sub_areas(self):
        return self._sub_areas

    @sub_areas.setter
    def sub_areas(self, new_category):
        self._sub_areas = new_category

    @property
    def identity(self):
        return self._id

    @property
    def polygon(self):
        return self._polygon

    def split(self, percentage, direction, inplace=True, new_category=Category.GARDEN):
        """
        Split an area in two areas. Store result in self.sub_areas if inplace == True.

        Args:
            percentage: float - percentage of surface for new area, between 0 and 1
            direction: int - side for first area (from center to 0 = North, 90 = East...)
            new_category: Category - category of the second area

        Returns: if inplace == False
            area1: Area
            area2: Area

        Tests:
            >>> surf = Area(Polygon([(0,0), (20,0), (20,40), (0,40)]), Category.HOUSE)
            >>> res = surf.split(0.25, 0, False)  # house takes 1/4 of surface and is north
            >>> res0 = Polygon([(0, 30), (0, 40), (20, 40), (20, 30), (0, 30)])
            >>> res0.symmetric_difference(res[0].polygon).area < 1
            True
        """
        assert(percentage > 0 and percentage < 1)
        percentage = 1 - percentage
        direction = (direction - 180) % 360
        if not self._polygon.exterior.is_ccw: # should be counter clockwise
            coords = list(self._polygon.exterior.coords)
            self._polygon = Polygon(coords[::-1])
        direction = np.deg2rad(90 - direction)  # degrees are cw while radian are ccw + 0 is North
        pts = np.array(self._polygon.minimum_rotated_rectangle.exterior.coords)
        diameter = np.sqrt(np.sum(np.square(pts[2] - pts[0])))
        start = np.array(self._polygon.centroid)
        end = start +  np.array([diameter * np.cos(direction), diameter * np.sin(direction)])
        path = LineString([start, end])
        pt_intersection = path.intersection(self._polygon.boundary)
        try:
            pt_intersection = list(pt_intersection)[-1]  # we may have more than one intersection
        except:
            pass
        pts = self._polygon.boundary.coords
        for pt1, pt2 in zip(pts[:-1], pts[1:]):
            if LineString((pt1, pt2)).distance(pt_intersection) < 1E-6:
                break
        pt1 = np.array(pt1)
        pt2 = np.array(pt2)
        dist = np.sqrt(np.sum(np.square(pt2 - pt1)))
        dir = (pt2 - pt1) / dist
        orth = np.array([-dir[1], dir[0]])  # ccw
        house_area = self._polygon.area * percentage
        width = diameter / 2 # hence we can reach from 0 to diameter
        res = [self._polygon,]
        dw = width
        while abs(res[0].area - house_area) > 1 or len(res) <= 1:  # 1 meter² error accepted and successful split
            cut = LineString([pt1 + width * orth - diameter * dir, pt2 + width * orth + diameter * dir])
            res = ops.split(self._polygon, cut)
            dw /= 2
            #if len(res) == 0:
            if len(res) <= 1:
                width -= dw
                continue
            if pt_intersection.distance(res[0]) > pt_intersection.distance(res[1]):
                res = MultiPolygon([res[1], res[0]])
            else:
                res = MultiPolygon([g for g in res])
            if res[0].area > house_area:
                width -= dw
            else:
                width += dw
        area0 = Area(res[0], self._category)
        area1 = Area(res[1], new_category)
        if inplace:
            self._sub_areas = [area0, area1]
        return area0, area1

    def add_subco(self, subco):
        """Add sub area to the components."""
        if self._sub_areas == [self]:
            self._sub_areas = [subco]
        else:
            self._sub_areas.append(subco)

    def components(self):
        """Return components."""
        if len(self._sub_areas) > 0:
            return self._sub_areas
        else:
            return [self,]

    def get_area(self):
        """Return surface of the polygon of the Area."""
        return self.polygon.area


def generate_perimeter(radius, dimensions = (8, 2)):
    """Return a Polygon whose dims respect the given radius."""
    return Polygon((2 * np.random.random(dimensions) - 1) * radius).convex_hull.buffer(radius / 2)
