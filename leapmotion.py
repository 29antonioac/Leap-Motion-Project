# coding=utf-8

# sonidos obtenidos de http://99sounds.org/drum-samples/

import Leap, sys, thread, time
import pygame
import graficos
import logicamenu

import time

posicion_media = []
direccion_media = []
string_sonidos = ['bombo.ogg','bombo2.ogg','caja.ogg','caja2.ogg']

tutorial_activo_leap = True
tutorial_iniciado_leap = False
inicio_tutorial = None
tiempo_baqueta_tutorial = 3

cambiosonido_iniciado = False
inicio_cambiosonido = None
tiempo_cambiosonido = 7
num_instrumento = None

hubo_gesto = False

# LeapMotion
class SampleListener(Leap.Listener):
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    num_maximo_baquetas = 2
    num_frame = 0
    num_medio_frames = 5
    DEBUG = False

    def inicializar(self):
        global string_sonidos
        # pygame.init()
        self.sonidos = [pygame.mixer.Sound("sonidos/" + s) for s in string_sonidos]

    # Función que se ejecuta al inicializar el programa
    def on_init(self, controller):
        self.inicializar()
        print "Inicializado"

    # Función que se ejecuta al conectar el Leap Motion
    def on_connect(self, controller):
        print "Conectado"

        # Activa el gesto Key Tap
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);

    # Función que se ejecuta al desconectar el Leap Motion
    def on_disconnect(self, controller):
        print "Desconectado"

    # Función que se ejecuta al salir del programa.
    # Las interrupciones por teclado están controladas en el Listener.
    def on_exit(self, controller):
        print "Saliendo..."

    # Función que se ejecuta al recibir cada frame.
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
                    # for i in range(len(self.sonidos)):
                    #     if self.DEBUG:
                    #         print tolerancia*(graficos.traslacion_baterias[i][0] - graficos.propiedades_baterias[i][0]),"<=",pos[0],"<=",tolerancia*(graficos.traslacion_baterias[i][0] + graficos.propiedades_baterias[i][0])
                    #         print tolerancia*(graficos.traslacion_baterias[i][1] - graficos.propiedades_baterias[i][1]),"<=",pos[1],"<=",tolerancia*(graficos.traslacion_baterias[i][1] + graficos.propiedades_baterias[i][1])
                    #         print tolerancia*(graficos.traslacion_baterias[i][2] - graficos.propiedades_baterias[i][0]),"<=",pos[2],"<=",tolerancia*(graficos.traslacion_baterias[i][2] + graficos.propiedades_baterias[i][0])
                        # if  tolerancia*(graficos.traslacion_baterias[i][0] - graficos.propiedades_baterias[i][0]) <= pos[0] <= tolerancia*(graficos.traslacion_baterias[i][0] + graficos.propiedades_baterias[i][0]) \
                        # and tolerancia*(graficos.traslacion_baterias[i][1] - graficos.propiedades_baterias[i][1]) <= pos[1] <= tolerancia*(graficos.traslacion_baterias[i][1] + graficos.propiedades_baterias[i][1]) \
                        # and tolerancia*(graficos.traslacion_baterias[i][2] - graficos.propiedades_baterias[i][0]) <= pos[2] <= tolerancia*(graficos.traslacion_baterias[i][2] + graficos.propiedades_baterias[i][0]):
                    if -graficos.desplazamiento_bateria <= pos[0] <= -graficos.comienzo_bateria and -graficos.desplazamiento_bateria <= pos[2] <= -graficos.comienzo_bateria:
                        if self.DEBUG:
                            print "Sonido 0"
                        self.sonidos[0].play()
                    if graficos.comienzo_bateria <= pos[0] <= graficos.desplazamiento_bateria and -graficos.desplazamiento_bateria <= pos[2] <= -graficos.comienzo_bateria:
                        if self.DEBUG:
                            print "Sonido 1"
                        self.sonidos[1].play()
                    if -graficos.desplazamiento_bateria <= pos[0] <= -graficos.comienzo_bateria and graficos.comienzo_bateria <= pos[2] <= graficos.desplazamiento_bateria:
                        if self.DEBUG:
                            print "Sonido 2"
                        self.sonidos[2].play()
                    if graficos.comienzo_bateria <= pos[0] <= graficos.desplazamiento_bateria and graficos.comienzo_bateria <= pos[2] <= graficos.desplazamiento_bateria:
                        if self.DEBUG:
                            print "Sonido 3"
                        self.sonidos[3].play()

                    if self.DEBUG:
                        print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
                            gesture.id, self.state_names[gesture.state], keytap.position, keytap.direction )

        if  tutorial_activo_leap and posicion_media:
            if not tutorial_iniciado_leap:
                if graficos.comienzo_bateria <= posicion_media[0][0] <= graficos.desplazamiento_bateria and graficos.comienzo_bateria <= posicion_media[0][2] <= graficos.desplazamiento_bateria:
                    tutorial_iniciado_leap = True
                    inicio_tutorial = time.time()
            else:
                #print(time.time() - inicio_tutorial)
                if time.time() - inicio_tutorial < tiempo_baqueta_tutorial:
                    if not(graficos.comienzo_bateria <= posicion_media[0][0]<= graficos.desplazamiento_bateria and graficos.comienzo_bateria <= posicion_media[0][2] <= graficos.desplazamiento_bateria):
                        tutorial_iniciado_leap = False
                else:
                    tutorial_activo_leap = False

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
                #print(time.time() - inicio_cambiosonido)
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
                    # TOQUETEAR POR Antonio
                    string_sonidos[num_instrumento] = logicamenu.cambio_instrumento(string_sonidos)
                    print string_sonidos
                    self.sonidos = [pygame.mixer.Sound("sonidos/" + s) for s in string_sonidos]

                    print("3 SEGUNDOS ALCANZADOS")
                    # input()
                    cambiosonido_iniciado = False

        if posicion_media:
            graficos.redibujar()

        posicion_media = []
        direccion_media = []
        hubo_gesto = False

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"
