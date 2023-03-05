from math import sin, cos, pi

import numpy

from heightmaps.data import generate_hilly_terrain
from heightmaps.png import write_png


HEIGHTMAPS_PATH = './assets/heightmaps/'


def get_rounded_square_route_points(size):
    left = size*0.2
    right = size*0.8
    top = size*0.8
    bottom = size*0.2
    turn_radius = size*0.1
    point_space = size*0.1
    points = []
    # top points
    for i in range((right - left - 2*turn_radius) // point_space):
        points.append(left + turn_radius + i * point_space, top)
    # top-right points
    for i in range((turn_radius*pi/2)//point_space):
        theta = i * point_space / turn_radius
        points.append(right - turn_radius + turn_radius * sin(theta), top - turn_radius * (1-cos(theta)))
    # right points
    for i in range((top - bottom - 2*turn_radius) // point_space):
        points.append(right, top - turn_radius - i * point_space)
    # bottom-right points
    for i in range((turn_radius*pi/2)//point_space):
        theta = i * point_space / turn_radius
        points.append(right - turn_radius * (1-cos(theta)), bottom + turn_radius - turn_radius * sin(theta))
    # bottom points
    for i in range((right - left - 2*turn_radius) // point_space):
        points.append(right - turn_radius - i * point_space, bottom)
    # bottom-left points
    for i in range((turn_radius*pi/2)//point_space):
        theta = i * point_space / turn_radius
        points.append(left + turn_radius - turn_radius * sin(theta), bottom + turn_radius * (1-cos(theta)))
    # left points
    for i in range((top - bottom - 2*turn_radius) // point_space):
        points.append(left, bottom + turn_radius + i * point_space)
    # top-left points
    for i in range((turn_radius*pi/2)//point_space):
        theta = i * point_space / turn_radius
        points.append(left + turn_radius * (1-cos(theta)), top - turn_radius + turn_radius * sin(theta))
    return points


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
    dx = x2 - x2
    magnitude = (dy**2 + dx**2)**0.5
    return dy/magnitude, -dx/magnitude


def get_slope_vector(point, heightmap):
    x, y = point
    left = heightmap[x-1][y]
    right = heightmap[x+1][y]
    top = heightmap[x][y-1]
    bottom = heightmap[x][y+1]
    return (right-left)/2, (top-bottom)/2


def refine_route(heightmap, route_points):
    # get average elevation
    # elevation_sum = 0
    # for point in route_points:
    #     elevation_sum += heightmap[point[0]][point[1]]
    # elevation_average = elevation_sum / len(route_points)
    num_points = len(route_points)
    new_route_points = []
    move_distance = 5
    for i in range(num_points):
        last_point = route_points[i-1 % num_points]
        next_point = route_points[i+1 % num_points]
        point = route_points[i]
        last_elevation = heightmap[last_point[0]][last_point[1]]
        next_elevation = heightmap[next_point[0]][next_point[1]]
        point_elevation = heightmap[point[0]][point[1]]
        if last_elevation > point_elevation and next_elevation > point_elevation:
            normal_vector = get_normal_vector(last_point, next_point)
            slope = get_slope_vector(point, heightmap)






def create_map(name, size):
    heightmap = generate_hilly_terrain(size, size, variance=256*128//4, corners=(256*128//2, 256*128//2, 256*128//2, 256*128//2))
    write_png(HEIGHTMAPS_PATH + name + '.png', heightmap)

    route = get_rounded_square_route_points(size)


    numpy.savetxt(HEIGHTMAPS_PATH + name + '.txt', heightmap, fmt='%d')


create_map('route1', 257)

