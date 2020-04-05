from flask import render_template, flash, redirect, url_for
from app import app
from flask_cors import CORS, cross_origin
# cors = CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

from app.utils.general import sanitize_input, convert_array_to_return_board_string
from app.utils.rand import pick_random_move, get_available_moves
from app.utils.suggest import convert_csv_to_Q, convert_input_to_keys, get_index_of_max

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

# suggest random move
@app.route('/api/v1/rand/turn/<turn>/board/<board>')
@cross_origin()
def random_move(turn, board):
    turn, board, ok = sanitize_input(turn,board)
    index = pick_random_move(board)
    if index > -1:
        board[index] = turn
    board = convert_array_to_return_board_string(board)
    return { "board" : board }

@app.route('/api/v1/turn/<turn>/board/<board>', methods=['GET'])
@cross_origin()
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

    return { "board" : board }
