'''Global Variables/Import Library Section '''
import random
import os

building_list = ['R', 'I', 'C', 'O', '*']
turn_count = 0
board = [[" " for _ in range(20)] for _ in range(20)]

alphabet = 'ABCDEFGHIJKLMNOPQRST'

def display_main_menu():  # SHOW MAIN MENU
    print('Welcome, mayor of Ngee Ann City!')
    print('--------------------------------')
    print('1. Start new game')  # start_new_game()
    print('2. Load saved game')  # load_save_game()
    print('3. Display high score')  # display_high_score()
    print('0. Exit')

    choice = input('Your choice? ')
    return choice


def display_game_menu(random_build1, random_build2):
    print('1. Build a ' + random_build1)
    print('2. Build a ' + random_build2)
    print('3. See current score')
    print()
    print('4. Save game')
    print('0. Exit to game menu')


# printing high scores
def print_high_score(high_scores):
    print()
    print('---------- HIGH SCORES ---------')
    print('{:5s}{:22s}{:5s}'.format('Pos', 'Player', 'Score'))
    print('---  ------                -----')
    for index, one_high_score in enumerate(high_scores):
        # one_high_score -> ('Never', 50)
        # one_high_score[0] -> 'Never'
        # one_high_score[1] -> 50
        # index -> 0

        print('{:2d}.  {:<22s}{:>5d}'.format(index + 1, one_high_score[0], one_high_score[1]))  # index-->starts from 0
    print('--------------------------------')
    print('\n')


def print_score(number_list):
    for index, number in enumerate(number_list):  # enumerate to find index of element and not only element  #index will be number_list[0] etc
        print(str(number), end='')  # end='' is to ensure everything is printed ona straight line (3 + 1 + 4 = 8 etc)
        if index == len(number_list) - 1:  # if this was the last numbers in the list (etc 4), print a '='
            print(' = ', end='')
        else:  # else if not last number in line, print '+'
            print(' + ', end='')
    print(sum(number_list))


def print_map(board):
    # print('{:>6}{:>6}{:>6}{:>6}{:>6}{:>6}{:>6}{:>6}{:>6}{:>6}{:>6}{:>6}
    # {:>6}{:>6}{:>6}{:>6}{:>6}{:>6}{:>6}{:>6}'.format('A','B','C','D','E'
    # ,'F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T')) #print header

    num_rows = len(board)  # get 20
    num_columns = len(board[0])  # get the inner list which is also 20
    for i in range(num_columns):
        print('{:>4}'.format(alphabet[i]), end='')
    print('')
    print(' ', end='')

    for column in range(num_columns):
        if column == 0:
            print(' +---', end='')
        else:
            print('+---', end='')
    print('+')

    for row in range(num_rows):
        if row < 9:
            print('{} '.format(row + 1), end='')
            for column in board[row]:
                print('| {} '.format(column), end='')
            print('|')

            for column in range(num_columns):
                if column == 0:
                    print('  +---', end='')
                else:
                    print('+---', end='')
            print('+')
        else:
            print((row + 1), end='')
            for column in board[row]:
                print('| {} '.format(column), end='')
            print('|')

            for column in range(num_columns):
                if column == 0:
                    print('  +---', end='')
                else:
                    print('+---', end='')
            print('+')

    return board


def play_game_build_building():
    house_list = ['R', 'I', 'C', 'O', '*']

    random_building1, random_building2 = random.sample(house_list, k=2)

    return random_building1, random_building2


def main_menu_validate(input):  # MAIN MENU USER INPUT FUNCTION (not in used)
    # while True:
    try:
        choice = int(input)
        assert choice in (1, 2, 3, 0)  # For AssertionError

        if choice == 1:
            start_new_game()

        elif choice == 2:
            load_save_game()

        elif choice == 3:
            display_high_score()

        else:
            print('Exiting game')

    except TypeError:
        print('Please enter the choice number')

    except AssertionError:
        print('Please enter available choices')

    except:
        print('Please try again')


# finding all the buildings top, down, left, right of current position
def find_neighbours(row, column):
    neighbours = []

    for i in [-1, 1]:
        if 0 <= row + i < len(board):  # checking if it's still within the board
            if board[row+i][column] != ' ':  # checking if it's a building or an empty space
                neighbours.append(board[row+i][column])

    # to find neighbours left and right. column +1 finds right of existing building. column -1 finds if there's building left of existing builing.
    for i in [-1, 1]:
        if 0 <= column + i < len(board[row]):
            if board[row][column+i] != ' ':
                neighbours.append(board[row][column+i])  # if within the board and not an empty space, appends left & right building into neighbours list,
                # another function checks what buildings are in the list to calculate score etc

    return neighbours


# finding all the buildings left, right of current position
def find_neighbours_left_right(row, column):
    neighbours = []

    # to find neighbours left and right. column +1 finds right of existing building. column -1 finds if there's building left of existing builing.
    for i in [-1, 1]:
        if 0 <= column + i < len(board[row]):
            if board[row][column + i] != ' ':
                neighbours.append(board[row][column + i])  # if within the board and not an empty space, appends left & right building into neighbours list,
                # another function checks what buildings are in the list to calculate score etc

    return neighbours


def check_add_coin(player_coins):
    for row in range(len(board)):
        for column in range(len(board)):
            if board[row][column] == 'I':
                industry_neighbours = find_neighbours(row, column)
                for building in industry_neighbours:
                    if building == 'R':
                        player_coins -= 1

            elif board[row][column] == 'C':
                commercial_neighbours = find_neighbours(row, column)
                for building in commercial_neighbours:
                    if building == 'R':
                        player_coins -= 1

    return player_coins


def count_score(player_coins):
    points_dict = {'R': [], 'I': [], 'C': [], 'O': [], '*': []}

    for row in range(len(board)):
        for column in range(len(board)):

            if board[row][column] == 'R':
                residential_point = 0
                residential_neighbours = find_neighbours(row, column)
                for building1 in residential_neighbours:
                    if building1 == 'I':
                        residential_point = 1
                        break
                    elif building1 == 'C' or building1 == 'R':
                        residential_point += 1
                    elif building1 == 'O':
                        residential_point += 2
                points_dict['R'].append(residential_point)

            elif board[row][column] == 'I':
                points_dict['I'].append(1)
                industry_neighbours = find_neighbours(row, column)
                for building in industry_neighbours:
                    if building == 'R':
                        player_coins -= 1

            elif board[row][column] == 'C':
                commercial_neighbours = find_neighbours(row, column)
                for building in commercial_neighbours:
                    if building == 'C':
                        points_dict['C'].append(1)
                    if building == 'R':
                        player_coins -= 1

            elif board[row][column] == 'O':
                park_point = 0
                park_neighbours = find_neighbours(row, column)
                for building in park_neighbours:
                    if building == 'O':
                        park_point += 1
                if park_point != 0:
                    points_dict['O'].append(park_point)

            elif board[row][column] == '*':
                road_point = 0
                road_neighbours = find_neighbours(row, column)
                for building in road_neighbours:
                    if building == '*':
                        road_point += 1
                if road_point != 0:
                    points_dict['*'].append(road_point)

    # another method of counting points for road. for this we count 1 point per connected road
    # for row in board:  # for each row in the board
    #     count = 0
    #     for building in row:  # for each building in each row of the board
    #         if building == '*':  # if it is a road
    #             count += 1
    #         else:
    #             if count > 1:
    #                 for i in range(count):
    #                     points_dict['*'].append(1)  # add 1
    #             count = 0

    return points_dict


# ending result
def show_score(num_of_coins):
    total_points=0
    points_dict = count_score(num_of_coins)

    for key in points_dict:
        total_points += sum(points_dict[key])   # loops over the list of numbers in each list('BCH' etc) and adds each number to each other.

    for key in points_dict:
        print(key + ': ', end='')
        print_score(points_dict[key])    # prints each buildings' scores

    print('Total score: '+str(total_points))
    return total_points


# for this function, it finds the top, down, left, right positions of a position on the board
# if all top, down, left, right positions are empty, it means there are no surrounding buildings around the place where the current building is being placed
# there MUST be surrounding buildings, since new buildings can only be placed next to another existing building on the board
def has_neighbour(row_input, column):  # when it runs the has_neighbour function it needs the 2 required arguments: row and column/2 parameters

    # check if there are neighbours above or below
    for i in [-1, 1]:
        if 0 <= row_input + i < len(board):
            if board[row_input + i][column] != ' ':  # check if the space is not empty
                return True  # if it is not empty, it means there is an existing building above or below current position, correct since there must be a building nearby current position

    # check if there are neighbours left right
    for i in [-1, 1]:
        if 0 <= column + i < len(board[row_input]):
            if board[row_input][column + i] != ' ':  # check if the space is not empty
                return True  # if it is not empty, it means there is an existing building left or right on current position, correct since there must be a building nearby current position

    return False  # after checking up, down, left, right, if there are no buildings then return False. False since new building cannot be placed in position with no surrounding buildings

def start_new_game(random_build1, random_build2):
    global R, I, C, O, asterisk
    game_count = 0
    coin_sum = 0

    while True: #added
        if coin_sum != 16: #added
            if check_full_board() == True: #added
                game_count += 1
                print('\nTurn ' + str(game_count))
                print('Number of coins available: ' + str(16 - coin_sum) )
                      ##+ '\tTotal Score: ' + str(show_total_score(coin_sum)))

                print_map(board)
                display_game_menu(random_build1, random_build2)

                while True:
                    your_choice = input('Your choice? ')
                    if your_choice in ('1', '2', '3', '4', '0'):
                        break
                    else:
                        print('Please enter correct number option 0-4')

                if (your_choice == '1') or (your_choice == '2'):

                    # validate user input build where
                    while True:
                        build_where = input('Build where? ')

                        if len(build_where) == 3 or len(build_where) == 2:

                            row_letter = build_where[0]

                            if (row_letter == 'a'):
                                column = 0
                            elif (row_letter == 'b'):
                                column = 1
                            elif (row_letter == 'c'):
                                column = 2
                            elif (row_letter == 'd'):
                                column = 3
                            elif (row_letter == 'e'):
                                column = 4
                            elif (row_letter == 'f'):
                                column = 5
                            elif (row_letter == 'g'):
                                column = 6
                            elif (row_letter == 'h'):
                                column = 7
                            elif (row_letter == 'i'):
                                column = 8
                            elif (row_letter == 'j'):
                                column = 9
                            elif (row_letter == 'k'):
                                column = 10
                            elif (row_letter == 'l'):
                                column = 11
                            elif (row_letter == 'm'):
                                column = 12
                            elif (row_letter == 'n'):
                                column = 13
                            elif (row_letter == 'o'):
                                column = 14
                            elif (row_letter == 'p'):
                                column = 15
                            elif (row_letter == 'q'):
                                column = 16
                            elif (row_letter == 'r'):
                                column = 17
                            elif (row_letter == 's'):
                                column = 18
                            elif (row_letter == 't'):
                                column = 19
                            else:
                                column = None

                            if len(build_where) == 2:
                                if not build_where[1].isdigit():  # if the row input is not a number, row becomes None
                                    row = None
                                else:
                                    row = int(build_where[1])
                            else:
                                if not build_where[1:3].isdigit():  # if the row input is not a number, row becomes None
                                    row = None
                                else:
                                    row = int(build_where[1:3])

                            # if the column/row is not None, means something inside
                            # row must be greater than 0, smaller than length of the board
                            if column is not None and row is not None and (0 <= row <= len(board)):
                                break
                            else:
                                print('Please type again. You have either typed something out of the board or the letter is capitalized.')
                        else:
                            print('Please enter correct input such as a2.')

                    if (has_neighbour(row - 1, column) or game_count == 1) and (board[row - 1][column] == ' '):

                        building = ''
                        if your_choice == '1':
                            building = random_build1
                            random_build1, random_build2 = play_game_build_building()  # will shuffle the building after every successful build

                        if your_choice == '2':
                            building = random_build2
                            random_build1, random_build2 = play_game_build_building()  # will shuffle the building after every successful build

                        board[row - 1][column] = building

                        coin_sum = check_add_coin(coin_sum)

                        coin_sum += 1

                    else:
                        if board[row - 1][column] != ' ':  # if building placed in a space with existing building which is not an empty space
                            print('You must build in an empty spot in the board.')

                        else:
                            print('You must build next to an existing building')
                        game_count = game_count - 1

                elif your_choice == '3':
                    show_score(coin_sum)
                    game_count -= 1

                elif your_choice == '4':
                    save_game()

                elif your_choice == '0':
                    print('See you!\n') #added
                    reset_game()
                    break
            else: #added
                print('\nYour Board is Full')
                print('The Game has ended.\n')
                print_map(board)
                print()
                show_final_score(coin_sum)
                reset_game()
                print()
                break
        else: #added   
            print('\nYou Ran Out of Coin')
            print('The Game has ended.\n')
            print_map(board)
            print()
            show_final_score(coin_sum)
            reset_game()
            print()
            break
    
#added        
# reset game
def reset_game():
    global board
    board = [[" " for _ in range(20)] for _ in range(20)]

# show final score
def show_final_score(num_of_coins):
    total_points=0
    points_dict = count_score(num_of_coins)

    for key in points_dict:
        total_points += sum(points_dict[key])   # loops over the list of numbers in each list('BCH' etc) and adds each number to each other.

    for key in points_dict:
        print(key + ': ', end='')
        print(sum(points_dict[key]))    # prints each buildings' scores

    print('Final Total Score: '+str(total_points))
    return total_points

# show total score only
def show_total_score(num_of_coins):
    total_points=0
    points_dict = count_score(num_of_coins)

    for key in points_dict:
        total_points += sum(points_dict[key])   # loops over the list of numbers in each list('BCH' etc) and adds each number to each other.

    return total_points

# check board
def check_full_board():
    global board
    if(any(' ' in x for x in board)): #any ' ' in board
        return True # return true if board have empty space
    else:
        return False

##board - one empty space board for testing of code
##board = [['R', 'I', 'C', 'O', '*', ' ', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*'], \
##       ['R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*'], \
##       ['R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*'], \
##       ['R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*'], \
##       ['R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*'], \
##       ['R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*'], \
##       ['R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*'], \
##       ['R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*'], \
##       ['R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*'], \
##       ['R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*'], \
##       ['R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*'], \
##       ['R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*'], \
##       ['R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*'], \
##       ['R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*'], \
##       ['R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*'], \
##       ['R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*'], \
##       ['R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*'], \
##       ['R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*'], \
##       ['R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*'], \
##       ['R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*', 'R', 'I', 'C', 'O', '*']]


'''---------------------Start Game---------------------'''

while True:
    user_input = display_main_menu()
    if (user_input == '1'):      
        random_build1, random_build2 = play_game_build_building()  # get the 2 random buildings for the start of the game
        start_new_game(random_build1, random_build2)
    elif (user_input == '2'):
        print('load game')
    elif (user_input == '3'):
        print('display high score')
    elif (user_input == '0'):
        print('Exiting game...')
        break
    else:
        print('Please enter a valid input')
