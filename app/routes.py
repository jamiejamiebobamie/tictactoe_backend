from flask import render_template, flash, redirect, url_for
from app import app
import random
# from ./utils import sanitizeInput, convertInputToKeys, suggest_move

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/api/v1/rand/turn/<turn>/board/<board>')
def rand():
    turn, board, ok = sanitizeInput(turn,board)
    if ok:
        lookup_keys = convertInputToKeys(turn,board)
    else:
        return render_template('404.html'), 404
    index = pick_random_move(lookup_keys[0])
    if index > -1:
        board[index] = turn
    return board

@app.route('/api/v1/turn/<turn>/board/<board>', methods=['GET'])
def returnUpdatedBoard(turn,board):
    file_path = './Q.csv'
    turn, board, ok = sanitizeInput(turn,board)
    if ok:
        lookup_keys = convertInputToKeys(turn,board)
    else:
        return render_template('404.html'), 404
    Q = convert_csv_to_Q(file_path)
    board_index, ok = suggest_move(lookup_keys,Q)
    if ok:
        board[board_index] = turn
    return board
