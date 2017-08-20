#~~~~~~~ GUI INITIALISATION FILE ~~~~~~~~

#~~~~~~~~ Imports ~~~~~~~~

from os import path
from math import floor
from random import randint, choice

import display_settings
import game_rules
import pygame


#~~~~~~ INITIALIZATION ~~~~~~

#---- Launch Pygame ------
pygame.init()
pygame.mixer.init()

#Add icon
path_for_icon = path.abspath('../assets/images/icon/')
icon_image = pygame.image.load(path.join(path_for_icon,'Scrabble_launcher.ico'))
icon = pygame.transform.scale(icon_image, (32, 32))
pygame.display.set_icon(icon)
pygame.display.set_caption('Scrabble')

print('PyGame initialization OK')

if display_settings.RESOLUTION_AUTO :
    monitor_resolution = pygame.display.Info()
    display_settings.WIDTH = monitor_resolution.current_w
    display_settings.HEIGH = monitor_resolution.current_h
    print('Resolution set to : ', display_settings.WIDTH, ' * ', display_settings.HEIGH)

window =  pygame.display.set_mode( (0, 0) )
background = window.copy()

#~~~~~~~~~ (x, y) positioning ~~~~~~~~~~

pos_params = {
'title_line_heigh' : 0.0,
'line_heigh' : 0.0,
'turn_info' : [0.0, 0.0],
'hand_holder' : [0.0, 0.0],
'hand' : [500.0, 500.0],
'next_hand' : [0.0, 0.0],
'score' : [0.0, 0.0],
'turn_summary' : [0.0, 0.0],
'button_end_turn' : [0.0, 0.0]
}

#~~~~~~~~ Sizes expressed in TILES ~~~~~~~~~~

#Better experience if TILE_SIZE is set to 60 pixels, black stripes otherwise
#TILE_SIZE must divide both 1920 and 1080 / for instance 12; 15; 20; 24; 30; 40; 60 work
TILE_SIZE = 60 

TILE_PER_BOARD_COLUMN = 15 

WIDTH_SCREEN_IN_TILES = 1920 / 60
HEIGH_SCREEN_IN_TILES = 1080 / 60

BOARD_SIZE_IN_TILES = 18

MENU_WIDTH_IN_TILES = WIDTH_SCREEN_IN_TILES - BOARD_SIZE_IN_TILES
MENU_HEIGH_IN_TILES = HEIGH_SCREEN_IN_TILES

HAND_HOLDER_WIDTH_IN_TILES = 7 + 0.2
HAND_HOLDER_HEIGH_IN_TILES = 1.2

BUTTON_END_TURN_WIDTH_IN_TILES = 3
BUTTON_END_TURN_HEIGH_IN_TILES = 1

#~~~~~~~~~ Sizes expressed in pixels ~~~~~~~~~~~~

zoom_factor = 1.0 #default value for the default resolution of 1920*1080

tile_size = 60.0 #default value
delta = 1.5 * tile_size #distance of board from top left corner

board_size = round(BOARD_SIZE_IN_TILES * tile_size)
menu_width = round(MENU_WIDTH_IN_TILES * tile_size)
menu_heigh = round(MENU_HEIGH_IN_TILES * tile_size)

hand_holder_width = round(HAND_HOLDER_WIDTH_IN_TILES * tile_size)
hand_holder_heigh = round(HAND_HOLDER_HEIGH_IN_TILES * tile_size)

button_end_turn_width = round(BUTTON_END_TURN_WIDTH_IN_TILES * tile_size)
button_end_turn_heigh = round(BUTTON_END_TURN_HEIGH_IN_TILES * tile_size)


#~~~~~~~~~~ Abstract variables needed for gui ~~~~~~~~


NO_LETTER = '_'
PLAYERS = []
id_player = 0

color_light_grey = (143,144,138)
color_red = (243,112,118)

#~~~~~~~~~ functions ~~~~~~~~~~~~

#-------- IMAGES RELOAD --------

def reloadTiles() :
	path_for_tiles = path.abspath('../assets/images/tiles/')
	return {
    'start' : pygame.image.load(path.join(path_for_tiles,'start.png')),
    'empty' : pygame.image.load(path.join(path_for_tiles,'empty.png')),
    'double_letter' : pygame.image.load(path.join(path_for_tiles,'double_letter.png')),
    'triple_letter' : pygame.image.load(path.join(path_for_tiles,'triple_letter.png')),
    'double_word' : pygame.image.load(path.join(path_for_tiles,'double_word.png')),
    'triple_word' : pygame.image.load(path.join(path_for_tiles,'triple_word.png'))
	}

def reloadLetters() :
	path_for_letters = path.abspath('../assets/images/letters/')
	path_for_letters = path.join(path_for_letters, game_rules.LANGUAGE)
	return {
    '*' : pygame.image.load(path.join(path_for_letters,'joker.png')),
    'A' : pygame.image.load(path.join(path_for_letters,'A.png')),
    'B' : pygame.image.load(path.join(path_for_letters,'B.png')),
    'C' : pygame.image.load(path.join(path_for_letters,'C.png')),
    'D' : pygame.image.load(path.join(path_for_letters,'D.png')),
    'E' : pygame.image.load(path.join(path_for_letters,'E.png')),
    'F' : pygame.image.load(path.join(path_for_letters,'F.png')),
    'G' : pygame.image.load(path.join(path_for_letters,'G.png')),
    'H' : pygame.image.load(path.join(path_for_letters,'H.png')),
    'I' : pygame.image.load(path.join(path_for_letters,'I.png')),
    'J' : pygame.image.load(path.join(path_for_letters,'J.png')),
    'K' : pygame.image.load(path.join(path_for_letters,'K.png')),
    'L' : pygame.image.load(path.join(path_for_letters,'L.png')),
    'M' : pygame.image.load(path.join(path_for_letters,'M.png')),
    'N' : pygame.image.load(path.join(path_for_letters,'N.png')),
    'O' : pygame.image.load(path.join(path_for_letters,'O.png')),
    'P' : pygame.image.load(path.join(path_for_letters,'P.png')),
    'Q' : pygame.image.load(path.join(path_for_letters,'Q.png')),
    'R' : pygame.image.load(path.join(path_for_letters,'R.png')),
    'S' : pygame.image.load(path.join(path_for_letters,'S.png')),
    'T' : pygame.image.load(path.join(path_for_letters,'T.png')),
    'U' : pygame.image.load(path.join(path_for_letters,'U.png')),
    'V' : pygame.image.load(path.join(path_for_letters,'V.png')),
    'W' : pygame.image.load(path.join(path_for_letters,'W.png')),
    'X' : pygame.image.load(path.join(path_for_letters,'X.png')),
    'Y' : pygame.image.load(path.join(path_for_letters,'Y.png')),
    'Z' : pygame.image.load(path.join(path_for_letters,'Z.png'))
    }

def reloadBoard() :
	path_for_back_images = path.abspath('../assets/images/background/')
	return pygame.image.load(path.join(path_for_back_images, 'board.png')) 

def reloadHandHolder() :
	path_for_back_images = path.abspath('../assets/images/background/')
	return pygame.image.load(path.join(path_for_back_images, 'hand_holder.png'))

def reloadMenu() :
	path_for_back_images = path.abspath('../assets/images/background/')
	return pygame.image.load(path.join(path_for_back_images, 'menu.png'))


#--------- DRAW FUNCTIONS ---------------

#Draw playing board
def drawBoard(board_state) :
    x_pos = 0 + delta
    y_pos = 0 + delta

    #DRAW BOARD + TILES + LETTERS
    #board borders
    window.blit(board, (0, 0))

    #tiles
    for row in range(0,TILE_PER_BOARD_COLUMN) :
        for column in range(0, TILE_PER_BOARD_COLUMN) :
            if game_rules.LAYOUT[row][column] == 0 :
                window.blit(tiles['start'],(x_pos, y_pos))
            elif game_rules.LAYOUT[row][column] == 1 :
                window.blit(tiles['empty'],(x_pos, y_pos))
            elif game_rules.LAYOUT[row][column] == 2 :
                window.blit(tiles['double_letter'],(x_pos, y_pos))
            elif game_rules.LAYOUT[row][column] == 3 :
                window.blit(tiles['triple_letter'],(x_pos, y_pos))
            elif game_rules.LAYOUT[row][column] == 4 :
                window.blit(tiles['double_word'],(x_pos, y_pos))
            elif game_rules.LAYOUT[row][column] == 5 :
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
def drawTurnInfo(player, title_line_heigh, turn_info_x, turn_info_y) :
    #TO DO general font
    font = pygame.font.SysFont("Calibri", floor(title_line_heigh))
    font.set_bold(1)
    test_text = font.render(player.name+"'s turn",1,color_light_grey)
    window.blit(test_text,(turn_info_x, turn_info_y))


def drawHandHolder(hand_holder_x, hand_holder_y):
    window.blit(hand_holder, (hand_holder_x, hand_holder_y))


def drawHand(hand, hand_x, hand_y) :
    for id_letter in range(len(hand)) :
        if hand[id_letter] != NO_LETTER :
            window.blit(letters[hand[id_letter]], (hand_x + id_letter*tile_size , hand_y)) 


def drawScores(current_player, line_heigh, score_x, score_y) :
    if(len(PLAYERS) <= 8) :

        delta_y = score_y
       
        #TODO : general font for title
        font = pygame.font.SysFont("Calibri", floor(1.1*line_heigh))
        font.set_bold(1) 
        header = font.render('Scores :',1,color_light_grey)

        font = pygame.font.SysFont("Calibri", floor(0.9*line_heigh))
        font.set_bold(0)
        window.blit(header, (score_x, delta_y) )
        delta_y += 2*line_heigh

        for player in PLAYERS :
            if player == current_player :
                font.set_bold(1)
                player_score_text = font.render('   '+player.name+" : "+str(player.points),1,color_light_grey)
            else :
                font.set_bold(0)
                player_score_text = font.render('    '+player.name+" : "+str(player.points),1,color_light_grey)
            window.blit(player_score_text, (score_x, delta_y) )
            delta_y += line_heigh


def drawSumarryEndTurn(words_and_scores, line_heigh, turn_summary_x, turn_summary_y) :
    delta_y = turn_summary_y

    id_previous_player = (id_player + len(PLAYERS) - 1) % len(PLAYERS)
    previous_player_name = PLAYERS[id_previous_player].name

    if len(words_and_scores) > 0 :

        font = pygame.font.SysFont("Calibri", floor(1*line_heigh))
        font.set_bold(1)
        header = font.render('Last turn '+previous_player_name+' played :' ,1 ,color_light_grey )
        window.blit(header, (turn_summary_x, delta_y) )
        delta_y += line_heigh

        font = pygame.font.SysFont("Calibri", floor(0.9*line_heigh))        
        font.set_bold(0)

        for association in words_and_scores :
            if association[0] == '!! SCRABBLE !!':
                delta_y += line_heigh
                text = font.render('    !! SCRABBLE gives 50 points !!',1,(243,112,118))
                window.blit(text, (turn_summary_x, delta_y) )

            else:
                delta_y += line_heigh
                text = font.render('    Word '+"'"+association[0]+"'"+' for '+str(association[1])+' points',1,color_light_grey)
                window.blit(text, (turn_summary_x, delta_y) )

    else :

        font = pygame.font.SysFont("Calibri", floor(0.9*line_heigh))
        font.set_bold(0)
        text = font.render('Nothing played by '+previous_player_name+' last turn',1,color_light_grey)
        window.blit(text, (turn_summary_x, delta_y) )

    delta_y += 2*line_heigh
    text = font.render('Remaining tiles in bag : '+str(len(game_rules.BAG_OF_LETTERS)), 1 ,color_light_grey )
    window.blit(text, (turn_summary_x, delta_y))


def drawNextPlayerHand(next_player, line_heigh, next_hand_x, next_hand_y) :
    if game_rules.DISPLAY_NEXT_PLAYER_HAND :

        delta_y = next_hand_y

        font = pygame.font.SysFont("Calibri", floor(1.1*line_heigh))
        font.set_bold(1) 
        header = font.render(next_player.name+ "'s hand :",1,color_light_grey)
        window.blit(header, (next_hand_x, delta_y) )

        delta_y = delta_y + 2*line_heigh
        font.set_bold(0) 

        next_player_letters = "    "
        for letter in next_player.hand :
            next_player_letters += letter + " "
            
        text = font.render(next_player_letters, 1, color_light_grey)
        window.blit(text, (next_hand_x, delta_y) )


def drawMenu(current_player, last_words_and_scores, pos_params) :
    window.blit(menu, (board_size, 0))
    drawHandHolder(pos_params['hand_holder'][0], pos_params['hand_holder'][1])
    drawHand(current_player.hand, pos_params['hand'][0], pos_params['hand'][1])                                
    drawNextPlayerHand(PLAYERS[(id_player + 1) % len(PLAYERS)], pos_params['line_heigh'], pos_params['next_hand'][0], pos_params['next_hand'][1])        
    drawTurnInfo(current_player, pos_params['title_line_heigh'], pos_params['turn_info'][0], pos_params['turn_info'][1])
    drawScores(current_player, pos_params['line_heigh'], pos_params['score'][0], pos_params['score'][1])
    drawSumarryEndTurn(last_words_and_scores, pos_params['line_heigh'], pos_params['turn_summary'][0], pos_params['turn_summary'][1])


def drawVictoryScreen() :
    path_for_music = path.abspath('../assets/music/')
    pygame.mixer.music.load(path.join(path_for_music, 'victory-fanfare.mp3'))
    pygame.mixer.music.play()

    mask = pygame.Surface((display_settings.WIDTH, display_settings.HEIGH))
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
            window.blit( (choice(list(letters.values()))) ,(it_x*tile_size, it_y*tile_size))
            pygame.display.flip()
            pygame.time.delay(6)

        cpt +=1


#-------- UPDATES of POSITIONS DUE TO WINDOW RESIZING -------------
def updatePositions(tile_size) :

    return{
    'title_line_heigh' : 0.9*tile_size,
    'line_heigh' : 0.6*tile_size,
    'turn_info' : [1*delta + TILE_PER_BOARD_COLUMN*tile_size + 1*delta + 1*tile_size, 1.3*delta],
    'hand_holder' : [1*delta + TILE_PER_BOARD_COLUMN*tile_size + 1*delta + 1*tile_size - 0.1*tile_size, delta + 2*tile_size - 0.1*tile_size],
    'hand' : [1*delta + TILE_PER_BOARD_COLUMN*tile_size + 1*delta + 1*tile_size, delta + 2*tile_size],
    'next_hand' : [1*delta + TILE_PER_BOARD_COLUMN*tile_size + 1*delta + 1*tile_size, delta + 4*tile_size],
    'score' : [1*delta + TILE_PER_BOARD_COLUMN*tile_size + 1*delta + 1*tile_size, delta + 4*tile_size + 1*tile_size + 2*tile_size*int(game_rules.DISPLAY_NEXT_PLAYER_HAND)],
    'turn_summary' : [1*delta + TILE_PER_BOARD_COLUMN*tile_size + 1*delta + 1*tile_size, delta + 5*tile_size + 2*0.6*tile_size + (len(PLAYERS)*0.6*tile_size) + tile_size + 2*tile_size*int(game_rules.DISPLAY_NEXT_PLAYER_HAND)],
    'button_end_turn' : [27*tile_size, delta + 2*tile_size]
    }


#-------- UPDATES OF SIZES DUE TO WINDOW RESIZING -------------
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


#Game window creation
def refreshWindow(width, heigh) :
    if display_settings.FULLSCREEN :
        if display_settings.DOUBLEBUF :
            if display_settings.HWSURFACE :
                window = pygame.display.set_mode( (width, heigh), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
            else :
                window = pygame.display.set_mode( (width, heigh), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        else:
            window = pygame.display.set_mode( (width, heigh), pygame.FULLSCREEN)
    else :
        if display_settings.RESIZABLE :
            if display_settings.DOUBLEBUF :
                if display_settings.HWSURFACE :
                    window = pygame.display.set_mode( (width, heigh), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
                else :
                    window = pygame.display.set_mode( (width, heigh), pygame.RESIZABLE | pygame.DOUBLEBUF)
            else:
                window = pygame.display.set_mode( (width, heigh) | pygame.RESIZABLE)
        else:
            window = pygame.display.set_mode( (width, heigh))
    return window

#~~~~~~ IMAGES LOADING ~~~~~~

print ('    Loading images...')

tiles = reloadTiles()
letters = reloadLetters()
board = reloadBoard()
menu = reloadMenu()
hand_holder = reloadHandHolder()

print('    Images loaded')
