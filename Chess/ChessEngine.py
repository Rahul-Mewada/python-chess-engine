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
import uuid
import Pieces as p

class GameState():
    def __init__(self):

        # board state from white's starting perspective represented as an 8x8 list
        # the first charecter represents the color of the piece
        # the second charecter represents the type of the piece
        # '..' represents an empty tile
        self.string_board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["..", "..", "..", "..", "..", "..", "..", "..",],
            ["..", "..", "..", "..", "..", "..", "..", "..",],
            ["..", "..", "..", "..", "..", "..", "..", "..",],
            ["..", "..", "..", "..", "..", "..", "..", "..",],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
            ]

        

        self.white_to_move = True
        self.move_log = []             # stack that keeps track of all moves made so far
        self.redo_move_log = []        # stack that keeps track of all moves undo'ed so far to enable the redo move feature
        self.is_first_move = True
        self.white_playable_pieces = []
        self.black_playable_pieces = []
        self.captured_pieces = []

        self.board = self.init_board()

    '''
    Converts a board of strings into a board of Pieces and populates the white and black piece arrays
    '''
    def init_board(self):
        piece_dict = {
            "P": lambda row, col, board, color: p.Pawn(row, col, board, color),
            "N": lambda row, col, board, color: p.Knight(row, col, board, color),
            "B": lambda row, col, board, color: p.Bishop(row, col, board, color),
            "Q": lambda row, col, board, color: p.Queen(row, col, board, color),
            "K": lambda row, col, board, color: p.King(row, col, board, color),
            "R": lambda row, col, board, color: p.Rook(row, col, board, color),
        }
        for row in range(0, 8):
            for col in range(0,8):
                piece = self.string_board[row][col]
                if piece != "..":
                    piece_color = piece[0]
                    if piece_color == 'b':
                        piece_color = "black"
                    else:
                        piece_color = "white"
                    piece_type = piece[1]
                    self.string_board[row][col] = piece_dict[piece_type](row, col, self.string_board, piece_color)
                    if piece_color == "black":
                        self.black_playable_pieces.append(self.string_board[row][col])
                    else:
                        self.white_playable_pieces.append(self.string_board[row][col])
        return self.string_board
    
    def change_cords(self, piece, row, col, to_capture):
        piece.row = row
        piece.col = col
        piece.current_sq = (row, col)
        if to_capture:
            piece.is_captured = True

    def do_coords_match(self):
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                piece = self.board[row][col]
                if piece != "..":
                    if piece.row != row and piece.col != col:
                        return False
        return True
    '''
    Takes a move as a param and executes it. Will not work for castling, en passant, or pawn promotion
    '''
    def make_move(self, move):
        piece_moved = self.board[move.start_row][move.start_col]
        piece_captured = self.board[move.end_row][move.end_col]
        self.board[move.start_row][move.start_col] = ".." # adds an empty piece to the starting row and col of the move
        if piece_captured != "..":                                  # if the square where the piece wants to go has another piece
            self.change_cords(piece_captured, 8, 8, True)           # change the co-ordinates of the piece and mark it as being captured
            if piece_captured.color == "black":                     # appends the non-empty piece to the captured_pieces list
                self.captured_pieces.append(self.pop_piece(piece_captured, self.black_playable_pieces))
            else:
                self.captured_pieces.append(self.pop_piece(piece_captured, self.white_playable_pieces))

        self.board[move.end_row][move.end_col] = piece_moved
        self.change_cords(piece_moved, move.end_row, move.end_col, False) 
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        self.is_first_move = False

    '''
    Reverses the last action and adds the reveresed moved to the redo move stack
    '''
    def undo_move(self):
        if len(self.move_log) >= 1:
            undo = self.move_log.pop()
            piece_moved = undo.piece_moved
            piece_captured = undo.piece_captured
            self.board[undo.start_row][undo.start_col] = piece_moved
            self.change_cords(piece_moved, undo.start_row, undo.start_col, False)
            self.board[undo.end_row][undo.end_col] = piece_captured
            self.change_cords(piece_captured, undo.end_row, undo.end_col, False)
            piece_removed = self.captured_pieces.pop()

            if piece_removed.color == "black":
                self.black_playable_pieces.append(piece_removed)
            else:
                self.white_playable_pieces.append(piece_removed)

            if len(self.move_log) == 0:
                self.is_first_move = True
            self.redo_move_log.append(undo)

    '''
    Reverses the last undo move
    '''
    def redo_move(self):
        if len(self.redo_move_log) >= 1:
            redo = self.redo_move_log.pop()
            self.make_move(redo)
        else:
            pass

    def pop_piece(self, piece, arr):
        found_piece = False
        for element in arr:
            if element.id == piece.id:
                return arr.pop(arr.index(element))
    

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






