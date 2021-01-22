"""
This class is responsible for storing all the information of the current state of
a chess game. Also responsible for determining the valid moves of a chess state 
and keeps a move log.
b / w -> denotes the color of the piece
R     -> rook
N     -> knight
B     -> bishop
Q     -> queen
K     -> king
ex) bK represents a black(b) king(K)
"""
import numpy as np


class GameState():
    def __init__(self):

        # board state from white's starting perspective represented as an 8x8 list
        # the first charecter represents the color of the piece
        # the second charecter represents the type of the piece
        # '..' represents an empty tile
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["..", "..", "..", "..", "..", "..", "..", "..",],
            ["..", "..", "..", "..", "..", "..", "..", "..",],
            ["..", "..", "..", "..", "..", "..", "..", "..",],
            ["..", "..", "..", "..", "..", "..", "..", "..",],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
            ]) 
        self.white_to_move = True
        self.move_log = []             # stack that keeps track of all moves made so far
        self.redo_move_log = []        # stack that keeps track of all moves undo'ed so far to enable the redo move feature
        self.is_first_move = True

    '''
    Takes a move as a param and executes it. Will not work for castling, en passant, or pawn promotion
    '''
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = ".."
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(self.move)
        self.white_to_move = not self.white_to_move
        self.is_first_move = False
    
    '''
    Reverses the last action and adds the reveresed moved to the redo move stack
    '''
    def undo_move(self):
        if len(self.move_log) >= 1:
            move_to_undo = self.move_log.pop()
            self.board[move_to_undo.start_row][move_to_undo.start_col] = move_to_undo.piece_moved
            self.board[move_to_undo.end_row][move_to_undo.end_col] = move_to_undo.piece_captured
            self.white_to_move = not self.white_to_move
            if len(move_log) == 0:
                self.is_first_move = True
            self.redo_move_log.append(move_to_undo)
        else:
            pass

    def redo_move(self):
        if len(self.redo_move_log) >= 1:
            move_to_redo = self.redo_move_log.pop()
            self.board[move_to_redo.start_row][move_to_redo.start_col] = move_to_redo.piece_captured
            self.board[move_to_redo.end_row][move_to_redo.end_col] = move_to_redo.piece_moved
            self.white_to_move = not self.white_to_move
            self.move_log.append(move_to_redo)
        else:
            pass
            

class Move():
    rank_to_row = {"8": 0, "7": 1, "6": 2, "5": 3, "4": 4, "3": 5, "2": 6, "1": 7}
    row_to_rank = {val: key for key, val in rank_to_row.items()}
    file_to_col = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    col_to_file = {val: key for key, val in file_to_col.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

    def get_simple_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        return self.col_to_file[col] + self.row_to_rank[row]


