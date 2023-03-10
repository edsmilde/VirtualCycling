from math import pi, sin, cos


from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
import numpy
from panda3d.core import NodePath, Point3, GeoMipTerrain, Shader, DirectionalLight, Texture


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


ROUTE_PATH = 'assets/routes'

def load_route(route):
    return numpy.loadtxt(f'{ROUTE_PATH}/{route}.txt')



LOOP_TIME_SECONDS = 60
CAMERA_HORIZONTAL_DISTANCE = 20
CAMERA_VERTICAL_DISTANCE = 5
CAMERA_OLD_POINT = 5

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Disable the camera trackball controls.
        self.disableMouse()

        self.route_points = load_route('route1')

        terrain = GeoMipTerrain("terrain")
        terrain.setHeightfield("assets/heightmaps/route1.png")
        # terrain.setColorMap("t.jpg")
        terrain.setBruteforce(True)
        terrain.setBlockSize(64)
        terrain.setNear(20)
        terrain.setFar(100)


        texture = self.loader.loadTexture("assets/textures/route1.png")

        terrain.generate()

        self.terrain = terrain

        root = terrain.getRoot()
        root.setTexture(texture)
        
        root.reparentTo(self.render)
        self.vert_scale = 60
        root.setSz(self.vert_scale)
        dlight = DirectionalLight('dlight')
        dlight.setColor((0.8, 0.8, 0.5, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        self.render.setLight(dlnp)
        self.camera.setPos(-10, -10, 50)
        self.camera.lookAt(128, 128, 0)
        self.focus = (128, 128)
        self.direction = 45
        self.last_time = 0
        self.taskMgr.add(self.follow_route_task, "follow_route_task")
        # self.taskMgr.add(self.moveFocusTask, "moveFocusTask")
    
    def moveFocusTask(self, task):
        step_size = 10 * (task.time - self.last_time)
        angle_step = 20 * (task.time - self.last_time) * (numpy.random.random() - 0.5)
        self.direction = (self.direction + angle_step) % 360
        self.last_time = task.time
        self.focus = (self.focus[0] + step_size*cos_degrees(self.direction), self.focus[1] + step_size*sin_degrees(self.direction))
        focus_point = Point3(self.focus[0], self.focus[1], self.vert_scale*self.terrain.getElevation(self.focus[0], self.focus[1]))
        camera_distance = 10
        camera_vert = 5
        camera_point = Point3(self.focus[0] - camera_distance*cos_degrees(self.direction),
            self.focus[1] - camera_distance*sin_degrees(self.direction), self.vert_scale*self.terrain.getElevation(self.focus[0], self.focus[1]) + camera_vert)
        self.camera.setPos(camera_point)
        self.camera.lookAt(focus_point)
        return Task.cont

    def follow_route_task(self, task):
        step = (task.time % LOOP_TIME_SECONDS) / LOOP_TIME_SECONDS * len(self.route_points)
        step_int = int(step)
        step_frac = step - step_int
        last_point = self.route_points[step_int]
        next_point = self.route_points[(step_int + 1) % len(self.route_points)]
        current_point = interpolate_point(last_point, next_point, step_frac)
        current_point_height = self.vert_scale*self.terrain.getElevation(current_point[0], current_point[1])

        old_point = self.route_points[(step_int - CAMERA_OLD_POINT) % len(self.route_points)]
        camera_horizontal_displacement = diff_normalized(old_point, next_point, scale=CAMERA_HORIZONTAL_DISTANCE)
        focus_point = Point3(current_point[0], current_point[1], current_point_height)
        self.camera.setPos(current_point[0] - camera_horizontal_displacement[0], current_point[1] - camera_horizontal_displacement[1], current_point_height + CAMERA_VERTICAL_DISTANCE)
        self.camera.lookAt(focus_point)
        return Task.cont




app = MyApp()
app.run()







