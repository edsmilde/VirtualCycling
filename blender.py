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



def radians(degrees):
    return degrees * pi / 180

def sin_degrees(degrees):
    return sin(radians(degrees))

def cos_degrees(degrees):
    return cos(radians(degrees))


def normalize(vector, scale=1):
    x, y = vector
    magnitude = (x**2 + y**2)**0.5
    if magnitude == 0:
        return 0, 0
    return x/magnitude*scale, y/magnitude*scale


def interpolate_point_2d(point_1, point_2, ratio):
    x1, y1 = point_1
    x2, y2 = point_2
    return x1 + (x2-x1)*ratio, y1 + (y2-y1)*ratio


def interpolate_point_3d(point_1, point_2, ratio):
    x1, y1, z1 = point_1
    x2, y2, z2 = point_2
    return x1 + (x2-x1)*ratio, y1 + (y2-y1)*ratio, z1 + (z2-z1)*ratio



def diff(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    return x2-x1, y2-y1

def diff_normalized(point_1, point_2, scale=1):
    return normalize(diff(point_1, point_2), scale=scale)



def load_route_points(route):
    return numpy.loadtxt(f'{ROUTES_PATH}/{route}.txt')



LOOP_TIME_SECONDS = 60
CAMERA_HORIZONTAL_DISTANCE = 10
CAMERA_VERTICAL_DISTANCE = 2
CAMERA_OLD_POINT = 4
CAMERA_ROTATE_TIME_SECONDS = 1

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Disable the camera trackball controls.
        self.disableMouse()

        map = self.loader.loadModel(f"{OBJECTS_PATH}/plain_16x16.bam")
        map.set_scale(100)
        texture = self.loader.loadTexture(f"{TEXTURES_PATH}/map4.png")
        old_texture = map.findTexture('PlainTexture')
        map.replaceTexture(old_texture, texture)

        map.reparentTo(self.render)

        vd = map.children[0].children[0].node().modifyGeom(0).modifyVertexData()
        vw = GeomVertexWriter(vd, 'vertex')

        self.camera.setPos(-150, -150, 30)
        self.camera.lookAt(0, 0, 0)



        dlight = DirectionalLight('dlight')
        dlight.setColor((0.8, 0.7, 0.5, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        self.render.setLight(dlnp)
    




app = MyApp()
app.run()







