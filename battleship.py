from random import randint

print "What size grid would you like to play?"
# input for how many vertical colums
x = int(raw_input("> "))
print "by"
# input for how many horizontal rows
y = int(raw_input("> "))

# building base row
board = []
for i in range(0, y):
    board.append(["O"] * x)

# builds entire board
def print_board(board):
    for row in board:
        print " ".join(row)

print_board(board)

# program generated "ship" location
def random_row(board):
    return randint(0, len(board[0])-1)

def random_col(board):
    return randint(0, len(board[0])-1)

ship_row = random_row(board)
ship_col = random_col(board)
# print ship_row, ship_col

# Game Loop
for turn in range(4):
    print "Turn", turn + 1
    guess_row = int(raw_input("Guess Row:"))
    guess_col = int(raw_input("Guess Column:"))
    if guess_row == ship_row and guess_col == ship_col:
       print "Congratulations! You sank my battleship!", "Game Over"
       break
    else:
        if guess_row not in range(0, x) or guess_col not in range(0, y):
            print "Oops, that's not even in the ocean."
            print_board(board)
        elif board[guess_row][guess_col] == "X":
            print "You guessed that one already."
            print_board(board)
        else:
            print "You missed my battleship!"
            board[guess_row][guess_col] = "X"
            print_board(board)
            if turn == 3:
                print "Game Over"
