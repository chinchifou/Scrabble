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



#CONSTANTS
global BOARD_SIZE, TILE_SIZE
BOARD_SIZE = 16
TILE_SIZE = 60

#CHANGING WITH WINDOW RESIZING
window =  pygame.display.set_mode( (0, 0) )
ratio = float(cfg.WIDTH / 1920)
tile_size = round(TILE_SIZE * ratio)



#IMAGES LOADING
print ('    Loading images...')
tile = pygame.image.load("./images/tile.png") # TODO change path for Linux ?
footer = pygame.image.load("./images/footer.png")
menu = pygame.image.load("./images/menu.png")
print('    Images loaded')



#FUNCTIONS

#Draw playing board
def drawBoard(tile_size) :
    x_pos = 0
    y_pos = 0

    for row in range(0,BOARD_SIZE) :
        for column in range(0, BOARD_SIZE) :
            window.blit(tile,(x_pos, y_pos))
            x_pos += tile_size
        x_pos = 0
        y_pos += tile_size

    #window.blit(footer, (0, 960))

    pygame.display.flip()


#Resize tiles
def resizeTile(ratio) :
    tile_size = round(60 * ratio)
    return pygame.transform.smoothscale(tile, (tile_size, tile_size) )

#Game window creation
def refreshWindow(window, width, heigh) :
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


def updateRatio(width) :
    return float(width / 1920)

def updateTileSize(width) :
    return round(TILE_SIZE * ratio)

def updateSize() :
    ratio = updateRatio(event.dict['size'][0])

    tile_size = updateTileSize(event.dict['size'][0])
    tile = resizeTile(event.dict['size'][0])


#WINDOW INITIALIZATION
window = refreshWindow(window, cfg.WIDTH, cfg.HEIGH)
tile = resizeTile(ratio)
drawBoard(tile_size)



#MAIN  GAME LOOP
while running:
    for event in pygame.event.get():

        if (event.type == pygame.QUIT) : #close the game window
            running = False #exit the game

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False #exit the game


        elif (cfg.FULLSCREEN == False and cfg.RESIZABLE == True and event.type == VIDEORESIZE) :
            window = refreshWindow(window, event.dict['size'][0], event.dict['size'][1])
            tile = pygame.image.load("./images/tile.png") #to regain quality 

            ratio = updateRatio(event.dict['size'][0])
            tile_size = updateTileSize(event.dict['size'][0])
            tile = resizeTile(ratio)

            drawBoard(tile_size)


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
