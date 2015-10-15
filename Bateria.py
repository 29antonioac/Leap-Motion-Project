#!/usr/bin/env python2


import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import pygame

class SampleListener(Leap.Listener):
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    # Función que se ejecuta al inicializar el Leap Motion
    def on_init(self, controller):
        print "Inicializado"

    # Función que se ejecuta al conectar el Leap Motion
    def on_connect(self, controller):
        print "Conectado"

        # Activar gestos
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
        # Tomamos un frame
        frame = controller.frame()

        # Comprobamos los gestos
        for gesture in frame.gestures():
            # Key tap (gesto similar al de pulsar una tecla)
            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                keytap = KeyTapGesture(gesture)
                song.play()
                print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
                        gesture.id, self.state_names[gesture.state],
                        keytap.position, keytap.direction )

        # if not (frame.hands.is_empty and frame.gestures().is_empty):
        #     print ""

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():
    # Inicializamos pygame (para el audio)
    pygame.init()

    # Cargamos la canción (a meter en la clase)
    global song
    song = pygame.mixer.Sound('s.ogg')

    # Creamos un listener
    listener = SampleListener()

    # Creamos un controlador
    controller = Leap.Controller()

    # Configurando el controller
    # Le cambiamos valores de velocidad, historia y distancia
    # para que consiga reconocer mejor el gesto
    controller.config.set("Gesture.KeyTap.MinDownVelocity", 20.0)
    controller.config.set("Gesture.KeyTap.HistorySeconds", 0.2)
    controller.config.set("Gesture.KeyTap.MinDistance", 1.0)
    controller.config.save()


    # Añadimos el listener al controller para que así éste reciba toda la
    # información desde el Leap Motion
    controller.add_listener(listener)

    # Hay que mantener la hebra principal activa
    print "Pulsa enter para salir..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Borrar el listener al salir
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
