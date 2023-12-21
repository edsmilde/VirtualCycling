import json
import random


from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
import numpy
from panda3d.core import ( 
    NodePath, Point3, GeomVertexWriter, GeomVertexReader,
    GeoMipTerrain, Shader, DirectionalLight, AmbientLight, Texture, TextureStage,
    Material
)
from panda3d.egg import EggData

from tools.heightmaps import (
    round, get_2d_array, get_normals, get_random_block, adjust_to_anchors
)

MAP_SEEDS_PATH = './input/maps'
FILE_EXTENSION = '.json'
ASSETS_PATH = './assets'
GROUND_MODELS_PATH = f'{ASSETS_PATH}/models/ground'
GROUND_TEXTURES_PATH = f'{ASSETS_PATH}/textures/ground'
MAPS_PATH = f'{ASSETS_PATH}/maps'





TILE_SIZE=2

class ModelAssembler(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
    
    def create_tile(self, map_name, tile_type, x, y, heightmap=None, normals=None, resolution=4):
        texture_prefix = 'path_'
        texture_path = f'{GROUND_TEXTURES_PATH}/{texture_prefix}{tile_type}.png'
        resolution_tag = f'{resolution}x{resolution}'
        model_path = f'{GROUND_MODELS_PATH}/plain_{resolution_tag}.bam'
        model = self.loader.load_model(model_path)
        texture = self.loader.load_texture(texture_path)

        # Create a texture stage and set its properties
        # ts = TextureStage('ts')
        # ts.setMode(TextureStage.MModulate)
        # ts.setSort(1)

        # Create a material and set its properties
        # material = Material()
        # material.setShininess(50.0)
        # material.setAmbient((0.2, 0.2, 0.2, 1.0))
        # material.setDiffuse((1.0, 1.0, 1.0, 1.0))
        # material.setSpecular((1.0, 1.0, 1.0, 1.0))

        # Apply the material and texture to the model
        # model.setMaterial(mat)
        # model.setTexture(ts, texture)



        plain_texture = model.find_texture('PlainTexture')
        # plain_material = model.find_material('*')
        model.replace_texture(plain_texture, texture)
        # model.replace_material(plain_material, material)

        # Vertex manipulation
        if heightmap:
            vertex_writer = GeomVertexWriter(model.get_child(0).get_child(0).node().modify_geom(0).modify_vertex_data(), 'vertex')
            normal_writer = GeomVertexWriter(model.get_child(0).get_child(0).node().modify_geom(0).modify_vertex_data(), 'normal')
            vertex_reader = GeomVertexReader(model.get_child(0).get_child(0).node().get_geom(0).get_vertex_data(), 'vertex')
            while not vertex_reader.is_at_end():
                vx, vy, vz = vertex_reader.get_data3f()
                i = round((vx + TILE_SIZE/2) / TILE_SIZE * resolution)
                j = round((vy + TILE_SIZE/2) / TILE_SIZE * resolution)
                new_z = heightmap[i][j]
                normal = normals[i][j]
                vertex_writer.set_data3f(vx, vy, new_z)
                normal_writer.set_data3f(normal[0], normal[1], normal[2])
                


        model.write_bam_file(f'{MAPS_PATH}/{map_name}/tile_{x}_{y}.bam')


assembler = ModelAssembler()


def generate_map(map_name):
    map_seed_filename = f'{MAP_SEEDS_PATH}/{map_name}{FILE_EXTENSION}'
    with open(map_seed_filename, 'r') as map_seed_file:
        map_seed_data = json.load(map_seed_file)
    width_blocks = map_seed_data['dimensions']['width']
    height_blocks = map_seed_data['dimensions']['height']
    tiles = get_2d_array(width_blocks, height_blocks, default_value='plain')
    zs = get_2d_array(width_blocks, height_blocks, default_value=None)
    base_resolution = 16
    block_size=20
    resolutions = get_2d_array(width_blocks, height_blocks, default_value=base_resolution)
    route = map_seed_data['route']
    route_length = len(route)
    height_anchors = []
    for i in range(route_length):
        point = route[i]
        (x, y, z) = point
        world_point = (int((x+0.5) * base_resolution), int((y+0.5) * base_resolution), z/block_size)
        height_anchors.append(world_point)
        last_point = route[(i - 1) % route_length]
        next_point = route[(i + 1) % route_length]
        if last_point[0] == point[0] and next_point[0] == point[0]:
            tiles[point[1]][point[0]] = 'ns'
        elif last_point[1] == point[1] and next_point[1] == point[1]:
            tiles[point[1]][point[0]] = 'ew'
        elif last_point[0] < point[0]:
            if next_point[1] > point[1]:
                tiles[point[1]][point[0]] = 'nw'
            else:
                tiles[point[1]][point[0]] = 'sw'
        elif last_point[0] > point[0]:
            if next_point[1] > point[1]:
                tiles[point[1]][point[0]] = 'ne'
            else:
                tiles[point[1]][point[0]] = 'se'
        elif last_point[1] < point[1]:
            if next_point[0] > point[0]:
                tiles[point[1]][point[0]] = 'se'
            else:
                tiles[point[1]][point[0]] = 'sw'
        elif last_point[1] > point[1]:
            if next_point[0] > point[0]:
                tiles[point[1]][point[0]] = 'ne'
            else:
                tiles[point[1]][point[0]] = 'nw'
        zs[point[1]][point[0]] = point[2]
    
    width_points = width_blocks * base_resolution + 1
    height_points = height_blocks * base_resolution + 1
    zmap = get_random_block(width_points, height_points, 0.5, 0.5)
    adjust_to_anchors(zmap, height_anchors)
    normals = get_normals(zmap)
    for i in range(width_blocks):
        for j in range(height_blocks):
            res = resolutions[i][j]
            tile_heightmap = get_2d_array(base_resolution+1, base_resolution+1, default_value=0)
            tile_normals = get_2d_array(base_resolution+1, base_resolution+1, default_value=[0, 0, 0])
            for k in range(res+1):
                for l in range(res+1):
                    tile_heightmap[k][l] = zmap[i*res+k][j*res+l]
                    tile_normals[k][l] = normals[i*res+k][j*res+l]
            assembler.create_tile(map_name, tiles[j][i], i, j, heightmap=tile_heightmap, normals=tile_normals, resolution=resolutions[i][j])

    map_data = {
        'dimensions': {
            'width': width_blocks,
            'height': height_blocks
        },
    }
    json.dump(map_data, open(f'{MAPS_PATH}/{map_name}/info.json', 'w'), indent=4)
        

    





