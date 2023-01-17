import numpy as np
board = np.zeros((8,8), dtype=int)
for i in range(0,8, 2):
    for j in range(0,8, 2):
        board[i][j] = 1
for i in range(1,8, 2):
    for j in range(1,8, 2):
        board[i][j] = 1
letters = "abcdefgh"
letters = [letter for letter in letters]
while True:
    square = [0,0]
    inp = str(input("Input chess square in form XN e.g. A1\n>>"))
    if len(inp) != 2:
        print("Input two characters only")
    elif inp[0].lower() not in letters:
        print("Invalid letter")
    elif inp[1] not in "12345678":
        print("Invalid number")
    else:
        x = letters.index(inp[0].lower())
        y = int(inp[1]) - 1
        if board[x,y] == 1:
            print("Black")
        else:
            print("White")