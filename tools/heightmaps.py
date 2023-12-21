from enum import Enum
import math
import random


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3



def radians(degrees):
    return degrees * math.pi / 180


def round(num):
    return int(num + 0.5)



def interpolate_scalar(a, b, ratio):
    return a + (b - a) * ratio


def interpolate_vector(a, b, ratio):
    size = len(a)
    if len(b) != size:
        raise ValueError('Vectors must be the same size')
    result = []
    for i in range(size):
        value = interpolate_scalar(a[i], b[i], ratio)
        result.append(value)
    return result


def get_distance(a, b):
    size = len(a)
    if len(b) != size:
        raise ValueError('Vectors must be the same size')
    sum = 0
    for i in range(size):
        diff = a[i] - b[i]
        sum += diff * diff
    return math.sqrt(sum)


def interpolate_scalar_2d(sw, se, nw, ne, x_ratio, y_ratio):
    val = sw*x_ratio*y_ratio
    val += se*(1-x_ratio)*y_ratio
    val += nw*x_ratio*(1-y_ratio)
    val += ne*(1-x_ratio)*(1-y_ratio)
    return val


def get_or_default(array, x, y, default_value=None):
    try:
        return array[x][y]
    except IndexError:
        return default_value



def get_2d_array(width, height, default_value=0):
    array = []
    for i in range(width):
        row = [default_value] * height
        array.append(row)
    return array


def get_normals(heightmap, base_resolution=4):
    width = len(heightmap)
    height = len(heightmap[0])
    normals = get_2d_array(width, height, default_value=None)
    for i in range(width):
        for j in range(height):
            z = heightmap[i][j]
            z_x_right = get_or_default(heightmap, i+1, j, default_value=z)
            z_x_left = get_or_default(heightmap, i-1, j, default_value=z)
            z_y_top = get_or_default(heightmap, i, j+1, default_value=z)
            z_y_bottom = get_or_default(heightmap, i, j-1, default_value=z)
            normal_x = (z_x_left - z_x_right)*2/base_resolution
            normal_y = (z_y_bottom - z_y_top)*2/base_resolution
            normals[i][j] = [normal_x, normal_y, 1]
    return normals




def round_down(num):
    return int(num)

def round_up(num):
    if num == int(num):
        return int(num)
    else:
        return int(num) + 1




def power_2_random_block(size, horizontal_variance, vertical_variance):
    block = get_2d_array(size, size, default_value=0)
    step_size = size-1
    vertical_variance_step = vertical_variance
    horizontal_variance_step = horizontal_variance
    while step_size > 1:
        for i in range(0, size-1, step_size):
            for j in range(0, size-1, step_size):
                value_bottom_left = block[i][j]
                value_bottom_right = block[i+step_size][j]
                value_top_left = block[i][j+step_size]
                value_top_right = block[i+step_size][j+step_size]
                value_top = (value_top_left + value_top_right) / 2 + random.uniform(-horizontal_variance_step, horizontal_variance_step)
                value_bottom = (value_bottom_left + value_bottom_right) / 2 + random.uniform(-horizontal_variance_step, horizontal_variance_step)
                value_left = (value_bottom_left + value_top_left) / 2 + random.uniform(-vertical_variance_step, vertical_variance_step)
                value_right = (value_bottom_right + value_top_right) / 2 + random.uniform(-vertical_variance_step, vertical_variance_step)
                center_variance = (horizontal_variance_step + vertical_variance_step) / 2
                value_center = (value_left + value_right + value_bottom + value_top) / 4 + random.uniform(-center_variance, center_variance)
                block[i+step_size//2][j] = value_bottom
                block[i+step_size//2][j+step_size] = value_top
                block[i][j+step_size//2] = value_left
                block[i+step_size][j+step_size//2] = value_right
                block[i+step_size//2][j+step_size//2] = value_center
        step_size //= 2
        vertical_variance_step /= 2
        horizontal_variance_step /= 2
    return block


def decrease_resolution_inline(block, x, y, size, new_resolution):
    ratio = int(new_resolution/size)
    for i in range(size+1):
        for j in range(size+1):
            if i % ratio == 0 and j % ratio == 0:
                continue
            ratio_i = (i % ratio) / ratio
            ratio_j = (j % ratio) / ratio
            left = x + i - i % ratio
            right = left + ratio
            bottom = y + j - j % ratio
            top = bottom + ratio
            value = interpolate_scalar_2d(block[left][bottom], block[right][bottom], block[left][top], block[right][top], ratio_i, ratio_j)
            block[x+i][y+j] = value
    return


def scale_block(block, desired_width, desired_height):
    block_width = len(block)
    block_height = len(block[0])
    new_block = get_2d_array(desired_width, desired_height, default_value=0)
    for i in range(desired_width):
        for j in range(desired_height):
            x = i * (block_width-1) / (desired_width-1)
            x_int = int(x)
            x_frac = x - x_int
            y = j * (block_height-1) / (desired_height-1)
            y_int = int(y)
            y_frac = y - y_int
            
            val_bottom_left = get_or_default(block, x_int, y_int, 0)
            val_bottom_right = get_or_default(block, x_int+1, y_int, 0)
            val_top_left = get_or_default(block, x_int, y_int+1, 0)
            val_top_right = get_or_default(block, x_int+1, y_int+1, 0)
            val = interpolate_scalar_2d(val_bottom_left, val_bottom_right, val_top_left, val_top_right, x_frac, y_frac)
            # val = val_bottom_left * (1-x_frac) * (1-y_frac) + val_bottom_right * x_frac * (1-y_frac) + val_top_left * (1-x_frac) * y_frac + val_top_right * x_frac * y_frac
            new_block[i][j] = val
    return new_block


def get_random_block(width, height, variance_horizontal=1, variance_vertical=1):
    block = get_2d_array(width, height, default_value=0)
    size = 2
    while size < width or size < height:
        size = (size - 1) * 2 + 1
    power_2_block = power_2_random_block(size, variance_horizontal, variance_vertical)
    block = scale_block(power_2_block, width, height)
    return block


def adjust_to_anchors(block, height_anchors):
    width = len(block)
    height = len(block[0])
    anchor_diffs = {}
    for anchor in height_anchors:
        x, y, z = anchor
        diff = z - block[x][y]
        anchor_diffs[(x, y)] = diff
    for i in range(width):
        for j in range(height):
            harmonic_sum = 0
            harmonic_denom = 0
            diff = 0
            is_anchor = False
            for anchor_diff in anchor_diffs:
                x, y = anchor_diff
                if x == i and y == j:
                    diff = anchor_diffs[anchor_diff]
                    is_anchor = True
                    continue
                distance = get_distance((i, j), (x, y))
                harmonic_sum += anchor_diffs[anchor_diff] / distance
                harmonic_denom += 1 / distance
            if not is_anchor:
                diff = harmonic_sum / harmonic_denom
            block[i][j] += diff


def get_path_point(x, y, tiles, resolutions):

    pass




def get_direction(first_point, second_point):
    if first_point[0] < second_point[0]:
        return Direction.WEST
    elif first_point[0] > second_point[0]:
        return Direction.EAST
    elif first_point[1] < second_point[1]:
        return Direction.SOUTH
    elif first_point[1] > second_point[1]:
        return Direction.NORTH
    else:
        return None


def get_path_direction(point, last_point, next_point):
    last_direction = get_direction(last_point, point)
    next_direction = get_direction(point, next_point)
    return last_direction, next_direction



def get_path_directions(route_points):
    directions = []
    num_points = len(route_points)
    for i in range(len(route_points)):
        point = route_points[i]
        next_point = route_points[(i+1) % num_points]
        last_point = route_points[(i-1) % num_points]
        last_direction, next_direction = get_path_direction(point, last_point, next_point)
        directions.append((last_direction, next_direction))
    return directions





def interpolate_tile(directions, ratio):
    if directions[0] == Direction.NORTH:
        if directions[1] == Direction.EAST:
            return interpolate_tile_arc((1, 1), 0.5, radians(180), radians(270), ratio)
        elif directions[1] == Direction.WEST:
            return interpolate_tile_arc((0, 1), 0.5, radians(0), radians(-90), ratio)
        else:
            return (0.5, 1 - ratio)
    elif directions[0] == Direction.SOUTH:
        if directions[1] == Direction.EAST:
            return interpolate_tile_arc((1, 0), 0.5, radians(180), radians(90), ratio)
        elif directions[1] == Direction.WEST:
            return interpolate_tile_arc((0, 0), 0.5, radians(0), radians(90), ratio)
        else:
            return (0.5, ratio)
    elif directions[0] == Direction.EAST:
        if directions[1] == Direction.NORTH:
            return interpolate_tile_arc((1, 1), 0.5, radians(270), radians(180), ratio)
        elif directions[1] == Direction.SOUTH:
            return interpolate_tile_arc((1, 0), 0.5, radians(90), radians(180), ratio)
        else:
            return (1 - ratio, 0.5)
    elif directions[0] == Direction.WEST:
        if directions[1] == Direction.NORTH:
            return interpolate_tile_arc((0, 1), 0.5, radians(-90), radians(0), ratio)
        elif directions[1] == Direction.SOUTH:
            return interpolate_tile_arc((0, 0), 0.5, radians(90), radians(0), ratio)
        else:
            return (ratio, 0.5)
    else:
        raise ValueError("Invalid direction: " + str(directions))




def interpolate_tile_arc(center, radius, start_angle, end_angle, ratio):
    angle = start_angle + (end_angle - start_angle) * ratio
    x = center[0] + radius * math.cos(angle)
    y = center[1] + radius * math.sin(angle)
    return x, y



def get_tile_road_distance_point(directions, relative_point):
    x, y = relative_point
    if directions[0] == Direction.NORTH:
        if directions[1] == Direction.EAST:
            return get_tile_arc_path_position((1, 1), 0.5, radians(180), radians(270), relative_point)



def get_tile_arc_path_position(center, radius, start_angle, end_angle, relative_point):
    x, y = relative_point
    center_x, center_y = center
    center_distance = get_distance(center, relative_point)
    path_distance = math.abs(center_distance - radius)
    if x == center_x:
        if y > center_y:
            angle = radians(90)
        else:
            angle = radians(270)
    else:
        angle = math.atan((y - center_y) / (x - center_x))
    while angle < start_angle:
        angle += radians(180)
    while angle > end_angle:
        angle -= radians(180)
    angle_ratio = (angle - start_angle) / (end_angle - start_angle)
    return angle_ratio, path_distance
    

def flatten_path(block, route_points, base_resolution):
    directions = get_path_directions(route_points)
    for k in range(len(route_points)):
        point = route_points[k]
        base_x = point[0]*base_resolution
        base_y = point[1]*base_resolution
        for i in range(base_resolution):
            for j in range(base_resolution):
                x = base_x + i
                y = base_y + j

                pass


        pass


    pass



