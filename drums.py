#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# baqueta
# https://pixabay.com/p-149338/?no_redirect

import Leap, sys, thread
import os, time, pygame
from pygame.locals import *
from pygame.compat import geterror
import pygbutton

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

main_dir = os.path.split(os.path.abspath(__file__))[0]
image_dir = os.path.join(main_dir, 'data/images')
sound_dir = os.path.join(main_dir, 'data/sounds')


inputDevice = pygame.mouse

# TODO: clean button class
# TODO: add effect when gesture happend in stick
# TODO: add controller to button (remove global variable)

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

def volumeSounds(sounds, option):

    if option == 0:
        volume = 0.1
    elif option == 1:
        volume = 0.5
    elif option == 2:
        volume = 1
    else:
        raise ValueError("Volume option not 0, 1 or 2")

    for s in sounds:
        s.set_sound(volume)



#classes for our game objects
class Stick(pygame.sprite.Sprite):
    """moves a stick on the screen, following the mouse"""
    def __init__(self, controller):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image('stick.png',-1)
        self.kicking = False
        self.controller = controller

    def update(self):
        "move the stick based on the mouse position"

        if self.controller.get_pos():
            pos = self.controller.get_pos()

        else:
            pos = (0,0)
        self.rect.midtop = pos

        self.rect.midtop = pos
        if self.kicking:
            print "hello"
            #self.rect.move_ip(5, 10)

    def kick(self, targets):
        "returns the target that the stick collides with"
        if not self.kicking:
            self.kicking = True
            hitbox = self.rect.inflate(-5, -5)
            for target in targets:
                if hitbox.colliderect(target.rect):
                    target.kicked()
                    return target
            else:
                return None

    def unkick(self):
        "called to pull the stick back"
        self.kicking = False

class Instrument(pygame.sprite.Sprite):
    def __init__(self,imagename,topleft):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image(imagename,-1)
        self.original = self.image.copy()
        self.rect.topleft = topleft
        self.kicking = False

    def update(self):
        self.image = self.original

        if self.rect.collidepoint(inputDevice.get_pos()):
            self.image = pygame.transform.smoothscale(self.image,
                (int(self.original.get_height()*1.1),
                int(self.original.get_width()*1.1)))

        if self.kicking:
            self.image = pygame.transform.flip(self.image, 1, 1)

    def kicked(self):
        if not self.kicking:
            self.kicking = True

    def unkicked(self):
        self.kicking = False

class Button(pygame.sprite.Sprite):
    def __init__(self,imagename,text,topleft=(0,0),center=None):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image(imagename,-1)

        if center:
            self.rect.center = center
        else:
            self.rect.topleft = topleft
        #self.kicking = 0

        font = pygame.font.Font(None, 20)
        self.text = font.render(text, 1, (255, 255, 255))
        self.textpos = self.text.get_rect(centerx=self.image.get_width()/2,
            centery=self.image.get_height()/2)
        self.image.blit(self.text, self.textpos)

        self.original = self.image.copy()

        self.hovered = False
        self.starthovering = None
        self.speedhovering = 60
        self.hoveringended = False

    def update(self):
        self.image = self.original.copy()

        if self.rect.collidepoint(inputDevice.get_pos()):
            if self.hovered:
                timepast = time.time() - self.starthovering
            else:
                timepast = 0
                self.hovered = True
                self.starthovering = time.time()

            self.image.fill((0,100,0),self.image.get_rect().inflate(-100+(timepast*self.speedhovering),-15))
            self.image.blit(self.text, self.textpos)

            if timepast*self.speedhovering > self.image.get_width()-22:
                self.hoveringended = True
                self.hovered = False
        else:
            self.hovered = False

# Leap Motion controller class
class DataController:
    def __init__(self, controller):
        self.controller = controller
        self.lastFrame = None
        self.lastFrameID = 0
        self.lastProcessedFrameID = 0
        self.detectedGesture = False
        self.sticksPosition = None
        self.sticksDirection = None

        self.controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);

    def get_pos(self):
        return self.sticksPosition

    def map2Dcoordinates(self):
        app_width = 800
        app_height = 800

        pointable = self.lastFrame.pointables.frontmost
        iBox = self.lastFrame.interaction_box
        leapPoint = pointable.stabilized_tip_position
        normalizedPoint = iBox.normalize_point(leapPoint, False)

        app_x = normalizedPoint.x * app_width
        # app_y = (1 - normalizedPoint.y) * app_height
        app_y = (normalizedPoint.z) * app_height
        #The z-coordinate is not used
        pos = (app_x, app_y)
        return pos

    def processNextFrame(self):
        frame = self.controller.frame()

        if(frame.id == self.lastFrameID):
            return
        if(frame.is_valid):
            for tool in frame.tools:
                self.sticksPosition = self.map2Dcoordinates()
                self.sticksDirection = tool.direction
            if self.lastFrame:
                #print self.lastFrameID, frame.id
                gestures = frame.gestures(self.lastFrame)
                #print len(gestures)
                for gesture in gestures:
                    # Key tap
                    if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                        self.detectedGesture = True
            else:
                self.detectedGesture = None

        self.lastFrame = frame
        self.lastFrameID = frame.id

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    screen_with = 800
    screen_height = 800
    screen = pygame.display.set_mode((screen_with, screen_height))
    pygame.display.set_caption('Drums')
    pygame.mouse.set_visible(0)
    controller = Leap.Controller()
    dataController = DataController(controller)

    # inputDevice = controller

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

    # stick = Stick(dataController)
    stick = Stick(inputDevice)

    # startScreen
    buttonStart = Button('button.bmp','Start',
        center=(5*screen_with/10, 5*screen_height/10))
    spritesStartScreen = pygame.sprite.OrderedUpdates()
    spritesStartScreen.add(buttonStart)
    spritesStartScreen.add(stick)

    # drumsScreen

    buttonOptions = Button('button.bmp','Options',
        (4*screen_with/5, 3*screen_height/20))
    snare = Instrument('snare.bmp',
        (1*screen_with/5, 3*screen_height/5))
    floortom = Instrument('floortom.bmp',
        (3*screen_with/5, 3*screen_height/5))
    instruments = [floortom,snare]

    spritesDrumsScreen = pygame.sprite.OrderedUpdates()
    for instrument in instruments:
        spritesDrumsScreen.add(instrument)
    spritesDrumsScreen.add(buttonOptions)
    spritesDrumsScreen.add(stick)

    # optionsScreen
    buttonBackToDrums = Button('button.bmp','Back',
        (4*screen_with/5, 1*screen_height/20))
    buttonSetVolume = Button('button.bmp','Volume',
        center=(2*screen_with/10, 2*screen_height/10))
    buttonVolume0 = Button('button.bmp','Bajo',
        center=(4*screen_with/10, 2*screen_height/10))
    buttonVolume1 = Button('button.bmp','Medio',
        center=(6*screen_with/10, 2*screen_height/10))
    buttonVolume2 = Button('button.bmp','Alto',
        center=(8*screen_with/10, 2*screen_height/10))

    spritesOptionsScreen = pygame.sprite.OrderedUpdates()
    spritesOptionsScreen.add(buttonBackToDrums)
    spritesOptionsScreen.add(buttonSetVolume)
    spritesOptionsScreen.add(buttonVolume0)
    spritesOptionsScreen.add(buttonVolume1)
    spritesOptionsScreen.add(buttonVolume2)
    spritesOptionsScreen.add(stick)

#Main Loop
    going = True
    startScreen = True
    optionsScreen = False
    backToDrumsScreen = False
    while going:
        clock.tick(60)
        dataController.processNextFrame()

        if dataController.detectedGesture:
            instrument_kicked = stick.kick(instruments)
            if instrument_kicked == floortom:
                floortom_sound.play()
            elif instrument_kicked == snare:
                snare_sound.play()
        else:
            stick.unkick()
            for instrument in instruments:
                instrument.unkicked()
        dataController.detectedGesture = False

        #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q):
                going = False

        if startScreen:
            spritesStartScreen.update()
        else:
            if optionsScreen and not backToDrumsScreen:
                spritesOptionsScreen.update()
            else:
                spritesDrumsScreen.update()

        #Draw Everything
        screen.blit(background, (0, 0))
        if startScreen:
            spritesStartScreen.draw(screen)
        else:
            if optionsScreen and not backToDrumsScreen:
                spritesOptionsScreen.draw(screen)
            else:
                spritesDrumsScreen.draw(screen)

        pygame.display.flip()
        startScreen = not buttonStart.hoveringended
        optionsScreen = buttonOptions.hoveringended
        backToDrumsScreen = buttonBackToDrums.hoveringended

    pygame.quit()

#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
