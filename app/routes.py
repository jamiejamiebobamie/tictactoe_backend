from flask import render_template, flash, redirect, url_for
from app import app

from app.utils.general import sanitize_input, convert_array_to_return_board_string
from app.utils.rand import pick_random_move, get_available_moves
from app.utils.suggest import convert_csv_to_Q, convert_input_to_keys, get_index_of_max

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

# suggest random move
@app.route('/api/v1/rand/turn/<turn>/board/<board>')
def random_move(turn, board):
    turn, board, ok = sanitize_input(turn,board)
    index = pick_random_move(board)
    if index > -1:
        board[index] = turn
    board = convert_array_to_return_board_string(board)
    return board

@app.route('/api/v1/turn/<turn>/board/<board>', methods=['GET'])
def suggest_move(turn,board):

    opponent_LOOKUP = {'x':'o','o':'x'}

    file_path = 'Q.csv'
    Q = convert_csv_to_Q(file_path)

    turn, board, ok = sanitize_input(turn, board)

    # the Q is built with arbitrary player labels: "True" and "False"
        # as opposed to 'x' and 'o'.
    # as a result, it might be useful to lookup both instances in the Q
        # for the best move.
    if ok:
        lookup_keys = convert_input_to_keys(turn, board)
    else:
        return render_template('404.html'), 404

    valid_moves0 = Q.get(lookup_keys[0],False)
    valid_moves1 = Q.get(lookup_keys[1],False)

    # if both entries are in the dictionary, find the best possible move from
        # both.
    if valid_moves0 and valid_moves1:

        LOOKUP = {}

        index0 = get_index_of_max(valid_moves0)
        max_from_false = valid_moves0[index0]
        LOOKUP[max_from_false] = (index0, valid_moves0)

        index1 = get_index_of_max(valid_moves1)
        max_from_true = valid_moves1[index1]
        LOOKUP[max_from_true] = (index1, valid_moves1)

        max_move = max(max_from_false, max_from_true)
        # determine which board has the max_move
        (max_move_index, _) = LOOKUP[max_move]

        board = list(board)
        board[max_move_index] = turn

    # if only False's entry is in the dictionary, get the max.
    elif valid_moves0:
        max_move_index = get_index_of_max(valid_moves0)
        # convert tuple to list
        board = list(board)
        board[max_move_index] = turn

    # if only True's entry is in the dictionary, get the max.
    elif valid_moves1:
        max_move_index = get_index_of_max(valid_moves1)
        # convert tuple to list
        board = list(board)
        board[max_move_index] = turn

    board = convert_array_to_return_board_string(board)

    return board
#
# def sanitize_input(turn, board):
#     """Sanitizes the input and checks for errors."""
#     ok = False
#
#     if len(turn) > 1:
#         return turn, board, ok
#
#     turn = turn.lower()
#
#     if turn != 'x' and turn != 'o':
#         return turn, board, ok
#
#     board = [space.lower() if space != "!" else None for space in board]
#
#     if len(board) > 9:
#         return turn, board, ok
#
#     if len(board) < 9:
#         num_trailing_spaces = 9 - len(board)
#         trailing_empty_spaces = num_trailing_spaces * [None]
#         board += trailing_empty_spaces
#
#     ok = True
#
#     return turn, board, ok
#
# def get_index_of_max(iterable):
#     """Return the first index of one of the maximum items in the iterable."""
#     max_i = -1
#     max_v = float('-inf')
#
#     for i, iter in enumerate(iterable):
#         temp = max_v
#         max_v = max(iter,max_v)
#         if max_v != temp:
#             max_i = i
#
#     return max_i
#
# def convert_array_to_return_board_string(board):
#     """Converts an array of 'x','o', None into a string of 'x','o','!'
#     """
#     board = [space if space != None else '!' for space in board]
#     board = ''.join(board)
#     return board
#
# def pick_random_move(board):
#     """Takes in an array_board and returns a random index in that
#     board that contains None."""
#     possible_moves = get_available_moves(board)
#     number_of_possible_moves = len(possible_moves)
#
#     if number_of_possible_moves < 1:
#         return -1
#
#     random_index_into_possible_moves = random.randint(0,
#                                                 number_of_possible_moves-1)
#
#     return possible_moves[random_index_into_possible_moves]
#
# def get_available_moves(board):
#     """Return an array of board positions/indices that contain "None"."""
#     possible_moves = []
#     for i, board_position in enumerate(board):
#         if board_position == None:
#             possible_moves.append(i)
#
#     return possible_moves
#
# def convert_input_to_keys(turn, board):
#     """There's definitely a more pythonic way of writing this."""
#     bit_turn1 = True
#     board_state1 = []
#     for space in board:
#         if space == turn:
#             board_state1.append(1)
#         elif space != None:
#             board_state1.append(0)
#         else:
#             board_state1.append(None)
#
#     bit_turn0 = False
#     board_state0 = []
#     for space in board:
#         if space == turn:
#             board_state0.append(0)
#         elif space != None:
#             board_state0.append(1)
#         else:
#             board_state0.append(None)
#
#     return [(bit_turn0, tuple(board_state0)), (bit_turn1, tuple(board_state1))]
#
# def get_index_of_max(iterable):
#     """
#     Return the first index of one of the maximum items in the iterable.
#     """
#     max_i = -1
#     max_v = float('-inf')
#
#     for i, iter in enumerate(iterable):
#         temp = max_v
#         max_v = max(iter,max_v)
#         if max_v != temp:
#             max_i = i
#
#     return max_i
#
# def convert_csv_to_Q(file_path):
#     """Converts a .csv file to a dictionary."""
#     with open(file_path) as csv_file:
#         reader = csv.reader(csv_file)
#         Q = dict()
#         for row in reader:
#
#             turn = row[0][1]
#             if turn == "T":
#                 turn = True
#             else:
#                 turn = False
#
#             key_list = row[0][2:-1].split(",")
#             board = []
#             for i, entry in enumerate(key_list):
#                 for char in entry:
#                     if char == '1':
#                         board.append(1)
#                         break
#                     elif char == '0':
#                         board.append(0)
#                         break
#                     elif char == 'N':
#                         board.append(None)
#                         break
#
#             board_state = tuple(board)
#
#             key = (turn, board_state)
#
#             value = list()
#             i = 1
#             while i < len(row):
#                 new_value = float(row[i])
#                 value.append(new_value)
#                 i+=1
#
#             Q.update( {key: value} )
#
#     return Q
