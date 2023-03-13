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
    dx1, dy1 = vector1
    dx2, dy2 = vector2
    denominator = dx1*dy2 - dy1*dx2
    if denominator == 0:
        return None
    x = ((x1*dy1 - y1*dx1)*dx2 - (x2*dy2 - y2*dx2)*dx1)/denominator
    y = ((x1*dy1 - y1*dx1)*dy2 - (x2*dy2 - y2*dx2)*dy1)/denominator
    return x, y


def get_arc_angle_degrees(point, center):
    x1, y1 = point
    x2, y2 = center
    if x1 == x2:
        if y1 > y2:
            return 90
        else:
            return 270
    else:
        arctan = atan((y1-y2)/(x1-x2))/pi*180
        if x1 > x2:
            return arctan % 360
        else:
            return (arctan + 180) % 360


def get_arc(start_point, end_point, vertex):
    start_vector = get_normal(start_point, vertex)
    end_vector = get_normal(end_point, vertex)
    intersection = get_intersection(start_point, end_point, start_vector, end_vector)
    radius = get_distance(vertex, intersection)
    start_angle = get_arc_angle_degrees(start_point, intersection)
    end_angle = get_arc_angle_degrees(end_point, intersection)
    top_left = (intersection[0] - radius, intersection[1] + radius)
    bottom_right = (intersection[0] + radius, intersection[1] - radius)
    if np.abs(start_angle - end_angle)/180*pi*radius > 10:
        pass
    return top_left, bottom_right, start_angle, end_angle


def get_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

def point_to_image_xy(point, resolution, side_length):
    x, y = point
    y_max = side_length*resolution-1
    return x*resolution, y_max-y*resolution


def image_angle(angle):
    return -angle % 360


def draw_line_and_circle(draw, start_point, end_point, width, resolution, side_length, color):
    x1, y1 = point_to_image_xy(start_point, resolution, side_length)
    x2, y2 = point_to_image_xy(end_point, resolution, side_length)
    draw_width = width*resolution
    line_bounds = (x1, y1, x2, y2)
    draw.line(line_bounds, fill=color, width=draw_width)
    circle_bounds = (x2-draw_width/2, y2-draw_width/2, x2+draw_width/2, y2+draw_width/2)
    draw.ellipse(circle_bounds, fill=color)
    return


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


CURVE_RATIO = 0.2
ARC_LINES = 10

def write_route_arc_png(path, route, side_length, background_color=BACKGROUND_COLOR, route_color=ROUTE_COLOR, resolution=1):
    img = Image.new("RGB", (side_length*resolution, side_length*resolution), color=background_color)
    draw = ImageDraw.Draw(img)
    y_max = side_length*resolution-1
    draw_width = PATH_WIDTH*resolution
    for i in range(len(route)):
        point1 = route[i]
        point2 = route[(i+1) % len(route)]
        point3 = route[(i+2) % len(route)]
        # Line segment
        start_point = interpolate(point1, point2, CURVE_RATIO)
        end_point = interpolate(point2, point1, CURVE_RATIO)
        draw_line_and_circle(draw, start_point, end_point, PATH_WIDTH, resolution, side_length, route_color)
        # Arc
        next_start_point = interpolate(point2, point3, CURVE_RATIO)
        arc_points = []
        for i in range(ARC_LINES+1):
            ratio = i/ARC_LINES
            this_anchor = interpolate(end_point, point2, ratio)
            next_anchor = interpolate(point2, next_start_point, ratio)
            this_point = interpolate(this_anchor, next_anchor, ratio)
            arc_points.append(this_point)
        for i in range(ARC_LINES):
            line_bounds = point_to_image_xy(arc_points[i], resolution, side_length) + point_to_image_xy(arc_points[i+1], resolution, side_length)
            draw_line_and_circle(draw, arc_points[i], arc_points[i+1], PATH_WIDTH, resolution, side_length, route_color)
            
            

    img.save(path, optimize=True, compress_level=9)



