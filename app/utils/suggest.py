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

def convert_input_to_key(turn, board):
    """Converts the sanitized input into dictionary keys in the Q.

    Sanitized input = 'x', ['x','o','x', None, 'o', None, None, None, None]
    Dictionary keys =
                      (True, (1,0,1, None, 0, None, None, None, None))
    """
    turn_LOOKUP = {'x':1,'o':0}

    board_state = []
    for space in board:
        converted = turn_LOOKUP.get(space, None)
        board_state.append(converted)

    key = (bool(turn_LOOKUP[turn]), tuple(board_state))

    return key

def convert_Q_key_to_string_array(board):
    """Converts the sanitized input into dictionary keys in the Q.

    Sanitized input = 'x', ['x','o','x', None, 'o', None, None, None, None]
    Dictionary keys =
                      (True, (1,0,1, None, 0, None, None, None, None))
    """
    LOOKUP = {1:'x', 0:'o'}
    string_array = []
    for space in board:
        converted = LOOKUP.get(space, '!')
        string_array.append(converted)

    return string_array

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

def get_indices_of_max(iterable):
    """Return the max indices of the iterable."""

    max_indices = []
    max_v = float('-inf')
    ACCEPTABLE_DIFFERENCE = 1 # hyperparameter

    for i, iter in enumerate(iterable):
        difference = max_v - iter
        squared_difference = difference*difference
        if squared_difference < ACCEPTABLE_DIFFERENCE:
            max_indices.append(i)
        else:
            temp = max_v
            max_v = max(iter,max_v)
            if max_v != temp:
                max_indices = []
                max_i = i
                max_indices.append(max_i)

    return max_indices

def check_winner(board_state):
    """
        Iterates over the board spaces,
        Recording the indices of 1's (1) and 0's (0) in two sets.

        Iterates through the winning combinations in WINNERS
        to see if there is a winner.

        Returns 1, 0, or -1 if True wins, False wins,
        or if there is a tie, respectively.

        Returns None if there is no winner or tie.

        (True and False can represent X's or O's in the game
        and either True or False can go first.)
    """

    # the indices of the winning positions.
    WINNERS = set()
    WINNERS.add((0,1,2))
    WINNERS.add((3,4,5))
    WINNERS.add((6,7,8))
    WINNERS.add((0,3,6))
    WINNERS.add((1,4,7))
    WINNERS.add((2,5,8))
    WINNERS.add((0,4,8))
    WINNERS.add((2,4,6))

    indices_ones = set()
    indices_zeroes = set()

    # iterate over board spaces. record indices in sets.
    for i, board_position in enumerate(board_state):
        if board_position == 1:
            indices_ones.add(i)
        elif board_position == 0:
            indices_zeroes.add(i)

    # iterate through the set of winner tuples.
    # for each item in a winning configuration, check
    # if the item is contained in one of the sets.
    for winner in WINNERS:
        One_count = 0
        Zero_count = 0
        for w in winner:
            if w in indices_ones:
                One_count += 1
            elif w in indices_zeroes:
                Zero_count += 1

        # 1 wins
        if One_count == 3:
            return 1
        # 0 wins
        elif Zero_count == 3:
            return 0

    # tie
    return -1 if len(indices_ones) + len(indices_zeroes) == len(board_state) else None


def compute_R(state):
    """
    Compute the rewards array which signifies the rewards for the given board
    state and player's turn. "Immediate gratification."

    Input:
        state:
            (True, (None,None,None,1,1,0,1,0,None))

    Output:
        an array of integers, the largest integer being the best move.

    """
    turn, board_state = state

    # possible actions given current state
    Reward_Array = []

    # look for empty board_positions
    for i, board_position in enumerate(board_state):
        if board_position == None:
            Reward_Array.append(0)
        else:
            Reward_Array.append(-1)

    # builds up the values in the rewards array by iterating through the board
    # and testing if either the opponent or the player is one move away from
    # winning
    for i, reward in enumerate(Reward_Array):
        if reward != -1:

            test_board_state = list()
            # deep copy needed.
            for j, board_position in enumerate(board_state):
                if j != i:
                    test_board_state.append(board_position)
                else:
                    test_board_state.append(int(turn))

            possible_winner = check_winner(test_board_state)

            # if the possible winner equals the person's who turn it is.
            if possible_winner == turn:
                Reward_Array[i] += 100 # LOG WINNING MOVE.

            test_board_state = list()
            # deep copy needed.
            for j, board_position in enumerate(board_state):
                if j != i:
                    test_board_state.append(board_position)
                else:
                    test_board_state.append(int(not turn))

            possible_winner = check_winner(test_board_state)

            # if the possible winner equals the other guy.
            if possible_winner == (not turn):
                Reward_Array[i] += 50 # BLOCK THE OTHER PLAYER.

    return Reward_Array
