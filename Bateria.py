#!/usr/bin/env python2
# coding=utf-8

import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import pygame
from time import sleep

import OpenGL
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import gluOrtho2D
from OpenGL.GLUT import *
import sys, time
from OpenGL.constants import GLfloat
from OpenGL.GL.ARB.multisample import GL_MULTISAMPLE_ARB
import math
vec4 = GLfloat_4
tStart = t0 = time.time()
frames = 0
camara_angulo_x = +10
camara_angulo_y = -45
ventana_pos_x  = 50
ventana_pos_y  = 50
ventana_tam_x  = 1024
ventana_tam_y  = 800
frustum_factor_escala = 1.0
frustum_dis_del = 0.1
frustum_dis_tra = 10.0
frustum_ancho = 0.5 * frustum_dis_del
frustum_factor_escala = 1.0
strings_ayuda = ["Hola"," Adios",]
p = [0,0,0]
d = [0,0,0]

# LeapMotion
class SampleListener(Leap.Listener):
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']


    # Función que se ejecuta al inicializar el programa
    def on_init(self, controller):
        self.hard = pygame.mixer.Sound('Snare_hard.ogg')
        self.soft = pygame.mixer.Sound('Snare_soft.ogg')
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
        global p,d
        # Tomamos un frame
        frame = controller.frame()

        for tool in frame.tools:
            #print "  Tool id: %d, position: %s, direction: %s" % (
            #    tool.id, tool.tip_position, tool.direction)
            p = tool.tip_position
            d = tool.direction
            #print p, d

        # Comprobamos los gestos
        for gesture in frame.gestures():
            # Key tap (gesto similar al de pulsar una tecla)
            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                keytap = KeyTapGesture(gesture)
                self.hard.play()
                print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
                        gesture.id, self.state_names[gesture.state],
                        keytap.position, keytap.direction )
        glutPostRedisplay()

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

# OpenGL
def fijarProyeccion():
    ratioYX = float(ventana_tam_y) / float(ventana_tam_x)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glFrustum(-frustum_ancho, +frustum_ancho, -frustum_ancho*ratioYX, +frustum_ancho*ratioYX, +frustum_dis_del, +frustum_dis_tra)

    glTranslatef( 0.0,0.0,-0.5*(frustum_dis_del+frustum_dis_tra))

    glScalef( frustum_factor_escala, frustum_factor_escala,  frustum_factor_escala )

def fijarViewportProyeccion():
    glViewport( 0, 0, ventana_tam_x, ventana_tam_y )
    fijarProyeccion()

def fijarCamara():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glRotatef(camara_angulo_x,1,0,0)
    glRotatef(camara_angulo_y,0,1,0)

def dibujarEjes():
    long_ejes = 30.0

    # establecer modo de dibujo a lineas (podría estar en puntos)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE );

    # Ancho de línea
    glLineWidth( 1.5 );
    # dibujar tres segmentos
    glBegin(GL_LINES)

    # eje X, color rojo
    glColor3f( 1.0, 0.0, 0.0 )
    glVertex3f( -long_ejes, 0.0, 0.0 )
    glVertex3f( +long_ejes, 0.0, 0.0 )
    # eje Y, color verde
    glColor3f( 0.0, 1.0, 0.0 )
    glVertex3f( 0.0, -long_ejes, 0.0 )
    glVertex3f( 0.0, +long_ejes, 0.0 )
    # eje Z, color azul
    glColor3f( 0.0, 0.0, 1.0 )
    glVertex3f( 0.0, 0.0, -long_ejes )
    glVertex3f( 0.0, 0.0, +long_ejes )

    glEnd()

def dibujarObjetos():
    glColor3f(0,0,0)
    # print p, d
    glBegin(GL_LINES)
    glVertex3f(p[0],p[1],p[2])
    glVertex3f(p[0]-20*d[0],p[1]-20*d[1],p[2]-20*d[2])
    glEnd()

def ayuda():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0.0, ventana_tam_x, 0.0, ventana_tam_y)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(1.0, 0.0, 0.0)

    num_lineas = 0
    for s in strings_ayuda:
        glWindowPos2i(10, ventana_tam_y - 15*(num_lineas + 1))
        for c in s:
            glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(c));
        num_lineas += 1

    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()

# Función de dibujado
def dibujar():
    rotationRate = (time.time() - tStart) * 1.05
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    fijarViewportProyeccion()
    fijarCamara()
    dibujarEjes()

    dibujarObjetos()

    ayuda()

    glutSwapBuffers()

# Teclas normales: para cambiar escala y velocidad
def teclaNormal(k, x, y):
    global frustum_factor_escala, vertice_actual, velocidad, camara_angulo_x, camara_angulo_y, dibujoEvoluta
    global modoPunto,modoAlambre,modoSolido,modoSolidoColoreado,modoSolidoColoreado,modoNormalesVertices

    if k == b'+':
        frustum_factor_escala *= 1.05
    elif k == b'-':
        frustum_factor_escala /= 1.05
    elif k == b'r':
        camara_angulo_x = camara_angulo_y = 0.0
    elif k == b'q' or k == b'Q' or ord(k) == 27: # Escape
        sys.exit(0)
    else:
        return
    glutPostRedisplay()

# Teclas especiales: para cambiar la cámara
def teclaEspecial(k, x, y):
    global camara_angulo_x, camara_angulo_y

    if k == GLUT_KEY_UP:
        camara_angulo_x += 5.0
    elif k == GLUT_KEY_DOWN:
        camara_angulo_x -= 5.0
    elif k == GLUT_KEY_LEFT:
        camara_angulo_y += 5.0
    elif k == GLUT_KEY_RIGHT:
        camara_angulo_y -= 5.0
    else:
        return
    glutPostRedisplay()

# Nuevo tamaño de ventana
def cambioTamanio(width, height):
    global ventana_tam_x,ventana_tam_y

    ventana_tam_x = width
    ventana_tam_y = height

    fijarViewportProyeccion()
    glutPostRedisplay()

origen = [-1,-1]
def pulsarRaton(boton,estado,x,y):
    da = 5.0
    redisp = False
    global frustum_factor_escala,origen,camara_angulo_x,camara_angulo_y

    if boton == GLUT_LEFT_BUTTON:
        if estado == GLUT_UP:
            origen = [-1,-1]
        else:
            origen = [x,y]
    elif boton == 3: # Rueda arriba aumenta el zoom
        frustum_factor_escala *= 1.05;
        redisp = True
    elif boton == 4: # Rueda abajo disminuye el zoom
        frustum_factor_escala /= 1.05;
        redisp = True
    elif boton == 5: # Llevar la rueda a la izquierda gira la cámara a la izquierda
        camara_angulo_y -= da
        redisp = True
    elif boton == 6: # Llevar la rueda a la derecha gira la cámara a la derecha
        camara_angulo_y += da
        redisp = True

    if redisp:
        glutPostRedisplay();

def moverRaton(x,y):
    global camara_angulo_x,camara_angulo_y, origen

    if origen[0] >= 0 and origen[1] >= 0:
        camara_angulo_x += (y - origen[1])*0.25;
        camara_angulo_y += (x - origen[0])*0.25;

        origen[0] = x;
        origen[1] = y;

        # Redibujar
        glutPostRedisplay();

def inicializar():
    glEnable(GL_NORMALIZE)
    glEnable(GL_MULTISAMPLE_ARB);
    glClearColor( 1.0, 1.0, 1.0, 1.0 ) ;
    glColor3f(0.0,0.0,0.0)

def main():
    # opengl funciones
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_MULTISAMPLE | GLUT_ALPHA)

    glutInitWindowPosition(0, 0)
    glutInitWindowSize(ventana_tam_x, ventana_tam_y)
    glutCreateWindow("Bateria")
    inicializar()

    glEnable( GL_DEPTH_TEST )

    glutDisplayFunc(dibujar)
    glutReshapeFunc(cambioTamanio)
    glutKeyboardFunc(teclaNormal)
    glutSpecialFunc(teclaEspecial)
    glutMouseFunc(pulsarRaton)
    glutMotionFunc(moverRaton)


    # Inicializamos pygame (para el audio)
    pygame.init()


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
    glutMainLoop()
    controller.remove_listener(listener)
    """
    print "Pulsa enter para salir..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Borrar el listener al salir
        controller.remove_listener(listener)
    """

if __name__ == "__main__":
    main()
