import ChessEngine as c
import uuid
from watchpoints import watch

class Piece():
    def __init__(self, row, col, board):
        self.row = row        # row co-ordinate of the piece
        self.col = col        # column co-ordinate of the piece
        self.color = "empty"  # color of the piece
        self.board = board    # state of the board
        self.moves_dict = {
            "up": lambda row, col, possible_moves, moves_dict: self.generate_possible_moves(row-1, col, possible_moves, moves_dict, "up"),
            "down": lambda row, col, possible_moves, moves_dict: self.generate_possible_moves(row+1, col, possible_moves, moves_dict, "down"),
            "right": lambda row, col, possible_moves, moves_dict: self.generate_possible_moves(row, col+1, possible_moves, moves_dict, "right"),
            "left": lambda row, col, possible_moves, moves_dict: self.generate_possible_moves(row, col-1, possible_moves, moves_dict, "left"),
            "up-right": lambda row, col, possible_moves, moves_dict: self.generate_possible_moves(row-1, col+1, possible_moves, moves_dict, "up-right"),
            "up-left": lambda row, col, possible_moves, moves_dict: self.generate_possible_moves(row-1, col-1, possible_moves, moves_dict, "up-left"),
            "down-right": lambda row, col, possible_moves, moves_dict: self.generate_possible_moves(row+1, col+1, possible_moves, moves_dict, "down-right"),
            "down-left": lambda row, col, possible_moves, moves_dict: self.generate_possible_moves(row+1, col-1, possible_moves, moves_dict, "down-left")
        }                      # dictionary containing the function calls for different directions
        self.current_sq = (self.row, self.col)
        self.is_captured = False
        self.is_pinned = False
        self.pin_direction = ()
        self.opp_direction = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left",
            "up-right": "down-left",
            "up-left": "down-right",
            "down-right": "up-left",
            "down-left": "up-right"
        }
        self.id = uuid.uuid1()
        self.piece_square_table = [
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            []
        ]

    '''
    Function that returns an array containing all valid moves that a piece can take
    '''
    def possible_moves(self):
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
    def generate_possible_moves(self, row, col, possible_moves, moves_dict, direction):
        end_sq = (row, col)
        if not (self.is_valid_square(end_sq)):
            return
        if not self.is_pinned or self.pin_direction == direction or self.opp_direction[self.pin_direction] == direction:
            possible_moves.append(c.Move(self.current_sq, end_sq, self.board))
        if self.board[row][col] != ".." and self.board[row][col].color != self.color: # if the piece is of an opposing color
            return 
        return self.moves_dict[direction](row, col, possible_moves, moves_dict)

    '''
    Returns true if the square (row, col) passed is in the bounds of the chess board
    '''
    def in_bounds(self, square):
        row, col = square
        if row >=0 and row < 8 and col >=0 and col < 8:
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
    
    def __eq__(self, other):
        if isinstance(other, Piece):
            return self.id == other.id
        return False

    '''
    Returns the positional value of a piece using it's piece square table
    '''
    def pos_value(self):
        return self.piece_square_table[self.row][self.col]


class Pawn(Piece):
    def __init__(self, row, col, board, color, special_moves):
        super().__init__(row, col, board)
        self.color = color
        self.name = "pawn"
        self.special_moves = special_moves
        self.value = 1
        self.piece_square_table = [
            [0,  0,  0,  0,  0,  0,  0,  0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [5,  5, 10, 25, 25, 10,  5,  5],
            [0,  0,  0, 20, 20,  0,  0,  0],
            [5, -5,-10,  0,  0,-10, -5,  5],
            [5, 10, 10,-20,-20, 10, 10,  5],
            [0,  0,  0,  0,  0,  0,  0,  0]
        ]
    '''
    Returns the positional value of a piece using it's piece square table
    '''
    def pos_value(self):
        if self.color == "white":
            return self.piece_square_table[self.row][self.col]
        else:
            return self.piece_square_table[7 - self.row][self.col]

    def is_valid_square(self, square):
        row, col = square
        if self.in_bounds(square):
            if self.board[row][col] == "..":
                return self.in_bounds(square)
        return False
 
    '''
    Returns all possible moves that the particular piece can take. Not accounting for potential checkmates or en passant
    '''
    def possible_moves(self):
        possible_moves = []
        if self.color == "black":
            one_forward = (self.row + 1, self.col)
            two_forward = (self.row + 2, self.col)
            diag_right = (self.row + 1, self.col + 1)
            diag_left = (self.row + 1, self.col -1)
            current_sq = (self.row, self.col)
            
            # foreward moves
            if self.is_valid_square(one_forward):
                if not self.is_pinned or self.pin_direction == "down":
                    possible_moves.append(c.Move((self.row, self.col), one_forward, self.board))
                    if self.row == 1 and self.is_valid_square(two_forward):
                        possible_moves.append(c.Move((self.row, self.col), two_forward, self.board))
            # regular captures
            if self.in_bounds(diag_right) and self.board[diag_right[0]][diag_right[1]] != ".." and self.board[diag_right[0]][diag_right[1]].color != self.color:
                if not self.is_pinned or self.pin_direction == "down-right":
                    possible_moves.append(c.Move((self.row, self.col), diag_right, self.board))
            if self.in_bounds(diag_left) and self.board[diag_left[0]][diag_left[1]] != ".." and self.board[diag_left[0]][diag_left[1]].color != self.color:
                if not self.is_pinned or self.pin_direction == "down-left":
                    possible_moves.append(c.Move((self.row, self.col), diag_left, self.board))
            
            # enpassant captures
            if self.in_bounds(diag_right) and diag_right == self.special_moves.enpassant_sq:
                if not self.is_pinned or self.pin_direction == "down-right":
                    possible_moves.append(c.Move((self.row, self.col), diag_right, self.board, is_enpassant = True))
            if self.in_bounds(diag_left) and diag_left == self.special_moves.enpassant_sq:
                if not self.is_pinned or self.pin_direction == "down-left":
                    possible_moves.append(c.Move((self.row, self.col), diag_left, self.board, is_enpassant = True))
            
        if self.color == "white":
            one_forward = (self.row - 1, self.col)
            two_forward = (self.row - 2, self.col)
            diag_right = (self.row - 1, self.col + 1)
            diag_left = (self.row - 1, self.col - 1)

            # forward moves
            if self.is_valid_square(one_forward):
                if not self.is_pinned or self.pin_direction == "up":
                    possible_moves.append(c.Move((self.row, self.col), one_forward, self.board))
                    if self.row == 6 and self.is_valid_square(two_forward):
                        possible_moves.append(c.Move((self.row, self.col), two_forward, self.board))

            # regular captures
            if self.in_bounds(diag_right) and self.board[diag_right[0]][diag_right[1]] != ".." and self.board[diag_right[0]][diag_right[1]].color != self.color:
                if not self.is_pinned or self.pin_direction == "up-right":
                    possible_moves.append(c.Move((self.row, self.col), diag_right, self.board))
            if self.in_bounds(diag_left) and self.board[diag_left[0]][diag_left[1]] != ".." and self.board[diag_left[0]][diag_left[1]].color != self.color:
                if not self.is_pinned or self.pin_direction == "up-left":
                    possible_moves.append(c.Move((self.row, self.col), diag_left, self.board))
    
            # enpassant captures
            if self.in_bounds(diag_right) and diag_right == self.special_moves.enpassant_sq:
                if not self.is_pinned or self.pin_direction == "up-right":
                    possible_moves.append(c.Move((self.row, self.col), diag_right, self.board, is_enpassant=True))
            if self.in_bounds(diag_left) and diag_left == self.special_moves.enpassant_sq:
                if not self.is_pinned or self.pin_direction == "up-left":
                    possible_moves.append(c.Move((self.row, self.col), diag_left, self.board, is_enpassant=True))

        return possible_moves

class Knight(Piece):
    def __init__(self, row, col, board, color):
        super().__init__(row, col, board)
        self.color = color
        self.name = "knight"
        self.value = 3
        self.piece_square_table = [
            [-50,-40,-30,-30,-30,-30,-40,-50],
            [-40,-20,  0,  0,  0,  0,-20,-40],
            [-30,  0, 10, 15, 15, 10,  0,-30],
            [-30,  5, 15, 20, 20, 15,  5,-30],
            [-30,  0, 15, 20, 20, 15,  0,-30],
            [-30,  5, 10, 15, 15, 10,  5,-30],
            [-40,-20,  0,  5,  5,  0,-20,-40],
            [-50,-40,-30,-30,-30,-30,-40,-50]
        ]

    '''
    Returns all possible moves that a knight can take. Not accounting for potential checks or checkmates.
    '''
    def possible_moves(self):
        list_possible_moves = [
            (self.row+2, self.col+1), (self.row+2,self.col-1), (self.row+1, self.col+2), (self.row+1, self.col-2),
            (self.row-2, self.col+1), (self.row-2, self.col-1), (self.row-1,self.col+2), (self.row-1, self.col-2)
            ]
        current_sq = (self.row, self.col)
        if not self.in_bounds(current_sq):
            print("****************RED FLAG****************")
            print(self.name + " " + self.color)
            print(current_sq)

        valid_moves = []
        for move in list_possible_moves:
            if self.is_valid_square(move) and not self.is_pinned:
                possible_king = self.board[move[0]][move[1]]
                valid_moves.append(c.Move(current_sq, move, self.board))
        return valid_moves


            
class Bishop(Piece):
    def __init__(self, row, col, board, color):
        super().__init__(row, col, board)
        self.color = color
        self.name = "bishop"
        self.value = 3
        self.piece_square_table = [
            [-20,-10,-10,-10,-10,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5, 10, 10,  5,  0,-10],
            [-10,  5,  5, 10, 10,  5,  5,-10],
            [-10,  0, 10, 10, 10, 10,  0,-10],
            [-10, 10, 10, 10, 10, 10, 10,-10],
            [-10,  5,  0,  0,  0,  0,  5,-10],
            [-20,-10,-10,-10,-10,-10,-10,-20]
        ]

    '''
    Returns all possible moves that a bishop can take. Not accounting for potential checks or checkmates.
    '''
    def possible_moves(self):
        possible_moves = []
        current_sq = (self.row, self.col)
        if not self.in_bounds(current_sq):
            print("****************RED FLAG****************")
            print(self.name + " " + self.color)
            print(current_sq)

        possible_directions = ["up-right", "up-left", "down-right", "down-left"]
        
        for direction in possible_directions:
            self.moves_dict[direction](self.row, self.col, possible_moves, self.moves_dict)

        return possible_moves


class Rook(Piece):
    def __init__(self, row, col, board, color):
        super().__init__(row, col, board)
        self.color = color
        self.is_empty = False
        self.name = "rook"
        self.value = 3
        self.piece_square_table = [
            [0,  0,  0,  0,  0,  0,  0,  0],
            [5, 10, 10, 10, 10, 10, 10, 5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [0,  0,  0,  5,  5,  0,  0,  0]
        ]

    def possible_moves(self):
        possible_moves = []
        current_sq = (self.row, self.col)
        if not self.in_bounds(current_sq):
            print("****************RED FLAG****************")
            print(self.name + " " + self.color)
            print(current_sq)
        possible_directions = ["up", "down", "right", "left"]
        
        for direction in possible_directions:
            self.moves_dict[direction](self.row, self.col, possible_moves, self.moves_dict)

        return possible_moves
    
class Queen(Piece):
    def __init__(self, row, col, board, color):
        super().__init__(row, col, board)
        self.color = color
        self.is_empty = False
        self.name = "queen"
        self.value = 9
        self.piece_square_table = [
            [-20,-10,-10, -5, -5,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5,  5,  5,  5,  0,-10],
            [-5,  0,  5,  5,  5,  5,  0, -5],
            [0,  0,  5,  5,  5,  5,  0, -5],
            [-10,  5,  5,  5,  5,  5,  0,-10],
            [-10,  0,  5,  0,  0,  0,  0,-10],
            [-20,-10,-10, -5, -5,-10,-10,-20]
        ]
    
    def possible_moves(self):
        possible_moves = []
        current_sq = (self.row, self.col)
        if not self.in_bounds(current_sq):
            print("****************RED FLAG****************")
            print(self.name + " " + self.color)
            print(current_sq)
        possible_directions = ["up", "down", "right", "left", "up-right", "up-left", "down-right", "down-left"]
        
        for direction in possible_directions:
            self.moves_dict[direction](self.row, self.col, possible_moves, self.moves_dict)

        return possible_moves

class King(Piece):
    def __init__(self, row, col, board, color):
        super().__init__(row, col, board)
        self.color = color
        self.is_empty = False
        self.name = "king"
        self.value = 9999
        self.piece_square_table = [
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-20,-30,-30,-40,-40,-30,-30,-20],
            [-10,-20,-20,-20,-20,-20,-20,-10],
            [20, 20,  0,  0,  0,  0, 20, 20],
            [20, 30, 10,  0,  0, 10, 30, 20]
        ]

    def possible_moves(self):
        possible_moves = []
        current_sq = (self.row, self.col)
        if not self.in_bounds(current_sq):
            print("****************RED FLAG****************")
            print(self.name + " " + self.color)
            print(current_sq)
        possible_directions = [
            (self.row+1,self.col), (self.row+1, self.col+1), (self.row+1, self.col-1),
            (self.row-1, self.col), (self.row-1, self.col+1), (self.row-1, self.col-1),
            (self.row, self.col-1), (self.row, self.col + 1)
        ]
        
        for direction in possible_directions:
            if(self.in_bounds(direction) and self.has_no_opposing_pieces(direction)):
                possible_moves.append(c.Move(current_sq, direction, self.board))
                
        return possible_moves

    
