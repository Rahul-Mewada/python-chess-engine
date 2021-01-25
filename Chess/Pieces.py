import Chess.ChessEngine as c
import uuid
class Piece():
    def __init__(self, row, col, board, color):
        self.row = row
        self.col = col
        self.color = color
        self.board = board
        self.moves_dict = {
            "up": lambda row, col, valid_moves, moves_dict: generate_valid_moves((row+1, col), valid_moves, moves_dict, "up"),
            "down": lambda row, col, valid_moves, moves_dict: generate_valid_moves((row-1, col), valid_moves, moves_dict, "down"),
            "right": lambda row, col, valid_moves, moves_dict: generate_valid_moves((row, col+1), valid_moves, moves_dict, "right"),
            "left": lambda row, col, valid_moves, moves_dict: generate_valid_moves((row, col-1), valid_moves, moves_dict, "left"),
            "up-right": lambda row, col, valid_moves, moves_dict: generate_valid_moves((row+1, col+1), valid_moves, moves_dict, "up-right"),
            "up-left": lambda row, col, valid_moves, moves_dict: generate_valid_moves((row+1, col-1), valid_moves, moves_dict, "up-left"),
            "down-right": lambda row, col, valid_moves, moves_dict: generate_valid_moves((row-1, col+1), valid_moves, moves_dict, "down-right"),
            "down-left": lambda row, col, valid_moves, moves_dict: generate_valid_moves((row-1, col-1), valid_moves, moves_dict, "down-left")
        }
        self.current_sq = (row, col)

    def valid_moves(self):
        pass

    def in_bounds(self, square):
        row, col = square
        if row >=0 and row < 8 and col >=0 and col > 8:
            return True
        else:
            return False

    def can_be_placed(self, square):
        row, col = square
        if self.board[row][col] == ".." or self.board[row][col]: #if the square if empty or if it has a piece of the opposing color
            return True
        else:
            return False

    def generate_valid_moves(self, end_sq, valid_moves, moves_dict, direction):
        row, col = end_sq
        if not (self.in_bounds(end_sq) and self.can_be_placed(end_sq)):
            return
        valid_moves.append(c.Move(self.current_sq, end_sq, self.board))
        return self.moves_dict[direction]()

class Pawn(Piece):
    def __init__(self, row, col, board, color):
        super().__init__(row, col, board, color)
        self.id = uuid.uuid1()

    def valid_moves(self):
        valid_moves = []
        if self.row < 8: # if the tile above the pawn is in bounds
            if self.board[self.row+1][self.col] == "..": # if the tile above the pawn is empty
                valid_moves.append(c.Move((self.row, self.col), (self.row+1, self.col), self.board))
            if (self.col + 1) < 8 and self.board[self.row + 1][self.col + 1] != "..": # if the tile that is diagonally (right) of the piece has a black piece
                valid_moves.append(c.Move((self.row, self.col), (self.row+1, self.col+1), self.board))
            if (self.col - 1) >= 0 and self.board[self.row + 1][self.col - 1] != "..": # if the tile that is diagonally (left) of the piece has a black piece
                valid_moves.append(c.Move((self.row, self.col), (self.row+1, self.col-1), self.board))
        return valid_moves

class Knight(Piece):
    def __init__(self, row, col, board, color):
        super().__init__(row, col, board, color)
        self.id = uuid.uuid1()

    def valid_moves(self):
        possible_moves = [(self.row+2, self.col+1), (self.row+2,self.col-1), (self.row+1, self.col+2), (self.row+1, self.col-2),
                         (self.row-2, self.col+1), (self.row-2, self.col-1), (self.row-1,self.col+2), (self.row-1, self.col-2)]
        current_sq = (self.row, self.col)
        valid_moves = []
        for move in possible_moves:
            if self.in_bounds(move) and self.can_be_placed(move):
                valid_moves.append(c.Move(current_sq, move, self.board))

        
        
        
class Bishop(Piece):
    def __init__(self, row, col, color):
        super().__init(row, col, color)
        self.id = uuid.uuid1()
    
    def valid_moves(self):
        valid_moves = []
        current_sq = (self.row, self.col)
        possible_moves = ["up", "down", "right", "left"]
        
        for move in possible_moves:
            self.moves_dict[move](self.row, self.col, valid_moves, self.moves_dict)

        return valid_moves


class Rook(Piece):
    def __init__(self, row, col, color):
        super().__init(row, col, color)
        self.id = uuid.uuid1()
        self.current_sq = (row, col)
    
    def valid_moves(self):
        valid_moves = []
        current_sq = (self.row, self.col)
        possible_moves = ["up", "down", "right", "left"]
        
        for move in possible_moves:
            self.moves_dict[move](self.row, self.col, valid_moves, self.moves_dict)

        return valid_moves
    
class Queen(Piece):
    def __init__(self, row, col, board, color):
        super().__init__(row, col, board, color)
        self.id = uuid.uuid1()
        self.current_sq = (row, col)
    
    def valid_moves(self):
        valid_moves = []
        current_sq = (self.row, self.col)
        possible_moves = ["up", "down", "right", "left", "up-right", "up-left", "down-right", "down-left"]
        
        for move in possible_moves:
            self.moves_dict[move](self.row, self.col, valid_moves, self.moves_dict)

        return valid_moves

class King(Piece):
    def __init__(self, row, col, board, color):
        super().__init__(row, col, board, color)
        self.id = uuid.uuid1()
        self.current_sq = (row, col)
    
    def valid_moves(self):
        valid_moves = []
        current_sq = (self.row, self.col)
        possible_moves = [
            (self.row+1,self.col), (self.row+1, self.col+1), (self.row+1, self.col-1),
            (self.row-1, self.col), (self.row-1, self.col+1), (self.row-1, self.col-1),
            (self.row, self.col-1), (self.row, self.col + 1)
        ]
        
        for move in possible_moves:
            if(self.in_bounds(move) and self.can_be_placed(move)):
                valid_moves.append(c.Move(current_sq, move, self.board))

        return valid_moves
