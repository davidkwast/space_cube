import sys
from math import radians, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBase import loadPrcFileData
from direct.showbase.ShowBase import DirectObject
from panda3d.core import ClockObject
from panda3d.core import KeyboardButton
from panda3d.core import WindowProperties

# from direct.task import Task

class ReadKeys(DirectObject.DirectObject):
    def __init__(self, base):
        self.base = base
        self.is_down = base.mouseWatcherNode.is_button_down
        self.forward_button = KeyboardButton.ascii_key(b'w')
        self.backward_button = KeyboardButton.ascii_key(b's')
        self.strafe_left_button = KeyboardButton.ascii_key(b'a')
        self.strafe_right_button = KeyboardButton.ascii_key(b'd')
    
    def process(self, task):
        base = self.base
        dt = base.taskMgr.globalClock.getDt()
        pos = base.camera.getPos()
        
        
        
        if base.mouseWatcherNode.hasMouse():
            mouse_x = base.mouseWatcherNode.getMouseX()
            mouse_y = base.mouseWatcherNode.getMouseY()
            base.camera.setHpr(-mouse_x*50, mouse_y*50, 0)
        
        direction = base.camera.getHpr()
        
        update_pos = False
        speed = 15
        if self.is_down(self.forward_button):
            invert_direction = 1
            speed = 15
            update_pos = True
            strafe = False
        if self.is_down(self.backward_button):
            invert_direction = -1
            speed = 10
            update_pos = True
            strafe = False
        if self.is_down(self.strafe_left_button):
            invert_direction = 1
            speed = 12
            update_pos = True
            strafe = True
        if self.is_down(self.strafe_right_button):
            invert_direction = -1
            speed = 12
            update_pos = True
            strafe = True
        
        if update_pos:
            delta = dt * speed * invert_direction
            x = delta * sin(radians(direction[0]))
            y = delta * cos(radians(direction[0]))
            if strafe:
                y, x = x, y
                y = y * -1
            pos[0] -= x
            pos[1] += y
            base.camera.setPos(pos)
        

class Game(ShowBase):
    
    def __init__(self):
        
        ## panda3d config (meta-engine)
        loadPrcFileData("", "window-type none") # makes panda3d to don't open a window
        super().__init__() # init
        self.makeDefaultPipe(printPipeTypes = False) # supress panda3d messages
        self.openDefaultWindow() # makes panda3d to don't open a window
        
        
        ## engine config (game)
        
        # camera
        self.camLens.setFov(60)
        self.camLens.setNearFar(.1, 1000)
        
        # mouse
        self.disableMouse()
        props = WindowProperties()
        props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.M_relative)
        self.win.requestProperties(props)
        
        # frame-rate limiting
        self.taskMgr.globalClock.setMode(ClockObject.MLimited)
        self.taskMgr.globalClock.setFrameRate(60)
        
        # input controls
        self.accept('escape', sys.exit)
        r = ReadKeys(self)
        def taskFunc(task):
            r.process(task)
            return task.cont
        self.taskMgr.add(taskFunc, 'task-readkeys')
        
        
        ## code
        
        scene = self.loader.loadModel("models/environment")
        scene.reparentTo(self.render)
        scene.setScale(0.1, 0.1, 0.1)
        scene.setPos(-2, 16, -0.5)
        
        cube = self.loader.loadModel("resources/models/cube.egg")
        self.cube = cube
        cube.reparentTo(self.render)
        
        cube.setPos(0, 0, 0.5)
        
        self.camera.setPos(0, -6, 1.7)

game = Game()
game.run()
