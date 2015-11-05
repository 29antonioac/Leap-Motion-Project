# coding=utf-8

import Leap, sys, thread, time
import pygame
import graficos
import logicamenu
import time

# Posición y dirección de las baquetas
posicion_media = []
direccion_media = []

# Nombres de sonidos actuales
string_sonidos = ['caja.ogg','platillo.ogg','bombo.ogg','tom-tom.ogg']

# Variables relacionadas con el estado del programa
tutorial_activo_leap = True
tutorial_iniciado_leap = False
inicio_tutorial = None
tiempo_baqueta_tutorial = 3

cambiosonido_iniciado = False
inicio_cambiosonido = None
tiempo_cambiosonido = 3
num_instrumento = None

hubo_gesto = False

"""
Clase que hereda de Leap.Listener y actúa como Listener para escuchar los eventos
del Leap Motion
"""
class BateriaListener(Leap.Listener):
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    num_maximo_baquetas = 2
    num_frame = 0
    num_medio_frames = 5
    DEBUG = False

    """
    Inicialización de los miembros de instancia. En este caso son sólo los sonidos
    """
    def inicializar(self):
        global string_sonidos
        pygame.mixer.init(44100, -16,2,2048)
        self.sonidos = [pygame.mixer.Sound("sonidos/" + s) for s in string_sonidos]

    """
    Función que se ejecuta al inicializar el programa
    """
    def on_init(self, controller):
        self.inicializar()
        print "Inicializado"

    """
    Función que se ejecuta al conectar el Leap Motion
    """
    def on_connect(self, controller):
        print "Conectado"

        # Activa el gesto Key Tap
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);


    """
    Función que se ejecuta al desconectar el Leap Motion
    """
    def on_disconnect(self, controller):
        print "Desconectado"

    """
    Función que se ejecuta al salir del programa.
    Las interrupciones por teclado están controladas en el Listener.
    """
    def on_exit(self, controller):
        print "Saliendo..."

    """
    Función que se ejecuta al recibir cada frame.
    """
    def on_frame(self, controller):
        global direccion_media, posicion_media,tutorial_activo_leap, tutorial_iniciado_leap, inicio_tutorial,tiempo_baqueta_tutorial, string_sonidos
        global cambiosonido_iniciado, inicio_cambiosonido, tiempo_cambiosonido, num_instrumento
        global hubo_gesto

        # Tomamos un frame
        frame = controller.frame()

        # Obtenemos la posicion y la direccion de la baqueta(s)
        for tool in frame.tools:
            posicion_media.append(tool.tip_position)
            direccion_media.append(tool.direction)

        if not tutorial_activo_leap:
            # Comprobamos los gestos
            for gesture in frame.gestures():
                # Key tap (gesto similar al de pulsar una tecla)
                if gesture.type == Leap.Gesture.TYPE_KEY_TAP:

                    keytap = Leap.KeyTapGesture(gesture)
                    pos = keytap.position
                    hubo_gesto = True

                    tolerancia = 1.5

                    if self.DEBUG:
                        print "pos = ", pos,

                    # Dependiendo de la región, reproducimos un sonido u otro
                    if -graficos.desplazamiento_bateria <= pos[0] <= -graficos.comienzo_bateria and -graficos.desplazamiento_bateria <= pos[2] <= -graficos.comienzo_bateria:
                        if self.DEBUG: print "Sonido 0"
                        self.sonidos[0].play()
                    if graficos.comienzo_bateria <= pos[0] <= graficos.desplazamiento_bateria and -graficos.desplazamiento_bateria <= pos[2] <= -graficos.comienzo_bateria:
                        if self.DEBUG: print "Sonido 1"
                        self.sonidos[1].play()
                    if -graficos.desplazamiento_bateria <= pos[0] <= -graficos.comienzo_bateria and graficos.comienzo_bateria <= pos[2] <= graficos.desplazamiento_bateria:
                        if self.DEBUG: print "Sonido 2"
                        self.sonidos[2].play()
                    if graficos.comienzo_bateria <= pos[0] <= graficos.desplazamiento_bateria and graficos.comienzo_bateria <= pos[2] <= graficos.desplazamiento_bateria:
                        if self.DEBUG: print "Sonido 3"
                        self.sonidos[3].play()

                    if self.DEBUG:
                        print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
                            gesture.id, self.state_names[gesture.state], keytap.position, keytap.direction )


        # Lógica para hacer el gesto de reconocimiento
        if  tutorial_activo_leap and posicion_media:
            if not tutorial_iniciado_leap:
                if graficos.comienzo_bateria <= posicion_media[0][0] <= graficos.desplazamiento_bateria and graficos.comienzo_bateria <= posicion_media[0][2] <= graficos.desplazamiento_bateria:
                    tutorial_iniciado_leap = True
                    inicio_tutorial = time.time()
            else:
                if time.time() - inicio_tutorial < tiempo_baqueta_tutorial:
                    if not(graficos.comienzo_bateria <= posicion_media[0][0]<= graficos.desplazamiento_bateria and graficos.comienzo_bateria <= posicion_media[0][2] <= graficos.desplazamiento_bateria):
                        tutorial_iniciado_leap = False
                else:
                    tutorial_activo_leap = False

        # Lógica para cambiar el sonido de una región
        if not tutorial_activo_leap and posicion_media:
            if not cambiosonido_iniciado :
                if -graficos.desplazamiento_bateria <= posicion_media[0][0] <= -graficos.comienzo_bateria and -graficos.desplazamiento_bateria <= posicion_media[0][2] <= -graficos.comienzo_bateria:
                    num_instrumento = 0
                if graficos.comienzo_bateria <= posicion_media[0][0] <= graficos.desplazamiento_bateria and -graficos.desplazamiento_bateria <= posicion_media[0][2] <= -graficos.comienzo_bateria:
                    num_instrumento = 1
                if -graficos.desplazamiento_bateria <= posicion_media[0][0] <= -graficos.comienzo_bateria and graficos.comienzo_bateria <= posicion_media[0][2] <= graficos.desplazamiento_bateria:
                    num_instrumento = 2
                if graficos.comienzo_bateria <= posicion_media[0][0] <= graficos.desplazamiento_bateria and graficos.comienzo_bateria <= posicion_media[0][2] <= graficos.desplazamiento_bateria:
                    num_instrumento = 3
                if num_instrumento is not None:
                    cambiosonido_iniciado = True
                    inicio_cambiosonido = time.time()
            else:
                if hubo_gesto:
                    cambiosonido_iniciado = False
                elif time.time() - inicio_cambiosonido < tiempo_cambiosonido:
                    if num_instrumento == 0:
                        if not(-graficos.desplazamiento_bateria <= posicion_media[0][0] <= -graficos.comienzo_bateria and -graficos.desplazamiento_bateria <= posicion_media[0][2] <= -graficos.comienzo_bateria):
                            cambiosonido_iniciado = False
                    elif num_instrumento == 1:
                        if not(graficos.comienzo_bateria <= posicion_media[0][0] <= graficos.desplazamiento_bateria and -graficos.desplazamiento_bateria <= posicion_media[0][2] <= -graficos.comienzo_bateria):
                            cambiosonido_iniciado = False
                    elif num_instrumento == 2:
                        if not(-graficos.desplazamiento_bateria <= posicion_media[0][0] <= -graficos.comienzo_bateria and graficos.comienzo_bateria <= posicion_media[0][2] <= graficos.desplazamiento_bateria):
                            cambiosonido_iniciado = False
                    elif num_instrumento == 3:
                        if not(graficos.comienzo_bateria <= posicion_media[0][0] <= graficos.desplazamiento_bateria and graficos.comienzo_bateria <= posicion_media[0][2] <= graficos.desplazamiento_bateria):
                            cambiosonido_iniciado = False
                else:
                    string_sonidos[num_instrumento] = logicamenu.cambio_instrumento(string_sonidos)
                    self.sonidos = [pygame.mixer.Sound("sonidos/" + s) for s in string_sonidos]

                    cambiosonido_iniciado = False

        # Si hay baquetas, redibujar
        if posicion_media:
            graficos.redibujar()

        # Quitar baquetas
        posicion_media = []
        direccion_media = []
        hubo_gesto = False

    """
    Función para convertir los estados de Leap Motion a string
    """
    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"
