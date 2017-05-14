#IMPORTS
import pygame
from pygame.locals import *

import config as cfg
from config import *



#INITIALIZATION

#launch Pygame
pygame.init()
running = True
print ('Game is running')



#GLOBAL VARIABLES
global BOARD_SIZE, WINDOW, RATIO, TILE_SIZE, TILE

#CONSTANTS
BOARD_SIZE = 16

#CHANGING WITH WINDOW RESIZING
WINDOW =  pygame.display.set_mode( (0, 0) )
RATIO = float(cfg.WIDTH / 1920)
TILE_SIZE = round(60 * RATIO)
print('TILE SIZE : A ', TILE_SIZE)



#IMAGES LOADING
print ('    Loading images...')
TILE = pygame.image.load("./images/tile.png") # TODO change path for Linux ?
print('    Images loaded')



#FUNCTIONS

#Draw playing board
def drawBoard(tile_size) :
    x_pos = 0
    y_pos = 0

    print('TILE SIZE B : ', tile_size)
    for row in range(0,BOARD_SIZE) :
        for column in range(0, BOARD_SIZE) :
            WINDOW.blit(TILE,(x_pos, y_pos))
            x_pos += tile_size
        x_pos = 0
        y_pos += tile_size

    pygame.display.flip()

#Resize tiles
def resizeTile(width, old_tile) :
    RATIO = float(width / 1920)
    TILE_SIZE = round(60 * RATIO)
    print('TILE SIZE C : ', TILE_SIZE)
    return pygame.transform.smoothscale(TILE, (TILE_SIZE, TILE_SIZE) )

#Game window creation
def refresh(window, width, heigh) :
    if cfg.FULLSCREEN :
        if cfg.DOUBLEBUF :
            if cfg.HWSURFACE :
                window = pygame.display.set_mode( (width, heigh), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
            else :
                window = pygame.display.set_mode( (width, heigh), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        else:
            window = pygame.display.set_mode( (width, heigh), pygame.FULLSCREEN)
    else :
        if cfg.RESIZABLE :
            if cfg.DOUBLEBUF :
                if cfg.HWSURFACE :
                    window = pygame.display.set_mode( (width, heigh), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
                else :
                    window = pygame.display.set_mode( (width, heigh), pygame.RESIZABLE | pygame.DOUBLEBUF)
            else:
                window = pygame.display.set_mode( (width, heigh) | pygame.RESIZABLE)
        else:
            window = pygame.display.set_mode( (width, heigh))
    return window


#WINDOW INITIALIZATION
WINDOW = refresh(WINDOW, cfg.WIDTH, cfg.HEIGH)
TILE = resizeTile(cfg.WIDTH, TILE)
drawBoard(TILE_SIZE)



#MAIN  GAME LOOP
while running:
    for event in pygame.event.get():

        if (event.type == pygame.QUIT) : #close the game window
            running = False #exit the game

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False #exit the game


        elif (cfg.FULLSCREEN == False and cfg.RESIZABLE == True and event.type == VIDEORESIZE) :
            #print('dict contains ', event.dict['size'])
            WINDOW = refresh(WINDOW, event.dict['size'][0], event.dict['size'][1])
            #window = pygame.display.set_mode( event.dict['size'], pygame.RESIZABLE )
            #window.blit(pygame.transform.smoothscale(background, event.dict['size']), (0, 0))
            RATIO = float(event.dict['size'][0] / 1920) 
            TILE = resizeTile(event.dict['size'][0], TILE)
            drawBoard(TILE_SIZE)


print('    Shutting down ...')
pygame.quit() #exit if running == false
print('Game is closed')


""" examples ...
#get edges
pygame.transform.laplacian()
find edges in a surface
laplacian(Surface, DestSurface = None) -> Surface

#two keys at the same time
keys = pygame.key.get_pressed()

if keys[K_LEFT]:
    self.char_x += 10
"""
