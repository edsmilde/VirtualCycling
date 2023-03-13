from math import sin, cos, pi




def get_distance_2d(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return ((x2-x1)**2 + (y2-y1)**2)**0.5


def get_diff_2d(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return x2-x1, y2-y1


def get_diff_3d(point1, point2):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    return x2-x1, y2-y1, z2-z1



def get_height_rounded(heightmap, point):
    x, y = point
    x_int = round(x+0.5)
    y_int = round(y+0.5)
    return heightmap[y_int][x_int]




def get_midpoint(point1, point2):
    return interpolate_points(point1, point2, 0.5)


def get_normal(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    dy = y2 - y1
    dx = x2 - x2
    return dy, -dx




def get_normal_vector_2d(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    dy = y2 - y1
    dx = x2 - x1
    magnitude = (dy**2 + dx**2)**0.5
    if magnitude == 0:
        return 0, 0
    else:
        return dy/magnitude, -dx/magnitude



def get_normalized_vector_2d(point, scale=1):
    x, y = point
    magnitude = (x**2 + y**2)**0.5
    if magnitude == 0:
        return 0, 0
    else:
        return x/magnitude*scale, y/magnitude*scale



def get_normalized_vector_3d(point, scale=1):
    x, y, z = point
    magnitude = (x**2 + y**2 + z**2)**0.5
    if magnitude == 0:
        return 0, 0, 0
    else:
        return x/magnitude*scale, y/magnitude*scale, z/magnitude*scale




def get_slope_vector(point, heightmap):
    x, y = point
    left = get_height_rounded(heightmap, (x-1, y))
    right = get_height_rounded(heightmap, (x+1, y))
    top = get_height_rounded(heightmap, (x, y+1))
    bottom = get_height_rounded(heightmap, (x, y-1))
    return (right-left)/2, (top-bottom)/2



def interpolate_points(point1, point2, ratio):
    x1, y1 = point1
    x2, y2 = point2
    x = x1 + (x2-x1)*ratio
    y = y1 + (y2-y1)*ratio
    return x, y



def normalize_vector(vector):
    x, y = vector
    magnitude = (x**2 + y**2)**0.5
    return x/magnitude, y/magnitude






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


def round(x):
    return int(x+0.5)


