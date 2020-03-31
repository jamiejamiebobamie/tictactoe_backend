def suggest_move(Q, key):
    """
        Given a trained brain, Q, and a key:
            (True, (0, 1, 0, 1, None, None, None, None, 0))
        recieve an index of the board for the suggested next move.
    """
    board_state = key[1]
    winner = check_winner(board_state)
    # there is already a winner.
    if winner != None:
        return -1

    max_indices = []
    max_choice = float("-inf")

    # test to see if the move is in the dictionary.
    valid = Q.get(state, None)

    # if it is not, add an empty set of actions to the brain.
    # this is a fail safe. this should never happen.
    if not valid:
        empty_actions = [0,0,0,0,0,0,0,0,0]
        new_entry = {state: empty_actions}
        Q.update(new_entry)
        print("NEW STATE ADDED! CHECK CODE. SOMETHING IS WRONG.")
        print(new_entry)

    Q_reward_array = Q[state]

    # NOTE: this block of code seems to only affect the instances when both
        # players are using the AI. the built model switches from 100% ties
        # to a 100% wins for the player who went first when this block is
        # commented out, leading me to think there are errors in how the Q
        # model is built. it *should* be contentious when both are using the
        # AI.
    max_Q_action = int(max(Q_reward_array))
    # if the Q table is empty (all zeroes)
    # fallback on the Rewards Array.
    if max_Q_action == 0:
        R = compute_R(state)
        index_of_max_R = get_index_of_max(R)
        return index_of_max_R

    # find all of the max positions from the Q for a given state.
    for i, choice in enumerate(Q_reward_array):
        if board_state[i] == None:
            temp = max_choice
            max_choice = max(max_choice, choice)
            if temp != max_choice:
                max_indices = []
                max_indices.append(i)
            if choice == max_choice:
                max_indices.append(i)

    return random.choice(max_indices)

def get_index_of_max(iterable):
    """
    Return the first index of one of the maximum items in the iterable.
    """
    max_i = -1
    max_v = float('-inf')

    for i, iter in enumerate(iterable):
        temp = max_v
        max_v = max(iter,max_v)
        if max_v != temp:
            max_i = i

    return max_i

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
    if len(indices_ones) + len(indices_zeroes) == len(board_state):
        return -1
