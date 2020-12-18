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
        self.posx_i, self.posy_i = 0, 0
        self.posx_act, self.posy_act = 0, 0
        self.posx_f, self.posy_f = rd.uniform(-0.5,0.5), rd.uniform(-0.5,0.5)
        self.estado = 0 # 0: sano , 1: enfermo , 2: recuperado , si muere se borrara
        self.grupo = num_grupo
        self.dias_contagiados = 0


    def draw(self,pipeline):
        glUseProgram(pipeline.shaderProgram)
        if self.estado == 0:
            sg.drawSceneGraphNode(self.model_sano,pipeline,'transform')
        elif self.estado == 1:
            sg.drawSceneGraphNode(self.model_enfermo,pipeline,'transform')
        elif self.estado == 2:
            sg.drawSceneGrapgNode(self.model_recuperado,pipeline,'transform')
        else:
            pass
    
    def cambiar_estado(self,nuevo_estado):
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
    def __init__(self,n,prob_contagio,radio_contagio,dias_recuperacion):

        self.sanos = n-1
        self.enfermos = 1
        self.recuperados = 0
        self.fallecidos = 0
        self.habitantes = n

        self.listado = []
        self.listado_enfermos = [0] # Guardo solo los indices de los enfermos para buscarlo en self.listado
        self.listado_recuperados = [] # Guardar indices de los recuperados para no tomarlos en el metodo de contagiar
        self.actualizar = True

        self.prob_contagio = prob_contagio
        self.radio_contagio = radio_contagio
        self.dias_recuperacion = dias_recuperacion

        for i in range(self.habitantes):
            self.listado.append(Individuo())
        self.listado[0].cambiar_estado(1)

    def iteracion(self,t):
        for individuo in self.listado:
            individuo.mover_disc(t)
    
    def actualizar_puntos(self):
        for i in range(len(self.listado)):
            self.listado[i].nuevos_puntos()
            #if i in self.listado_enfermos:
            #    self.listado[i].dias_contagiados += 1
            #    if rd.random() <= self.prob_morir:
            #        self.listado.pop(i)
            #        self.fallecidos += 1
            #        self.enfermos -= 1
            #    if self.listado[i].dias_contagiados > self.dias_recuperacion:
            #        self.
    

    def contagiar(self):
        for i in self.listado_enfermos:
            x, y = self.listado[i].posx_act, self.listado[i].posy_act
            for j in range(len(self.listado)):
                if i != j and not j in self.listado_recuperdados and rd.random() < self.prob_contagio and self.listado[j].posible_contagio(x,y,self.radio_contagio):
                    self.listado[j].cambiar_estado(1)
                    self.sanos -= 1
                    self.enfermos += 1
        
    def draw(self,pipeline):
        for individuo in self.listado:
            individuo.draw(pipeline)

class Mundo:
    def __init__(self,datos):
        pass
        
    
        


