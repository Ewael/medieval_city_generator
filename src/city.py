#!/usr/bin/env python3

import tools


class City(Area):
    def __init__(self, population, density=10000, has_walls=False, has_castel=False, has_river=False):
        self.population = population
        # 10 000 ha/km2 by default, between 2000 ha/km2 with the fields and 30000 ha/km2
        self.density = density
        self.has_walls = has_walls
        self.has_castel = has_castel
        self.has_river = has_river
        self.districts = []
        ...


if __name__ == "__main__":
    city = City(5000)
    tools.json(city, '../outfiles/city.json')
