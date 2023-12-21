from PIL import Image, ImageDraw


BACKGROUND_COLOR = (0, 150, 0)
PATH_COLOR = (90, 90, 90)

SIDE_LENGTH = 1024
PATH_WIDTH = 128

ASSETS_PATH = './assets'
TEXTURES_PATH = f'{ASSETS_PATH}/textures'
FILE_EXTENSION = '.png'

def generate_paths():
    minor_side = (SIDE_LENGTH-PATH_WIDTH)/2
    major_side = (SIDE_LENGTH+PATH_WIDTH)/2
    path_prefix = "path_"
    def get_path(path_name):
        return f'{TEXTURES_PATH}/{path_prefix}{path_name}{FILE_EXTENSION}'

    image_plain = Image.new('RGB', (SIDE_LENGTH, SIDE_LENGTH), BACKGROUND_COLOR)
    image_plain.save(get_path("plain"))


    image_ns = Image.new('RGB', (SIDE_LENGTH, SIDE_LENGTH), BACKGROUND_COLOR)
    draw_ns = ImageDraw.Draw(image_ns)
    draw_ns.rectangle((minor_side, 0, major_side, SIDE_LENGTH), fill=PATH_COLOR)
    image_ns.save(get_path("ns"))

    image_ew = Image.new('RGB', (SIDE_LENGTH, SIDE_LENGTH), BACKGROUND_COLOR)
    draw_ew = ImageDraw.Draw(image_ew)
    draw_ew.rectangle((0, minor_side, SIDE_LENGTH, major_side), fill=PATH_COLOR)
    image_ew.save(get_path("ew"))



    image_ne = Image.new('RGB', (SIDE_LENGTH, SIDE_LENGTH), BACKGROUND_COLOR)
    draw_ne = ImageDraw.Draw(image_ne)
    draw_ne.ellipse((minor_side, -major_side, SIDE_LENGTH+major_side, major_side), fill=PATH_COLOR)
    draw_ne.ellipse((major_side, -minor_side, SIDE_LENGTH+minor_side, minor_side), fill=BACKGROUND_COLOR)
    image_ne.save(get_path("ne"))

    image_sw = Image.new('RGB', (SIDE_LENGTH, SIDE_LENGTH), BACKGROUND_COLOR)
    draw_sw = ImageDraw.Draw(image_sw)
    draw_sw.ellipse((-major_side, minor_side, major_side, SIDE_LENGTH+major_side), fill=PATH_COLOR)
    draw_sw.ellipse((-minor_side, major_side, minor_side, SIDE_LENGTH+minor_side), fill=BACKGROUND_COLOR)
    image_sw.save(get_path("sw"))

    image_se = Image.new('RGB', (SIDE_LENGTH, SIDE_LENGTH), BACKGROUND_COLOR)
    draw_se = ImageDraw.Draw(image_se)
    draw_se.ellipse((minor_side, minor_side, SIDE_LENGTH+major_side, SIDE_LENGTH+major_side), fill=PATH_COLOR)
    draw_se.ellipse((major_side, major_side, SIDE_LENGTH+minor_side, SIDE_LENGTH+minor_side), fill=BACKGROUND_COLOR)
    image_se.save(get_path("se"))


    image_nw = Image.new('RGB', (SIDE_LENGTH, SIDE_LENGTH), BACKGROUND_COLOR)
    draw_nw = ImageDraw.Draw(image_nw)
    draw_nw.ellipse((-major_side, -major_side, major_side, major_side), fill=PATH_COLOR)
    draw_nw.ellipse((-minor_side, -minor_side, minor_side, minor_side), fill=BACKGROUND_COLOR)
    image_nw.save(get_path("nw"))






