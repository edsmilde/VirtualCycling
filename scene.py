from math import pi, sin, cos


from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
import numpy
from panda3d.core import NodePath, Point3, GeoMipTerrain, Shader, DirectionalLight, Texture


from tools.route import RouteReader
from tools.geometry import *


ASSETS_PATH = 'assets'
ROUTES_PATH = f'{ASSETS_PATH}/routes'
HEIGHTMAPS_PATH = f'{ASSETS_PATH}/heightmaps'




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


def interpolate_point(point_1, point_2, ratio):
    x1, y1 = point_1
    x2, y2 = point_2
    return x1 + (x2-x1)*ratio, y1 + (y2-y1)*ratio


def diff(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    return x2-x1, y2-y1

def diff_normalized(point_1, point_2, scale=1):
    return normalize(diff(point_1, point_2), scale=scale)



def load_route_points(route):
    return numpy.loadtxt(f'{ROUTES_PATH}/{route}.txt')



LOOP_TIME_SECONDS = 60
CAMERA_HORIZONTAL_DISTANCE = 20
CAMERA_VERTICAL_DISTANCE = 5
CAMERA_OLD_POINT = 4
CAMERA_ROTATE_TIME_SECONDS = 1

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Disable the camera trackball controls.
        self.disableMouse()

        self.load_map('route1')

        dlight = DirectionalLight('dlight')
        dlight.setColor((0.8, 0.8, 0.5, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        self.render.setLight(dlnp)
        point, direction, slope = self.route_reader.get_interpolated_point_info(0)
        camera_displacement = get_normalized_vector_2d(direction, CAMERA_HORIZONTAL_DISTANCE)
        self.go_to_point_direction(point, camera_displacement)
        self.direction = 45
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
    

    def go_to_point_direction(self, point, camera_displacement):
        camera_point = point[0] + camera_displacement[0], point[1] + camera_displacement[1], point[2] + CAMERA_VERTICAL_DISTANCE
        self.camera.setPos(camera_point)
        self.camera.lookAt(point)
        self.camera_displacement = camera_displacement


    def follow_route_task(self, task):
        ratio = (task.time % LOOP_TIME_SECONDS) / LOOP_TIME_SECONDS
        # step_int = int(step)
        # step_frac = step - step_int
        # last_point = self.route_points[step_int]
        # next_point = self.route_points[(step_int + 1) % len(self.route_points)]
        # current_point = interpolate_point(last_point, next_point, step_frac)
        # current_point_height = self.vert_scale*self.terrain.getElevation(current_point[0], current_point[1])

        # old_point_last = self.route_points[(step_int - CAMERA_OLD_POINT) % len(self.route_points)]
        # old_point_next = self.route_points[(step_int - CAMERA_OLD_POINT + 1) % len(self.route_points)]
        # old_point = interpolate_point(old_point_last, old_point_next, step_frac)
        # camera_horizontal_displacement = diff_normalized(old_point, next_point, scale=CAMERA_HORIZONTAL_DISTANCE)
        # focus_point = Point3(current_point[0], current_point[1], current_point_height)
        point, direction, slope = self.route_reader.get_interpolated_point_info(ratio)
        time_delta = task.time - self.last_time
        self.last_time = task.time
        target_camera_displacement = get_normalized_vector_2d(direction, CAMERA_HORIZONTAL_DISTANCE)
        camera_displacement_diff = get_distance_2d(target_camera_displacement, self.camera_displacement)/CAMERA_HORIZONTAL_DISTANCE
        camera_move_distance = time_delta/CAMERA_ROTATE_TIME_SECONDS
        if camera_move_distance >= camera_displacement_diff:
            camera_displacement = target_camera_displacement
        else:
            camera_displacement = interpolate_point(self.camera_displacement, target_camera_displacement, camera_move_distance/camera_displacement_diff)
        self.go_to_point_direction(point, camera_displacement)
        return Task.cont




app = MyApp()
app.run()







