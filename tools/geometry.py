from math import sin, cos, pi




def get_distance_2d(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return ((x2-x1)**2 + (y2-y1)**2)**0.5


def get_distance_3d(point1, point2):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    return ((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)**0.5



def get_diff_2d(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return x2-x1, y2-y1


def get_diff_3d(point1, point2):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    return x2-x1, y2-y1, z2-z1



def get_height_int(heightmap, point):
    x, y = point
    height = heightmap.shape[1]
    return heightmap[height - 1 - y, x]



def get_height_interpolated(heightmap, point):
    x, y = point
    x_left = int(x)
    x_right = x_left + 1
    y_bottom = int(y)
    y_top = y_bottom + 1
    x_ratio = x - x_left
    y_ratio = y - y_bottom
    height_top_left = get_height_int(heightmap, (x_left, y_top))
    height_top_right = get_height_int(heightmap, (x_right, y_top))
    height_bottom_left = get_height_int(heightmap, (x_left, y_bottom))
    height_bottom_right = get_height_int(heightmap, (x_right, y_bottom))
    height_top = interpolate(height_top_left, height_top_right, x_ratio)
    height_bottom = interpolate(height_bottom_left, height_bottom_right, x_ratio)
    return interpolate(height_top, height_bottom, y_ratio)



def get_height_rounded(heightmap, point):
    x, y = point
    x_int = round(x)
    # y_int = round(y)
    width = heightmap.shape[0]
    height = heightmap.shape[1]
    return heightmap[height - 1 - y_int, x_int]




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



def interpolate(value1, value2, ratio):
    return value1 + (value2-value1)*ratio



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


