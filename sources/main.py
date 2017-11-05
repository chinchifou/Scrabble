#~~~~~~ IMPORTS ~~~~~~

#------ Standard library imports ------
from random import randint
from math import floor

#------ User's imports -------
import pygame
import gui
import game_rules
import display_settings

#------ Constants ------

ACTIONS = ('SELECT_A_LETTER', 'PLAY_A_LETTER')

DISPLAY_NEXT_PLAYER_HAND = game_rules.DISPLAY_NEXT_PLAYER_HAND


#CHANGING DURING THE GAME
bag_of_letters = game_rules.BAG_OF_LETTERS

gui.board_state = [ ['?' for i in range(gui.TILE_PER_BOARD_COLUMN)] for j in range(gui.TILE_PER_BOARD_COLUMN) ]

#BUTTONS
#path_for_buttons = './images/buttons/'
#button_end_turn = path_for_buttons+'end_turn.png'

#Never change this value without changing the layout accordingly


tile_x_hand = 0
selected_letter = ''
letter_from_board = False
letters_just_played = {} #format {'a' : (x, y)}

last_words_and_scores = []

clock = pygame.time.Clock()
timer = clock.tick()
delta_clic = [0.5, 0.5]

#TODO : BACKUP TO ALLOW RESET
board_state_at_turns_begining = gui.board_state 
hand_at_turns_begining = []


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
def cursorIsOnBoard(cursor_x, cursor_y) :
    tile_x = floor( (cursor_x - gui.delta)/gui.tile_size)
    tile_y = floor( (cursor_y - gui.delta)/gui.tile_size)
    if ( tile_x in range (0, gui.TILE_PER_BOARD_COLUMN ) ) and ( tile_y in range (0, gui.TILE_PER_BOARD_COLUMN ) ) :
        return True
    else :
        return False
def cursorIsOnHand(cursor_x, cursor_y, hand) : #TO DEBUG ?? use collidepoint
    delta_hand_x = 1*gui.delta + gui.TILE_PER_BOARD_COLUMN*gui.tile_size + 1*gui.delta + 1*gui.tile_size
    delta_hand_y = gui.delta + 2*gui.tile_size

    tile_x = floor( (cursor_x - delta_hand_x)/gui.tile_size)
    tile_y = floor( (cursor_y - delta_hand_y)/gui.tile_size)

    if ( tile_x in range (0, len(hand)) ) and ( tile_y in range (0, 1) ) :
        return True
    else :
        return False


def emptySlot(x,y) :
    if gui.board_state[x][y] == '?':
        return True
    else :
        return False


def calculatePoints(letters_played) :
    #FORMAT letters_just_played {'a' : (x, y)}
    if len(letters_played) > 1 :
        print ('   ', len(letters_played),' letters played' )
    else :
        print ('   ', len(letters_played),' letter played' )  

    if len(letters_played) == 0 :
        print( '    NOTHING PLAYED')
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
  
            #find first letter
            start_y = min_y
            while( ( (start_y - 1) >= 0) and (gui.board_state[min_x][start_y - 1] != '?') ) :
                start_y = start_y - 1

            #find last letter
            end_y = max_y
            while( ( (end_y + 1) <= gui.TILE_PER_BOARD_COLUMN-1) and (gui.board_state[min_x][end_y + 1] != '?') ) :
                end_y = end_y + 1

            #words_and_scores = []

            if ( end_y > start_y ) : #prevent one letter word
                print('    VERTICAL WORD')
                #FIRST PASSAGE
                #store word just created
                new_word = ''
                new_word_multiplier = 1
                new_word_score = 0

                for it_y in range( start_y, end_y+1 ) :
                    letter = gui.board_state[min_x][it_y]
                    new_word += letter
                    if ((min_x, it_y) in letters_played ): #letters just played
                        #calculate points for each letter
                        bonus = game_rules.LAYOUT[min_x][it_y]
                        if bonus == 0 : #start_tile
                            new_word_multiplier *= 2
                            bonus = 1
                        elif bonus == 4:
                            new_word_multiplier *= 2
                            bonus = 1
                        elif bonus == 5:
                            new_word_multiplier *= 3
                            bonus = 1

                        new_letter_points = game_rules.POINTS[letter]
                        new_word_score = new_word_score + (bonus * new_letter_points)

                    else : #old letters
                        old_letter_points = game_rules.POINTS[letter]
                        new_word_score = new_word_score + old_letter_points
                        
                new_word_score = new_word_score * new_word_multiplier
                words_and_scores.append([new_word, new_word_score])


            #SECOND PASSAGE
            for it_y in range( start_y, end_y+1 ) :
                #check for horizontal words
                it_x = min_x
                if (it_x, it_y) in (letters_played) : #prevent to count already existing words

                    condition_1 = ( (it_x - 1) >= 0 ) and ( gui.board_state[it_x-1][it_y] != '?' )
                    condition_2 = ( (it_x + 1) <= gui.TILE_PER_BOARD_COLUMN-1 ) and ( gui.board_state[it_x+1][it_y] != '?' ) 

                    if ( condition_1  or condition_2 ) :       
                        print('    HORIZONTAL WORD')
                
                        while( ( (it_x - 1) >= 0) and (gui.board_state[it_x-1][it_y] != '?') ) : #go to the begining of the word
                            it_x = it_x - 1


                        old_word = ''
                        old_word_score = 0
                        old_word_multiplier = 1  

                        while( ( (it_x) <= gui.TILE_PER_BOARD_COLUMN-1) and (gui.board_state[it_x][it_y] != '?') ) : #go to the end of the word

                            old_letter = gui.board_state[it_x][it_y]
                            old_word += old_letter

                            if (it_x, it_y) in (letters_played) :

                                bonus = game_rules.LAYOUT[it_x][it_y]

                                if bonus == 0 : #start_tile
                                    old_word_multiplier *= 2
                                    bonus = 1
                                elif bonus == 4:
                                    old_word_multiplier *= 2
                                    bonus = 1
                                elif bonus == 5:
                                    old_word_multiplier *= 3
                                    bonus = 1

                                old_word_score += game_rules.POINTS[old_letter] * bonus

                            else :
                                old_word_score += game_rules.POINTS[old_letter]

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
            #find first letter
            start_x = min_x
            while( ( (start_x - 1) >= 0) and (gui.board_state[start_x - 1][min_y] != '?') ) :
                start_x = start_x - 1

            #find last letter
            end_x = max_x
            while( ( (end_x + 1) <= gui.TILE_PER_BOARD_COLUMN-1) and (gui.board_state[end_x + 1][min_y] != '?') ) :
                end_x = end_x + 1

            if ( end_x > start_x ) : #prevent one letter word
                print('    HORIZONTAL WORD')
                #FIRST PASSAGE
                #store word just created  
                new_word = ''
                new_word_multiplier = 1
                new_word_score = 0

                for it_x in range( start_x, end_x+1 ) :
                    letter = gui.board_state[it_x][min_y]
                    new_word += letter
                    if ((it_x, min_y) in letters_played ): #letters just played
                        #calculate points for each letter
                        bonus = game_rules.LAYOUT[it_x][min_y]
                        if bonus == 0 : #start_tile
                            new_word_multiplier *= 2
                            bonus = 1
                        elif bonus == 4:
                            new_word_multiplier *= 2
                            bonus = 1
                        elif bonus == 5:
                            new_word_multiplier *= 3
                            bonus = 1

                        new_letter_points = game_rules.POINTS[letter]
                        new_word_score = new_word_score + (bonus * new_letter_points)

                    else : #old letters
                        old_letter_points = game_rules.POINTS[letter]
                        new_word_score = new_word_score + old_letter_points
                        
                new_word_score = new_word_score * new_word_multiplier
                words_and_scores.append([new_word, new_word_score])


            #SECOND PASSAGE
            for it_x in range( start_x, end_x+1 ) :
                #check for vertical words
                it_y = min_y
                if (it_x, it_y) in (letters_played) : #prevent to count already existing words

                    condition_1 = ( (it_y - 1) >= 0 ) and ( gui.board_state[it_x][it_y-1] != '?' )
                    condition_2 = ( (it_y + 1) <= gui.TILE_PER_BOARD_COLUMN-1 ) and ( gui.board_state[it_x][it_y+1] != '?' ) 

                    if ( condition_1  or condition_2 ) :
                        print('    VERTICAL WORD')

                        while( ( (it_y - 1) >= 0) and (gui.board_state[it_x][it_y-1] != '?') ) : #go to the begining of the word
                            it_y = it_y - 1


                        old_word = ''
                        old_word_score = 0
                        old_word_multiplier = 1

                        while( ( (it_y) <= gui.TILE_PER_BOARD_COLUMN-1) and (gui.board_state[it_x][it_y] != '?') ) : #go to the end of the word

                            old_letter = gui.board_state[it_x][it_y]
                            old_word += old_letter

                            if (it_x, it_y) in (letters_played) :

                                bonus = game_rules.LAYOUT[it_x][it_y]

                                if bonus == 0 : #start_tile
                                    old_word_multiplier *= 2
                                    bonus = 1
                                elif bonus == 4:
                                    old_word_multiplier *= 2
                                    bonus = 1
                                elif bonus == 5:
                                    old_word_multiplier *= 3
                                    bonus = 1

                                old_word_score += game_rules.POINTS[old_letter] * bonus

                            else :
                                old_word_score += game_rules.POINTS[old_letter]
                            
                            it_y = it_y + 1

                        old_word_score = old_word_score * old_word_multiplier
                        words_and_scores.append([old_word, old_word_score])

            total_score = 0 #TEMP

            for association in words_and_scores :
                print('Word "', association[0], '" gives ', association[1], ' points' )
                total_score += association[1]
            
            print ('total_score : ', total_score)

            return words_and_scores


#___WINDOW INITIALIZATION___

window = gui.refreshWindow(display_settings.WIDTH, display_settings.HEIGH) #call 'event.type == VIDEORESIZE'

#___GAME INITIALIZATION___
#Draw letters for each players
for player_name in game_rules.PLAYERS_NAME :
    start_hand = []
    for i in range(game_rules.LETTERS_PER_HAND) :
        random_int = randint(0,len(bag_of_letters)-1)
        start_hand.append(bag_of_letters[random_int])
        #bag_of_letters.remove(bag_of_letters[random_int])
        del(bag_of_letters[random_int])

    gui.PLAYERS.append(Player(player_name,0,start_hand))

#First player, first action
current_player = gui.PLAYERS[gui.id_player]
current_action = ACTIONS[0] #select a letter

hand_at_turns_begining = current_player.hand
gui.board_state_at_turns_begining = gui.board_state



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
        elif ( event_type == pygame.VIDEORESIZE ) : #properly refresh the game window if a resize is detected

            print('resize')
            window = gui.refreshWindow(event.dict['size'][0], event.dict['size'][1])
            #load again all images to gain quality in case of a zoom in after a zoom out
            gui.letters = gui.reloadLetters()
            gui.tiles = gui.reloadTiles()
            gui.board = gui.reloadBoard() 
            gui.menu = gui.reloadMenu()
            gui.hand_holder = gui.reloadHandHolder() 

            #--------- RESIZE ASSETS ---------

            #update values
            gui.zoom_factor = gui.updateZoomFactor(event.dict['size'][0], event.dict['size'][1])
            gui.tile_size = gui.updateTileSize()
            gui.delta = gui.updateDelta()
            gui.board_size = gui.updateBoardSize()
            gui.menu_width = gui.updateMenuWidth()
            gui.menu_heigh = gui.updateMenuHeigh()
            gui.hand_holder_width = gui.updateHandHolderWidth()
            gui.hand_holder_heigh = gui.updateHandHolderHeigh()

            #resize based on new values            
            gui.board = pygame.transform.smoothscale( gui.board, (gui.board_size, gui.board_size) )
            gui.menu = pygame.transform.smoothscale( gui.menu, (gui.menu_width, gui.menu_heigh) )
            gui.hand_holder = pygame.transform.smoothscale( gui.hand_holder, (gui.hand_holder_width, gui.hand_holder_heigh) )

            for key in gui.letters.keys() :
                gui.letters[key] = pygame.transform.smoothscale(gui.letters[key], (gui.tile_size, gui.tile_size) )
            for key in gui.tiles.keys() :
                gui.tiles[key] = pygame.transform.smoothscale(gui.tiles[key], (gui.tile_size, gui.tile_size) )

            #--------- PLACE ASSETS ON THE SCREEN ---------
            gui.pos_params = gui.updatePositions(gui.tile_size)

            gui.drawBoard(gui.board_state)
            gui.drawMenu(current_player, last_words_and_scores, gui.pos_params)
            gui.background = window.copy() #save gui.background

            pygame.display.flip()

        #~~~~~~~~~~~ KEYBOARD KEY DOWN ~~~~~~~~~~~
        elif ( event_type == pygame.KEYDOWN ) :
            key_pressed = event.key

            #------ SECURITY -------
            if ( current_action == "SELECT_A_LETTER" ) :

                #------ QUIT -------
                if ( key_pressed == pygame.K_ESCAPE ) :
                    running = False #exit the game

                #------ VICTORY -------
                elif ( key_pressed == pygame.K_BACKSPACE ) :
                    gui.drawVictoryScreen()
            
                #------ NEXT PLAYER -------
                elif( key_pressed == pygame.K_SPACE ) :
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
                        if current_player.hand[id_letter] == gui.NO_LETTER :
                            del( current_player.hand[id_letter] )
                        else :
                            id_letter += 1

                    while len(current_player.hand) < game_rules.LETTERS_PER_HAND and len(game_rules.BAG_OF_LETTERS) > 0 :
                        random_int = randint(0,len(bag_of_letters)-1)
                        current_player.hand.append(bag_of_letters[random_int])
                        del(bag_of_letters[random_int])

                    #NEXT PLAYER
                    gui.id_player = (gui.id_player + 1) % len(gui.PLAYERS)
                    current_player = gui.PLAYERS[gui.id_player]
                    gui.PLAYERS[gui.id_player].printInstanceVariables()
                    current_action = ACTIONS[0] #select a letter

                    hand_at_turns_begining = current_player.hand
                    gui.board_state_at_turns_begining = gui.board_state

                    gui.drawBoard(gui.board_state)
                    gui.drawMenu(current_player, last_words_and_scores, gui.pos_params)
                    gui.background = window.copy()
                    pygame.display.flip()

        #~~~~~~~~~~~ MOUSE BUTTONS ~~~~~~~~~~~
        elif ( ( (event_type == pygame.MOUSEBUTTONDOWN) or (event_type == pygame.MOUSEBUTTONUP) ) and event.button == 1 ) :
            
            timer = clock.tick()            
            #~~~~~~~~~~~ PRESS LEFT CLIC ~~~~~~~~~~~
            if ( event_type == pygame.MOUSEBUTTONDOWN ) :
                
                cursor_x = event.pos[0]
                cursor_y = event.pos[1]

                #------ SELECT A LETTER -------
                if current_action == 'SELECT_A_LETTER' :

                    if cursorIsOnBoard(cursor_x, cursor_y) :

                        tile_x_board = floor( (cursor_x - gui.delta)/gui.tile_size)
                        tile_y_board = floor( (cursor_y - gui.delta)/gui.tile_size)

                        delta_clic[0] = ( (cursor_x - gui.delta)/gui.tile_size) - tile_x_board
                        delta_clic[1] = ( (cursor_y - gui.delta)/gui.tile_size) - tile_y_board

                        #letter just played ?
                        if ( (tile_x_board, tile_y_board) in letters_just_played.keys() ) :

                            selected_letter = gui.board_state[tile_x_board][tile_y_board]
                            #letter_from_board ???
                            letter_from_board = True
                            del(letters_just_played[(tile_x_board, tile_y_board)])
                            gui.board_state[tile_x_board][tile_y_board] = '?'
                            current_action = ACTIONS[1] #next action : play a letter

                            gui.drawBoard(gui.board_state)
                            gui.background = window.copy() #save gui.background

                    elif cursorIsOnHand(cursor_x, cursor_y, current_player.hand) :

                        delta_hand_x = 1*gui.delta + gui.TILE_PER_BOARD_COLUMN*gui.tile_size + 1*gui.delta + 1*gui.tile_size
                        delta_hand_y = gui.delta + 2*gui.tile_size

                        tile_x_hand = floor( (cursor_x - delta_hand_x)/gui.tile_size)
                        tile_y_hand = floor( (cursor_y - delta_hand_y)/gui.tile_size)

                        delta_clic[0] = ( (cursor_x - delta_hand_x)/gui.tile_size) - tile_x_hand
                        delta_clic[1] = ( (cursor_y - delta_hand_y)/gui.tile_size) - tile_y_hand

                        if current_player.hand[tile_x_hand] != gui.NO_LETTER :

                            selected_letter = current_player.hand[tile_x_hand]
                            current_player.hand[tile_x_hand] = gui.NO_LETTER
                            letter_from_board = False
                            current_action = ACTIONS[1] #next action : play a letter

                            gui.drawHandHolder(gui.pos_params['hand_holder'][0], gui.pos_params['hand_holder'][1])
                            gui.drawHand(current_player.hand, gui.pos_params['hand'][0], gui.pos_params['hand'][1])     

                            gui.background = window.copy() #save gui.background

                #------ PLAY A LETTER -------
                elif current_action == 'PLAY_A_LETTER' :

                    if cursorIsOnBoard(cursor_x, cursor_y) :

                        tile_x_board = floor( (cursor_x - gui.delta)/gui.tile_size)
                        tile_y_board = floor( (cursor_y - gui.delta)/gui.tile_size)

                        if emptySlot(tile_x_board,tile_y_board) : 

                            gui.board_state[tile_x_board][tile_y_board] = selected_letter

                            gui.drawBoard(gui.board_state)
                            gui.background = window.copy() #save gui.background
                            pygame.display.flip()

                            letters_just_played[(tile_x_board, tile_y_board)] = selected_letter
                            selected_letter = ''
                            current_action = ACTIONS[0]

                    elif cursorIsOnHand(cursor_x, cursor_y, current_player.hand) :

                        delta_hand_x = 1*gui.delta + gui.TILE_PER_BOARD_COLUMN*gui.tile_size + 1*gui.delta + 1*gui.tile_size
                        tile_x_hand = floor( (cursor_x - delta_hand_x)/gui.tile_size)

                        underneath_letter = current_player.hand[tile_x_hand]

                        if underneath_letter == gui.NO_LETTER :

                            current_player.hand[tile_x_hand] = selected_letter

                            gui.drawMenu(current_player, last_words_and_scores, gui.pos_params)
                            gui.background = window.copy() #save gui.background
                            pygame.display.flip()

                            selected_letter = ''
                            current_action = ACTIONS[0] #next action : select a letter

            #~~~~~~~~~~~ RELEASE LEFT CLIC ~~~~~~~~~~~
            elif ( event_type == pygame.MOUSEBUTTONUP ) :

                #timer = clock.tick()
                cursor_x = event.pos[0]
                cursor_y = event.pos[1]

                if current_action == 'PLAY_A_LETTER' :
                    
                    #not a simple fast clic
                    if ( timer > 100 )  : 

                        if cursorIsOnBoard(cursor_x, cursor_y) :

                            tile_x_board = floor( (cursor_x - gui.delta)/gui.tile_size)
                            tile_y_board = floor( (cursor_y - gui.delta)/gui.tile_size)

                            if emptySlot(tile_x_board,tile_y_board) : 

                                gui.board_state[tile_x_board][tile_y_board] = selected_letter

                                gui.drawBoard(gui.board_state)    
                                gui.background = window.copy() #save gui.background
                                pygame.display.flip()

                                letters_just_played[(tile_x_board, tile_y_board)] = selected_letter
                                selected_letter = ''                  
                                current_action = ACTIONS[0] #Next action : select a letter

                        elif cursorIsOnHand(cursor_x, cursor_y, current_player.hand) :

                            delta_hand_x = 1*gui.delta + gui.TILE_PER_BOARD_COLUMN*gui.tile_size + 1*gui.delta + 1*gui.tile_size
                            tile_x_hand = floor( (cursor_x - delta_hand_x)/gui.tile_size)

                            underneath_letter = current_player.hand[tile_x_hand]

                            if underneath_letter == gui.NO_LETTER :

                                current_player.hand[tile_x_hand] = selected_letter #ADDED

                                gui.drawMenu(current_player, last_words_and_scores, gui.pos_params)
                                gui.background = window.copy() #save gui.background
                                pygame.display.flip()

                                selected_letter = ''
                                current_action = ACTIONS[0] #next action : select a letter

        #~~~~~~~~~~~ MOUSE MOTION ~~~~~~~~~~~
        elif ( event_type == pygame.MOUSEMOTION ) :

            #------ PLAY A LETTER -------
            if current_action == 'PLAY_A_LETTER' :  

                mouse_pos = pygame.mouse.get_pos()
                cursor_x = mouse_pos[0]
                cursor_y = mouse_pos[1]

                window.blit(gui.background, (0, 0))
                window.blit( gui.letters[selected_letter], (cursor_x - delta_clic[0]*gui.tile_size, cursor_y - delta_clic[1]*gui.tile_size) )
                pygame.display.flip()  

print('    Shutting down ...')
pygame.quit() #exit if running == false
print('Game is closed')
