def calculatePointsForOneWord(letters_played) :
    word_score = 0

    word_multiplier = 1

    for key in letters_played.keys() :

        bonus = LAYOUT[key[0]][key[1]]
        if bonus == 0 : #start_tile
            word_multiplier *= 2
            bonus = 1
        elif bonus == 4:
            word_multiplier *= 2
            bonus = 1
        elif bonus == 5:
            word_multiplier *= 3
            bonus = 1

        letter_points = POINTS[letters_played[key]]
        word_score = word_score + (bonus * letter_points)

    word_score = word_score * word_multiplier
    return word_score


#OLD : to remove
def calculatePoints(letters_played) :
    #FORMAT letters_just_played {'a' : (x, y)}
    if len(letters_played) == 0 :
        print( '  NOTHING PLAYED')
        return 0

    elif len(letters_played) == 1 : #TODO
        print('  ONE LETTER WORD')
        return 0

    elif len(letters_played) > 1 :
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

            if (len(letters_played) == (max(delta_x, delta_y) +1)) :
                print ('    WORD DOES NOT HAVE A HOLE')
                #find where is the adjacent letter
                y_border_1 = -1 
                y_border_2 = -1 

                if ( (min_y - 1) >= 0 ) : 
                    if board_state[min_x][min_y-1] != '?' :
                        y_border_1 = min_y-1
                if ( (max_y + 1) <= (TILE_PER_BOARD_COLUMN-1) ) :
                    if board_state[min_x][max_y+1] != '?' :
                        y_border_2 = max_y+1

                if (y_border_1 == -1 and y_border_2 == -1) :
                    print('      THIS WORD DOES NOT CROSS OTHER WORDS')

                    new_word_score = calculatePointsForOneWord(letters_played)
                    x_sider_1 = -1
                    x_sider_2 = -1
                    y_sider_1 = -1
                    y_sider_2 = -1

                    if ( (min_x - 1) >= 0 ):
                        for pos in letters_played.keys() :
                            if board_state[pos[0]-1][pos[1]] != '?':
                                x_sider_1 = pos[0]-1
                                y_sider_1 = pos[1] 
                    if ( (min_x + 1) <= TILE_PER_BOARD_COLUMN-1 ) :
                        for pos in letters_played.keys() :
                            if board_state[pos[0]+1][pos[1]] != '?':
                                x_sider_2 = pos[0]+1
                                y_sider_2 = pos[1]

                    old_word_score_1 = 0
                    if ( (x_sider_1 >= 0) and (y_sider_1 >= 0) ) :
                        print('        THIS WORD ENDS AN EXISTING WORD')
                        it_x = x_sider_1 + 1 #to count the common letter

                        old_word_letters = []
                        while( (it_x >= 0) and (board_state[it_x][y_sider_1] != '?') ) :
                            old_word_letters.append(board_state[it_x][y_sider_1])
                            it_x = it_x - 1

                        for letter in old_word_letters :
                            old_word_score_1 = old_word_score_1 + POINTS[letter]

                    old_word_score_2 = 0
                    if ( (x_sider_2 >= 0) and (y_sider_2 >= 0) ) :
                        print('        THIS WORD BEGINS AN EXISTING WORD')
                        #This code does not work if the created word begins/ends two different words ...
                        it_x = x_sider_2 - 1

                        old_word_letters = []
                        while( (it_x >= 0) and (board_state[it_x][y_sider_2] != '?') ) :
                            old_word_letters.append(board_state[it_x][y_sider_2])
                            it_x = it_x + 1

                        for letter in old_word_letters :
                            old_word_score_2 = old_word_score_2 + POINTS[letter]

                    total_score = new_word_score + old_word_score_1 + old_word_score_2
                    print('----WORD SCORE : ', total_score, ' -----')
                    return total_score


                elif y_border_1 > 0 and y_border_2 > 0 : #DONE
                    print('      THIS WORD CUT TWO OTHERS WORDS')
                    missing_letter_1 = board_state[min_x][y_border_1]
                    missing_letter_2 = board_state[min_x][y_border_2]

                    word_score = POINTS[missing_letter_1] + POINTS[missing_letter_2] + calculatePointsForOneWord(letters_played)
                    print('----WORD SCORE : ', word_score, ' -----')
                    return word_score

                else : #DONE
                    print('      THIS WORD CUT ONE OTHER WORD')
                    y_border = max(y_border_1, y_border_2)
                    missing_letter = board_state[min_x][y_border]

                    word_score = POINTS[missing_letter] + calculatePointsForOneWord(letters_played)
                    print('----WORD SCORE : ', word_score, ' -----')
                    return word_score

            else : #DONE
                print('    THERE IS A HOLE IN THE WORD') #not working with word multiplier

                #TODO : case where this word also begins or ends a other words ...

                word_score = 0

                y_holes = []
                for y_pos in range(min_y, max_y+1) :
                    if ( not ( (min_x, y_pos) in letters_played ) ) :
                        y_holes.append(y_pos)

                old_layout = {}
                for y_hole in y_holes :
                    letters_played[(min_x, y_hole)] = board_state[min_x][y_hole]
                    old_layout[(min_x, y_hole)] = LAYOUT[min_x][y_hole]
                    LAYOUT[min_x][y_hole] = 1

                word_score = calculatePointsForOneWord(letters_played)

                for key in old_layout.keys() :
                    LAYOUT[key[0]][key[1]] = old_layout[key] #set layout back to normal

                print('----WORD SCORE : ', word_score, ' -----')
                return word_score



        elif delta_y == 0 : #TODO
            print (' HORIZONTAL WORD')

            if (len(letters_played) == (max(delta_x, delta_y) +1)) :
                print ('    WORD DOES NOT HAVE A HOLE')
            else :
                print('    THERE IS A HOLE IN THE WORD')

        else :
            print('  PROBLEM')


    return 0 #TEMP