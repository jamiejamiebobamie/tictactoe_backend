from flask import Flask, render_template, flash, redirect, url_for
from app import app
from flask_cors import CORS, cross_origin
from flask_talisman import Talisman
import random


# public API, allow all requests *
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# redirects http traffic to use https
# Talisman(app)

from app.utils.general import sanitize_input, convert_array_to_return_string
from app.utils.rand import pick_random_move, get_available_moves
from app.utils.suggest import convert_csv_to_Q, convert_input_to_key, get_index_of_max, get_available_moves, check_winner, get_indices_of_max, compute_R, convert_Q_key_to_string_array

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

    file_path = 'Q.csv'
    Q = convert_csv_to_Q(file_path)

    turn, board, ok = sanitize_input(turn, board)

    winner = None

    if ok:
        key = convert_input_to_key(turn, board)
        state = key
        turn, board_state = state

        # check that there isn't a winner
        winner = check_winner(board_state)
        if winner == None:
            # check to see if are any immediate winning or blocking moves
            immediate_rewards = compute_R(state)
            if max(immediate_rewards) > 0:
                move_here = get_index_of_max(immediate_rewards)
            else:
                indices_possible_moves = get_available_moves(board_state)
                # test to see if the state is in the Q.
                valid_state = Q.get(state, False)
                if valid_state:
                    rewards_of_moves = []
                    for index in indices_possible_moves:
                        rewards_of_moves.append(valid_state[index])
                    best_moves = get_indices_of_max(rewards_of_moves)
                    move_here = random.choice(best_moves)
                else:
                    move_here = random.choice(indices_possible_moves)
            board = list(board_state)
            board[move_here] = int(turn)
            board = convert_Q_key_to_string_array(board)

    board = convert_array_to_return_string(board)

    return { "board" : board, "winner": str(winner)}
