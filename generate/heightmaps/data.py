from PIL import Image
import numpy as np



MAX_DEPTH = 256*256-1
MID_DEPTH = 256*128

SIDE_LENGTH = 257

def value_or_zero(value):
    if value < 0:
        return 0
    elif value > MAX_DEPTH:
        return MAX_DEPTH
    else:
        return value




def generate_hilly_terrain(height, width, variance=0, corners=(MID_DEPTH, MID_DEPTH, MID_DEPTH, MID_DEPTH)):
    data = np.zeros((height, width), dtype=np.uint16)
    data[0][0] = corners[0]
    data[0][width-1] = corners[1]
    data[height-1][0] = corners[2]
    data[height-1][width-1] = corners[3]

    step_size = width - 1
    while step_size > 1:
        half_step = step_size // 2
        # Horizontal
        for y in range(0, height, step_size):
            for x in range(0, width - 1, step_size):
                # Horizontal
                x_mid = x + half_step
                avg = (int(data[y][x]) + int(data[y][x + step_size])) // 2
                data[y][x_mid] = value_or_zero(avg + np.random.randint(-variance, variance))
        # Vertical
        for y in range(0, height - 1, step_size):
            for x in range(0, width, step_size):
                y_mid = y + half_step
                avg = (int(data[y][x]) + int(data[y + step_size][x])) // 2
                data[y_mid][x] = value_or_zero(avg + np.random.randint(-variance, variance))
        # Center
        for y in range(0, height - 1, step_size):
            for x in range(0, width - 1, step_size):
                x_mid = x + half_step
                y_mid = y + half_step
                avg = (int(data[y_mid][x]) + int(data[y_mid][x + step_size]) + int(data[y][x_mid]) + int(data[y + step_size][x_mid])) // 4
                data[y_mid][x_mid] = value_or_zero(avg + np.random.randint(-variance, variance))
 
        step_size //= 2
        variance //= 2


    return data


# my_data = generate_hilly_terrain(SIDE_LENGTH, SIDE_LENGTH, variance=MAX_DEPTH//4, corners=(MAX_DEPTH//2, MAX_DEPTH//2, MAX_DEPTH//2, MAX_DEPTH//2))

# image = Image.fromarray(my_data, mode='I;16')

# image.save('height_257.png')
