"""
Tic Tac Toe Player
"""

import math
import numpy as np
from copy import deepcopy

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
    x_count = 0
    o_count = 0

    # if board == initial_state():
    #     return X
    # else:
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == X:
                x_count += 1
            elif board[i][j] == O:
                o_count += 1

    if x_count > o_count:
        return O
    else:
        return X          


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                actions.add((i, j))

    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Cell is not EMPTY!")

    i, j = action
    new_board = deepcopy(board)    
    new_board[i][j] = player(board)

    return new_board

def winner_row(board, player):
    for i in range(len(board)):
        check = np.all(board[i] == player)
        if check:
            return True
    return False

def winner_column(board, player):
    transposed_board = [[row[i] for row in board] for i in range(len(board[0]))]
    for i in range(len(transposed_board)):
        check = np.all(transposed_board[i] == player)
        if check:
            return True
    return False

def winner_diagonal_1(board, player):
    count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if (i == j) & (board[i][j] == player):
                count += 1
    if count == len(board):
        return True
    else:
        return False 

def winner_diagonal_2(board, player):
    count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            row = (len(board)-i-1)
            if (row == j) & (board[i][j] == player):
                count += 1
    if count == len(board):
        return True
    else:
        return False 

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    if winner_row(board, X) | winner_column(board, X) | winner_diagonal_1(board, X) | winner_diagonal_2(board, X):
        return X
    elif winner_row(board, O) | winner_column(board, O) | winner_diagonal_1(board, O) | winner_diagonal_2(board, O):
        return O
    else:
        return None    

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if (winner(board) != None) | len(actions(board)) == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def min_value(board):
    if terminal(board):
        return utility(board)
    else:
        v = np.inf
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v    


def max_value(board):
    if terminal(board):
        return utility(board)
    else:
        v = -np.inf
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v   


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if player(board) == X:
        all_actions = actions(board)
        made_actions = list()
        values = list()
        for action in all_actions:
            values.append(min_value(result(board, action)))
            made_actions.append(action)
        return made_actions[values.index(max(values))]
    elif player(board) == O:
        all_actions = actions(board)
        made_actions = list()
        values = list()
        for action in all_actions:
            values.append(max_value(result(board, action)))
            made_actions.append(action)
        return made_actions[values.index(min(values))]
