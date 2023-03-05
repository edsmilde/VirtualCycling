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


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Disable the camera trackball controls.
        self.disableMouse()


        terrain = GeoMipTerrain("terrain")
        terrain.setHeightfield("assets/heightmaps/height_257.png")
        # terrain.setColorMap("t.jpg")
        terrain.setBruteforce(True)
        terrain.setBlockSize(64)
        terrain.setNear(20)
        terrain.setFar(100)


        texture = self.loader.loadTexture("assets/textures/green.png")

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
        self.taskMgr.add(self.moveFocusTask, "moveFocusTask")
    
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




app = MyApp()
app.run()







