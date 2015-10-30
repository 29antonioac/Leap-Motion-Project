# Batería con Leap Motion

Este proyecto para la asignatura Nuevos Paradigmas de Interacción de la UGR
consta de una batería virtual.

## Autores
Sus autores somos [Antonio Álvarez Caballero](https://github.com/analca3)
y [Adrián Ranea Robles](https://github.com/ranea).

## Fecha de realización

Desde el día 16 de Octubre hasta el 30 de Octubre.

## Descripción del problema que se aborda

El problema abordado es una batería virtual: utilizando dos lápices, rotuladores o similar,
podremos simular de manera sencilla y simple el funcionamiento de una batería.

## Descripción de la solución que se aporta

La solución propuesta es la siguiente: en un entorno virtual se dibujan cuatro regiones
cuadradas de igual tamaño. Tomando como referencia una herramienta (lápiz, bolígrafo, rotuladores...)
pintamos en pantalla algo similar a una baqueta, y al posicionarla encima de cada una
de las regiones y detectar un gesto, se reproducirá un sonido asociado a dicha región.

Manteniendo la baqueta sin realizar gestos en una determinada región, podemos cambiar
el sonido que ofrece de manera sencilla.

Para poder ejecutar este proyecto, hacen falta varias cosas:

* Python
* PyOpenGL
* Pygame
* Leap Motion SDK

Para instalar esto en nuestras máquinas de desarrollo (Archlinux x86_64), sólo hacen
falta un par de órdenes. Notar que [pacman](https://wiki.archlinux.org/index.php/Pacman)
es el gestor de paquetes de Archlinux y [pacaur](https://aur.archlinux.org/packages/pacaur/)
es un wrapper para instalar paquetes de la comunidad fácilmente. En caso de no tenerlo
se pueden acceder a los paquetes de Leap de la comunidad desde [aquí](https://aur.archlinux.org/packages/?O=0&K=leap+motion)

```bash
$ sudo pacman -Syu python2 python2-opengl python2-numpy python2-pygame
$ pacaur -Syu leap-motion-driver leap-motion-sdk
```

Al instalar el SDK de Leap Motion, debemos modificar el PKGBUILD para añadir ${pkgdir} en dos de las
últimas líneas, quedando así

```
install -D -m644 "${pkgdir}/usr/lib/Leap/Leap.py" "${pkgdir}/usr/lib/python2.7/site-packages/Leap.py"
install -D -m644 "${pkgdir}/usr/lib/Leap/LeapPython.so" "${pkgdir}/usr/lib/python2.7/site-packages/LeapPython.so"
```

En otras distribuciones de GNU/Linux es probable que estén los paquetes de Python en los
repositorios oficiales, pero en caso de que no, se pueden instalar usando **pip**. En la
página oficial de Leap Motion también encontramos descargas para GNU/Linux.

Después de esto, deberíamos ser capaces de ejecutar nuestro proyecto sin ningún problema.

## Sección de errores frecuentes o aspectos destacados

Alguno de los errores destacados ha sido ...

## Sección de lecturas recomendadas

La documentación oficial para [LeapMotion](https://developer.leapmotion.com/documentation/python/index.html),
[Pygame](https://www.pygame.org/docs/) y [PyOpenGL](http://pyopengl.sourceforge.net/documentation/) son imprescindibles.

## Referencias

El entorno gráfico de OpenGL ha sido sacado de [aquí](https://github.com/analca3/TriedroFrenet_Evoluta), y
todo lo referido a [Leap Motion](https://developer.leapmotion.com/documentation/python/index.html) y
[Pygame](https://www.pygame.org/docs/) ha sido sacado de la documentación oficial.

Los sonidos de ejemplo han sido sacados de [aquí](http://99sounds.org/drum-samples/), que
son libres mientras no lo usemos en ámbito comercial.
