def pick_random_move(key):
    """
    Input:
         a Q key:
            (True, (0,1,0,None,None,None,None,None,None))
         a tuple of the player's turn and board's state
    Output:
         a random move from the possibilities.
    """
    key[1] = board_state
    possible_moves = get_available_moves(board_state)
    number_of_possible_moves = len(possible_moves)

    if number_of_possible_moves < 1:
        return -1

    random_index_into_possible_moves = random.randint(0,
                                                number_of_possible_moves-1)

    return possible_moves[random_index_into_possible_moves]

def get_available_moves(board_state):
    """
    Return an array of board positions/indices that contain "None".
    Input:
         board_state:
            (0,1,0,None,None,None,None,None,None)
         a tuple of the board's state
    Output:
         an array of board positions/indices of possible moves:
            [3,4,5,6,7,8]
    """
    possible_moves = []
    for i, board_position in enumerate(board_state):
        if board_position == None:
            possible_moves.append(i)

    return possible_moves
