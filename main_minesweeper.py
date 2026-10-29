import random
from collections import deque

# Default of the game
row = 9
col = 9
bombs_number = 10
failed = False
first_click = False
arah_x = [-1, 0, 1, -1, 1, -1, 0, 1]
arah_y = [-1, -1, -1, 0, 0, 1, 1, 1]

# Generating the board
board = [["#" for _ in range(col)] for _ in range(row)]
actual_board = [["-" for _ in range(col)] for _ in range(row)]
finish = [["-" for _ in range(col)] for _ in range(row)]

for line in board:
    print(" ".join(line))

# Random placing for the bomb
bombs_coords = list()
for _ in range (bombs_number):

    temp_row, temp_col = random.randint(0, row - 1), random.randint(0, col - 1)

    # If the bomb located at the same place, resuffle the coords
    while ([temp_row, temp_col] in bombs_coords):
        temp_row, temp_col = random.randint(0, row - 1), random.randint(0, col - 1)

    bombs_coords.append([temp_row, temp_col])
    actual_board[temp_row][temp_col] = '*'
    finish[temp_row][temp_col] = '*'

# Generate actual_board and finish condition
def valid_coords(x, y):
    if(0 <= x < row and 0 <= y < col):
        return True
    return False

for i in range (row):
    for j in range (col):

        if(actual_board[i][j] == '*'):
            continue
        count = 0
        
        for k in range (8):
            coor_x = i + arah_x[k]
            coor_y = j + arah_y[k]
            if (valid_coords(coor_x, coor_y)):
                #print("coords = ",coor_x, coor_y)
                if(actual_board[coor_x][coor_y] == '*'):
                    count += 1
    
        actual_board[i][j] = str(count)
        finish[i][j] = str(count)
        if(count == 0):
            finish[i][j] = '.'

# First click condition
def safe_for_first_click(x, y):
    global actual_board
    global finish
    global bombs_coords
    count_bomb_at_the_first_click = 0
    blocked_coords = []

    # is the click coords is bomb 
    if (actual_board[x][y] == '*'):
        count_bomb_at_the_first_click += 1 
        bombs_coords.remove([x, y]) # delete the bomb from the list
    
    blocked_coords.append([x, y])
    actual_board[x][y] == '0' # because we will remove the bomb arround it also
    finish[x][y] == '.'

    # also check around it
    for i in range (8):
        new_x, new_y = x + arah_x[i], y + arah_y[i]

        if(valid_coords(new_x, new_y)):
            blocked_coords.append([new_x, new_y]) # make sure its valid first

            if(actual_board[new_x][new_y] == '*'):
                count_bomb_at_the_first_click += 1
                bombs_coords.remove([new_x, new_y]) # also delete it

                # also change the count 
                for j in range (8):
                    new_x2, new_y2 = new_x + arah_x[j], new_y + arah_y[j]

                    if(valid_coords(new_x2, new_y2)):
                        
                        if(actual_board[new_x2][new_y2] != '*'):
                            actual_board[new_x2][new_y2] = str(int(actual_board[new_x2][new_y2]) - 1)
                        
                            if(finish[new_x2][new_y2] == '1'):
                                finish[new_x2][new_y2] = '.'
                            elif(finish[new_x2][new_y2].isdigit()):
                                finish[new_x2][new_y2] = str(int(finish[new_x2][new_y2]) - 1)

    # rerandomize the coords, also make sure it wasnt in the blocked coords
    for _ in range (count_bomb_at_the_first_click):
        temp_row, temp_col = random.randint(0, row - 1), random.randint(0, col - 1)

        while([temp_row, temp_col] in blocked_coords or [temp_row, temp_col] in bombs_coords):
            temp_row, temp_col = random.randint(0, row - 1), random.randint(0, col - 1)
        
        bombs_coords.append([temp_row, temp_col])
        actual_board[temp_row][temp_col] = '*'
        finish[temp_row][temp_col] = '*'

        # Update the number of the cell visit his neighbor one by one
        for i in range (8):
            new_x, new_y = temp_row + arah_x[i], temp_col + arah_y[i]

            if(valid_coords(new_x, new_y)):

                if(actual_board[new_x][new_y] != '*'):
                    actual_board[new_x][new_y] = str(int(actual_board[new_x][new_y]) + 1)

                    if(finish[new_x][new_y] == '.'):
                        finish[new_x][new_y] = '1'
                    else:
                        finish[new_x][new_y] = str(int(finish[new_x][new_y]) + 1)

    # Update the count bomb arround the click (the coords in blocked_coords)
    for temp_x, temp_y in blocked_coords:
        count = 0

        for i in range (8):
            new_x, new_y = temp_x + arah_x[i], temp_y + arah_y[i]

            if(valid_coords(new_x, new_y)):

                if ([new_x, new_y] in bombs_coords):
                    count += 1

                for j in range (8):
                    new_x2, new_y2 = new_x + arah_x[j], new_y + arah_y[j]

                    if(valid_coords(new_x2, new_y2) and not [new_x2, new_y2] in blocked_coords):

                        if([new_x2, new_y2] not in bombs_coords):
                        
                            count2 = 0
                            for k in range (8):
                                new_x3, new_y3 = new_x2 + arah_x[k], new_y2 + arah_y[k]

                                if(valid_coords(new_x3, new_y3)):

                                    if(actual_board[new_x3][new_y3] == '*'):
                                        count2 += 1
                                
                                actual_board[new_x2][new_y2] = str(count2)
                                if(count2 == 0):
                                    finish[new_x2][new_y2] = '.'
                                else:
                                    finish[new_x2][new_y2] = str(count2)

        actual_board[temp_x][temp_y] = str(count) # write it back
        if(count == 0): 
            finish[temp_x][temp_y] = '.'
        else:
            finish[temp_x][temp_y] = str(count)

# Subprogram, Procedure, and Function
def click(x, y):
    global board
    global actual_board
    global failed
    global first_click

    visited = [[False for _ in range(col)] for _ in range(row)]

    # Let the first click open the cell
    if(not first_click):
        safe_for_first_click(x, y)
    first_click = True

    # First Condition "is the x, y is a bomb"
    if(actual_board[x][y] == '*'):
        #print(bomb_reveal(board))
        failed = True
        print("Game Over!, HAHAHAHAHAHAHAHA")
        return
    
    bfs = deque()
    bfs.append([x, y])
    
    # If isnt a BOMB
    while bfs:

        cur_x, cur_y = bfs.popleft()

        visited[cur_x][cur_y] = True

        # if the adjacent are bomb, stop the recursive from that Node
        if(actual_board[cur_x][cur_y].isdigit() and actual_board[cur_x][cur_y] != '0'):
            board[cur_x][cur_y] = actual_board[cur_x][cur_y]
            continue

        # Change The Value
        if(actual_board[cur_x][cur_y] == '0'):
            board[cur_x][cur_y] = '.'

        for i in range (8):
            new_x = cur_x + arah_x[i]
            new_y = cur_y + arah_y[i]

            if(valid_coords(new_x, new_y)  and not(visited[new_x][new_y])): # new index valid
                bfs.append([new_x, new_y])

def flag(x, y):
    global board
    if(board[x][y] == '#'): # Only unexposed cell can be flagged 
        board[x][y] = 'f'

def menang():
    global board
    global finish
    for i in range (row):
        for j in range (col):
            #negasi dari (board == finish atau bom === flag)
            #board != finish and board != flag
            if(finish[i][j] == '*' and (board[i][j] == 'f' or board[i][j] == '#')):
                #ini boleh
                continue
            if(board[i][j] != finish[i][j]):
                return False
    
    return True


#Main Interaction
def main_interaction():
    print("=== Welocome to Minesweeper ===")
    masukan = input("press [Enter] to play: ")

    while ((masukan == "")):

        #print current board
        for line in board:
            print(" ".join(line))

        instruction = input("type 'f' to FLAG! or 'c' to CLICK!: ")

        while (instruction != "f" and instruction != "c"):
            print("Please type a valid action..")
            instruction = input("type 'f' to FLAG! or 'c' to CLICK!: ")

        while True:
            try:
                temp_row, temp_col = map(int, input("type the coordinate 'r' [space] 'c': ").split())

                break
            
            except TypeError as e:
                print("please type a valid coordinate..")

        if (instruction == "f"):
            flag(temp_row, temp_col)

        elif (instruction == "c"):
            click(temp_row, temp_col)

            if(failed):
                break
        
        else:
            print("type a valid action..")
            continue

        if(menang()):
            for line in board:
                print(" ".join(line))
            print("Congratss!!, good game boys")
            break

        # masukan = input("press [Enter] to continue..")

main_interaction()

"""
# Update 27-10-2026
1. make sure the input are valid (interactions and coordinates), if not ask for the input again
2. safe for the first click and at least open the map by 3 * 3 - adj cell tha out of board

Step by step:

1. give all the default parameters
2. put the bomb by random.randint
3. mark bomb as '*' in actual_board
4. generate all the adjacent of the bomb
    count the bomb for all 8 direction from that coords
    represent to actual_board by number of adjacent bomb

5. interaction session by typing 'start'
6. ask the player to type 'f' for flag and 'c' for click
    *click and flag are prosedure (didnt return a value)
    if the interaction is f -> just change that cords by 'f'
    if the interaction is c 
        -> chect it fist is it a bomb
            -> if the bomb, revealed all the bomb (revelaing the actual board)
            -> else check for all adjacent and do BFS
        
7. The games end if "board == finish" or "bomb were clicked"
*finish is a board for the win condition (contain bom, number adjacent, zero)

Note:
- board' used as the main board as the POV board from player
- actual_board' used as the board where store the actual adjacent BOMB of it 0 for nothing
- finish' the board for finish condition, so to find out 'is the games end' just ask is(board == finish)
- the board, actual_board, finish, direction are 0-based list
- '*' use for bomb, '#' use for non revealed land, '(any nember)' represent the number of adjacent bomb

Example:

bombs_coords = [[1, 3], [2, 1] [2, 6], [3, 1], [5, 5], [5, 6], [6, 1], [8, 2], [8, 7]]

board: 
    #########
    #########
    #########
    #########
    #########
    #########
    #########
    #########
    #########

actual_board:
    001110000
    112*11110
    2*3111*10
    2*2001110
    111012210
    11101**10
    1*1012210
    122100111
    01*1001*1

finish:
    ..111....
    112*1111.
    2*3111*1.
    2*2..111. 
    111.1221.
    111.1**1.
    1*1.1221.
    1221..111
    .1*1..1*1

"""
