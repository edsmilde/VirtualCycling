from math import pi, sin, cos


from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
import numpy
from panda3d.core import NodePath, Point3, GeoMipTerrain, Shader, DirectionalLight, AmbientLight, Texture


from tools.route import RouteReader
from tools.geometry import *


ASSETS_PATH = 'assets'
ROUTES_PATH = f'{ASSETS_PATH}/routes'
HEIGHTMAPS_PATH = f'{ASSETS_PATH}/heightmaps'
OBJECTS_PATH = f'{ASSETS_PATH}/objects'



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

        self.load_map('map3')

        for i in range(100):
            tree_num = numpy.random.randint(1, 4)
            tree = self.loader.loadModel(f"{OBJECTS_PATH}/tree{tree_num}.bam")
            tree.reparentTo(self.render)
            tree_pos_ratio = numpy.random.rand()
            tree_pos = self.route_reader.get_interpolated_point_3d(tree_pos_ratio)
            tree.setPos(*tree_pos)
            tree.setScale(0.5)



        dlight = DirectionalLight('dlight')
        dlight.setColor((0.8, 0.8, 0.5, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        self.render.setLight(dlnp)
        alight = AmbientLight('alight')
        alight.setColor((0.5, 0.5, 0.5, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)




        point, direction, slope = self.route_reader.get_interpolated_point_info(0)
        self.position_camera(point, direction, slope, 0, init=True)
        self.last_time = 0

        self.taskMgr.add(self.follow_route_task, "follow_route_task")
    

    def load_map(self, route):
        route_file = f"{ROUTES_PATH}/{route}.txt"
        heightmap_file = f"{HEIGHTMAPS_PATH}/{route}.txt"

        self.route_points = numpy.loadtxt(route_file)
        
        self.route_reader = RouteReader(vert_scale=120, heightmap_file=heightmap_file, points_file=route_file)

        terrain = GeoMipTerrain("terrain")
        terrain.setHeightfield(f"{HEIGHTMAPS_PATH}/{route}.png")
        terrain.setBruteforce(True)
        terrain.setBlockSize(64)
        terrain.setNear(20)
        terrain.setFar(100)

        texture = self.loader.loadTexture(f"assets/textures/{route}.png")

        terrain.generate()

        self.terrain = terrain

        root = terrain.getRoot()
        root.setTexture(texture)
        
        root.reparentTo(self.render)
        self.vert_scale = 120
        root.setSz(self.vert_scale)
    
    def position_camera(self, point, direction, slope, time_delta, init=False):
        target_xy_displacement = get_normalized_vector_2d(direction, CAMERA_HORIZONTAL_DISTANCE)
        target_z_displacement = CAMERA_VERTICAL_DISTANCE
        target_displacement = target_xy_displacement[0], target_xy_displacement[1], target_z_displacement
        if init:
            self.camera_displacement = target_displacement
        camera_displacement_diff = get_distance_3d(target_displacement, self.camera_displacement)
        camera_move_distance = time_delta/CAMERA_ROTATE_TIME_SECONDS*CAMERA_HORIZONTAL_DISTANCE
        if camera_move_distance >= camera_displacement_diff:
            camera_displacement = target_displacement
        else:
            camera_displacement = interpolate_point_3d(self.camera_displacement, target_displacement, camera_move_distance/camera_displacement_diff)
        camera_point = point[0] + camera_displacement[0], point[1] + camera_displacement[1], point[2] + camera_displacement[2]
        self.camera.setPos(camera_point)
        self.camera.lookAt(point)
        self.camera_displacement = camera_displacement




    def follow_route_task(self, task):
        ratio = (task.time % LOOP_TIME_SECONDS) / LOOP_TIME_SECONDS
        point, direction, slope = self.route_reader.get_interpolated_point_info(ratio)
        time_delta = task.time - self.last_time
        self.last_time = task.time
        self.position_camera(point, direction, slope, time_delta)

        return Task.cont




app = MyApp()
app.run()







