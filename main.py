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
TILE_PER_BOARD_COLUMN = 16 #NEVER CHANGE

TILE_SIZE = 60 #MUST DIVIDE BTH 1920 and 1080 / for instance 12; 15; 20; 24; 30; 40; 60 work

TILE_WIDTH_SCREEN = 1920 / TILE_SIZE
TILE_HEIGH_SCREEN = 1080 / TILE_SIZE


FOOTER_WIDTH = TILE_PER_BOARD_COLUMN * TILE_SIZE
FOOTER_HEIGH = ( TILE_HEIGH_SCREEN - TILE_PER_BOARD_COLUMN ) * TILE_SIZE
MENU_WIDTH = ( TILE_WIDTH_SCREEN - TILE_PER_BOARD_COLUMN ) * TILE_SIZE
MENU_HEIGH = TILE_HEIGH_SCREEN * TILE_SIZE



#CHANGING WITH WINDOW RESIZING
ratio = float(cfg.WIDTH / 1920) #reference resolution is 1920*1080
window =  pygame.display.set_mode( (0, 0) )
tile_size = round(TILE_SIZE * ratio)
footer_width = round(FOOTER_WIDTH * ratio)
footer_heigh = round(FOOTER_HEIGH * ratio)
menu_width = round(MENU_WIDTH * ratio)
menu_heigh = round(MENU_HEIGH * ratio)



#IMAGES LOADING
print ('    Loading images...')
tile = pygame.image.load("./images/tile.png") # TODO change path for Linux ?
footer = pygame.image.load("./images/footer_textured.png")
menu = pygame.image.load("./images/menu.png")
print('    Images loaded')



#FUNCTIONS

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

#Draw playing board
def drawBoard() :
    x_pos = 0
    y_pos = 0

    for row in range(0,TILE_PER_BOARD_COLUMN) :
        for column in range(0, TILE_PER_BOARD_COLUMN) :
            window.blit(tile,(x_pos, y_pos))
            x_pos += tile_size
        x_pos = 0
        y_pos += tile_size

    window.blit(footer, (0, TILE_PER_BOARD_COLUMN*tile_size))
    window.blit(menu, (TILE_PER_BOARD_COLUMN*tile_size, 0))
    pygame.display.flip()

def updateRatio(width, heigh) :
    return min( float(width / 1920), float(heigh/1080) )

#Resize tile
def resizeTile() :
    return pygame.transform.smoothscale(tile, (tile_size, tile_size) )

def updateTileSize() :
    return round(TILE_SIZE * ratio) #TO IMPROVE, Based on tile size

#Resize footer
def resizeFooter() :
    return pygame.transform.smoothscale(footer, (footer_width, footer_heigh) )

def updateFooterWidth() :
    return round(TILE_PER_BOARD_COLUMN * tile_size)

def updateFooterHeigh() :
    return round(( TILE_HEIGH_SCREEN - TILE_PER_BOARD_COLUMN ) * tile_size)

#Resize menu
def resizeMenu() :
    return pygame.transform.smoothscale(menu, (menu_width, menu_heigh) )

def updateMenuWidth() :
    return round(( TILE_WIDTH_SCREEN - TILE_PER_BOARD_COLUMN ) * tile_size)

def updateMenuHeigh() :
    return round(TILE_HEIGH_SCREEN * tile_size)



#WINDOW INITIALIZATION
window = refreshWindow(window, cfg.WIDTH, cfg.HEIGH)

tile_size = updateTileSize()
tile = resizeTile()

footer_width = updateMenuWidth()
footer_heigh = updateFooterHeigh()
footer = resizeFooter()

menu_width = updateMenuWidth()
menu_heigh = updateMenuHeigh()
menu = resizeMenu()

drawBoard()



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
            footer = pygame.image.load("./images/footer_textured.png")
            menu = pygame.image.load("./images/menu.png") 

            ratio = updateRatio(event.dict['size'][0], event.dict['size'][1])

            tile_size = updateTileSize()
            tile = resizeTile()

            footer_width = updateMenuWidth()
            footer_heigh = updateFooterHeigh()
            footer = resizeFooter()

            menu_width = updateMenuWidth()
            menu_heigh = updateMenuHeigh()
            menu = resizeMenu()

            drawBoard()


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
