import csv

def convert_csv_to_Q(file_path):
    """Converts a .csv file to a dictionary."""
    with open(file_path) as csv_file:
        reader = csv.reader(csv_file)
        Q = dict()
        for row in reader:

            turn = row[0][1]
            if turn == "T":
                turn = True
            else:
                turn = False

            key_list = row[0][2:-1].split(",")
            board = []
            for i, entry in enumerate(key_list):
                for char in entry:
                    if char == '1':
                        board.append(1)
                        break
                    elif char == '0':
                        board.append(0)
                        break
                    elif char == 'N':
                        board.append(None)
                        break

            board_state = tuple(board)

            key = (turn, board_state)

            value = list()
            i = 1
            while i < len(row):
                new_value = float(row[i])
                value.append(new_value)
                i+=1

            Q.update( {key: value} )

    return Q

def convert_input_to_keys(turn, board):
    """Converts the sanitized input into dictionary keys in the Q.

    Sanitized input = 'x', ['x','o','x', None, 'o', None, None, None, None]
    Dictionary keys =
                      (True, (1,0,1, None, 0, None, None, None, None))
                      (False, (0,1,0, None, 1, None, None, None, None))
    """
    bit_turn1 = True
    board_state1 = []
    for space in board:
        if space == turn:
            board_state1.append(1)
        elif space != None:
            board_state1.append(0)
        else:
            board_state1.append(None)

    bit_turn0 = False
    board_state0 = []
    for space in board:
        if space == turn:
            board_state0.append(0)
        elif space != None:
            board_state0.append(1)
        else:
            board_state0.append(None)

    return [(bit_turn0, tuple(board_state0)), (bit_turn1, tuple(board_state1))]

def get_index_of_max(iterable):
    """Return the first index of one of the maximum items in the iterable."""
    max_i = -1
    max_v = float('-inf')

    for i, iter in enumerate(iterable):
        temp = max_v
        max_v = max(iter,max_v)
        if max_v != temp:
            max_i = i

    return max_i
