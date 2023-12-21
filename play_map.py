import json
from math import pi, sin, cos


from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
import numpy
from panda3d.core import NodePath, Point3, GeomVertexWriter, GeoMipTerrain, Shader, DirectionalLight, AmbientLight, Texture, TextureStage
from panda3d.egg import EggData

from tools.route import RouteReader
from tools.geometry import *


ASSETS_PATH = 'assets'
ROUTES_PATH = f'{ASSETS_PATH}/routes'
HEIGHTMAPS_PATH = f'{ASSETS_PATH}/heightmaps'
OBJECTS_PATH = f'{ASSETS_PATH}/objects'
TEXTURES_PATH = f'{ASSETS_PATH}/textures'

MAPS_PATH = f'{ASSETS_PATH}/maps'



LOOP_TIME_SECONDS = 60
CAMERA_HORIZONTAL_DISTANCE = 10
CAMERA_VERTICAL_DISTANCE = 2
CAMERA_OLD_POINT = 4
CAMERA_ROTATE_TIME_SECONDS = 1

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Disable the camera trackball controls.
        self.disable_mouse()

        self.load_map('map2')





        dlight = DirectionalLight('dlight')
        dlight.setColor((0.8, 0.7, 0.5, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(180, -60, 0)
        self.render.setLight(dlnp)

        self.camera.set_pos((-40, -40, 40))
        self.camera.look_at((40, 40, 0))

    
    def load_map(self, map_name):
        BLOCK_SIZE = 20
        map_path = f'{MAPS_PATH}/{map_name}'
        map_info = json.load(open(f'{map_path}/info.json'))
        height = map_info['dimensions']['height']
        width = map_info['dimensions']['height']
        for i in range(width):
            for j in range(height):
                block = self.loader.load_model(f"{map_path}/tile_{i}_{j}.bam")
                block.reparent_to(self.render)
                block.setPos((i+0.5)*BLOCK_SIZE, (j+0.5)*BLOCK_SIZE, 0)
                block.setScale(BLOCK_SIZE/2)
                # texture = self.loader.load_texture(f"{TEXTURES_PATH}/map4.png")
                # old_texture = block.find_texture('PlainTexture')
                # block.replace_texture(old_texture, texture)



        pass
    




app = MyApp()
app.run()







