from math import atan, pi

from PIL import Image, ImageDraw
import numpy as np


BACKGROUND_COLOR = (0, 150, 0)
ROUTE_COLOR = (90, 90, 90)

PATH_WIDTH = 3



def interpolate(point1, point2, ratio):
    x1, y1 = point1
    x2, y2 = point2
    return x1 + (x2-x1)*ratio, y1 + (y2-y1)*ratio


def get_normal(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    dy = y2 - y1
    dx = x2 - x1
    return dy, -dx


def get_intersection(point1, point2, vector1, vector2):
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = vector1
    x4, y4 = vector2
    denominator = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if denominator == 0:
        return None
    x = ((x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4)) / denominator
    y = ((x1*y2-y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4)) / denominator
    return x, y


def get_arc_angle_degrees(point, center):
    x1, y1 = point
    x2, y2 = center
    if x1 == x2:
        if y1 > y2:
            return 90
        else:
            return -90
    else:
        arctan = atan((y1-y2)/(x1-x2))/pi*180
        if x1 > x2:
            return arctan
        else:
            return arctan + 180


def get_arc(start_point, end_point, vertex):
    start_angle = get_arc_angle_degrees(start_point, vertex)
    end_angle = get_arc_angle_degrees(end_point, vertex)
    start_vector = get_normal(start_point, vertex)
    end_vector = get_normal(end_point, vertex)
    intersection = get_intersection(start_point, end_point, start_vector, end_vector)
    radius = get_distance(vertex, intersection)
    top_left = (intersection[0] - radius, intersection[1] + radius)
    bottom_right = (intersection[0] + radius, intersection[1] - radius)
    return top_left, bottom_right, start_angle, end_angle


def get_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

def point_to_image_xy(point, resolution, side_length):
    x, y = point
    y_max = side_length*resolution-1
    return x*resolution, y_max-y*resolution



def write_route_png(path, route, side_length, background_color=BACKGROUND_COLOR, route_color=ROUTE_COLOR, resolution=1):
    img = Image.new("RGB", (side_length*resolution, side_length*resolution), color=background_color)
    draw = ImageDraw.Draw(img)
    y_max = side_length*resolution-1
    for i in range(len(route)):
        x1, y1 = route[i]
        x2, y2 = route[(i+1) % len(route)]
        line_bounds = (x1*resolution, y_max-y1*resolution, x2*resolution, y_max-y2*resolution)
        draw.line(line_bounds, fill=route_color, width=PATH_WIDTH*resolution)
        circle_bounds = (x1*resolution-PATH_WIDTH*resolution/2, y_max-(y1*resolution+PATH_WIDTH*resolution/2), x1*resolution+PATH_WIDTH*resolution/2, y_max-(y1*resolution-PATH_WIDTH*resolution/2))
        draw.ellipse(circle_bounds, fill=route_color)
    img.save(path, optimize=True, compress_level=9)



