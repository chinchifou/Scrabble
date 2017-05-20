#___IMPORTS___

import pygame
from pygame.locals import *

import display_settings as settings
from display_settings import *

import game_rules as rules
from game_rules import *

from math import floor



#___INITIALIZATION___

#launch Pygame
pygame.init()
running = True
print ('Game is running')

if RESOLUTION_AUTO :
    monitor_resolution = pygame.display.Info()
    settings.WIDTH = monitor_resolution.current_w
    settings.HEIGH = monitor_resolution.current_h
    print('Resolution set to : ', settings.WIDTH, ' * ', settings.HEIGH)

#CONSTANTS
TILE_PER_BOARD_COLUMN = 15 #NEVER CHANGE

# ! better experience if TILE_SIZE is set to 60 pixels, black stripes otherwise !
TILE_SIZE = 60 #MUST DIVIDE BOTH 1920 and 1080 / for instance 12; 15; 20; 24; 30; 40; 60 work

WIDTH_SCREEN_IN_TILES = 1920 / 60
HEIGH_SCREEN_IN_TILES = 1080 / 60

BOARD_SIZE_IN_TILES = 18

MENU_WIDTH_IN_TILES = WIDTH_SCREEN_IN_TILES - BOARD_SIZE_IN_TILES
MENU_HEIGH_IN_TILES = HEIGH_SCREEN_IN_TILES


#CHANGING WITH WINDOW RESIZING
zoom_factor = float(settings.WIDTH / 1920.0) #reference resolution is 1920*1080
window =  pygame.display.set_mode( (0, 0) )

tile_size = round(TILE_SIZE * zoom_factor)
delta = 1.5 * tile_size #distance of board from top left corner
board_size = round(BOARD_SIZE_IN_TILES * tile_size)
menu_width = round(MENU_WIDTH_IN_TILES * tile_size)
menu_heigh = round(MENU_HEIGH_IN_TILES * tile_size)


#CHANGING DURING THE GAME
board_state = [ ['?' for i in range(TILE_PER_BOARD_COLUMN)] for j in range(TILE_PER_BOARD_COLUMN) ]



#___IMAGES LOADING___

print ('    Loading images...')
# TODO change path for Linux ?
tile_start = pygame.image.load('./images/tiles/tile_start.png')
tile = pygame.image.load('./images/tiles/tile_empty.png') 
tile_double_letter = pygame.image.load('./images/tiles/tile_double_letter.png')
tile_triple_letter = pygame.image.load('./images/tiles/tile_triple_letter.png')
tile_double_word = pygame.image.load('./images/tiles/tile_double_word.png')
tile_triple_word = pygame.image.load('./images/tiles/tile_triple_word.png')

board = pygame.image.load('./images/board.png')
menu = pygame.image.load('./images/menu.png')

#TODO store letters images in an array
#LETTERS
path_for_letters = './images/letters/'+LANGUAGE+'/letter_'

letters = {
'_joker' : pygame.image.load(path_for_letters+'_joker.png'),
'A' : pygame.image.load(path_for_letters+'A.png'),
'B' : pygame.image.load(path_for_letters+'B.png'),
'C' : pygame.image.load(path_for_letters+'C.png'),
'D' : pygame.image.load(path_for_letters+'D.png'),
'E' : pygame.image.load(path_for_letters+'E.png'),
'F' : pygame.image.load(path_for_letters+'F.png'),
'G' : pygame.image.load(path_for_letters+'G.png'),
'H' : pygame.image.load(path_for_letters+'H.png'),
'I' : pygame.image.load(path_for_letters+'I.png'),
'J' : pygame.image.load(path_for_letters+'J.png'),
'K' : pygame.image.load(path_for_letters+'K.png'),
'L' : pygame.image.load(path_for_letters+'L.png'),
'M' : pygame.image.load(path_for_letters+'M.png'),
'N' : pygame.image.load(path_for_letters+'N.png'),
'O' : pygame.image.load(path_for_letters+'O.png'),
'P' : pygame.image.load(path_for_letters+'P.png'),
'Q' : pygame.image.load(path_for_letters+'Q.png'),
'R' : pygame.image.load(path_for_letters+'R.png'),
'S' : pygame.image.load(path_for_letters+'S.png'),
'T' : pygame.image.load(path_for_letters+'T.png'),
'U' : pygame.image.load(path_for_letters+'U.png'),
'V' : pygame.image.load(path_for_letters+'V.png'),
'W' : pygame.image.load(path_for_letters+'W.png'),
'X' : pygame.image.load(path_for_letters+'X.png'),
'Y' : pygame.image.load(path_for_letters+'Y.png'),
'Z' : pygame.image.load(path_for_letters+'Z.png')
}
print('    Images loaded')



#___FUNCTIONS___

#Game window creation
def refreshWindow(window, width, heigh) :
    if settings.FULLSCREEN :
        if settings.DOUBLEBUF :
            if settings.HWSURFACE :
                window = pygame.display.set_mode( (width, heigh), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
            else :
                window = pygame.display.set_mode( (width, heigh), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        else:
            window = pygame.display.set_mode( (width, heigh), pygame.FULLSCREEN)
    else :
        if settings.RESIZABLE :
            if settings.DOUBLEBUF :
                if settings.HWSURFACE :
                    window = pygame.display.set_mode( (width, heigh), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
                else :
                    window = pygame.display.set_mode( (width, heigh), pygame.RESIZABLE | pygame.DOUBLEBUF)
            else:
                window = pygame.display.set_mode( (width, heigh) | pygame.RESIZABLE)
        else:
            window = pygame.display.set_mode( (width, heigh))
    return window

#Draw playing board
def drawAll() :
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


    window.blit(letters['A'],(1.5*tile_size, 1.5*tile_size)) #TEMP
    window.blit(letters['B'],(1.5*tile_size+tile_size, 1.5*tile_size)) #TEMP
    window.blit(letters['C'],(1.5*tile_size+2*tile_size, 1.5*tile_size)) #TEMP
   
    window.blit(menu, (board_size, 0))
    pygame.display.flip()

#update due to window resizing
def updateZoomFactor(width, heigh) :
    return min( float(width / 1920), float(heigh/1080) )
def updateDelta() :
    return 1.5 * tile_size

#Resize tile
#TODO to be improved  
def updateTileSize() :
    return floor(TILE_SIZE * zoom_factor) #TO IMPROVE, Based on tile size
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
#TODO without return but parameters
def updateBoardSize() :
    return round( BOARD_SIZE_IN_TILES  * tile_size )
def resizeBoard() :
    return pygame.transform.smoothscale(board, (board_size, board_size) )

#Resize menu
def updateMenuWidth() :
    return round( MENU_WIDTH_IN_TILES * tile_size)
def updateMenuHeigh() :
    return round( MENU_HEIGH_IN_TILES * tile_size)
def resizeMenu() :
    return pygame.transform.smoothscale(menu, (menu_width, menu_heigh) )



#___WINDOW INITIALIZATION___

window = refreshWindow(window, settings.WIDTH, settings.HEIGH) #call 'event.type == VIDEORESIZE'



#___MAIN  GAME LOOP___

while running:
    for event in pygame.event.get():

        if (event.type == pygame.QUIT) : #close the game window
            running = False #exit the game

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False #exit the game

        elif (event.type == VIDEORESIZE) : #properly refresh the game window if a resize is detected
            window = refreshWindow(window, event.dict['size'][0], event.dict['size'][1])
            #load again all images to gain quality in case of a zoom in after a zoom out
            tile_start = pygame.image.load('./images/tiles/tile_start.png')
            tile = pygame.image.load('./images/tiles/tile_empty.png')
            tile_double_letter = pygame.image.load('./images/tiles/tile_double_letter.png')
            tile_triple_letter = pygame.image.load('./images/tiles/tile_triple_letter.png')
            tile_double_word = pygame.image.load('./images/tiles/tile_double_word.png')
            tile_triple_word = pygame.image.load('./images/tiles/tile_triple_word.png')

            board = pygame.image.load('./images/board.png') 
            menu = pygame.image.load('./images/menu.png') 

            letters = {
            '_joker' : pygame.image.load(path_for_letters+'_joker.png'),
            'A' : pygame.image.load(path_for_letters+'A.png'),
            'B' : pygame.image.load(path_for_letters+'B.png'),
            'C' : pygame.image.load(path_for_letters+'C.png'),
            'D' : pygame.image.load(path_for_letters+'D.png'),
            'E' : pygame.image.load(path_for_letters+'E.png'),
            'F' : pygame.image.load(path_for_letters+'F.png'),
            'G' : pygame.image.load(path_for_letters+'G.png'),
            'H' : pygame.image.load(path_for_letters+'H.png'),
            'I' : pygame.image.load(path_for_letters+'I.png'),
            'J' : pygame.image.load(path_for_letters+'J.png'),
            'K' : pygame.image.load(path_for_letters+'K.png'),
            'L' : pygame.image.load(path_for_letters+'L.png'),
            'M' : pygame.image.load(path_for_letters+'M.png'),
            'N' : pygame.image.load(path_for_letters+'N.png'),
            'O' : pygame.image.load(path_for_letters+'O.png'),
            'P' : pygame.image.load(path_for_letters+'P.png'),
            'Q' : pygame.image.load(path_for_letters+'Q.png'),
            'R' : pygame.image.load(path_for_letters+'R.png'),
            'S' : pygame.image.load(path_for_letters+'S.png'),
            'T' : pygame.image.load(path_for_letters+'T.png'),
            'U' : pygame.image.load(path_for_letters+'U.png'),
            'V' : pygame.image.load(path_for_letters+'V.png'),
            'W' : pygame.image.load(path_for_letters+'W.png'),
            'X' : pygame.image.load(path_for_letters+'X.png'),
            'Y' : pygame.image.load(path_for_letters+'Y.png'),
            'Z' : pygame.image.load(path_for_letters+'Z.png')
            }


            zoom_factor = updateZoomFactor(event.dict['size'][0], event.dict['size'][1])

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

            for key in letters.keys() :
                letters[key] = pygame.transform.smoothscale(letters[key], (tile_size, tile_size) ) #TEMP

            drawAll() #draw everything on screen



print('    Shutting down ...')
pygame.quit() #exit if running == false
print('Game is closed')


""" examples ...
from random import randint
print(randint(0,9))


#get edges
pygame.transform.laplacian()
find edges in a surface
laplacian(Surface, DestSurface = None) -> Surface

#two keys at the same time
keys = pygame.key.get_pressed()

if keys[K_LEFT]:
    self.char_x += 10


font = pygame.font.Font("./images/Futura-BoldRegular.ttf", 60)
test_letter = font.render('A',1,(0,0,0))
window.blit(test_letter,(1.5*tile_size, 1.5*tile_size))
pygame.display.flip()
"""
