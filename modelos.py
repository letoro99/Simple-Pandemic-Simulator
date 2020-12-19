# Modelos para las personas
# Contendra su forma , la trayectoria, tipos, etc.

from OpenGL.GL import *
import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es

import random as rd
import math as mt
import numpy as np
import matplotlib.pyplot as plt

class Individuo:
    def __init__(self,num_grupo=0):
        #Figuras basicas
        gpu_sano = es.toGPUShape(bs.createColorQuad(0,1,0))
        gpu_enfermo = es.toGPUShape(bs.createColorQuad(1,0,0))
        gpu_repcuperado = es.toGPUShape(bs.createColorQuad(0,0,1))
        # Creamos los estados
        #sano
        sano = sg.SceneGraphNode('sano')
        sano.transform = tr.uniformScale(0.01)
        sano.childs += [gpu_sano]
        sano_tr = sg.SceneGraphNode('sano_tr')
        sano_tr.childs += [sano]
        #enfermo
        enfermo = sg.SceneGraphNode('enfermo')
        enfermo.transform = tr.uniformScale(0.01)
        enfermo.childs += [gpu_enfermo]
        enfermo_tr = sg.SceneGraphNode('enfermo_tr')
        enfermo_tr.childs += [enfermo]
        #recuperado
        recuperado = sg.SceneGraphNode("recuperado")
        recuperado.transform = tr.uniformScale(0.01)
        recuperado.childs += [gpu_repcuperado]
        recuperado_tr = sg.SceneGraphNode("recuperado_tr")
        recuperado_tr.childs += [recuperado]

        self.model_sano = sano_tr
        self.model_enfermo = enfermo_tr
        self.model_recuperado = recuperado_tr
        self.model = self.model_sano

        self.posx_act, self.posy_act = 0, 0
        self.posx_i,self.posy_i = 0, 0

        self.estado = 0 # 0: sano , 1: enfermo , 2: inmune , si muere se borrara
        self.grupo = num_grupo
        self.dias_contagiados = 1
        self.prob_viajar = rd.uniform(0,0.05)

        if self.grupo == 0:
            self.posx_f, self.posy_f = rd.uniform(-0.9,-0.1), rd.uniform(0.1,0.9)
        elif self.grupo == 1:
            self.posx_f, self.posy_f = rd.uniform(0.1,0.9), rd.uniform(0.1,0.9)
        elif self.grupo == 2:
            self.posx_f, self.posy_f = rd.uniform(0.1,0.9), rd.uniform(-0.9,-0.1)
        else:
            self.posx_f, self.posy_f = rd.uniform(-0.9,-0.1), rd.uniform(-0.9,-0.1)

    def draw(self,pipeline):
        glUseProgram(pipeline.shaderProgram)
        if self.estado == 0:
            sg.drawSceneGraphNode(self.model_sano,pipeline,'transform')
        elif self.estado == 1:
            sg.drawSceneGraphNode(self.model_enfermo,pipeline,'transform')
        elif self.estado == 2:
            sg.drawSceneGraphNode(self.model_recuperado,pipeline,'transform')
        else:
            pass
    
    def cambiar_estado(self,nuevo_estado):
        if nuevo_estado == 0:
            self.model_sano.transform = self.model.transform
            self.model = self.model_sano
            self.estado = 0
        if nuevo_estado == 1:
            self.model_enfermo.transform = self.model.transform
            self.model = self.model_enfermo
            self.estado = 1
        elif nuevo_estado == 2:
            self.model_recuperado.transform = self.model.transform
            self.model = self.model_recuperado
            self.estado = 2
        else:
            pass

    def nuevos_puntos(self):
        self.posx_i, self.posy_i = self.posx_f, self.posy_f
        self.posx_f , self.posy_f = rd.uniform(self.posx_i-0.1,self.posx_i+0.1),rd.uniform(self.posy_i-0.1,self.posy_i+0.1)
        while self.posx_f < -0.5 or self.posx_f > 0.5 or self.posy_f < -0.5 or self.posy_f > 0.5:
            self.posx_f , self.posy_f = rd.uniform(self.posx_i-0.1,self.posx_i+0.1),rd.uniform(self.posy_i-0.1,self.posy_i+0.1)
        
    def nuevo_puntos_pobla(self,cuarentena):
        if rd.random() <= self.prob_viajar and cuarentena%2 == 0:
            self.posx_i, self.posy_i = self.posx_f, self.posy_f
            self.grupo = rd.randint(0,3)
            if self.grupo == 0:
                self.posx_f, self.posy_f = rd.uniform(-0.9,-0.1), rd.uniform(0.1,0.9)
            elif self.grupo == 1:
                self.posx_f, self.posy_f = rd.uniform(0.1,0.9), rd.uniform(0.1,0.9)
            elif self.grupo == 2:
                self.posx_f, self.posy_f = rd.uniform(0.1,0.9), rd.uniform(-0.9,-0.1)
            else:
                self.posx_f, self.posy_f = rd.uniform(-0.9,-0.1), rd.uniform(-0.9,-0.1)
        else:
            self.posx_i, self.posy_i = self.posx_f, self.posy_f
            self.posx_f , self.posy_f = rd.uniform(self.posx_i-0.05,self.posx_i+0.05),rd.uniform(self.posy_i-0.05,self.posy_i+0.05)
            if self.grupo == 0:
                while self.posx_f < -0.9 or self.posx_f > -0.1 or self.posy_f < 0.1 or self.posy_f > 0.9:
                    self.posx_f , self.posy_f = rd.uniform(self.posx_i-0.05,self.posx_i+0.05),rd.uniform(self.posy_i-0.05,self.posy_i+0.05)
            elif self.grupo == 1:
                while self.posx_f < 0.1 or self.posx_f > 0.9 or self.posy_f < 0.1 or self.posy_f > 0.9:
                    self.posx_f , self.posy_f = rd.uniform(self.posx_i-0.05,self.posx_i+0.05),rd.uniform(self.posy_i-0.05,self.posy_i+0.05)
            elif self.grupo == 2:
                while self.posx_f < 0.1 or self.posx_f > 0.9 or self.posy_f < -0.9 or self.posy_f > -0.1:
                    self.posx_f , self.posy_f = rd.uniform(self.posx_i-0.05,self.posx_i+0.05),rd.uniform(self.posy_i-0.05,self.posy_i+0.05)
            else:
                while self.posx_f < -0.9 or self.posx_f > -0.1 or self.posy_f < -0.9 or self.posy_f > -0.1:
                    self.posx_f , self.posy_f = rd.uniform(self.posx_i-0.05,self.posx_i+0.05),rd.uniform(self.posy_i-0.05,self.posy_i+0.05)
    
    def mover_disc(self,t):
        self.posx_act = (1-t)*self.posx_i+t*self.posx_f
        self.posy_act = (1-t)*self.posy_i+t*self.posy_f
        self.model.transform = tr.translate(self.posx_act,self.posy_act,0)
    
    def posible_contagio(self,pos_x,pos_y,radio):
        distancia = ((self.posx_act - pos_x)**2 + (self.posy_act - pos_y)**2)**0.5
        if distancia < radio:
            return True 
        else:
            return False
    

class Sociedad: # NOooOOOOooOo la S-palabra
    def __init__(self,n,prob_contagio,radio_contagio,dias_recuperacion,prob_morir):

        self.sanos = n-1
        self.enfermos = 1
        self.recuperados = 0
        self.fallecidos = 0
        self.transcurso = [[self.sanos],[self.enfermos],[self.recuperados],[self.fallecidos]]

        self.listado = []
        self.actualizar = False
        self.terminar = False

        self.prob_contagio = prob_contagio
        self.radio_contagio = radio_contagio
        self.dias_recuperacion = dias_recuperacion
        self.prob_morir = prob_morir
        self.cuarentena = 0

        i = 0
        while i != n+1:
            self.listado.append(Individuo(int(i%4)))
            i += 1
        self.listado[rd.randint(0,3)].cambiar_estado(1)

    def iteracion(self,t):
        for individuo in self.listado:
            individuo.mover_disc(t)
    
    def actualizar_puntos(self,first):
        eliminar = []
        for i in range(0,len(self.listado)):
            self.listado[i].nuevo_puntos_pobla(self.cuarentena)
            if self.listado[i].estado == 1 and first == 1:
                self.listado[i].dias_contagiados += 1
                if rd.random() <= self.prob_morir and self.listado[i].dias_contagiados <= self.dias_recuperacion and self.listado[i].estado == 1:
                    eliminar.append(i)
                    self.enfermos -= 1
                    self.fallecidos += 1
                elif self.listado[i].dias_contagiados > self.dias_recuperacion:
                    self.listado[i].dias_contagiados = int(self.listado[i].dias_contagiados/2)+1
                    self.listado[i].cambiar_estado(2)
                    self.enfermos -= 1
                    self.recuperados += 1
            elif self.listado[i].estado == 2 and first == 1:
                self.listado[i].dias_contagiados -= 1
                if self.listado[i].dias_contagiados == 1:
                    self.listado[i].cambiar_estado(0)
                    self.recuperados -= 1
                    self.sanos += 1
        n_elim = 0
        for i in eliminar:
            self.listado.pop(i-n_elim)
            n_elim += 1
        self.transcurso[0].append(self.sanos)
        self.transcurso[1].append(self.enfermos)
        self.transcurso[2].append(self.recuperados)
        self.transcurso[3].append(self.fallecidos)

    def contagiar(self):
        for enfermo in self.listado:
            if enfermo.estado == 1:
                x,y = enfermo.posx_act, enfermo.posy_act
                for individuo in self.listado:
                    if individuo.estado == 0 and rd.random() <= self.prob_contagio and individuo.posible_contagio(x,y,self.radio_contagio):
                        individuo.cambiar_estado(1)
                        self.sanos -= 1
                        self.enfermos += 1

    def draw(self,pipeline):
        for individuo in self.listado:
            individuo.draw(pipeline)

class Mundo:
    def __init__(self,datos):
        gpu_sano = es.toGPUShape(bs.createColorQuad(0,1,0))
        gpu_enfermo = es.toGPUShape(bs.createColorQuad(1,0,0))
        gpu_repcuperado = es.toGPUShape(bs.createColorQuad(0,0,1))
        self.datos = datos
        self.mostrar_graficos = False
    
    def get_datos(self):
        return self.datos
    
    def set_datos(self,nuevos_datos):
        self.datos = nuevos_datos

    def generar_plot(self):
        x = np.arange(len(self.datos[0]))
        fig, ax = plt.subplots()
        ax.plot(x,self.datos[0], label='Sanos')
        ax.plot(x,self.datos[1], label='Contagiados')
        ax.plot(x,self.datos[2], label='Inmunes')
        ax.plot(x,self.datos[3], label='Fallecidos')
        ax.set_xlabel('Día')
        ax.set_ylabel('Cantidad de personas')
        ax.set_title('Transcurso de la epidemia')
        ax.legend()
        plt.show()
        pass
        
    
        


