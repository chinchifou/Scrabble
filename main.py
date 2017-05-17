#IMPORTS
import pygame
from pygame.locals import *

import config as cfg
from config import *

from math import floor


#INITIALIZATION

#launch Pygame
pygame.init()
running = True
print ('Game is running')


#CONSTANTS
TILE_PER_BOARD_COLUMN = 15 #NEVER CHANGE

TILE_SIZE = 60 #MUST DIVIDE BTH 1920 and 1080 / for instance 12; 15; 20; 24; 30; 40; 60 work

WIDTH_SCREEN_IN_TILES = 1920 / TILE_SIZE
HEIGH_SCREEN_IN_TILES = 1080 / TILE_SIZE

BOARD_SIZE_IN_TILES = 18

MENU_WIDTH_IN_TILES = WIDTH_SCREEN_IN_TILES - BOARD_SIZE_IN_TILES
MENU_HEIGH_IN_TILES = HEIGH_SCREEN_IN_TILES

# 0 : start
# 1 : normal tile
# 2 : double letter
# 3 : triple letter
# 4 : double word
# 5 : triple word
LAYOUT = [
[5,1,1,2,1,1,1,5,1,1,1,2,1,1,5],
[1,4,1,1,1,3,1,1,1,3,1,1,1,4,1],
[1,1,4,1,1,1,2,1,2,1,1,1,4,1,1],
[2,1,1,4,1,1,1,2,1,1,1,4,1,1,2],
[1,1,1,1,4,1,1,1,1,1,4,1,1,1,1],
[1,3,1,1,1,3,1,1,1,3,1,1,1,3,1],
[1,1,2,1,1,1,2,1,2,1,1,1,2,1,1],
[5,1,1,2,1,1,1,0,1,1,1,2,1,1,5],
[1,1,2,1,1,1,2,1,2,1,1,1,2,1,1],
[1,3,1,1,1,3,1,1,1,3,1,1,1,3,1],
[1,1,1,1,4,1,1,1,1,1,4,1,1,1,1],
[2,1,1,4,1,1,1,2,1,1,1,4,1,1,2],
[1,1,4,1,1,1,2,1,2,1,1,1,4,1,1],
[1,4,1,1,1,3,1,1,1,3,1,1,1,4,1],
[5,1,1,2,1,1,1,5,1,1,1,2,1,1,5]
]



#CHANGING WITH WINDOW RESIZING
ratio = float(cfg.WIDTH / 1920) #reference resolution is 1920*1080
delta = 1.5 * TILE_SIZE #distance of board from top left corner
window =  pygame.display.set_mode( (0, 0) )
tile_size = round(TILE_SIZE * ratio)
board_size = round(BOARD_SIZE_IN_TILES * tile_size)
menu_width = round(MENU_WIDTH_IN_TILES * tile_size)
menu_heigh = round(MENU_HEIGH_IN_TILES * tile_size)



#IMAGES LOADING
print ('    Loading images...')

tile_start = pygame.image.load("./images/tile_start.png")

tile = pygame.image.load("./images/tile.png") # TODO change path for Linux ?

tile_double_letter = pygame.image.load("./images/tile_double_letter.png")
tile_triple_letter = pygame.image.load("./images/tile_triple_letter.png")

tile_double_word = pygame.image.load("./images/tile_double_word.png")
tile_triple_word = pygame.image.load("./images/tile_triple_word.png")

board = pygame.image.load("./images/board.png")

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
    x_pos = 0 + delta
    y_pos = 0 + delta

    window.blit(board, (0, 0))

    for row in range(0,TILE_PER_BOARD_COLUMN) :
        for column in range(0, TILE_PER_BOARD_COLUMN) :
            if LAYOUT[row][column] == 0 :
                window.blit(tile_start,(x_pos, y_pos))
            elif LAYOUT[row][column] == 1 :
                window.blit(tile,(x_pos, y_pos))
            elif LAYOUT[row][column] == 2 :
                window.blit(tile_double_letter,(x_pos, y_pos))
            elif LAYOUT[row][column] == 3 :
                window.blit(tile_triple_letter,(x_pos, y_pos))
            elif LAYOUT[row][column] == 4 :
                window.blit(tile_double_word,(x_pos, y_pos))
            elif LAYOUT[row][column] == 5 :
                window.blit(tile_triple_word,(x_pos, y_pos))
            x_pos += tile_size
        x_pos = 0 + delta
        y_pos += tile_size

    window.blit(menu, (board_size, 0))

    pygame.display.flip()

def updateRatio(width, heigh) :
    return min( float(width / 1920), float(heigh/1080) )

def updateDelta() :
    return 1.5 * tile_size

#Resize tile    
def updateTileSize() :
    return floor(TILE_SIZE * ratio) #TO IMPROVE, Based on tile size
def resizeTile() :
    return pygame.transform.smoothscale(tile, (tile_size, tile_size) )
def resizeTileDoubleLetter() :
    return pygame.transform.smoothscale(tile_double_letter, (tile_size, tile_size) )
def resizeTileTripleLetter() :
    return pygame.transform.smoothscale(tile_triple_letter, (tile_size, tile_size) )    
def resizeTileDoubleWord() :
    return pygame.transform.smoothscale(tile_double_word, (tile_size, tile_size) )
def resizeTileTripleWord() :
    return pygame.transform.smoothscale(tile_triple_word, (tile_size, tile_size) )
def resizeTileStart() :
    return pygame.transform.smoothscale(tile_start, (tile_size, tile_size) )    

#Resize board
def updateBoardSize() :
    return round( HEIGH_SCREEN_IN_TILES  * tile_size )
def resizeBoard() :
    return pygame.transform.smoothscale(board, (board_size, board_size) )

#Resize menu
def updateMenuWidth() :
    return round( ( WIDTH_SCREEN_IN_TILES - BOARD_SIZE_IN_TILES  ) * tile_size)
def updateMenuHeigh() :
    return round(HEIGH_SCREEN_IN_TILES * tile_size)
def resizeMenu() :
    return pygame.transform.smoothscale(menu, (menu_width, menu_heigh) )



#WINDOW INITIALIZATION
window = refreshWindow(window, cfg.WIDTH, cfg.HEIGH)

tile_size = updateTileSize()
delta = updateDelta()
tile = resizeTile()

board_size = updateBoardSize()
board = resizeBoard()

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
            tile_start = pygame.image.load("./images/tile_start.png")
            tile = pygame.image.load("./images/tile.png") #to regain quality
            tile_double_letter = pygame.image.load("./images/tile_double_letter.png")
            tile_triple_letter = pygame.image.load("./images/tile_triple_letter.png")
            tile_double_word = pygame.image.load("./images/tile_double_word.png")
            tile_triple_word = pygame.image.load("./images/tile_triple_word.png")
            
            board = pygame.image.load("./images/board.png") 
            menu = pygame.image.load("./images/menu.png") 

            ratio = updateRatio(event.dict['size'][0], event.dict['size'][1])

            tile_size = updateTileSize()
            delta = updateDelta()
            tile = resizeTile()
            tile_double_letter = resizeTileDoubleLetter()
            tile_triple_letter = resizeTileTripleLetter()
            tile_double_word = resizeTileDoubleWord()
            tile_triple_word = resizeTileTripleWord()
            tile_start = resizeTileStart()

            board_size = updateBoardSize()
            board = resizeBoard()

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
