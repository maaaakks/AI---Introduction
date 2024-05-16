"""
Tic Tac Toe Player
"""

import math
import time

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
    # count number of "X" in the board
    count_X = 0
    count_O = 0
    
    for row in board:
        for cell in row:
            if cell == "X":
                count_X += 1
            if cell == "O":
                count_O += 1

    if count_X > count_O:
        return "O"
    else: 
        return "X"

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_list = set()
    
    for row in range (3):
        for column in range (3):
            if board[row][column] == EMPTY:
                actions_list.add((row, column))
    return actions_list

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    current_player = player(board)
    copy_board = [row[:] for row in board]
    
    if action is not None:
        copy_board[action[0]][action[1]] = current_player
        return copy_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """  
    # Check if a row on the game board contains three identical symbols
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != EMPTY:
            return row[0]
    
    # Check if a columns on the game board contains three identical symbols      
    for col in range (3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != EMPTY:
            return board[0][col]
        
    # Check if a diagonal on the game board contains three identical symbols      
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY:
        return board[0][2]

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check for full board
    if all(cell != EMPTY for row in board for cell in row):
        return True
    
    if winner(board):
        return True
        
def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == "X":
        return 1
    elif winner(board) == "O":
        return -1
    else:
        return 0

#count = 0
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    #global count
    #count = 0
    
    if terminal(board):
        return None
    
    # Option to choose an arbitrary starting action, like the center
    if board == initial_state():
        return (1, 1)

    current_player = player(board)

    if current_player == "X":
        _, action = maxvalue(board, -math.inf, math.inf)
    else:
        _, action = minvalue(board, -math.inf, math.inf)
    return action

def maxvalue(board, alpha, beta):
    global count
    if terminal(board):
        return utility(board), None
    
    v = -math.inf
    best_action = None
    
    for action in actions(board):
        #count += 1
        new_v, _ = minvalue(result(board, action), alpha, beta)
        
        if new_v > v:
            v = new_v
            best_action = action
            
        if v >= beta:
            break
        
        alpha = max(alpha, v)
    
    return v, best_action


def minvalue(board, alpha, beta):
    #global count
    if terminal(board):
        return utility(board), None

    v = math.inf
    best_action = None
    
    for action in actions(board):
        #count += 1
        new_v, _ = maxvalue(result(board, action), alpha, beta)
    
        if new_v < v:
            v = new_v
            best_action = action
            
        if v <= alpha:
            break
        
        beta = min(beta, v)
            
    return v, best_action
    

