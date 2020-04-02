import random

def pick_random_move(board):
    """Takes in an array_board and returns a random index in that
    board that contains None."""
    possible_moves = get_available_moves(board)
    number_of_possible_moves = len(possible_moves)

    if number_of_possible_moves < 1:
        return -1

    random_index_into_possible_moves = random.randint(0,
                                                number_of_possible_moves-1)

    return possible_moves[random_index_into_possible_moves]

def get_available_moves(board):
    """Return an array of board positions/indices that contain "None"."""
    possible_moves = []
    for i, board_position in enumerate(board):
        if board_position == None:
            possible_moves.append(i)

    return possible_moves
