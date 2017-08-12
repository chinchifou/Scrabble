#___IMPORTS___
import pygame
from pygame.locals import *

import display_settings as settings
from display_settings import *

import game_rules as rules
from game_rules import *

from math import floor

from random import randint
import random

import os

#___GUI INITIALISATION___
#Font
gui_title_line_heigh = 0.0
gui_line_heigh = 0.0

#TURN INFO
gui_turn_info_x = 0.0
gui_turn_info_y = 0.0

#HAND HOLDER
gui_hand_holder_x = 0.0
gui_hand_holder_y = 0.0

#PLAYER HAND
gui_hand_x = 0.0
gui_hand_y = 0.0

#NEXT PLAYER HAND
gui_next_hand_x = 0.0
gui_next_hand_y = 0.0

#SCORES
gui_score_x = 0.0
gui_score_y = 0.0

#PREVIOUS TURN SUMMARY
gui_turn_summary_x = 0.0
gui_turn_summary_y = 0.0


#___INITIALIZATION___
#launch Pygame
pygame.init()
pygame.mixer.init()
print('PyGame initialization OK')

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

HAND_HOLDER_WIDTH_IN_TILES = LETTERS_PER_HAND + 0.2
HAND_HOLDER_HEIGH_IN_TILES = 1.2

ACTIONS = ('SELECT_A_LETTER', 'PLAY_A_LETTER')

PLAYERS = []
NO_LETTER = '_'

DISPLAY_NEXT_PLAYER_HAND = rules.DISPLAY_NEXT_PLAYER_HAND

color_light_grey = (143,144,138)
color_red = (243,112,118)

#CHANGING WITH WINDOW RESIZING
zoom_factor = float(settings.WIDTH / 1920.0) #reference resolution is 1920*1080
window =  pygame.display.set_mode( (0, 0) )
background = window.copy()

tile_size = round(TILE_SIZE * zoom_factor)
delta = 1.5 * tile_size #distance of board from top left corner

board_size = round(BOARD_SIZE_IN_TILES * tile_size)
menu_width = round(MENU_WIDTH_IN_TILES * tile_size)
menu_heigh = round(MENU_HEIGH_IN_TILES * tile_size)

hand_holder_width = round(HAND_HOLDER_WIDTH_IN_TILES * tile_size)
hand_holder_heigh = round(HAND_HOLDER_HEIGH_IN_TILES * tile_size)


#CHANGING DURING THE GAME
bag_of_letters = BAG_OF_LETTERS

board_state = [ ['?' for i in range(TILE_PER_BOARD_COLUMN)] for j in range(TILE_PER_BOARD_COLUMN) ]

id_player = 0

tile_x_hand = 0
selected_letter = ''
letter_from_board = False
letters_just_played = {} #format {'a' : (x, y)}

last_words_and_scores = []

clock = pygame.time.Clock()
timer = clock.tick()
delta_clic = [0.5, 0.5]

#TODO : BACKUP TO ALLOW RESET
board_state_at_turns_begining = board_state 
hand_at_turns_begining = []

#___IMAGES LOADING___
print ('    Loading images...')

#TILES
path_for_tiles = os.path.abspath('../assets/images/tiles/')
tiles = {
    'start' : pygame.image.load(os.path.join(path_for_tiles,'start.png')),
    'empty' : pygame.image.load(os.path.join(path_for_tiles,'empty.png')),
    'double_letter' : pygame.image.load(os.path.join(path_for_tiles,'double_letter.png')),
    'triple_letter' : pygame.image.load(os.path.join(path_for_tiles,'triple_letter.png')),
    'double_word' : pygame.image.load(os.path.join(path_for_tiles,'double_word.png')),
    'triple_word' : pygame.image.load(os.path.join(path_for_tiles,'triple_word.png'))
}

#LETTERS
path_for_letters = os.path.abspath('../assets/images/letters/')
path_for_letters = os.path.join(path_for_letters, LANGUAGE)
letters = {
'*' : pygame.image.load(os.path.join(path_for_letters,'joker.png')),
'A' : pygame.image.load(os.path.join(path_for_letters,'A.png')),
'B' : pygame.image.load(os.path.join(path_for_letters,'B.png')),
'C' : pygame.image.load(os.path.join(path_for_letters,'C.png')),
'D' : pygame.image.load(os.path.join(path_for_letters,'D.png')),
'E' : pygame.image.load(os.path.join(path_for_letters,'E.png')),
'F' : pygame.image.load(os.path.join(path_for_letters,'F.png')),
'G' : pygame.image.load(os.path.join(path_for_letters,'G.png')),
'H' : pygame.image.load(os.path.join(path_for_letters,'H.png')),
'I' : pygame.image.load(os.path.join(path_for_letters,'I.png')),
'J' : pygame.image.load(os.path.join(path_for_letters,'J.png')),
'K' : pygame.image.load(os.path.join(path_for_letters,'K.png')),
'L' : pygame.image.load(os.path.join(path_for_letters,'L.png')),
'M' : pygame.image.load(os.path.join(path_for_letters,'M.png')),
'N' : pygame.image.load(os.path.join(path_for_letters,'N.png')),
'O' : pygame.image.load(os.path.join(path_for_letters,'O.png')),
'P' : pygame.image.load(os.path.join(path_for_letters,'P.png')),
'Q' : pygame.image.load(os.path.join(path_for_letters,'Q.png')),
'R' : pygame.image.load(os.path.join(path_for_letters,'R.png')),
'S' : pygame.image.load(os.path.join(path_for_letters,'S.png')),
'T' : pygame.image.load(os.path.join(path_for_letters,'T.png')),
'U' : pygame.image.load(os.path.join(path_for_letters,'U.png')),
'V' : pygame.image.load(os.path.join(path_for_letters,'V.png')),
'W' : pygame.image.load(os.path.join(path_for_letters,'W.png')),
'X' : pygame.image.load(os.path.join(path_for_letters,'X.png')),
'Y' : pygame.image.load(os.path.join(path_for_letters,'Y.png')),
'Z' : pygame.image.load(os.path.join(path_for_letters,'Z.png'))
}

#BACKGROUND IMAGES
path_for_back_images = os.path.abspath('../assets/images/background/')
board = pygame.image.load(os.path.join(path_for_back_images, 'board.png'))
menu = pygame.image.load(os.path.join(path_for_back_images, 'menu.png'))
hand_holder = pygame.image.load(os.path.join(path_for_back_images, 'hand_holder.png'))

#BUTTONS
#path_for_buttons = './images/buttons/'
#button_end_turn = path_for_buttons+'end_turn.png'

print('    Images loaded')

#___CLASSES___
class Player :

    def __init__(self, name, points, hand) :
        self.name = name
        self.points = points
        self.hand = hand

    def printInstanceVariables(self) :
        padding = '    '
        print()
        print(padding+'name : ', self.name)
        print(padding+'points : ', self.points)
        print(padding+'hand : ', self.hand)


#___FUNCTIONS___

#LOGICAL FUNCTIONS
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


def cursorIsOnBoard(cursor_x, cursor_y) :
    tile_x = floor( (cursor_x - delta)/tile_size)
    tile_y = floor( (cursor_y - delta)/tile_size)
    if ( tile_x in range (0, TILE_PER_BOARD_COLUMN ) ) and ( tile_y in range (0, TILE_PER_BOARD_COLUMN ) ) :
        return True
    else :
        return False
def cursorIsOnHand(cursor_x, cursor_y, hand) : #TO DEBUG ?? use collidepoint
    delta_hand_x = 1*delta + TILE_PER_BOARD_COLUMN*tile_size + 1*delta + 1*tile_size
    delta_hand_y = delta + 2*tile_size

    tile_x = floor( (cursor_x - delta_hand_x)/tile_size)
    tile_y = floor( (cursor_y - delta_hand_y)/tile_size)

    if ( tile_x in range (0, len(hand)) ) and ( tile_y in range (0, 1) ) :
        return True
    else :
        return False


def emptySlot(x,y) :
    if board_state[x][y] == '?':
        return True
    else :
        return False


def calculatePoints(letters_played) :
    #FORMAT letters_just_played {'a' : (x, y)}
    print ('len letters played', len(letters_played))

    if len(letters_played) == 0 :
        print( '  NOTHING PLAYED')
        return []

    else :
        #__init__
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
        #__init__

        words_and_scores = []

        if len(letters_played) == 7 : #is a SCRABBLE ?
            words_and_scores.append(['!! SCRABBLE !!', 50])
            
        if delta_x == 0 :
            print('  HORIZONTAL WORD')
  
            #find first letter
            start_y = min_y
            while( ( (start_y - 1) >= 0) and (board_state[min_x][start_y - 1] != '?') ) :
                start_y = start_y - 1

            #find last letter
            end_y = max_y
            while( ( (end_y + 1) <= TILE_PER_BOARD_COLUMN-1) and (board_state[min_x][end_y + 1] != '?') ) :
                end_y = end_y + 1

            #words_and_scores = []

            if ( end_y > start_y ) : #prevent one letter word
                #FIRST PASSAGE
                #store word just created
                new_word = ''
                new_word_multiplier = 1
                new_word_score = 0

                for it_y in range( start_y, end_y+1 ) :
                    letter = board_state[min_x][it_y]
                    new_word += letter
                    if ((min_x, it_y) in letters_played ): #letters just played
                        #calculate points for each letter
                        bonus = LAYOUT[min_x][it_y]
                        if bonus == 0 : #start_tile
                            new_word_multiplier *= 2
                            bonus = 1
                        elif bonus == 4:
                            new_word_multiplier *= 2
                            bonus = 1
                        elif bonus == 5:
                            new_word_multiplier *= 3
                            bonus = 1

                        new_letter_points = POINTS[letter]
                        new_word_score = new_word_score + (bonus * new_letter_points)

                    else : #old letters
                        old_letter_points = POINTS[letter]
                        new_word_score = new_word_score + old_letter_points
                        
                new_word_score = new_word_score * new_word_multiplier
                words_and_scores.append([new_word, new_word_score])


            #SECOND PASSAGE
            for it_y in range( start_y, end_y+1 ) :
                #check for horizontal words
                it_x = min_x
                if (it_x, it_y) in (letters_played) : #prevent to count already existing words

                    condition_1 = ( (it_x - 1) >= 0 ) and ( board_state[it_x-1][it_y] != '?' )
                    condition_2 = ( (it_x + 1) <= TILE_PER_BOARD_COLUMN-1 ) and ( board_state[it_x+1][it_y] != '?' )  
                    if ( condition_1  or condition_2 ) :
                        #print('there is another word')
                        old_word = ''
                        old_word_score = 0

                        while( ( (it_x - 1) >= 0) and (board_state[it_x-1][it_y] != '?') ) : #go to the begining of the word
                            it_x = it_x - 1

                        while( ( (it_x) <= TILE_PER_BOARD_COLUMN-1) and (board_state[it_x][it_y] != '?') ) : #go to the end of the word

                            old_letter = board_state[it_x][it_y]
                            old_word += old_letter

                            old_word_multiplier = 1

                            if (it_x, it_y) in (letters_played) :

                                bonus = LAYOUT[it_x][it_y]

                                if bonus == 0 : #start_tile
                                    old_word_multiplier *= 2
                                    bonus = 1
                                elif bonus == 4:
                                    old_word_multiplier *= 2
                                    bonus = 1
                                elif bonus == 5:
                                    old_word_multiplier *= 3
                                    bonus = 1

                                old_word_score += POINTS[old_letter] * bonus

                            else :
                                old_word_score += POINTS[old_letter]
                            
                            it_x = it_x + 1

                        old_word_score = old_word_score * old_word_multiplier
                        words_and_scores.append([old_word, old_word_score])

            total_score = 0 

            for association in words_and_scores :
                print('Word "', association[0], '" gives ', association[1], ' points' )
                total_score += association[1]
            
            print ('total_score : ', total_score)

            return words_and_scores 


        else : 
            print('  HORIZONTAL WORD')

            #find first letter
            start_x = min_x
            while( ( (start_x - 1) >= 0) and (board_state[start_x - 1][min_y] != '?') ) :
                start_x = start_x - 1

            #find last letter
            end_x = max_x
            while( ( (end_x + 1) <= TILE_PER_BOARD_COLUMN-1) and (board_state[end_x + 1][min_y] != '?') ) :
                end_x = end_x + 1

            if ( end_x > start_x ) : #prevent one letter word
                #FIRST PASSAGE
                #store word just created  
                new_word = ''
                new_word_multiplier = 1
                new_word_score = 0

                for it_x in range( start_x, end_x+1 ) :
                    letter = board_state[it_x][min_y]
                    new_word += letter
                    if ((it_x, min_y) in letters_played ): #letters just played
                        #calculate points for each letter
                        bonus = LAYOUT[it_x][min_y]
                        if bonus == 0 : #start_tile
                            new_word_multiplier *= 2
                            bonus = 1
                        elif bonus == 4:
                            new_word_multiplier *= 2
                            bonus = 1
                        elif bonus == 5:
                            new_word_multiplier *= 3
                            bonus = 1

                        new_letter_points = POINTS[letter]
                        new_word_score = new_word_score + (bonus * new_letter_points)

                    else : #old letters
                        old_letter_points = POINTS[letter]
                        new_word_score = new_word_score + old_letter_points
                        
                new_word_score = new_word_score * new_word_multiplier
                words_and_scores.append([new_word, new_word_score])


            #SECOND PASSAGE
            for it_x in range( start_x, end_x+1 ) :
                #check for horizontal words
                it_y = min_y
                if (it_x, it_y) in (letters_played) : #prevent to count already existing words

                    condition_1 = ( (it_y - 1) >= 0 ) and ( board_state[it_x][it_y-1] != '?' )
                    condition_2 = ( (it_y + 1) <= TILE_PER_BOARD_COLUMN-1 ) and ( board_state[it_x][it_y+1] != '?' )  
                    if ( condition_1  or condition_2 ) :
                        #print('there is another word')
                        old_word = ''
                        old_word_score = 0

                        while( ( (it_y - 1) >= 0) and (board_state[it_x][it_y-1] != '?') ) : #go to the begining of the word
                            it_y = it_y - 1

                        while( ( (it_y) <= TILE_PER_BOARD_COLUMN-1) and (board_state[it_x][it_y] != '?') ) : #go to the end of the word

                            old_letter = board_state[it_x][it_y]
                            old_word += old_letter

                            old_word_multiplier = 1

                            if (it_x, it_y) in (letters_played) :

                                bonus = LAYOUT[it_x][it_y]

                                if bonus == 0 : #start_tile
                                    old_word_multiplier *= 2
                                    bonus = 1
                                elif bonus == 4:
                                    old_word_multiplier *= 2
                                    bonus = 1
                                elif bonus == 5:
                                    old_word_multiplier *= 3
                                    bonus = 1

                                old_word_score += POINTS[old_letter] * bonus

                            else :
                                old_word_score += POINTS[old_letter]
                            
                            it_y = it_y + 1

                        old_word_score = old_word_score * old_word_multiplier
                        words_and_scores.append([old_word, old_word_score])

            total_score = 0 #TEMP

            for association in words_and_scores :
                print('Word "', association[0], '" gives ', association[1], ' points' )
                total_score += association[1]
            
            print ('total_score : ', total_score)

            return words_and_scores


#DRAW FUNCTIONS
#Draw playing board
def drawBoard() :
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

    #TODO : split to improve perf
    #letters on board
    for row in range(0,TILE_PER_BOARD_COLUMN) :
        for column in range(0, TILE_PER_BOARD_COLUMN) :
            if board_state[row][column] != '?' :
                window.blit( letters[ board_state[row][column] ], (delta + row * tile_size, delta + column * tile_size) )


#Display on top of the screen the player who is currently playing
def drawTurnInfo(player) :
    #TO DO general font
    font = pygame.font.SysFont("Calibri", floor(gui_title_line_heigh))
    font.set_bold(1)
    test_text = font.render(player.name+"'s turn",1,color_light_grey)
    window.blit(test_text,(gui_turn_info_x, gui_turn_info_y))


def drawHandHolder():
    window.blit(hand_holder, (gui_hand_holder_x, gui_hand_holder_y))


def drawHand(hand) :
    for id_letter in range(len(hand)) :
        if hand[id_letter] != NO_LETTER :
            window.blit(letters[hand[id_letter]], (gui_hand_x + id_letter*tile_size , gui_hand_y)) 


def drawScores() :
    if(len(PLAYERS) <= 8) :

        delta_y = gui_score_y
       
        #TODO : general font for title
        font = pygame.font.SysFont("Calibri", floor(1.1*gui_line_heigh))
        font.set_bold(1) 
        header = font.render('Scores :',1,color_light_grey)

        font = pygame.font.SysFont("Calibri", floor(0.9*gui_line_heigh))
        font.set_bold(0)
        window.blit(header, (gui_score_x, delta_y) )
        delta_y += 2*gui_line_heigh

        for player in PLAYERS :
            if player == current_player :
                font.set_bold(1)
                player_score_text = font.render('   '+player.name+" : "+str(player.points),1,color_light_grey)
            else :
                font.set_bold(0)
                player_score_text = font.render('    '+player.name+" : "+str(player.points),1,color_light_grey)
            window.blit(player_score_text, (gui_score_x, delta_y) )
            delta_y += gui_line_heigh


def drawSumarryEndTurn(words_and_scores) :
    delta_y = gui_turn_summary_y

    id_previous_player = (id_player + len(PLAYERS) - 1) % len(PLAYERS)
    previous_player_name = PLAYERS[id_previous_player].name

    if len(words_and_scores) > 0 :

        font = pygame.font.SysFont("Calibri", floor(1*gui_line_heigh))
        font.set_bold(1)
        header = font.render('Last turn '+previous_player_name+' played :' ,1 ,color_light_grey )
        window.blit(header, (gui_turn_summary_x, delta_y) )
        delta_y += gui_line_heigh

        font = pygame.font.SysFont("Calibri", floor(0.9*gui_line_heigh))        
        font.set_bold(0)

        for association in words_and_scores :
            if association[0] == '!! SCRABBLE !!':
                delta_y += gui_line_heigh
                text = font.render('    !! SCRABBLE gives 50 points !!',1,(243,112,118))
                window.blit(text, (gui_turn_summary_x, delta_y) )

            else:
                delta_y += gui_line_heigh
                text = font.render('    Word '+"'"+association[0]+"'"+' for '+str(association[1])+' points',1,color_light_grey)
                window.blit(text, (gui_turn_summary_x, delta_y) )

    else :

        font = pygame.font.SysFont("Calibri", floor(0.9*gui_line_heigh))
        font.set_bold(0)
        text = font.render('Nothing played by '+previous_player_name+' last turn',1,color_light_grey)
        window.blit(text, (gui_turn_summary_x, delta_y) )

    delta_y += 2*gui_line_heigh
    text = font.render('Remaining tiles in bag : '+str(len(BAG_OF_LETTERS)), 1 ,color_light_grey )
    window.blit(text, (gui_turn_summary_x, delta_y))


def drawNextPayerHand(next_player) :
    if DISPLAY_NEXT_PLAYER_HAND :

        delta_y = gui_next_hand_y

        font = pygame.font.SysFont("Calibri", floor(1.1*gui_line_heigh))
        font.set_bold(1) 
        header = font.render(next_player.name+ "'s hand :",1,color_light_grey)
        window.blit(header, (gui_next_hand_x, delta_y) )

        delta_y += 2*gui_line_heigh
        font.set_bold(0) 

        next_player_letters = "    "
        for letter in next_player.hand :
            next_player_letters += letter + " "
            
        text = font.render(next_player_letters, 1, color_light_grey)
        window.blit(text, (gui_next_hand_x, delta_y) )


def drawMenu(player) :
    window.blit(menu, (board_size, 0))
    drawHandHolder()
    drawHand(player.hand)                                
    drawNextPayerHand(PLAYERS[(id_player + 1) % len(PLAYERS)])        
    drawTurnInfo(player)
    drawScores()
    drawSumarryEndTurn(last_words_and_scores)


#RELOAD IMAGES
def reloadTiles() :
    return {
    'start' : pygame.image.load(os.path.join(path_for_tiles,'start.png')),
    'empty' : pygame.image.load(os.path.join(path_for_tiles,'empty.png')),
    'double_letter' : pygame.image.load(os.path.join(path_for_tiles,'double_letter.png')),
    'triple_letter' : pygame.image.load(os.path.join(path_for_tiles,'triple_letter.png')),
    'double_word' : pygame.image.load(os.path.join(path_for_tiles,'double_word.png')),
    'triple_word' : pygame.image.load(os.path.join(path_for_tiles,'triple_word.png'))
}

def reloadLetters() :
    return {
    '*' : pygame.image.load(os.path.join(path_for_letters,'joker.png')),
    'A' : pygame.image.load(os.path.join(path_for_letters,'A.png')),
    'B' : pygame.image.load(os.path.join(path_for_letters,'B.png')),
    'C' : pygame.image.load(os.path.join(path_for_letters,'C.png')),
    'D' : pygame.image.load(os.path.join(path_for_letters,'D.png')),
    'E' : pygame.image.load(os.path.join(path_for_letters,'E.png')),
    'F' : pygame.image.load(os.path.join(path_for_letters,'F.png')),
    'G' : pygame.image.load(os.path.join(path_for_letters,'G.png')),
    'H' : pygame.image.load(os.path.join(path_for_letters,'H.png')),
    'I' : pygame.image.load(os.path.join(path_for_letters,'I.png')),
    'J' : pygame.image.load(os.path.join(path_for_letters,'J.png')),
    'K' : pygame.image.load(os.path.join(path_for_letters,'K.png')),
    'L' : pygame.image.load(os.path.join(path_for_letters,'L.png')),
    'M' : pygame.image.load(os.path.join(path_for_letters,'M.png')),
    'N' : pygame.image.load(os.path.join(path_for_letters,'N.png')),
    'O' : pygame.image.load(os.path.join(path_for_letters,'O.png')),
    'P' : pygame.image.load(os.path.join(path_for_letters,'P.png')),
    'Q' : pygame.image.load(os.path.join(path_for_letters,'Q.png')),
    'R' : pygame.image.load(os.path.join(path_for_letters,'R.png')),
    'S' : pygame.image.load(os.path.join(path_for_letters,'S.png')),
    'T' : pygame.image.load(os.path.join(path_for_letters,'T.png')),
    'U' : pygame.image.load(os.path.join(path_for_letters,'U.png')),
    'V' : pygame.image.load(os.path.join(path_for_letters,'V.png')),
    'W' : pygame.image.load(os.path.join(path_for_letters,'W.png')),
    'X' : pygame.image.load(os.path.join(path_for_letters,'X.png')),
    'Y' : pygame.image.load(os.path.join(path_for_letters,'Y.png')),
    'Z' : pygame.image.load(os.path.join(path_for_letters,'Z.png'))
    }

def reloadBoard() :
    return pygame.image.load(os.path.join(path_for_back_images, 'board.png')) 

def reloadHandHolder() :
    return pygame.image.load(os.path.join(path_for_back_images, 'hand_holder.png'))

def reloadMenu() :
    return pygame.image.load(os.path.join(path_for_back_images, 'menu.png'))



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
def updateHandHolderWidth() :
    return round(HAND_HOLDER_WIDTH_IN_TILES * tile_size)
def updateHandHolderHeigh() :
    return round(HAND_HOLDER_HEIGH_IN_TILES * tile_size)


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



running = True
print ('Game is running')

#___MAIN  GAME LOOP___

while running:

    for event in pygame.event.get():

        event_type = event.type

        #~~~~~~~~~~~ QUIT ~~~~~~~~~~~
        if ( event_type == pygame.QUIT ) : #close the game window
            running = False #exit the game        

        #~~~~~~~~~~~ WINDOW RESIZE ~~~~~~~~~~~
        elif ( event_type == VIDEORESIZE ) : #properly refresh the game window if a resize is detected
            window = refreshWindow(window, event.dict['size'][0], event.dict['size'][1])
            #load again all images to gain quality in case of a zoom in after a zoom out
            letters = reloadLetters()
            tiles = reloadTiles()
            board = reloadBoard() 
            menu = reloadMenu()
            hand_holder = reloadHandHolder() 

            #--------- RESIZE ASSETS ---------

            #update values
            zoom_factor = updateZoomFactor(event.dict['size'][0], event.dict['size'][1])
            tile_size = updateTileSize()
            delta = updateDelta()
            board_size = updateBoardSize()
            menu_width = updateMenuWidth()
            menu_heigh = updateMenuHeigh()
            hand_holder_width = updateHandHolderWidth()
            hand_holder_heigh = updateHandHolderHeigh()

            #resize based on new values            
            board = pygame.transform.smoothscale( board, (board_size, board_size) )
            menu = pygame.transform.smoothscale( menu, (menu_width, menu_heigh) )
            hand_holder = pygame.transform.smoothscale( hand_holder, (hand_holder_width, hand_holder_heigh) )

            for key in letters.keys() :
                letters[key] = pygame.transform.smoothscale(letters[key], (tile_size, tile_size) )
            for key in tiles.keys() :
                tiles[key] = pygame.transform.smoothscale(tiles[key], (tile_size, tile_size) )

            #--------- PLACE ASSETS ON THE SCREEN ---------
            #Font TODO to improve
            gui_title_line_heigh = 0.9*tile_size
            gui_line_heigh = 0.6*tile_size

            #turn info
            gui_turn_info_x = 1*delta + TILE_PER_BOARD_COLUMN*tile_size + 1*delta + 1*tile_size
            gui_turn_info_y = 1.3*delta

            #player hand
            gui_hand_x = 1*delta + TILE_PER_BOARD_COLUMN*tile_size + 1*delta + 1*tile_size
            gui_hand_y = delta + 2*tile_size

            #hand holder
            gui_hand_holder_x = gui_hand_x - 0.1*tile_size
            gui_hand_holder_y = gui_hand_y - 0.1*tile_size

            #next player hand
            gui_next_hand_x = 1*delta + TILE_PER_BOARD_COLUMN*tile_size + 1*delta + 1*tile_size
            gui_next_hand_y = delta + 4*tile_size

            #scores
            gui_score_x = 1*delta + TILE_PER_BOARD_COLUMN*tile_size + 1*delta + 1*tile_size
            gui_score_y = delta + 4*tile_size + 1*tile_size + 2*tile_size*int(DISPLAY_NEXT_PLAYER_HAND)

            #previous turn summary
            gui_turn_summary_x = 1*delta + TILE_PER_BOARD_COLUMN*tile_size + 1*delta + 1*tile_size
            gui_turn_summary_y = delta + 5*tile_size + 2*gui_line_heigh + (len(PLAYERS)*gui_line_heigh) + tile_size + 2*tile_size*int(DISPLAY_NEXT_PLAYER_HAND)


            drawBoard()
            drawMenu(current_player)
            background = window.copy() #save background

            pygame.display.flip()

        #~~~~~~~~~~~ KEYBOARD KEY DOWN ~~~~~~~~~~~
        elif ( event_type == KEYDOWN ) :
            key_pressed = event.key

            #------ SECURITY -------
            if ( current_action == "SELECT_A_LETTER" ) :

                #------ QUIT -------
                if ( key_pressed == K_ESCAPE ) :
                    running = False #exit the game

                #------ VICTORY -------
                elif ( key_pressed == K_BACKSPACE ) :
                    pygame.mixer.music.load('./music/victory-fanfare.mp3')
                    pygame.mixer.music.play()


                    mask = pygame.Surface((settings.WIDTH, settings.HEIGH))
                    mask.fill((0,0,0))
                    mask.set_alpha(210)

                    window.blit(mask,(0,0))
                    pygame.display.flip()
                    #pygame.time.delay(100)

                    template =[
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1,0,0,0,0,1,0,0],
                    [0,0,0,1,1,0,0,0,1,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0],
                    [0,0,0,0,1,1,0,1,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0],
                    [0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0],
                    [0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0],
                    [0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0],
                    [0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,1,1,0,0,0,1,0,0],
                    [0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,0,1,1,1,0,0,1,0,0],
                    [0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1,0,0,1,0,0],
                    [0,0,1,1,0,0,1,0,0,1,1,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1,1,0,1,0,0],
                    [0,0,0,1,0,1,1,1,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,1,1,1,0,0],
                    [0,0,0,1,1,1,0,1,1,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,1,1,0,0],
                    [0,0,0,0,1,1,0,1,1,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,1,0,0,0,0,1,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                    ]

                    available =[
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
                    ]

                    cpt = 0

                    temp_it_x = randint(0,31)
                    temp_it_y = randint(0,17)

                    while (cpt < 576) :

                        while (available[temp_it_y][temp_it_x] == 0) :
                            temp_it_x = randint(0,31)
                            temp_it_y = randint(0,17)

                        it_x = temp_it_x
                        it_y = temp_it_y


                        available[it_y][it_x] = 0

                        if (template[it_y][it_x] == 0) :
                            window.blit( (random.choice(list(letters.values()))) ,(it_x*tile_size, it_y*tile_size))
                            pygame.display.flip()
                            pygame.time.delay(6)

                        cpt +=1
            
                #------ NEXT PLAYER -------
                elif( key_pressed == K_SPACE ) :
                    last_words_and_scores = calculatePoints(letters_just_played)

                    for association in last_words_and_scores :
                        current_player.points +=  association[1]

                    tile_x_hand = 0
                    selected_letter = ''
                    letter_from_board = False
                    letters_just_played = {}

                    #clean hand from empty spot
                    id_letter = 0
                    while id_letter < len(current_player.hand) :
                        if current_player.hand[id_letter] == NO_LETTER :
                            del( current_player.hand[id_letter] )
                        else :
                            id_letter += 1

                    while len(current_player.hand) < LETTERS_PER_HAND and len(BAG_OF_LETTERS) > 0 :
                        random_int = randint(0,len(bag_of_letters)-1)
                        current_player.hand.append(bag_of_letters[random_int])
                        del(bag_of_letters[random_int])

                    #NEXT PLAYER
                    id_player = (id_player + 1) % len(PLAYERS)
                    current_player = PLAYERS[id_player]
                    PLAYERS[id_player].printInstanceVariables()
                    current_action = ACTIONS[0] #select a letter

                    hand_at_turns_begining = current_player.hand
                    board_state_at_turns_begining = board_state

                    drawBoard()
                    drawMenu(current_player)
                    background = window.copy()
                    pygame.display.flip()

        #~~~~~~~~~~~ MOUSE BUTTONS ~~~~~~~~~~~
        elif ( ( (event_type == MOUSEBUTTONDOWN) or (event_type == MOUSEBUTTONUP) ) and event.button == 1 ) :
            
            timer = clock.tick()            
            #~~~~~~~~~~~ PRESS LEFT CLIC ~~~~~~~~~~~
            if ( event_type == MOUSEBUTTONDOWN ) :
                
                cursor_x = event.pos[0]
                cursor_y = event.pos[1]

                #------ SELECT A LETTER -------
                if current_action == 'SELECT_A_LETTER' :

                    if cursorIsOnBoard(cursor_x, cursor_y) :

                        tile_x_board = floor( (cursor_x - delta)/tile_size)
                        tile_y_board = floor( (cursor_y - delta)/tile_size)

                        delta_clic[0] = ( (cursor_x - delta)/tile_size) - tile_x_board
                        delta_clic[1] = ( (cursor_y - delta)/tile_size) - tile_y_board

                        #letter just played ?
                        if ( (tile_x_board, tile_y_board) in letters_just_played.keys() ) :

                            selected_letter = board_state[tile_x_board][tile_y_board]
                            #letter_from_board ???
                            letter_from_board = True
                            del(letters_just_played[(tile_x_board, tile_y_board)])
                            board_state[tile_x_board][tile_y_board] = '?'
                            current_action = ACTIONS[1] #next action : play a letter

                            drawBoard()
                            background = window.copy() #save background

                    elif cursorIsOnHand(cursor_x, cursor_y, current_player.hand) :

                        delta_hand_x = 1*delta + TILE_PER_BOARD_COLUMN*tile_size + 1*delta + 1*tile_size
                        delta_hand_y = delta + 2*tile_size

                        tile_x_hand = floor( (cursor_x - delta_hand_x)/tile_size)
                        tile_y_hand = floor( (cursor_y - delta_hand_y)/tile_size)

                        delta_clic[0] = ( (cursor_x - delta_hand_x)/tile_size) - tile_x_hand
                        delta_clic[1] = ( (cursor_y - delta_hand_y)/tile_size) - tile_y_hand

                        if current_player.hand[tile_x_hand] != NO_LETTER :

                            selected_letter = current_player.hand[tile_x_hand]
                            current_player.hand[tile_x_hand] = NO_LETTER
                            letter_from_board = False
                            current_action = ACTIONS[1] #next action : play a letter

                            drawHandHolder()
                            drawHand(current_player.hand)     

                            background = window.copy() #save background

                #------ PLAY A LETTER -------
                elif current_action == 'PLAY_A_LETTER' :

                    if cursorIsOnBoard(cursor_x, cursor_y) :

                        tile_x_board = floor( (cursor_x - delta)/tile_size)
                        tile_y_board = floor( (cursor_y - delta)/tile_size)

                        if emptySlot(tile_x_board,tile_y_board) : 

                            board_state[tile_x_board][tile_y_board] = selected_letter

                            drawBoard()
                            background = window.copy() #save background
                            pygame.display.flip()

                            letters_just_played[(tile_x_board, tile_y_board)] = selected_letter
                            selected_letter = ''
                            current_action = ACTIONS[0]

                    elif cursorIsOnHand(cursor_x, cursor_y, current_player.hand) :

                        delta_hand_x = 1*delta + TILE_PER_BOARD_COLUMN*tile_size + 1*delta + 1*tile_size
                        tile_x_hand = floor( (cursor_x - delta_hand_x)/tile_size)

                        underneath_letter = current_player.hand[tile_x_hand]

                        if underneath_letter == NO_LETTER :

                            current_player.hand[tile_x_hand] = selected_letter

                            drawMenu(current_player)
                            background = window.copy() #save background
                            pygame.display.flip()

                            selected_letter = ''
                            current_action = ACTIONS[0] #next action : select a letter

            #~~~~~~~~~~~ RELEASE LEFT CLIC ~~~~~~~~~~~
            elif ( event_type == MOUSEBUTTONUP ) :

                #timer = clock.tick()
                cursor_x = event.pos[0]
                cursor_y = event.pos[1]

                if current_action == 'PLAY_A_LETTER' :
                    
                    #not a simple fast clic
                    if ( timer > 100 )  : 

                        if cursorIsOnBoard(cursor_x, cursor_y) :

                            tile_x_board = floor( (cursor_x - delta)/tile_size)
                            tile_y_board = floor( (cursor_y - delta)/tile_size)

                            if emptySlot(tile_x_board,tile_y_board) : 

                                board_state[tile_x_board][tile_y_board] = selected_letter

                                drawBoard()    
                                background = window.copy() #save background
                                pygame.display.flip()

                                letters_just_played[(tile_x_board, tile_y_board)] = selected_letter
                                selected_letter = ''                  
                                current_action = ACTIONS[0] #Next action : select a letter

                        elif cursorIsOnHand(cursor_x, cursor_y, current_player.hand) :

                            delta_hand_x = 1*delta + TILE_PER_BOARD_COLUMN*tile_size + 1*delta + 1*tile_size
                            tile_x_hand = floor( (cursor_x - delta_hand_x)/tile_size)

                            underneath_letter = current_player.hand[tile_x_hand]

                            if underneath_letter == NO_LETTER :

                                current_player.hand[tile_x_hand] = selected_letter #ADDED

                                drawHandHolder()
                                drawHand(current_player.hand)
                                background = window.copy() #save background
                                pygame.display.flip()

                                selected_letter = ''
                                current_action = ACTIONS[0] #next action : select a letter

        #~~~~~~~~~~~ MOUSE MOTION ~~~~~~~~~~~
        elif ( event_type == MOUSEMOTION ) :

            #------ PLAY A LETTER -------
            if current_action == 'PLAY_A_LETTER' :  

                mouse_pos = pygame.mouse.get_pos()
                cursor_x = mouse_pos[0]
                cursor_y = mouse_pos[1]

                window.blit(background, (0, 0))
                window.blit( letters[selected_letter], (cursor_x - delta_clic[0]*tile_size, cursor_y - delta_clic[1]*tile_size) )
                pygame.display.flip()  

print('    Shutting down ...')
pygame.quit() #exit if running == false
print('Game is closed')
