"""
Tic Tac Toe Player
"""

from cmath import inf
import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    move_count = [item for sublist in board for item in sublist].count(EMPTY)
    return (O if move_count % 2 == 0 else X)

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if col == EMPTY:
                actions.add((i, j))

    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)

    return new_board
  
def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    game_winner = EMPTY

    # Rows
    for row in board:
        if row.count(X) == 3:
            game_winner = X
        elif row.count(O) == 3:
            game_winner = O

    flatten_board = [item for sublist in board for item in sublist]

    # Cols
    if game_winner == EMPTY:
        for c in range(0,3,1):
            col_check = []
            
            for c1 in range(c,9,3):
                col_check.append(flatten_board[c1])

            if col_check.count(X) == 3:
                game_winner = X
                break
            elif col_check.count(O) == 3:
                game_winner = O
                break

    # Diags
    if game_winner == EMPTY:
        diag_check = []
        for c1 in range(0,3,1):
            diag_check.append(flatten_board[c1 * 3 + c1])

        if diag_check.count(X) == 3:
            game_winner = X
        elif diag_check.count(O) == 3:
            game_winner = O

    if game_winner == EMPTY:
        diag_check = []

        for c1 in range(3,0,-1):
            diag_check.append(flatten_board[c1 * 3 - c1])

            if diag_check.count(X) == 3:
                game_winner = X
            elif diag_check.count(O) == 3:
                game_winner = O

    return game_winner

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If someone won or the board is full (no actions left)
    return winner(board) != EMPTY or len(actions(board)) == 0

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)

    return (1 if game_winner == X else (-1 if game_winner == O else 0))


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    move = (0, 0)

    avaliable_actions = actions(board)

    if (player(board) == 'X'):
        value = -inf

        while len(avaliable_actions) > 0:
            # Make a move
            test_move = avaliable_actions.pop()
            new_board = result(board, test_move)
            move_score = min_score(new_board, move_score, inf)

            if move_score > value:
                move = test_move
                value = move_score

    else:
        value = inf
        
        while len(avaliable_actions) > 0:
            # Make a move
            test_move = avaliable_actions.pop()
            new_board = result(board, test_move)
            move_score = max_score(new_board, -inf, move_score)

            if move_score < value:
                move = test_move
                value = move_score

    return move


def max_score(board, alpha, beta):

    if terminal(board):
        return utility(board)


    avaliable_actions = actions(board)

    value = -inf

    while len(avaliable_actions) > 0:
        # Make a move
        test_move = avaliable_actions.pop()
        new_board = result(board, test_move)
        move_score = min_score(new_board, alpha, beta)

        if move_score > value:
            value = move_score
        
        if move_score < beta:
            break

    return value


def min_score(board, alpha, beta):

    if terminal(board):
        return utility(board)

    avaliable_actions = actions(board)

    value = inf
    while len(avaliable_actions) > 0:
        # Make a move
        test_move = avaliable_actions.pop()
        new_board = result(board, test_move)
        move_score = max_score(new_board, alpha, beta)

        if move_score < beta:
            value = move_score

        if move_score > alpha:
            break

    return value




