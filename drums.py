#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# baqueta
# https://pixabay.com/p-149338/?no_redirect

#Import the Modules
import os, time, pygame
from pygame.locals import *
from pygame.compat import geterror
import pygbutton

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

main_dir = os.path.split(os.path.abspath(__file__))[0]
image_dir = os.path.join(main_dir, 'data/images')
sound_dir = os.path.join(main_dir, 'data/sounds')

#functions to create our resources
def load_image(name, colorkey=None):
    fullname = os.path.join(image_dir, name)
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
    fullname = os.path.join(sound_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound


#classes for our game objects
class Stick(pygame.sprite.Sprite):
    """moves a stick on the screen, following the mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('stick.png',-1)
        self.kicking = 0

    def update(self):
        "move the stick based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        if self.kicking:
            self.rect.move_ip(5, 10)

    def kick(self, targets):
        "returns the target that the stick collides with"
        if not self.kicking:
            self.kicking = 1
            hitbox = self.rect.inflate(-5, -5)
            for target in targets:
                if hitbox.colliderect(target.rect):
                    target.kicked()
                    return target
            else:
                return None

    def unkick(self):
        "called to pull the stick back"
        self.kicking = 0


class Instrument(pygame.sprite.Sprite):
    def __init__(self,imagename,topleft):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image(imagename,-1)
        self.original = self.image.copy()
        self.rect.topleft = topleft
        self.kicking = 0

    def update(self):
        self.image = self.original

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = pygame.transform.smoothscale(self.image,
                (int(self.original.get_height()*1.1),
                int(self.original.get_width()*1.1)))

        if self.kicking:
            self.image = pygame.transform.flip(self.image, 1, 1)

    def kicked(self):
        if not self.kicking:
            self.kicking = 1

    def unkicked(self):
        self.kicking = 0


class Button(pygame.sprite.Sprite):
    def __init__(self,imagename,topleft):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image(imagename,-1)
        self.rect.topleft = topleft
        #self.kicking = 0

        font = pygame.font.Font(None, 20)
        self.text = font.render("Menu", 1, (255, 255, 255))
        self.textpos = self.text.get_rect(centerx=self.image.get_width()/2,
            centery=self.image.get_height()/2)
        self.image.blit(self.text, self.textpos)

        self.original = self.image.copy()

        self.hovered = False
        self.starthovering = None
        self.speedhovering = 30

    def update(self):
        self.image = self.original.copy()

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if self.hovered:
                timepast = time.time() - self.starthovering
            else:
                timepast = 0
                self.hovered = True
                self.starthovering = time.time()

            self.image.fill((0,100,0),self.image.get_rect().inflate(-100+(timepast*self.speedhovering),-15))
            self.image.blit(self.text, self.textpos)

            if timepast*self.speedhovering > self.image.get_width()-22:
                raw_input("Lanzar Menu")
        else:
            self.hovered = False

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    screen_with = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_with, screen_height))
    pygame.display.set_caption('Drums')
    pygame.mouse.set_visible(0)

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

#Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Virtual drums", 1, (255, 255, 255))
        textpos = text.get_rect(centerx=background.get_width()/2,centery=20)
        background.blit(text, textpos)

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

#Prepare Game Objects
    clock = pygame.time.Clock()
    floortom_sound = load_sound('floortom-acoustic01.wav')
    snare_sound = load_sound('snare-acoustic01.wav')

    stick = Stick()
    button = Button('button.bmp',
        (4*screen_with/5, 1*screen_height/20))
    snare = Instrument('snare.bmp',
        (1*screen_with/5, 3*screen_height/5))
    floortom = Instrument('floortom.bmp',
        (3*screen_with/5, 3*screen_height/5))
    instruments = [floortom,snare]

    allsprites = pygame.sprite.OrderedUpdates()
    for instrument in instruments:
        allsprites.add(instrument)
    allsprites.add(button)
    allsprites.add(stick)

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
                instrument_kicked = stick.kick(instruments)
                if instrument_kicked == floortom:
                    floortom_sound.play()
                elif instrument_kicked == snare:
                    snare_sound.play()
                elif instrument_kicked == button:
                    print "button pressed"
            elif event.type == MOUSEBUTTONUP:
                stick.unkick()
                for instrument in instruments:
                    instrument.unkicked()

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
