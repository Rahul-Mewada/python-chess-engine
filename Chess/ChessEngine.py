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
        self.whiteToMove = True
        self.moveLog = np.array([])