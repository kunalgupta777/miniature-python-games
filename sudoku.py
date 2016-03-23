import itertools, random, time
###################################################
def make_board(m=3):
    #Return a random filled m**2 x m**2 Sudoku board.
    n = m**2
    board = [[None for _ in range(n)] for _ in range(n)]

    def search(c=0):
        i, j = divmod(c, n)
        i0, j0 = i - i % 3, j - j % 3 # Origin of mxm block
        numbers = list(range(1, n + 1))
        random.shuffle(numbers)
        for x in numbers:
            if (x not in board[i]                     # row
                and all(row[j] != x for row in board) # column
                and all(x not in row[j0:j0+m]         # block
                        for row in board[i0:i])): 
                board[i][j] = x
                if c + 1 >= n**2 or search(c + 1):
                    return board
        else:
            # No number is valid in this cell: backtrack and try again.
            board[i][j] = None
            return None

    return search()
###################################################
def trans_to_sud(board):
    real_board = []
    real_board.append("  123 456 789")
    real_board.append(" -------------")
    for k in range(9):
        x = str(k+1)+"|"
        for l in range(9):
            x += str(board[k][l])
            if(l == 2 or l == 5):
                x += '|'
        real_board.append(x+'|')
        if(k == 2 or k == 5):
            real_board.append(" |---+---+---|")
    real_board.append(" -------------")
    return real_board
###################################################
def valid_move(move,to_be_filled):
    if(len(move) == 1):
        if(move == 'C' or move == 'c' or move == 'Q' or move == 'q' or move == 'r' or move == 'R'):
            return True
        else:
            return False
    elif(len(move) == 5):
        i,j,k = int(move[0]),int(move[2]),int(move[4])
        if([i,j] in to_be_filled):
            return True
        else:
            return False
    else:
        return False
###################################################
def print_board(sudoku_board):
    for k in sudoku_board:
        for l in k:
            print(l,end = ' ')
        print()
###################################################
def play_game():
    solution_board = make_board(3)
    copy = [[solution_board[x][y] for y in range(9)]for x in range(9)]

    empty_spots = []
    
    for k in range(9):
        x = random.randint(3,6)
        while(x > 0):
            z = random.randint(0,8)
            solution_board[k][z] = "."
            empty_spots.append([k+1,z+1])
            x = x - 1

    sudoku_board = trans_to_sud(solution_board)

    print("Preparing board ",end='')
    time.sleep(1)
    print('.',end=' ')
    time.sleep(1)
    print('.',end=' ')
    time.sleep(1)
    print('.')
    
    print_board(sudoku_board)

    while(True):
        matched = 0
        for kk in range(9):
            for ll in range(9):
                if(str(copy[kk][ll]) == str(solution_board[kk][ll])):
                    matched += 1
        if(matched == 81):
            print("Congratulations ! You've completed the game.")
            print("Would you like to play again ? (Y/N) : ",end = '')
            xx = input()
            if(xx == 'y' or xx == 'Y'):
                play_game()
            else:
                break
        print("Your move : ",end = '')
        move = input()
        while(valid_move(move,empty_spots) == False):
            print("Invalid move !\nYour move : ",end = '')
            move = input()
        if(len(move) == 1):
            if(move == 'r' or move == 'R'):
                play_game()
            elif(move == 'q' or move == 'Q'):
                print("Thanks for playing !")
                break
            else:
                false = []
                for x in range(9):
                    for y in range(9):
                        if(str(solution_board[x][y]) != str(copy[x][y]) and str(solution_board[x][y]) != '.'):
                            false.append('Cell (%d,%d) is filled wrong.' % (x+1,y+1))
                if(len(false) == 0):
                    print("You've done fine till now. No errors ^_^ ")
                else:
                    print("Oops! :( ")
                    time.sleep(1)
                    for line in false:
                        print(line)
        else:
            i,j,x = int(move[0]),int(move[2]),int(move[4])
            i = i-1
            j = j-1
            solution_board[i][j] = str(x)
            print("Making move . . .")
            time.sleep(1)
            sudoku_board = trans_to_sud(solution_board)
            print_board(sudoku_board)
            print("Cells you can edit : ")
            for index in range(len(empty_spots)):
                if(index != len(empty_spots)-1):
                    print(empty_spots[index],end = ' ,')
                else:
                    print(empty_spots[index])
    return      
###################################################
print("Welcome to Sudoku game")
print("Instructions :\n\t1. To fill a number , give input in format 'i j x' (without the quotes) to fill jth column of ith row with x.\n\t2. Press R(or r) and Enter to restart the game.\n\t3. Press C(or c) and Enter to check the sudoku.\n\t4. Press Q(or q) and Enter to quit the game.")
time.sleep(5)
play_game()
