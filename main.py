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
    
    entrada = sys.argv
    datos = {}
    with open(entrada[1]) as json_file:
        data = json.load(json_file)
        datos = data[0]
        total_pobla = datos['Initial_population']
        prob_contagio = datos['Contagious_prob']
        radio_contagio = datos['Radius']
        dias_recuperacion = datos['Days_to_heal']
        prob_muerte = datos['Death_rate']
    print(datos)
    

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

    glClearColor(1,1,1,1)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    poblacion = Sociedad(total_pobla,prob_contagio,radio_contagio,dias_recuperacion,prob_muerte) # Numero personas, prob_contagio, radio_contagio, dias_recuperacion, prob_morir
    poblacion.actualizar_puntos(0)
    mundo = Mundo(None)

    controlador.set_sociedad(poblacion)
    controlador.set_mundo(mundo)

    t0 = 0
    dt = 0
    t = 0
    dia = 1
    while not glfw.window_should_close(window):
        
        ti = glfw.get_time()
        dt = ti - t0
        if poblacion.actualizar == True and dt > 1 and not poblacion.terminar:
            poblacion.actualizar_puntos(1)
            poblacion.actualizar = False
            dt = 0
            t0 = ti
            print('Día n°: '+str(dia))
            dia += 1
        
        elif dt >= 0 and dt <= 1 and not poblacion.terminar:
            poblacion.iteracion(dt)
            poblacion.contagiar()
            
        glfw.poll_events()

        if poblacion.terminar and t == 0:
            t+=1
            if t==1:
                glClear(GL_COLOR_BUFFER_BIT)
            mundo.set_datos(poblacion.transcurso)
            mundo.generar_plot()
        else:
            glClear(GL_COLOR_BUFFER_BIT)
            poblacion.draw(pipeline)
        glfw.swap_buffers(window)

    glfw.terminate()
