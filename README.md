# Percusión con Leap Motion

Este proyecto para la asignatura Nuevos Paradigmas de Interacción de la UGR
consta de una batería virtual y otros instrumentos de percusión.

## Autores
Sus autores somos [Antonio Álvarez Caballero](https://github.com/analca3)
y [Adrián Ranea Robles](https://github.com/ranea).

## Fecha de realización

Desde el día 16 de Octubre hasta el 2 de Diciembre.

## Descripción del problema que se aborda

El problema abordado es tocar instrumentos de percusión
con el Leap. Utilizando hasta dos lápices, rotuladores o similar,
podremos simular de manera sencilla y simple el *golpeo* (kick)
al instrumento de percusión.

## Descripción de la solución que se aporta

La solución propuesta es la siguiente: en un entorno virtual se dibujan varios
instrumentos de percusión. Tomando como referencia una herramienta (lápiz, bolígrafo, rotuladores...)
pintamos en pantalla una baqueta que trackea el movimiento de la herramienta
utilizando los datos del Leap. Al posicionar la baqueta encima de un instrumento
y realizar el gesto [key tap](https://di4564baj7skl.cloudfront.net/documentation/images/Leap_Gesture_Tap.png)
(esto es agitar la baqueta hacia abajo como si golpeáramos una batería)
se reproducirá el sonido asociado a ese gesto.

Para navegar entre las distintas opciones lo único que hay que hacer es 
dejar la baqueta encima del botón un tiempo determinado y se
activará la opción asociada a dicho botón.

### Instalación

Para poder ejecutar este proyecto, hacen falta varias cosas:

* Python
* Pygame
* Leap Motion SDK

Para instalar esto en nuestras máquinas de desarrollo (Archlinux x86_64), sólo hacen
falta un par de órdenes. Notar que [pacman](https://wiki.archlinux.org/index.php/Pacman)
es el gestor de paquetes de Archlinux y [pacaur](https://aur.archlinux.org/packages/pacaur/)
es un wrapper para instalar paquetes de la comunidad fácilmente. En caso de no tenerlo
se pueden acceder a los paquetes de Leap de la comunidad desde [aquí](https://aur.archlinux.org/packages/?O=0&K=leap+motion)

```bash
$ sudo pacman -Syu python2 python2-pygame
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

### Ejecución

En Archlinux, bastaría conectar el Leap Motion mediante los comandos:
```bash
$ sudo leapd
```

Es necesaria activar la opción *Tool tracking en el panel de control de leap. En ArchLinux, puedes abrir dicho panel buscando la aplicación *Leap Motion Control Panel*. También puedes ejecutarla por consola

```bash
$ LeapControlPanel
```

![LeapPanel](data/snapshots/leappanel.png)

Para ejecutarlo este programa, basta escribir:
```bash
$ python2 drums.py
```

### Uso

Cuando ejecutes el programa, encontrarás un tutorial con la información necesaria para usar el programa.

Presta atención y... ¡disfruta tocando!

Entra en la configuración y verás algunas opciones que puedes modificar: volumen, sonidos y pantalla completa. Los sonidos no tienen por qué ser de batería, ¡entra y descubre cuáles son!

## Errores frecuentes o aspectos destacados

Alguno de los errores destacados en esta práctica han sido:

- Movimiento de la baqueta: Posicionar un Sprite de una baqueta según la posición reconocida por Leap Motion es trivial. Lo complicado es rotarla según una dirección y que siga colisionando con el entorno de manera más o menos precisa. Se ha resuelto realizando un pequeño cálculo y aproximando.

- No hay una gran de imágenes libres relacionadas con los distintos intrumentos de percusión y en muchos casos
las imágenes existentes no eran de la suficiente calidad como para utilizarlas.


## Lecturas recomendadas

La documentación oficial para [LeapMotion](https://developer.leapmotion.com/documentation/python/index.html) y
[Pygame](https://www.pygame.org/docs/) son imprescindibles.

## Referencias

Lo referido a [Leap Motion](https://developer.leapmotion.com/documentation/python/index.html) y
[Pygame](https://www.pygame.org/docs/) ha sido sacado de la documentación oficial.Además
se ha partido del ejemplo del tutorial de Pygame [chimp](https://www.pygame.org/docs/tut/chimp/ChimpLineByLine.html)

Los sonidos de ejemplo han sido sacados de [aquí](http://99sounds.org/drum-samples/)
y de [aquí](http://99sounds.org/percussion-samples/), que son libres.

Las imágenes la hemos sacado de:

 - [electronicdrums](https://www.flickr.com/photos/jtjdt/6026391058)
 - [rainstick](https://en.wikipedia.org/wiki/Rainstick#/media/File:Rainstick_01.png)
 - [cymbal](https://en.wikipedia.org/wiki/Cymbal#/media/File:2006-07-06_Crash_Zildjian_14.jpg)
 - [chime](https://en.wikipedia.org/wiki/Mark_tree#/media/File:Meinl_CH-12_Chimes.jpg)
 - [framedrumes](https://en.wikipedia.org/wiki/Pandeiro#/media/File:Pandeiro.jpg)
 - [drumstick](https://commons.wikimedia.org/wiki/File:Drumsticks.png)
