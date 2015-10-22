# coding=utf-8

import OpenGL
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import gluOrtho2D
from OpenGL.GLUT import *
import sys, time
from OpenGL.constants import GLfloat
from OpenGL.GL.ARB.multisample import GL_MULTISAMPLE_ARB
import math

import leapmotion

import time

vec4 = GLfloat_4
tStart = t0 = time.time()
frames = 0
camara_angulo_x = 25#+10
camara_angulo_y = 0#-45
ventana_pos_x  = 50
ventana_pos_y  = 50
ventana_tam_x  = 1024
ventana_tam_y  = 800
frustum_dis_del = 0.1
frustum_dis_tra = 10.0
frustum_ancho = 0.5 * frustum_dis_del
frustum_factor_escala = 0.005
strings_ayuda = ["Hola"," Adios"]

origen_ejes = [-500.0,0.0,-400.0]

posiciones_baquetas = []
direcciones_baquetas = []

tiempo_transcurrido_ultimo_dato = time.time()
margen_tiempo = 10

traslacion_baterias = [[-150,100,-0],[0,100,0],[150,100,-0]]
propiedades_baterias = [[50,50],[50,50],[50,50]]    # radio,altura

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

def dibujarRejilla():
    long_grid = 1000.0
    gap = 50.0

    num_lines = int( (long_grid*2)/gap )

    # establecer modo de dibujo a lineas (podría estar en puntos)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE );
    # Ancho de línea
    glLineWidth( 0.2 );

    # dibujar las líneas
    glBegin(GL_LINES)
    # Color negro
    glColor3f( 0.2, 0.2, 0.2 )

    for i in range(num_lines):
        # if i != num_lines/2:
        glVertex3f( -long_grid, 0.0, gap*(i-num_lines/2) )
        glVertex3f( +long_grid, 0.0, gap*(i-num_lines/2) )

        glVertex3f( gap*(i-num_lines/2), 0.0, -long_grid )
        glVertex3f( gap*(i-num_lines/2), 0.0, +long_grid )

    glEnd()

def dibujarEjes():
    long_ejes = 500.0
    # establecer modo de dibujo a lineas (podría estar en puntos)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE );
    # Ancho de línea
    glLineWidth( 1.5 );
    # dibujar tres segmentos
    glBegin(GL_LINES)
    # eje X, color rojo
    glColor3f( 1.0, 0.0, 0.0 )

    glVertex3f( origen_ejes[0]              , origen_ejes[1], origen_ejes[2] )
    glVertex3f( origen_ejes[0] +long_ejes   , origen_ejes[1], origen_ejes[2] )
    # eje Y, color verde
    glColor3f( 0.0, 1.0, 0.0 )
    glVertex3f( origen_ejes[0], origen_ejes[1]              , origen_ejes[2] )
    glVertex3f( origen_ejes[0], origen_ejes[1] +long_ejes   , origen_ejes[2] )
    # eje Z, color azul
    glColor3f( 0.0, 0.0, 1.0 )
    glVertex3f( origen_ejes[0], origen_ejes[1]  ,           origen_ejes[2]  )
    glVertex3f( origen_ejes[0], origen_ejes[1]  , origen_ejes[2] +long_ejes )
    glEnd()

    # Dibujar punto
    glColor3f( 1.0, 1.0, 1.0 )
    glutSolidSphere( 5.0, 20, 20 )

def dibujaCilindro(traslacion,propiedades):
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()

    glColor3f(0.5,0.5,0.5)
    glTranslatef(traslacion[0],traslacion[1],traslacion[2])
    glRotatef(-90,1,0,0)

    glVertex3f(0,0,0)
    glutSolidCylinder(propiedades[0],propiedades[1],100,100)

    glPopMatrix()

def dibujarObjetos():
    global posiciones_baquetas, direcciones_baquetas
    global traslacion_baterias, propiedades_baterias
    global tiempo_transcurrido_ultimo_dato, margen_tiempo

    for i in range(len(traslacion_baterias)):
        dibujaCilindro(traslacion_baterias[i],propiedades_baterias[i])

    glColor3f(1,1,1)

    glBegin(GL_LINES)
    for j in range(len(posiciones_baquetas)):
        p = posiciones_baquetas[j]
        d = direcciones_baquetas[j]
        glVertex3f(p[0],p[1],p[2])
        glVertex3f(p[0]-20*d[0],p[1]-20*d[1],p[2]-20*d[2])
    glEnd()

    if  time.time() - tiempo_transcurrido_ultimo_dato > margen_tiempo:
        print time.time() - tiempo_transcurrido_ultimo_dato
        posiciones_baquetas = []
        direcciones_baquetas = []

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
    dibujarRejilla()
    dibujarEjes()
    dibujarObjetos()
    ayuda()
    glutPostRedisplay()
    glutSwapBuffers()

# Teclas normales: para cambiar escala y velocidad
def teclaNormal(k, x, y):
    global frustum_factor_escala, vertice_actual, velocidad, camara_angulo_x, camara_angulo_y, dibujoEvoluta

    if k == b'+':
        frustum_factor_escala *= 1.05
    elif k == b'-':
        frustum_factor_escala /= 1.05
    elif k == b'r':
        camara_angulo_x = 25
        camara_angulo_y = 0.0
    elif k == b'q' or k == b'Q' or ord(k) == 27: # Escape
        glutLeaveMainLoop()
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
    global camara_angulo_x,camara_angulo_y, origen, tiempo_transcurrido_ultimo_dato, ahora

    tiempo_transcurrido_ultimo_dato = time.time()

    if origen[0] >= 0 and origen[1] >= 0:
        camara_angulo_x += (y - origen[1])*0.25;
        camara_angulo_y += (x - origen[0])*0.25;
        origen[0] = x;
        origen[1] = y;
        # Redibujar
        glutPostRedisplay();

def limpiarTodo():
    pass

def redibujar():
    global posiciones_baquetas, direcciones_baquetas, ahora, tiempo_transcurrido_ultimo_dato

    tiempo_transcurrido_ultimo_dato = time.time()
    posiciones_baquetas = leapmotion.posicion_media
    direcciones_baquetas = leapmotion.direccion_media

    glutPostRedisplay()

def openGLmainloop():
    glutMainLoop()

def inicializarOpenGL():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_MULTISAMPLE | GLUT_ALPHA)
    glutInitWindowPosition(0, 0)
    glutInitWindowSize(ventana_tam_x, ventana_tam_y)
    glutCreateWindow("Bateria")

    # funcion inicializar() antigua
    glEnable(GL_NORMALIZE)
    glEnable(GL_MULTISAMPLE_ARB)
    glEnable( GL_DEPTH_TEST )
    glClearColor( 0.0, 0.0, 0.0, 1.0 )
    glColor3f(0.0,0.0,0.0)

    glutIdleFunc(dibujar)
    glutDisplayFunc(dibujar)
    glutReshapeFunc(cambioTamanio)
    glutKeyboardFunc(teclaNormal)
    glutSpecialFunc(teclaEspecial)
    glutMouseFunc(pulsarRaton)
    glutMotionFunc(moverRaton)

    # TO DO
    glutCloseFunc(limpiarTodo);
    glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_GLUTMAINLOOP_RETURNS);
