from PIL import Image
import numpy as np



def write_png(path, data):
    image = Image.fromarray(data, mode='I;16')
    image.save(path, optimize=True, compress_level=9)

