import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import json

from modelos import *
from controller import Controller

import transformations as tr

if __name__ == "__main__":
    datos = {}
    with open('virus.json') as json_file:
        data = json.load(json_file)
        datos = data[0]

    if not glfw.init():
        sys.exit()

    width = 1400
    height = 900

    window = glfw.create_window(width, height, "MICROSOFT PANDEMIC SIMULATOS 2020", None, None)

    if not window:
        glfw.terminate()
        sys.exit()
    
    glfw.make_context_current(window)
    
    controlador = Controller()
    glfw.set_key_callback(window, controlador.on_key)

    pipeline = es.SimpleTransformShaderProgram()

    glClearColor(0,0,0,0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    poblacion = Sociedad(100,0.5,0.1,5) # Numero personas, prob_contagio, radio_contagio, dias_recuperacion
    poblacion.actualizar_puntos()

    controlador.set_sociedad(poblacion)

    t0 = 0
    dt = 10

    while not glfw.window_should_close(window):
        
        ti = glfw.get_time()
        dt = ti - t0

        if poblacion.actualizar == True and dt > 1:
            poblacion.actualizar_puntos()
            poblacion.actualizar = False
            dt = 0
            t0 = ti
        
        if dt >= 0 and dt <= 1 :
            poblacion.iteracion(dt)
            poblacion.contagiar()
            print(dt)

        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT)
    
        poblacion.draw(pipeline)

        glfw.swap_buffers(window)

    glfw.terminate()
