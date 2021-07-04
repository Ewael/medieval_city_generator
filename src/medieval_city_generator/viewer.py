#!/usr/bin/env python3

import math
import sys

import geopandas as gpd
import matplotlib.pylab as plt
from area import Category
from matplotlib.colors import ListedColormap


def to_percentage(L):
    """Return RGB values in percentage."""
    res = L
    res[0] /= 255
    res[1] /= 255
    res[2] /= 255
    return res

try:
    filename = sys.argv[1]
except:
    filename = '../../outfiles/city.json'

colors_dic = {Category.LAND:[255, 255, 205, 1],         # light yellow
              Category.FIELD:[255, 255, 102, 1],        # yellow
              Category.FOREST:[0, 102, 0, 1],           # dark green
              Category.RIVER:[102, 255, 255, 1],        # light blue
              Category.LAKE:[0, 102, 255, 1],           # blue
              Category.SEA:[0, 0, 204, 1],              # dark blue
              Category.PARK:[102, 153, 0, 1],           # green
              Category.GARDEN:[102, 255, 51, 1],        # light green
              Category.FARM:[204, 153, 0, 1],           # dark yellow
              Category.HOUSE:[204, 102, 0, 1],          # orange
              Category.MANSION:[128, 0, 0, 1],          # dark red
              Category.MARKET:[204, 0, 102, 1],         # dark pink
              Category.TOWNHALL:[255, 0, 0, 1],         # red
              Category.UNIVERSITY:[153, 51, 255, 1],    # purple
              Category.CHURCH:[255, 153, 255, 1],        # light pink
              Category.CATHEDRAL:[255, 0, 255, 1],      # pink
              Category.MONASTRY:[255, 102, 153, 1],     # faded pink
              Category.FORT:[165, 165, 165, 1],         # light grey
              Category.CASTLE:[94, 94, 94, 1],          # grey
              Category.STREET:[223, 223, 223, 1],       # very light grey
              Category.BRIDGE:[55, 71, 69, 1],          # dark grey
              Category.WALL:[0, 0, 0, 1],               # black
              Category.COMPOSITE:[0, 0, 0]              # composite
              }

# associate colors with categories
colors = [[1,0,0,1] for _ in range(max(colors_dic.keys())+1)]
for i in colors_dic:
    colors[i] = to_percentage(colors_dic[i])
color_map = ListedColormap(colors, name='Archi')

# read file
shapes = gpd.read_file(filename)
fig, ax = plt.subplots(figsize = (10,8))

# plot streets before walls
streets = shapes[(shapes.category == Category.STREET)]
width = math.log(len(streets), 200)
if len(streets) < 100:
    width = 2
if len(streets) > 900:
    width = 0.4
print(f"[+] Loaded {len(streets)} streets")
streets.geometry.boundary.plot(color=None,
        edgecolor='white', linewidth=width,
        aspect='equal', ax=ax)

# we plot the walls only
walls = shapes[(shapes.category == Category.WALL)]
if len(walls): # if city has walls then plot it
    walls.geometry.boundary.plot(color=None,
            edgecolor='black', linewidth=5,
            aspect='equal', ax=ax)

# we plot inner city without the walls
shapes = shapes[(shapes.category != Category.WALL)]
shapes = shapes[(shapes.category != Category.STREET)]
shapes = shapes[(shapes.category != Category.COMPOSITE)]
shapes.plot(column='category', cmap=color_map,
            k=len(colors)+1, vmin=0, vmax=len(colors),
            #edgecolor='black',
            aspect='equal', ax=ax)

# plot outer city
shapes = shapes[(shapes.category > 9)]
shapes.geometry.boundary.plot(color=None,
        edgecolor='black',
        linewidth=0.0,
        aspect='equal', ax=ax)

print(f"[+] Rendering city...")
plt.show()
