import json
import random

import numpy


from tools.geometry import *




def flatten_heightmap_around_path(heightmap, route_points):



    pass





RAND_MULTIPLE = 0.2
RAND_NUM_PLACEMENTS = 5

def get_route_points(heightmap, iterations=5, init_points=[]):
    side_length = len(heightmap)

    points = init_points

    for i in range(iterations):
        new_points = []
        for j in range(len(points)):
            point = points[j]
            next_point = points[(j+1) % len(points)]
            midpoint = get_midpoint(point, next_point)
            normal = get_normal_vector_2d(point, next_point)
            distance = get_distance_2d(point, next_point)
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


def round_corners_route_points(route_points, curve_ratio=0.2, curve_segments=10):
    new_route_points = []
    for i in range(len(route_points)):
        point = route_points[i]
        next_point = route_points[(i+1) % len(route_points)]
        third_point = route_points[(i+2) % len(route_points)]
        start_segment = interpolate_points(point, next_point, curve_ratio)
        end_segment = interpolate_points(point, next_point, 1-curve_ratio)
        next_start_segment = interpolate_points(next_point, third_point, curve_ratio)
        new_route_points.append(start_segment)
        for j in range(curve_segments):
            ratio = j / curve_segments
            this_anchor = interpolate_points(end_segment, next_point, ratio)
            next_anchor = interpolate_points(next_point, next_start_segment, ratio)
            new_route_points.append(interpolate_points(this_anchor, next_anchor, ratio))
    return new_route_points






    pass





def interpolate_route(route_points, ratio):

    

    pass


def read_route_points(file):
    route_points = numpy.loadtxt(file)
    return route_points


def read_heightmap(file):
    heightmap = numpy.loadtxt(file)
    return heightmap

def write_route_points(file, route_points):
    numpy.savetxt(file, route_points, fmt="%f")







HEIGHTMAP_RANGE = 65535

class RouteReader():
    def __init__(self, vert_scale=60, heightmap_data=None, heightmap_file=None, points_data=None, points_file=None):
        if points_data is not None:
            self.points = points_data
        elif points_file:
            self.points = read_route_points(points_file)
        else:
            raise ValueError("Must provide either points or file")
        if heightmap_data is not None:
            self.heightmap = heightmap_data
        elif heightmap_file:
            self.heightmap = read_heightmap(heightmap_file)
        else:
            raise ValueError("Must provide either heightmap or file")
        self.vert_scale = vert_scale
        self.generate_metadata()
    
    def generate_metadata(self):
        self.total_distance = 0
        self.distances = [0]
        num_points = len(self.points)
        for i in range(num_points):
            self.total_distance += get_distance_2d(self.points[i], self.points[(i+1) % num_points])
            self.distances.append(self.total_distance)

    def get_interpolated_point_2d(self, ratio):
        num_points = len(self.points)
        distance = self.total_distance * ratio
        for i in range(1, num_points + 1):
            if distance < self.distances[i]:
                sub_ratio = (distance - self.distances[i-1]) / (self.distances[i] - self.distances[i-1])
                return interpolate_points(self.points[i-1], self.points[i % num_points], sub_ratio)
    
    def get_interpolated_point_3d(self, ratio):
        point = self.get_interpolated_point_2d(ratio)
        z = self.get_height(point)
        return (point[0], point[1], z)
    
    def get_interpolated_point_info(self, ratio):
        num_points = len(self.points)
        distance = self.total_distance * ratio
        for i in range(1, num_points + 1):
            if distance < self.distances[i]:
                sub_ratio = (distance - self.distances[i-1]) / (self.distances[i] - self.distances[i-1])
                point = interpolate_points(self.points[i-1], self.points[i % num_points], sub_ratio)
                last_point = self.points[i-1]
                next_point = self.points[i % num_points]
                direction = get_diff_2d(next_point, last_point)
                last_height = self.get_height(last_point)
                next_height = self.get_height(next_point)
                distance = get_distance_2d(last_point, next_point)
                slope = (next_height - last_height) / distance
                height = self.get_height(point)
                point_3d = (point[0], point[1], height)
                return (point_3d, direction, slope)

    def get_height(self, point):
        heightmap_value = get_height_interpolated(self.heightmap, point)
        height = heightmap_value * self.vert_scale / HEIGHTMAP_RANGE
        return height

    def flatten_heightmap_around_path(self, path_width=5, smoothening=10, divisions=1000):
        heights = []
        for i in range(divisions):
            point = self.get_interpolated_point_3d(i / divisions)
            heights.append(point[2])
        rolling_sum = 0
        for i in range(-smoothening, smoothening+1):
            ratio = (smoothening % divisions) / divisions
            point = self.get_interpolated_point_3d(ratio)
            rolling_sum += point[2]
        new_heights = [rolling_sum / (smoothening * 2 + 1)]
        for i in range(1, divisions):
            rolling_sum -= heights[(i - smoothening - 1) % divisions]
            rolling_sum += heights[(i + smoothening) % divisions]
            new_heights.append(rolling_sum / (smoothening * 2 + 1))
        cols = self.heightmap.shape[0]
        rows = self.heightmap.shape[1]
        heightmap_modification_sums = numpy.zeros((cols, rows), dtype=numpy.float32)
        heightmap_modification_counts = numpy.zeros((cols, rows), dtype=numpy.int32)
        for i in range(divisions):
            point = self.get_interpolated_point_2d(i / divisions)
            x_int = round(point[0])
            y_int = round(point[1])
            height = new_heights[i]
            for j in range(path_width):
                for k in range(path_width):
                    x = x_int - path_width//2 + j
                    y = y_int - path_width//2 + k
                    heightmap_modification_sums[x, y] += height
                    heightmap_modification_counts[x, y] += 1
        for i in range(cols):
            for j in range(rows):
                if heightmap_modification_counts[i, j] > 0:
                    self.heightmap[cols - j - 1][i] = int(heightmap_modification_sums[i, j] / heightmap_modification_counts[i, j] / self.vert_scale * HEIGHTMAP_RANGE)
                    
        return

    
        


