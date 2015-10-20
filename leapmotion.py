# coding=utf-8

import Leap, sys, thread, time
import pygame
import graficos

posicion_media = []
direccion_media = []

# LeapMotion
class SampleListener(Leap.Listener):
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    num_maximo_baquetas = 2
    #posicion_media = [[0,0,0] for i in range(num_maximo_baquetas)]
    #direccion_media = [[0,0,0] for i in range(num_maximo_baquetas)]

    num_frame = 0
    num_medio_frames = 5
    DEBUG = False

    def inicializar(self):
        pygame.init()
        self.sonidohard = pygame.mixer.Sound('Snare_hard.ogg')
        self.sonidosoft = pygame.mixer.Sound('Snare_soft.ogg')

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
        #posicion_actual = []
        #direccion_actual = []
        #ids_baquetas = []
        for tool in frame.tools:
            #posicion_actual.append(tool.tip_position)
            #direccion_actual.append(tool.direction)
            #ids_baquetas.append(tool.id)
            posicion_media.append(tool.tip_position)
            direccion_media.append(tool.direction)

        # Comprobamos los gestos
        for gesture in frame.gestures():
            # Key tap (gesto similar al de pulsar una tecla)
            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                keytap = Leap.KeyTapGesture(gesture)
                pos = keytap.position

                if self.DEBUG:
                    print "pos[0] = ", pos[0],
                if pos[0] < 0:
                    if self.DEBUG:
                        print "HARD",
                    self.sonidohard.play()
                else:
                    if self.DEBUG:
                        print "SOFT",
                    self.sonidosoft.play()

                if self.DEBUG:
                    print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
                        gesture.id, self.state_names[gesture.state], keytap.position, keytap.direction )

        #print self.posicion_media[0]
        if  len(posicion_media) > 0:
            graficos.redibujar()
        posicion_media = []
        direccion_media = []
        """
        num_baquetas_actual = len(posicion_actual)
        for j in range(num_baquetas_actual):
            self.posicion_media[j] = [self.posicion_media[j][i]+posicion_actual[j][i] for i in range(3)]
            self.direccion_media[j] = [self.direccion_media[j][i]+direccion_actual[j][i] for i in range(3)]

        self.num_frame = (self.num_frame+1)%self.num_medio_frames
        if self.num_frame == 0:
            for j in range(num_baquetas_actual):
                self.posicion_media[j] = [float(self.posicion_media[j][i]/self.num_medio_frames) for i in range(3)]
                self.direccion_media[j] = [float(self.direccion_media[j][i]/self.num_medio_frames) for i in range(3)]

            if self.DEBUG:
                for j in range(num_baquetas_actual):
                    print ids_baquetas[j], self.posicion_media[j], self.direccion_media[j]

            graficos.redibujar()
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


