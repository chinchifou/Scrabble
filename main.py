#___IMPORTS___

import pygame
from pygame.locals import *

import display_settings as settings
from display_settings import *

import game_rules as rules
from game_rules import *

from math import floor

from random import randint


#___INITIALIZATION___

#launch Pygame
pygame.init()
font = pygame.font.Font("./images/defaultFont.ttf", 60)
running = True
print ('Game is running')

if RESOLUTION_AUTO :
    monitor_resolution = pygame.display.Info()
    settings.WIDTH = monitor_resolution.current_w
    settings.HEIGH = monitor_resolution.current_h
    print('Resolution set to : ', settings.WIDTH, ' * ', settings.HEIGH)

#CONSTANTS
TILE_PER_BOARD_COLUMN = 15 #NEVER CHANGE WITHOUT CHANGING THE LAYOUT

# ! better experience if TILE_SIZE is set to 60 pixels, black stripes otherwise !
TILE_SIZE = 60 #MUST DIVIDE BOTH 1920 and 1080 / for instance 12; 15; 20; 24; 30; 40; 60 work

WIDTH_SCREEN_IN_TILES = 1920 / 60
HEIGH_SCREEN_IN_TILES = 1080 / 60

BOARD_SIZE_IN_TILES = 18

MENU_WIDTH_IN_TILES = WIDTH_SCREEN_IN_TILES - BOARD_SIZE_IN_TILES
MENU_HEIGH_IN_TILES = HEIGH_SCREEN_IN_TILES

ACTIONS = ('SELECT_A_LETTER', 'PLAY_A_LETTER')

PLAYERS = []


#CHANGING WITH WINDOW RESIZING
zoom_factor = float(settings.WIDTH / 1920.0) #reference resolution is 1920*1080
window =  pygame.display.set_mode( (0, 0) )

tile_size = round(TILE_SIZE * zoom_factor)
delta = 1.5 * tile_size #distance of board from top left corner

board_size = round(BOARD_SIZE_IN_TILES * tile_size)
menu_width = round(MENU_WIDTH_IN_TILES * tile_size)
menu_heigh = round(MENU_HEIGH_IN_TILES * tile_size)

font = pygame.font.Font("./images/defaultFont.ttf", tile_size)



#CHANGING DURING THE GAME
bag_of_letters = BAG_OF_LETTERS

board_state = [ ['?' for i in range(TILE_PER_BOARD_COLUMN)] for j in range(TILE_PER_BOARD_COLUMN) ]

id_player = 0

tile_x_hand = 0
selected_letter = ''
letter_from_board = False
letters_just_played = {} #format {'a' : (x, y)}

#TODO : BACKUP TO ALLOW RESET
board_state_at_turns_begining = board_state 
hand_at_turns_begining = []

#___IMAGES LOADING___

print ('    Loading images...')

#TILES
path_for_tiles = './images/tiles/tile_'# TODO change path for Linux ?
tiles = {
    'start' : pygame.image.load(path_for_tiles+'start.png'),
    'empty' : pygame.image.load(path_for_tiles+'empty.png'),
    'double_letter' : pygame.image.load(path_for_tiles+'double_letter.png'),
    'triple_letter' : pygame.image.load(path_for_tiles+'triple_letter.png'),
    'double_word' : pygame.image.load(path_for_tiles+'double_word.png'),
    'triple_word' : pygame.image.load(path_for_tiles+'triple_word.png')
}

#LETTERS
path_for_letters = './images/letters/'+LANGUAGE+'/letter_'
letters = {
'*' : pygame.image.load(path_for_letters+'_joker.png'),
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

board = pygame.image.load('./images/board.png')
menu = pygame.image.load('./images/menu.png')

print('    Images loaded')

#___CLASSES___
class Player :

    def __init__(self, name, points, hand) :
        self.name = name
        self.points = points
        self.hand = hand

    def printInstanceVariables(self) :
        padding = '    '
        print(padding+'name : ', self.name)
        print(padding+'points : ', self.points)
        print(padding+'hand : ', self.hand)


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
def drawBoardAndMenu() :
    x_pos = 0 + delta
    y_pos = 0 + delta

    #DRAW BOARD + TILES + LETTERS
    #board borders
    window.blit(board, (0, 0))

    #tiles
    for row in range(0,TILE_PER_BOARD_COLUMN) :
        for column in range(0, TILE_PER_BOARD_COLUMN) :
            if LAYOUT[row][column] == 0 :
                window.blit(tiles['start'],(x_pos, y_pos))
            elif LAYOUT[row][column] == 1 :
                window.blit(tiles['empty'],(x_pos, y_pos))
            elif LAYOUT[row][column] == 2 :
                window.blit(tiles['double_letter'],(x_pos, y_pos))
            elif LAYOUT[row][column] == 3 :
                window.blit(tiles['triple_letter'],(x_pos, y_pos))
            elif LAYOUT[row][column] == 4 :
                window.blit(tiles['double_word'],(x_pos, y_pos))
            elif LAYOUT[row][column] == 5 :
                window.blit(tiles['triple_word'],(x_pos, y_pos))
            x_pos += tile_size
        x_pos = 0 + delta
        y_pos += tile_size
    #letters on board
    for row in range(0,TILE_PER_BOARD_COLUMN) :
        for column in range(0, TILE_PER_BOARD_COLUMN) :
            if board_state[row][column] != '?' :
                window.blit( letters[ board_state[row][column] ], (delta + row * tile_size, delta + column * tile_size) )
   #draw menu
    window.blit(menu, (board_size, 0))


#Display on top of the screen the player who is currently playing
def drawTurnInfo(player) :
    test_text = font.render(player.name+"'S TURN",1,(143,144,138))
    delta_info_x = 2*delta + TILE_PER_BOARD_COLUMN*tile_size + 2*tile_size
    delta_info_y = delta
    window.blit(test_text,(delta_info_x, delta_info_y))

def drawHand(hand) :
    delta_hand_x = 2*delta + TILE_PER_BOARD_COLUMN*tile_size + 2*tile_size
    delta_hand_y = delta + 2*tile_size
    for id_letter in range(len(hand)) :
        window.blit(letters[hand[id_letter]], (delta_hand_x + id_letter*tile_size , delta_hand_y)) 

def cursorIsOnBoard(cursor_x, cursor_y) :
    tile_x = floor( (cursor_x - delta)/tile_size)
    tile_y = floor( (cursor_y - delta)/tile_size)
    if ( tile_x in range (0, TILE_PER_BOARD_COLUMN ) ) and ( tile_y in range (0, TILE_PER_BOARD_COLUMN ) ) :
        return True
    else :
        return False

def cursorIsOnHand(cursor_x, cursor_y, hand) : #TO DEBUG
    delta_hand_x = 2*delta + TILE_PER_BOARD_COLUMN*tile_size + 2*tile_size
    delta_hand_y = delta + 2*tile_size

    tile_x = floor( (cursor_x - delta_hand_x)/tile_size)
    tile_y = floor( (cursor_y - delta_hand_y)/tile_size)

    if ( tile_x in range (0, len(hand)) ) and ( tile_y in range (0, 1) ) :
        return True
    else :
        return False

def idTileFromHand(x) :
    return (x - (2 + TILE_PER_BOARD_COLUMN + 2) )


def emptySlot(x,y) :
    if board_state[x][y] == '?':
        return True
    else :
        return False

#NEW
def calculatePoints(letters_played) :
    #FORMAT letters_just_played {'a' : (x, y)}
    if len(letters_played) == 0 :
        print( '  NOTHING PLAYED')
        return 0

    else :
        print( '  A WORD HAS BEEN PLAYED')
        all_x = []
        all_y = []

        for tuple_pos in letters_played.keys() :
            all_x.append(tuple_pos[0])
            all_y.append(tuple_pos[1])

        min_x = min(all_x)
        max_x = max(all_x)        
        min_y = min(all_y)
        max_y = max(all_y)

        delta_x = max_x - min_x
        delta_y = max_y - min_y

        if delta_x == 0 : #TODO
            print('  VERTICAL WORD')  

            #find first letter
            start_y = min_y
            while( ( (start_y - 1) >= 0) and (board_state[min_x][start_y - 1] != '?') ) :
                start_y = start_y - 1

            #find last letter
            end_y = max_y
            while( ( (end_y + 1) <= TILE_PER_BOARD_COLUMN-1) and (board_state[min_x][end_y + 1] != '?') ) :
                end_y = end_y + 1

            #store word just created
            main_word = ''
            word_multiplier = 1
            word_score = 0

            for it_y in range( start_y, end_y+1 ) :
                letter = board_state[min_x][it_y]
                main_word += letter
                if ((min_x, it_y) in letters_played ): #letters just played
                    #calculate points for each letter
                    bonus = LAYOUT[min_x][it_y]
                    if bonus == 0 : #start_tile
                        word_multiplier *= 2
                        bonus = 1
                    elif bonus == 4:
                        word_multiplier *= 2
                        bonus = 1
                    elif bonus == 5:
                        word_multiplier *= 3
                        bonus = 1

                    new_letter_points = POINTS[letter]
                    word_score = word_score + (bonus * new_letter_points)

                else : #old letters
                    old_letter_points = POINTS[letter]
                    word_score = word_score + old_letter_points
                    
            word_score = word_score * word_multiplier

            words_and_scores = []
            words_and_scores.append([main_word, word_score])

            for association in words_and_scores :
                print('Word ', association[0], ' gives ', association[1], ' points' )

            for it_y in range( start_y, end_y+1 ) :
                #check for horizontal words
                if (min_x, it_y) in (letters_played) : #prevent to count already existing words
                    condition_1 = ( (min_x - 1) >= 0 ) and ( board_state[min_x-1][it_y] != '?' )
                    condition_2 = ( (min_x + 1) <= TILE_PER_BOARD_COLUMN-1 ) and ( board_state[min_x+1][it_y] != '?' )  
                    if ( condition_1  or condition_2 ) :

                        print('there is another word')

                        #TODO

                        while( ( (min_x - 1) >= 0) and (board_state[min_x][start_y - 1] != '?') ) :

                        while( ( (end_y + 1) <= TILE_PER_BOARD_COLUMN-1) and (board_state[min_x][end_y + 1] != '?') ) :
               

                        #TODO







            return word_score #TODO : to change

        else :
            print('  HORIZONTAL WORD') 
            return 0

        

#RELOAD IMAGES
def reloadTiles() :
    return {
    'start' : pygame.image.load(path_for_tiles+'start.png'),
    'empty' : pygame.image.load(path_for_tiles+'empty.png'),
    'double_letter' : pygame.image.load(path_for_tiles+'double_letter.png'),
    'triple_letter' : pygame.image.load(path_for_tiles+'triple_letter.png'),
    'double_word' : pygame.image.load(path_for_tiles+'double_word.png'),
    'triple_word' : pygame.image.load(path_for_tiles+'triple_word.png')
    }

def reloadLetters() :
    return {
            '*' : pygame.image.load(path_for_letters+'_joker.png'),
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

def reloardBoard() :
    return pygame.image.load('./images/board.png') 

def reloadMenu() :
    return pygame.image.load('./images/menu.png')

#UPDATES DUE TO WINDOW RESIZING
def updateZoomFactor(width, heigh) :
    return min( float(width / 1920), float(heigh/1080) )
def updateDelta() :
    return 1.5 * tile_size 
def updateTileSize() :
    return floor(TILE_SIZE * zoom_factor) #TO IMPROVE, Based on tile size
def updateBoardSize() :
    return round( BOARD_SIZE_IN_TILES  * tile_size )
def updateMenuWidth() :
    return round( MENU_WIDTH_IN_TILES * tile_size)
def updateMenuHeigh() :
    return round( MENU_HEIGH_IN_TILES * tile_size)



#___WINDOW INITIALIZATION___

window = refreshWindow(window, settings.WIDTH, settings.HEIGH) #call 'event.type == VIDEORESIZE'

#___GAME INITIALIZATION___
#Draw letters for each players
for player_name in PLAYERS_NAME :
    start_hand = []
    for i in range(LETTERS_PER_HAND) :
        random_int = randint(0,len(bag_of_letters)-1)
        start_hand.append(bag_of_letters[random_int])
        #bag_of_letters.remove(bag_of_letters[random_int])
        del(bag_of_letters[random_int])

    PLAYERS.append(Player(player_name,0,start_hand))

#First player, first action
current_player = PLAYERS[id_player]
current_action = ACTIONS[0] #select a letter

hand_at_turns_begining = current_player.hand
board_state_at_turns_begining = board_state

#___MAIN  GAME LOOP___

while running:

    for event in pygame.event.get():

        #UNCOMMON EVENTS
        if event.type == KEYDOWN and event.key == K_ESCAPE : #keyboard -> ESCAPE
            running = False #exit the game

        elif (event.type == pygame.QUIT) : #close the game window
            running = False #exit the game        

        elif (event.type == VIDEORESIZE) : #properly refresh the game window if a resize is detected
            window = refreshWindow(window, event.dict['size'][0], event.dict['size'][1])
            #load again all images to gain quality in case of a zoom in after a zoom out
            letters = reloadLetters()
            tiles = reloadTiles()
            board = reloardBoard() 
            menu = reloadMenu() 

            #UPDATE VALUE OF VARIABLES
            zoom_factor = updateZoomFactor(event.dict['size'][0], event.dict['size'][1])
            tile_size = updateTileSize()
            delta = updateDelta()
            board_size = updateBoardSize()
            menu_width = updateMenuWidth()
            menu_heigh = updateMenuHeigh()

            #RESIZE ASSETS            
            board = pygame.transform.smoothscale( board, (board_size, board_size) )
            menu = pygame.transform.smoothscale( menu, (menu_width, menu_heigh) )

            for key in letters.keys() :
                letters[key] = pygame.transform.smoothscale(letters[key], (tile_size, tile_size) )

            for key in tiles.keys() :
                tiles[key] = pygame.transform.smoothscale(tiles[key], (tile_size, tile_size) )

            font = pygame.font.Font("./images/defaultFont.ttf", tile_size)

            drawBoardAndMenu() #draw everything on screen
            drawTurnInfo(current_player)
            drawHand(current_player.hand)
            pygame.display.flip()

        #COMMON EVENTS
        if event.type == KEYDOWN and event.key == K_SPACE : #NEXT PLAYER

            current_player.points= current_player.points + calculatePoints(letters_just_played) #scoring

            tile_x_hand = 0
            selected_letter = ''
            letter_from_board = False
            letters_just_played = {}

            #NEXT PLAYER
            id_player = (id_player + 1) % len(PLAYERS)
            current_player = PLAYERS[id_player]
            #print('Current player :')
            PLAYERS[id_player].printInstanceVariables()

            current_action = ACTIONS[0] #select a letter
            #print('Current action : ', current_action)

            hand_at_turns_begining = current_player.hand
            board_state_at_turns_begining = board_state

            while len(current_player.hand) < LETTERS_PER_HAND and len(BAG_OF_LETTERS) > 1 :
                random_int = randint(0,len(bag_of_letters)-1)
                current_player.hand.append(bag_of_letters[random_int])
                del(bag_of_letters[random_int])

            #print('remaining tiles in bag : ', len(BAG_OF_LETTERS))

            drawBoardAndMenu() #draw everything on screen
            drawTurnInfo(current_player)
            drawHand(current_player.hand)
            pygame.display.flip()

        elif ( event.type == MOUSEBUTTONDOWN and event.button == 1 ) : #left clic

            cursor_x = event.pos[0]
            cursor_y = event.pos[1]

            if current_action == 'SELECT_A_LETTER' :

                if cursorIsOnBoard(cursor_x, cursor_y) :
                    #print('tile is on board')

                    tile_x_board = floor( (cursor_x - delta)/tile_size)
                    tile_y_board = floor( (cursor_y - delta)/tile_size)

                    selected_letter = board_state[tile_x_board][tile_y_board]
                    #check if the letter has just been played by this player or not
                    if ( selected_letter in(letters_just_played.values()) and ( (tile_x_board, tile_y_board) in( letters_just_played.keys() ) ) ) :

                        letter_from_board = True
                        del(letters_just_played[(tile_x_board, tile_y_board)])
                        #print('selected_letter is : ', selected_letter)
                        board_state[tile_x_board][tile_y_board] = '?'

                        #NEXT ACION
                        current_action = ACTIONS[1] #play a letter
                        #print('Current action : ', current_action)

                    else :
                        selected_letter = ''

                else : #not on board
                    #print('tile is NOT on board')

                    if cursorIsOnHand(cursor_x, cursor_y, current_player.hand) :
                        #print('Tile is in hand')

                        delta_hand_x = 2*delta + TILE_PER_BOARD_COLUMN*tile_size + 2*tile_size
                        tile_x_hand = floor( (cursor_x - delta_hand_x)/tile_size)

                        selected_letter = current_player.hand[tile_x_hand]
                        letter_from_board = False
                        #print('selected_letter is : ', selected_letter)

                        #NEXT ACION
                        current_action = ACTIONS[1] #play a letter
                        #print('Current action : ', current_action)


            elif current_action == 'PLAY_A_LETTER' :

                if cursorIsOnBoard(cursor_x, cursor_y) :

                    tile_x_board = floor( (cursor_x - delta)/tile_size)
                    tile_y_board = floor( (cursor_y - delta)/tile_size)

                    if emptySlot(tile_x_board,tile_y_board) : 

                        board_state[tile_x_board][tile_y_board] = selected_letter

                        if letter_from_board == False :
                            del(current_player.hand[tile_x_hand])

                        drawBoardAndMenu()
                        window.blit( letters[selected_letter], (delta + tile_x_board*tile_size, delta + tile_y_board*tile_size) ) #TEMP?
                        drawTurnInfo(current_player)
                        drawHand(current_player.hand)
                        pygame.display.flip()

                        letters_just_played[(tile_x_board, tile_y_board)] = selected_letter
                        selected_letter = ''

                        #print(board_state)
                        #NEXT ACION
                        current_action = ACTIONS[0]
                        #print('Current action : ', current_action)




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

elif (event.type == MOUSEBUTTONDOWN and event.button == 1) :


#print on screen :
font = pygame.font.Font("./images/Futura-BoldRegular.ttf", 60)
test_letter = font.render('A',1,(0,0,0))
window.blit(test_letter,(1.5*tile_size, 1.5*tile_size))
pygame.display.flip()


#print('points for this slot : ', LAYOUT[tile_x][tile_y]) #TEMP
#print('score for this move : ', POINTS['B'] * LAYOUT[tile_x][tile_y]) #TEMP
"""
