from math import sin, cos, pi
import random

import numpy

from generate.heightmaps.data import generate_hilly_terrain
from generate.heightmaps.png import write_heightmap_png

from generate.textures.png import write_route_png, write_route_arc_png

from tools.route import get_route_points, round_corners_route_points




ASSETS_PATH = './assets'
HEIGHTMAPS_PATH = f'{ASSETS_PATH}/heightmaps'
TEXTURES_PATH = f'{ASSETS_PATH}/textures'
ROUTES_PATH = f'{ASSETS_PATH}/routes'




INNER_DISTANCE = 0.2
RAND_MULTIPLE = 0.2
RAND_NUM_PLACEMENTS = 5



INNER_DISTANCE = 0.2
RAND_MULTIPLE = 0.2
RAND_NUM_PLACEMENTS = 5

def create_map(name, side_length, iterations=4):
    heightmap = generate_hilly_terrain(side_length, side_length, variance=256*128//4, corners=(256*128//2, 256*128//2, 256*128//2, 256*128//2))
    write_heightmap_png(f'{HEIGHTMAPS_PATH}/{name}.png', heightmap)

    route_bottom_left = (INNER_DISTANCE*side_length, INNER_DISTANCE*side_length)
    route_top_right = ((1-INNER_DISTANCE)*side_length, (1-INNER_DISTANCE)*side_length)
    route_top_left = (route_bottom_left[0], route_top_right[1])
    route_bottom_right = (route_top_right[0], route_bottom_left[1])
    route_init_points = [route_bottom_left, route_bottom_right, route_top_right, route_top_left]
    init_route = get_route_points(heightmap, iterations=iterations, init_points=route_init_points)
    route = round_corners_route_points(init_route, curve_ratio=0.2, curve_segments=10)

    # write_route_png(f'{TEXTURES_PATH}/{name}.png', route, side_length, resolution=20)
    # write_route_arc_png(f'{TEXTURES_PATH}/{name}.png', route, side_length, resolution=20)
    write_route_png(f'{TEXTURES_PATH}/{name}.png', route, side_length, resolution=20)


    numpy.savetxt(f'{HEIGHTMAPS_PATH}/{name}.txt', heightmap, fmt='%d')

    with open(f'{ROUTES_PATH}/{name}.txt', 'w') as route_file:
        numpy.savetxt(route_file, route, fmt='%f')


# create_map('map1', 257, iterations=4)
# create_map('map2', 513, iterations=5)
# create_map('map3', 1025, iterations=6)

