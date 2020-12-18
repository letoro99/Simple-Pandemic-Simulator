# AHAHAHHAA

from modelos import *
import glfw
import sys

class Controller:
    def __init__(self):
        self.sociedad = None
    
    def set_sociedad(self,sociedad):
        self.sociedad = sociedad
    
    def on_key(self,window, key, scancode, action, mods):

        if action != glfw.PRESS:
            return
        
        elif key == glfw.KEY_RIGHT and action == glfw.PRESS and self.sociedad.actualizar == False:
            self.sociedad.actualizar = True