def sanitizeInput(turn,board):
    ok = True
    if len(turn) > 1:
        turn = turn[0]
    turn = turn.lower()
    board = [ space.lower() if space != "!" else None for space in board]
    if len(board) < 9:
        num_trailing_spaces = 9 - len(board)
        trailing_empty_spaces = num_trailing_spaces * [None]
        board += trailing_empty_spaces
    else:
        ok = False

    return turn, board, ok

def convertInputToKeys(turn, board):
    """There's definitely a more pythonic way of writing this."""
    turn0 = False
    board0 = []
    for space in board:
        if space == turn:
            space = int(turn0)
        elif space != None:
            space = int(not turn0)
        board0.append(space)

    turn1 = True
    board1 = []
    for space in board:
        if space == turn:
            space = int(turn1)
        elif space != None:
            space = int(not turn1)
        board1.append(space)

    return [(turn0,tuple(board0)),(turn1,tuple(board1))]

def suggest_move(keys):
    return keys


turn='x'
board='x!o'

turn, board, ok = sanitizeInput(turn,board)
print(convertInputToKeys(turn, board))
# print(suggest_move(keys))
