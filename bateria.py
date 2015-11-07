#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#Import Modules
import os, pygame
from pygame.locals import *
from pygame.compat import geterror

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

#functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(data_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound


#classes for our game objects
class Baqueta(pygame.sprite.Sprite):
    """moves a baqueta on the screen, following the mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('baqueta.png', -1)
        self.kicking = 0

    def update(self):
        "move the baqueta based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.kicking:
            self.rect.move_ip(5, 10)

    def kick(self, target):
        "returns true if the baqueta collides with the target"
        if not self.kicking:
            self.kicking = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unkick(self):
        "called to pull the baqueta back"
        self.kicking = 0


class Caja(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('caja.jpg', -1)
        self.original = self.image
        screen = pygame.display.get_surface()
        self.rect.topleft = 10, 10
        self.kicking = 0

    def update(self):
        if self.kicking:
            self.image = pygame.transform.flip(self.image, 1, 0)
        else:
            self.image = self.original

    def kicked(self):
        if not self.kicking:
            self.kicking = 1

    def unkick(self):
        self.kicking = 0


def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Bateria')
    pygame.mouse.set_visible(0)

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))

#Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Toca la batera", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width()/2)
        background.blit(text, textpos)

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

#Prepare Game Objects
    clock = pygame.time.Clock()
    whiff_sound = load_sound('whiff.wav')
    punch_sound = load_sound('kick.wav')
    caja = Caja()
    baqueta = Baqueta()
    allsprites = pygame.sprite.RenderPlain((baqueta, caja))


#Main Loop
    going = True
    while going:
        clock.tick(60)

        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == MOUSEBUTTONDOWN:
                if baqueta.kick(caja):
                    punch_sound.play() #kick
                    caja.kicked()
                else:
                    whiff_sound.play() #miss
            elif event.type == MOUSEBUTTONUP:
                baqueta.unkick()
                caja.unkick()

        allsprites.update()

        #Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

#Game Over


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
