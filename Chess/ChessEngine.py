"""
This class is responsible for storing all the information of the current state of
a chess game. Also responsible for determining the valid moves of a chess state 
and keeps a move log.
"""
import numpy as np

class GameState():
    def __init__(self):
        self.board = np.array([["bR", "bK"]])