#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# baqueta: link
# https://pixabay.com/p-149338/?no_redirect

# TODO: clean map2Dcoordinates()
# TODO: clean print
# change set volume to all instrument
# why thread, why pygbutton

import Leap, sys
import os, time, pygame
from pygame.locals import *
from pygame.compat import geterror
from math import asin, degrees
import pygbutton


if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

main_dir = os.path.split(os.path.abspath(__file__))[0]
image_dir = os.path.join(main_dir, 'data/images')
sound_dir = os.path.join(main_dir, 'data/sounds')

#inputDevice = pygame.mouse

#functions to create our resources
def loadImage(name, colorkey=None):
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

def loadSound(name):
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

def changeVolumeSounds(instruments, option):
    if option == 0:
        volume = 0.1
    elif option == 1:
        volume = 0.5
    elif option == 2:
        volume = 1
    else:
        raise ValueError("Volume option not 0, 1 or 2")

    for i in instruments:
        i.sound.set_volume(volume)

#classes for our game objects
class Stick(pygame.sprite.Sprite):
    """moves a stick on the screen, following the tool detected by the Leap"""
    controller = None
    lastID = 0
    def __init__(self, imageName):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.original, self.rect = loadImage(imageName,-1)
        self.image = self.original.copy()
        self.kicking = False
        self.idTool = Stick.lastID
        Stick.lastID += 1
        self.visible = False

    def update(self):
        "move the stick based on the tool position"
        if Stick.controller.sticksPosition[self.idTool]:
            self.rect.midtop  = Stick.controller.sticksPosition[self.idTool]
            self.visible = True
            deg = -degrees(asin(Stick.controller.sticksDirection[self.idTool][0]))
            #if deg > 90:
            self.image = pygame.transform.rotate(self.original,deg)
            # self.image = pygame.transform.rotate(
            #         self.image, )
        else:
            # if self.idTool == 0:
            #     self.rect.midtop = (100,100)
            #     self.visible = True
            # else:
            #     self.rect.midtop = (300,300)
            #     self.visible = True
            self.visible = False

    def kick(self, targets):
        "returns the target that the stick collides with"
        if not self.kicking:
            self.kicking = True
            # hitbox = self.rect.inflate(-5, -5)
            hitbox = self.rect
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
    controller = None
    def __init__(self,imageName,sound,topleft):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = loadImage(imageName,-1)
        self.original = self.image.copy()
        self.sound = sound
        self.rect.topleft = topleft
        self.kicking = False

    def update(self):
        self.image = self.original

        if (Instrument.controller.sticksPosition[0] and
                self.rect.collidepoint(Instrument.controller.sticksPosition[0])
                ) or (Instrument.controller.sticksPosition[1] and
                self.rect.collidepoint(Instrument.controller.sticksPosition[1]) ):
            self.image = pygame.transform.smoothscale(self.image,
                (int(self.original.get_height()*1.1),
                int(self.original.get_width()*1.1)))

        if self.kicking:
            self.image = pygame.transform.flip(self.image, 1, 1)

    def kicked(self):
        if not self.kicking:
            self.kicking = True
            self.sound.play()

    def unkicked(self):
        self.kicking = False

    def play(self):
        self.sound.play()

class Button(pygame.sprite.Sprite):
    def __init__(self,imagename,text,topleft=(0,0),center=None):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = loadImage(imagename,-1)

        if center:
            self.rect.center = center
        else:
            self.rect.topleft = topleft

        font = pygame.font.Font(None, 20)
        self.text = font.render(text, 1, (255, 255, 255))
        self.textpos = self.text.get_rect(centerx=self.image.get_width()/2,
            centery=self.image.get_height()/2)
        self.image.blit(self.text, self.textpos)

class ButtonHoverable(Button):
    controller = None
    def __init__(self,imagename,text,topleft=(0,0),center=None):
        Button.__init__(self,imagename,text,topleft,center)
        self.original = self.image.copy()

        self.hovered = False
        self.starthovering = None
        self.speedhovering = 60
        self.hoveringended = False
        self.is_enable = False

    def update(self):
        self.image = self.original.copy()

        if self.is_enable:
            self.image.fill((0,100,0))
            self.image.blit(self.text, self.textpos)
            return

        if ButtonHoverable.controller.sticksPosition[0] and self.rect.collidepoint(
                ButtonHoverable.controller.sticksPosition[0]):
            if self.hovered:
                timepast = time.time() - self.starthovering
            else:
                timepast = 0
                self.hovered = True
                self.starthovering = time.time()

            self.image.fill((0,100,0),self.image.get_rect().inflate(
                    -100+(timepast*self.speedhovering),-15))
            self.image.blit(self.text, self.textpos)

            if timepast*self.speedhovering > self.image.get_width()-22:
                self.hoveringended = True
                self.hovered = False
        else:
            self.hovered = False

    def enable(self):
        self.is_enable = True

    def disable(self):
        self.is_enable = False

# Leap Motion controller class
class DataController:
    def __init__(self, controller,app_width,app_height):
        self.controller = controller
        self.app_width = app_width
        self.app_height = app_height
        self.lastFrame = None
        self.lastFrameID = 0
        self.lastProcessedFrameID = 0
        self.detectedGesture = False
        self.sticksPosition = [None,None]
        self.sticksDirection = [None,None]

        self.controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);

    #def get_pos(self):
    #    return self.sticksPosition

    def map2Dcoordinates(self,pointable,frame):
        #if self.lastFrame and self.lastFrame.pointables:
        iBox = frame.interaction_box
        leapPoint = pointable.stabilized_tip_position
        normalizedPoint = iBox.normalize_point(leapPoint, False)

        app_x = normalizedPoint.x * self.app_width
        # app_y = (1 - normalizedPoint.y) * app_height
        app_y = 0.9*(normalizedPoint.z) * self.app_height
        #The z-coordinate is not used
        pos = (app_x, app_y)
        return pos
        #else:
        #    return (0,0)

    def processNextFrame(self):
        frame = self.controller.frame()

        if frame.id == self.lastFrameID:
            return
        if frame.is_valid:
            i = 0
            for tool in frame.tools:
                self.sticksPosition[i] = self.map2Dcoordinates(tool,frame)
                self.sticksDirection[i] = (tool.direction.x, tool.direction.y)
                i += 1
                if i == 2:
                    sortedSticks = sorted(self.sticksPosition,reverse=True)
                    if sortedSticks != self.sticksPosition:
                        self.sticksPosition = sortedSticks
                        self.sticksDirection.reverse()
                    break

            for j in range(i,2):
                self.sticksPosition[j] = None
                self.sticksDirection[j] = None

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
    # Initialize Everything
    pygame.init()
    max_resolution = pygame.display.list_modes()[0]
    screen_with = max_resolution[0]
    screen_height = max_resolution[1]
    screen = pygame.display.set_mode((screen_with, screen_height),
            pygame.FULLSCREEN | pygame.HWSURFACE)
    pygame.display.set_caption('Drums')
    pygame.mouse.set_visible(0)
    controller = Leap.Controller()
    dataController = DataController(controller,screen_with,screen_height)
    Stick.controller = dataController
    Instrument.controller = dataController
    ButtonHoverable.controller = dataController

    # if dataController.controller.is_connected:
        # global inputDevice
        # inputDevice = dataController
    # global inputDevice
    # inputDevice = dataController

    # Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((1, 1, 1))

    # Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Virtual drums", 1, (255, 255, 255))
        textpos = text.get_rect(centerx=background.get_width()/2,centery=30)
        background.blit(text, textpos)

    #Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()

    #Prepare Game Objects
    clock = pygame.time.Clock()

    stick1 = Stick('stick1.png')
    stick2 = Stick('stick2.png')
    # stick = Stick(dataController)
    # stick = Stick(inputDevice)

    #Start Screen
    buttonStart = ButtonHoverable('buttonHoverable.bmp','Start',
        center=(5*screen_with/10, 5*screen_height/10))

    spritesStartScreen = pygame.sprite.OrderedUpdates(buttonStart,stick1)

    #Drums Screen
    buttonOptions = ButtonHoverable('buttonHoverable.bmp','Options',
        (4*screen_with/5, 3*screen_height/20))

    buttonQuit = ButtonHoverable('buttonHoverable.bmp','Quit',
        (4*screen_with/5, 1*screen_height/20))

    # battery A
    snare = Instrument('snare.bmp',loadSound('snare-acoustic01.wav'),
        (1*screen_with/5, 3*screen_height/5))

    instrumentsBatteryA = [snare]
    changeVolumeSounds(instrumentsBatteryA,1)
    spritesBatteryA = pygame.sprite.OrderedUpdates()
    spritesBatteryA.add(*instrumentsBatteryA)
    spritesBatteryA.add(buttonOptions)
    spritesBatteryA.add(buttonQuit)

    # battery B
    floortom = Instrument('floortom.bmp', loadSound('floortom-acoustic01.wav'),
        (3*screen_with/5, 3*screen_height/5))

    instrumentsBatteryB = [floortom]
    changeVolumeSounds(instrumentsBatteryB,1)
    spritesBatteryB = pygame.sprite.OrderedUpdates()
    spritesBatteryB.add(*instrumentsBatteryB)
    spritesBatteryB.add(buttonOptions)
    spritesBatteryB.add(buttonQuit)

    #Options Screen
    buttonBackToDrums = ButtonHoverable('buttonHoverable.bmp','Back',
        (4*screen_with/5, 1*screen_height/20))
    buttonSetVolume = Button('button.bmp','Volume',
        center=(2*screen_with/10, 2*screen_height/10))
    buttonVolume0 = ButtonHoverable('buttonHoverable.bmp','Low',
        center=(4*screen_with/10, 2*screen_height/10))
    buttonVolume1 = ButtonHoverable('buttonHoverable.bmp','Medium',
        center=(6*screen_with/10, 2*screen_height/10))
    buttonVolume2 = ButtonHoverable('buttonHoverable.bmp','High',
        center=(8*screen_with/10, 2*screen_height/10))
    buttonSetBattery = Button('button.bmp','Battery',
        center=(2*screen_with/10, 4*screen_height/10))
    buttonBatteryA = ButtonHoverable('buttonHoverable.bmp','Battery A',
        center=(4*screen_with/10, 4*screen_height/10))
    buttonBatteryB = ButtonHoverable('buttonHoverable.bmp','Battery B',
        center=(6*screen_with/10, 4*screen_height/10))
    buttonSetFullScreen = Button('button.bmp','Full Screen',
        center=(2*screen_with/10, 6*screen_height/10))
    buttonFullScreenOn = ButtonHoverable('buttonHoverable.bmp','On',
        center=(4*screen_with/10, 6*screen_height/10))
    buttonFullScreenOff = ButtonHoverable('buttonHoverable.bmp','Off',
        center=(6*screen_with/10, 6*screen_height/10))

    spritesOptionsScreen = pygame.sprite.OrderedUpdates()
    spritesOptionsScreen.add(buttonBackToDrums,buttonSetVolume,
        buttonVolume0,buttonVolume1,buttonVolume2,
        buttonSetBattery,buttonBatteryA,buttonBatteryB,
        buttonSetFullScreen, buttonFullScreenOn, buttonFullScreenOff)

    # Main Loop
    going = True
    current_screen = "drumsScreen"
    currentInstruments = instrumentsBatteryA
    allInstruments = instrumentsBatteryA + instrumentsBatteryB
    spritesDrumsScreen = spritesBatteryA
    buttonVolume1.enable()
    buttonBatteryA.enable()
    buttonFullScreenOn.enable()
    instrument_kicked1 = None
    instrument_kicked2 = None
    fullScreen = True
    changedFullScreen = False
    while going:
        clock.tick(30)
        dataController.processNextFrame()

        if current_screen == "startScreen":
            currentSticks = pygame.sprite.OrderedUpdates(stick1)

            if buttonStart.hoveringended:
                current_screen = "drumsScreen"
                buttonStart.hoveringended = False
        elif current_screen == "drumsScreen":
            currentSticks = pygame.sprite.OrderedUpdates(stick1,stick2)

            if dataController.detectedGesture:
                instrument_kicked1 = stick1.kick(currentInstruments)
                instrument_kicked2 = stick2.kick(currentInstruments)
            else:
                stick1.unkick()
                stick2.unkick()
                if instrument_kicked1:
                    instrument_kicked1.unkicked()
                    instrument_kicked1 = None
                if instrument_kicked2:
                    instrument_kicked2.unkicked()
                    instrument_kicked2 = None
                #for instrument in currentInstruments:
                #    instrument.unkicked()
            dataController.detectedGesture = False
        elif current_screen == "optionsScreen":
            currentSticks = pygame.sprite.OrderedUpdates(stick1)

            if buttonBackToDrums.hoveringended:
                current_screen = "drumsScreen"
                buttonBackToDrums.hoveringended = False

            if buttonVolume0.hoveringended:
                buttonVolume0.hoveringended = False
                buttonVolume0.enable()
                buttonVolume1.disable()
                buttonVolume2.disable()
                changeVolumeSounds(allInstruments,0)
            elif buttonVolume1.hoveringended:
                buttonVolume1.hoveringended = False
                buttonVolume1.enable()
                buttonVolume0.disable()
                buttonVolume2.disable()
                changeVolumeSounds(allInstruments,1)
            elif buttonVolume2.hoveringended:
                buttonVolume2.hoveringended = False
                buttonVolume2.enable()
                buttonVolume0.disable()
                buttonVolume1.disable()
                changeVolumeSounds(allInstruments,2)
            elif buttonBatteryA.hoveringended:
                buttonBatteryA.hoveringended = False
                buttonBatteryA.enable()
                buttonBatteryB.disable()
                spritesDrumsScreen = spritesBatteryA
                currentInstruments = instrumentsBatteryA
            elif buttonBatteryB.hoveringended:
                buttonBatteryB.hoveringended = False
                buttonBatteryB.enable()
                buttonBatteryA.disable()
                spritesDrumsScreen = spritesBatteryB
                currentInstruments = instrumentsBatteryB
            elif buttonFullScreenOn.hoveringended:
                buttonFullScreenOn.hoveringended = False
                buttonFullScreenOn.enable()
                buttonFullScreenOff.disable()
                if not fullScreen:
                    changedFullScreen = True
                    fullScreen = True
            elif buttonFullScreenOff.hoveringended:
                buttonFullScreenOff.hoveringended = False
                buttonFullScreenOn.disable()
                buttonFullScreenOff.enable()
                if fullScreen:
                    changedFullScreen = True
                    fullScreen = False

        # Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q):
                going = False



        currentSticks.update()
        if current_screen == "startScreen":
            spritesStartScreen.update()
        elif current_screen == "drumsScreen":
            spritesDrumsScreen.update()
        elif current_screen == "optionsScreen":
            spritesOptionsScreen.update()

        #print (stick1.rect.midtop, stick2.rect.midtop)
        if stick1.visible == False:
             currentSticks.remove(stick1)
        if stick2.visible == False and current_screen == "drumsScreen":
             currentSticks.remove(stick2)

        # Draw Everything
        screen.blit(background, (0, 0))
        if current_screen == "startScreen":
            spritesStartScreen.draw(screen)
        elif current_screen == "drumsScreen":
            spritesDrumsScreen.draw(screen)
            if buttonOptions.hoveringended:
                current_screen = "optionsScreen"
                buttonOptions.hoveringended = False
            elif buttonQuit.hoveringended:
                going = False
        elif current_screen == "optionsScreen":
            spritesOptionsScreen.draw(screen)
        currentSticks.draw(screen)



        pygame.display.flip()


        if changedFullScreen:
            pygame.display.toggle_fullscreen()
            changedFullScreen = False


    pygame.quit()

#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    main()
