# AHAHAHHAA

from modelos import *
import glfw
import sys

class Controller:
    def __init__(self):
        self.sociedad = None
        self.mundo = None
    
    def set_sociedad(self,sociedad):
        self.sociedad = sociedad
    
    def set_mundo(self,mundo):
        self.mundo = mundo
    
    def on_key(self,window, key, scancode, action, mods):

        if action != glfw.PRESS:
            return
        
        elif key == glfw.KEY_RIGHT and action == glfw.PRESS and self.sociedad.actualizar == False and not self.sociedad.terminar:
            self.sociedad.actualizar = True
        
        elif key == glfw.KEY_P and action == glfw.PRESS:
            self.sociedad.terminar = True
            self.mundo.mostrar_graficos = True

        elif key == glfw.KEY_C and action == glfw.PRESS:
            self.sociedad.cuarentena += 1