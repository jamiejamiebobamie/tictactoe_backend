def sanitize_input(turn, board):
    """Sanitizes the input and checks for errors."""
    ok = False

    if len(turn) > 1:
        return turn, board, ok

    turn = turn.lower()

    if turn != 'x' and turn != 'o':
        return turn, board, ok

    board = [space.lower() if space != "!" else None for space in board]

    if len(board) > 9:
        return turn, board, ok

    if len(board) < 9:
        num_trailing_spaces = 9 - len(board)
        trailing_empty_spaces = num_trailing_spaces * [None]
        board += trailing_empty_spaces

    ok = True

    return turn, board, ok

def convert_array_to_return_board_string(board):
    """Converts an array of 'x','o', None into a string of 'x','o','!'
    """
    board = [space if space != None else '!' for space in board]
    board = ''.join(board)
    return board
