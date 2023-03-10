from math import sin, cos, pi
import random

import numpy

from heightmaps.data import generate_hilly_terrain
from heightmaps.png import write_heightmap_png

from textures.png import write_route_png


ASSETS_PATH = './assets'
HEIGHTMAPS_PATH = f'{ASSETS_PATH}/heightmaps'
TEXTURES_PATH = f'{ASSETS_PATH}/textures'
ROUTES_PATH = f'{ASSETS_PATH}/routes'


def round(x):
    return int(x+0.5)


def get_height_rounded(heightmap, point):
    x, y = point
    x_int = round(x+0.5)
    y_int = round(y+0.5)
    return heightmap[y_int][x_int]


def point_or_bound(point, heightmap, padding=0):
    height = len(heightmap)
    width = len(heightmap[0])
    x, y = point
    if x < padding:
        x = padding
    elif x > width-1-padding:
        x = width-1-padding
    if y < padding:
        y = padding
    elif y > height-1-padding:
        y = height-1-padding
    return x, y



def get_normal(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    dy = y2 - y1
    dx = x2 - x2
    return dy, -dx


def get_normal_vector(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    dy = y2 - y1
    dx = x2 - x1
    magnitude = (dy**2 + dx**2)**0.5
    if magnitude == 0:
        return 0, 0
    else:
        return dy/magnitude, -dx/magnitude


def get_slope_vector(point, heightmap):
    x, y = point
    left = get_height_rounded(heightmap, (x-1, y))
    right = get_height_rounded(heightmap, (x+1, y))
    top = get_height_rounded(heightmap, (x, y+1))
    bottom = get_height_rounded(heightmap, (x, y-1))
    return (right-left)/2, (top-bottom)/2


def normalize_vector(vector):
    x, y = vector
    magnitude = (x**2 + y**2)**0.5
    return x/magnitude, y/magnitude


def get_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return ((x2-x1)**2 + (y2-y1)**2)**0.5


def get_midpoint(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return (x1+x2)/2, (y1+y2)/2






INNER_DISTANCE = 0.2
RAND_MULTIPLE = 0.2
RAND_NUM_PLACEMENTS = 5

def get_loop_route(heightmap, iterations=5):
    side_length = len(heightmap)

    points = []
    # Corners
    left = INNER_DISTANCE*side_length
    right = (1-INNER_DISTANCE)*side_length
    top = (1-INNER_DISTANCE)*side_length
    bottom = INNER_DISTANCE*side_length
    points.append((left, bottom))
    points.append((right, bottom))
    points.append((right, top))
    points.append((left, top))

    for i in range(iterations):
        new_points = []
        for j in range(len(points)):
            point = points[j]
            next_point = points[(j+1) % len(points)]
            midpoint = get_midpoint(point, next_point)
            normal = get_normal_vector(point, next_point)
            distance = get_distance(point, next_point)
            best_new_point = None
            height_diff = None
            mid_height = (get_height_rounded(heightmap, point) + get_height_rounded(heightmap, next_point)) / 2
            for i in range(RAND_NUM_PLACEMENTS):
                new_rand_placement = (random.random() - 0.5) * 2 * distance * RAND_MULTIPLE
                new_point = (midpoint[0] + normal[0] * new_rand_placement, midpoint[1] + normal[1] * new_rand_placement)
                new_height = get_height_rounded(heightmap, new_point)
                new_height_diff = abs(new_height - mid_height)
                if height_diff is None or new_height_diff < height_diff:
                    best_new_point = new_point
                    height_diff = new_height_diff
            new_points.append(point)
            new_points.append(best_new_point)
        points = new_points.copy()



    return points



def create_map(name, side_length):
    heightmap = generate_hilly_terrain(side_length, side_length, variance=256*128//4, corners=(256*128//2, 256*128//2, 256*128//2, 256*128//2))
    write_heightmap_png(f'{HEIGHTMAPS_PATH}/{name}.png', heightmap)

    route = get_loop_route(heightmap, iterations=6)

    write_route_png(f'{TEXTURES_PATH}/{name}.png', route, side_length, resolution=20)


    numpy.savetxt(f'{HEIGHTMAPS_PATH}/{name}.txt', heightmap, fmt='%d')

    with open(f'{ROUTES_PATH}/{name}.txt', 'w') as route_file:
        numpy.savetxt(route_file, route, fmt='%f')


create_map('route1', 257)
# create_map('route2', 513)
# create_map('route3', 1025)

