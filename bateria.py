#!/usr/bin/env python2
# coding=utf-8

import Leap, sys

import leapmotion
import graficos
import logicamenu
import pygame


def main():
    # Inicializar pygame
    pygame.init()

    # Mostramos el tutorial
    logicamenu.tutorial()

    # Inicializamos openGL
    graficos.inicializarOpenGL()

    # Creamos un listener y un controlador
    listener = leapmotion.BateriaListener()
    controller = Leap.Controller()
    controller.add_listener(listener) # añadimos el listener al controlador

    # Comenzamos la gestión de eventos de OpenGL
    graficos.openGLmainloop()

    # Al terminar, pulsar Enter para salir
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
