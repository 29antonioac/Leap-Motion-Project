# coding=utf-8

import Leap, sys, thread, time
import pygame
import graficos

posicion_media = []
direccion_media = []
string_sonidos = ['Kick_hard.ogg','Kick_soft.ogg','Snare_hard.ogg','Snare_soft.ogg']

# LeapMotion
class SampleListener(Leap.Listener):
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    num_maximo_baquetas = 2
    num_frame = 0
    num_medio_frames = 5
    DEBUG = True

    def inicializar(self):
        global string_sonidos
        pygame.init()
        self.sonidos = [pygame.mixer.Sound(s) for s in string_sonidos]

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
        global direccion_media, posicion_media

        # Tomamos un frame
        frame = controller.frame()

        # Obtenemos la posicion y la direccion de la baqueta(s)
        for tool in frame.tools:
            posicion_media.append(tool.tip_position)
            direccion_media.append(tool.direction)

        # Comprobamos los gestos
        for gesture in frame.gestures():
            # Key tap (gesto similar al de pulsar una tecla)
            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                keytap = Leap.KeyTapGesture(gesture)
                pos = keytap.position

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
                if -100 <= pos[0] <= 0 and 0 <= pos[1] <= 200 and -100 <= pos[2] <= 0:
                    if self.DEBUG:
                        print "Sonido 0"
                    self.sonidos[0].play()
                if 0 <= pos[0] <= 100 and 0 <= pos[1] <= 200 and -100 <= pos[2] <= 0:
                    if self.DEBUG:
                        print "Sonido 1"
                    self.sonidos[1].play()
                if -100 <= pos[0] <= 0 and 0 <= pos[1] <= 200 and 0 <= pos[2] <= 100:
                    if self.DEBUG:
                        print "Sonido 2"
                    self.sonidos[2].play()
                if 0 <= pos[0] <= 100 and 0 <= pos[1] <= 200 and 0 <= pos[2] <= 100:
                    if self.DEBUG:
                        print "Sonido 3"
                    self.sonidos[3].play()


                if self.DEBUG:
                    print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
                        gesture.id, self.state_names[gesture.state], keytap.position, keytap.direction )

        if posicion_media:
            graficos.redibujar()

        posicion_media = []
        direccion_media = []

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"
