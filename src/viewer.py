#!/usr/bin/env python3

from matplotlib.colors import ListedColormap

import matplotlib.pylab as plt
import geopandas as gpd
import sys

from area import Category


def to_percentage(L):
    res = L
    res[0] /= 255
    res[1] /= 255
    res[2] /= 255
    return res

try:
    filename = sys.argv[1]
except:
    filename = '../outfiles/house.json'

colors_dic = {1:[255, 255, 205, 1],         # light yellow
              2:[255, 255, 102, 1],         # yellow
              3:[0, 102, 0, 1],             # dark green
              4:[102, 255, 255, 1],         # light blue
              5:[0, 102, 255, 1],           # blue
              6:[0, 0, 204, 1],             # dark blue
              7:[102, 153, 0, 1],           # green
              8:[102, 255, 51, 1],          # light green
              9:[204, 153, 0, 1],           # dark yellow
              10:[204, 102, 0, 1],          # orange
              11:[128, 0, 0, 1],            # dark red
              12:[204, 0, 102, 1],          # dark pink
              13:[255, 0, 0, 1],            # red
              14:[153, 51, 255, 1],         # purple
              20:[255, 153, 255, 1],        # light pink
              21:[255, 0, 255, 1],          # pink
              22:[255, 102, 153, 1],        # faded pink
              31:[165, 165, 165, 1],        # light grey
              32:[94, 94, 94, 1],           # grey
              50:[223, 223, 223, 1],        # very light grey
              51:[55, 71, 69, 1],           # dark grey
              52:[0, 0, 0, 1],              # black
              90:[0, 0, 0]                  # composite
              }

colors = [[1,0,0,1] for _ in range(max(colors_dic.keys())+1)]
for i in colors_dic:
    colors[i] = to_percentage(colors_dic[i])
color_map = ListedColormap(colors, name='Archi')

shapes = gpd.read_file(filename)
fig, ax = plt.subplots(figsize = (10,8))

# we plot the walls only
walls = shapes[(shapes.category == Category.WALL)]
print(walls)
if len(walls): # if city has walls then plot it
    walls.geometry.boundary.plot(color=None,
            edgecolor='black', linewidth=5,
            aspect='equal', ax=ax)

# we plot city without the walls
shapes = shapes[(shapes.category != Category.WALL)]
shapes.plot(column='category', cmap=color_map,
            k=len(colors)+1, vmin=0, vmax=len(colors),
            #edgecolor='black',
            aspect='equal', ax=ax)
shapes = shapes[(shapes.category > 9)]
shapes.geometry.boundary.plot(color=None,
        edgecolor='black', linewidth=0.5,
        aspect='equal', ax=ax)

#plt.grid()
plt.show()
