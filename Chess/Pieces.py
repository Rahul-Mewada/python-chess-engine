import ChessEngine as c
import uuid

class Piece():
    def __init__(self, row, col, board):
        print("piece initialized")
        self.row = row        # row co-ordinate of the piece
        self.col = col        # column co-ordinate of the piece
        self.color = "empty"  # color of the piece
        self.board = board    # state of the board
        self.moves_dict = {
            "up": lambda row, col, valid_moves, moves_dict: generate_valid_moves((row+1, col), valid_moves, moves_dict, "up"),
            "down": lambda row, col, valid_moves, moves_dict: generate_valid_moves((row-1, col), valid_moves, moves_dict, "down"),
            "right": lambda row, col, valid_moves, moves_dict: generate_valid_moves((row, col+1), valid_moves, moves_dict, "right"),
            "left": lambda row, col, valid_moves, moves_dict: generate_valid_moves((row, col-1), valid_moves, moves_dict, "left"),
            "up-right": lambda row, col, valid_moves, moves_dict: generate_valid_moves((row+1, col+1), valid_moves, moves_dict, "up-right"),
            "up-left": lambda row, col, valid_moves, moves_dict: generate_valid_moves((row+1, col-1), valid_moves, moves_dict, "up-left"),
            "down-right": lambda row, col, valid_moves, moves_dict: generate_valid_moves((row-1, col+1), valid_moves, moves_dict, "down-right"),
            "down-left": lambda row, col, valid_moves, moves_dict: generate_valid_moves((row-1, col-1), valid_moves, moves_dict, "down-left")
        }                      # dictionary containing the function calls for different directions
        self.current_sq = (self.row, self.col)
        self.is_captured = False


    '''
    Function that returns an array containing all valid moves that a piece can take
    '''
    def valid_moves(self):
        pass

    '''
    Returns true if the piece can be placed on the specified square (row, col). This includes replacing a piece of the opposing color
    '''
    def is_valid_square(self, square):
        if self.in_bounds(square) and self.has_no_opposing_pieces(square):
            return True
        else:
            return False

    '''
    Private function used to process the valid moves of pieces that move on a row, column or diagonal basis (eg: queen, bishop and knight)
    '''
    def generate_valid_moves(self, end_sq, valid_moves, moves_dict, direction):
        row, col = end_sq
        if not (self.is_valid_square(end_sq)):
            return
        valid_moves.append(c.Move(self.current_sq, end_sq, self.board))
        return self.moves_dict[direction]()

    '''
    Returns true if the square (row, col) passed is in the bounds of the chess board
    '''
    def in_bounds(self, square):
        row, col = square
        if row >=0 and row < 8 and col >=0 and col > 8:
            return True
        else:
            return False

    '''
    Returns true if the square (row, col) passed is either empty or contains a piece of the opposing color
    '''
    def has_no_opposing_pieces(self, square):
        row, col = square
        if self.board[row][col] == ".." or self.board[row][col].color != self.color: #if the square if empty or if it has a piece of the opposing color
            return True
        else:
            return False

   

class Pawn(Piece):
    def __init__(self, row, col, board, color):
        super().__init__(row, col, board)
        self.id = uuid.uuid1()
        self.color = color
        self.name = "pawn"

    def valid_moves(self):
        valid_moves = []
        if self.row+1 < 8: # if the tile above the pawn is in bounds
            if self.board[self.row+1][self.col].is_empty(): # if the tile above the pawn is empty
                valid_moves.append(c.Move((self.row, self.col), (self.row+1, self.col), self.board))
            if (self.col + 1) < 8 and self.board[self.row + 1][self.col + 1].color != self.color: # if the tile that is diagonally (right) of the piece has a black piece
                valid_moves.append(c.Move((self.row, self.col), (self.row+1, self.col+1), self.board))
            if (self.col - 1) >= 0 and self.board[self.row + 1][self.col - 1].color != self.color: # if the tile that is diagonally (left) of the piece has a black piece
                valid_moves.append(c.Move((self.row, self.col), (self.row+1, self.col-1), self.board))
        return valid_moves

class Knight(Piece):
    def __init__(self, row, col, board, color):
        super().__init__(row, col, board)
        self.id = uuid.uuid1()
        self.color = color
        self.name = "knight"

    def valid_moves(self):
        possible_moves = [
            (self.row+2, self.col+1), (self.row+2,self.col-1), (self.row+1, self.col+2), (self.row+1, self.col-2),
            (self.row-2, self.col+1), (self.row-2, self.col-1), (self.row-1,self.col+2), (self.row-1, self.col-2)
            ]
        current_sq = (self.row, self.col)
        valid_moves = []
        for move in possible_moves:
            if self.in_bounds(move) and self.has_no_opposing_pieces(move):
                valid_moves.append(c.Move(current_sq, move, self.board))

        
class Bishop(Piece):
    def __init__(self, row, col, board, color):
        super().__init__(row, col, board)
        self.id = uuid.uuid1()
        self.color = color
        self.name = "bishop"

    def valid_moves(self):
        valid_moves = []
        current_sq = (self.row, self.col)
        possible_moves = ["up", "down", "right", "left"]
        
        for move in possible_moves:
            self.moves_dict[move](self.row, self.col, valid_moves, self.moves_dict)

        return valid_moves


class Rook(Piece):
    def __init__(self, row, col, board, color):
        super().__init__(row, col, board)
        self.id = uuid.uuid1()
        self.color = color
        self.is_empty = False
        self.name = "rook"
    
    def valid_moves(self):
        valid_moves = []
        current_sq = (self.row, self.col)
        possible_moves = ["up", "down", "right", "left"]
        
        for move in possible_moves:
            self.moves_dict[move](self.row, self.col, valid_moves, self.moves_dict)

        return valid_moves
    
class Queen(Piece):
    def __init__(self, row, col, board, color):
        super().__init__(row, col, board)
        self.id = uuid.uuid1()
        self.color = color
        self.is_empty = False
        self.name = "queen"
    
    def valid_moves(self):
        valid_moves = []
        current_sq = (self.row, self.col)
        possible_moves = ["up", "down", "right", "left", "up-right", "up-left", "down-right", "down-left"]
        
        for move in possible_moves:
            self.moves_dict[move](self.row, self.col, valid_moves, self.moves_dict)

        return valid_moves

class King(Piece):
    def __init__(self, row, col, board, color):
        super().__init__(row, col, board)
        self.id = uuid.uuid1()
        self.color = color
        self.is_empty = False
        self.name = "king"
    
    def valid_moves(self):
        valid_moves = []
        current_sq = (self.row, self.col)
        possible_moves = [
            (self.row+1,self.col), (self.row+1, self.col+1), (self.row+1, self.col-1),
            (self.row-1, self.col), (self.row-1, self.col+1), (self.row-1, self.col-1),
            (self.row, self.col-1), (self.row, self.col + 1)
        ]
        
        for move in possible_moves:
            if(self.in_bounds(move) and self.has_no_opposing_pieces(move)):
                valid_moves.append(c.Move(current_sq, move, self.board))

        return valid_moves
