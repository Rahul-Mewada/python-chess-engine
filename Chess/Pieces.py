import ChessEngine as c
import uuid

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
        self.opp_direciton = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left",
            "up-right": "down-left",
            "up-left": "down-right",
            "down-right": "up-left",
            "down-left": "up-right"
        }

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
        if not self.is_pinned or self.pin_direction == direction or self.opp_direction[pin_direction] == direction:
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



class Pawn(Piece):
    def __init__(self, row, col, board, color):
        super().__init__(row, col, board)
        self.id = uuid.uuid1()
        self.color = color
        self.name = "pawn"

    def is_valid_square(self, square):
        row, col = square
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

            if self.is_valid_square(one_forward):
                if not self.is_pinned or pin_direction == "down":
                    possible_moves.append(c.Move((self.row, self.col), one_forward, self.board))
                    if self.row == 1 and self.is_valid_square(two_forward):
                        possible_moves.append(c.Move((self.row, self.col), two_forward, self.board))

            if self.in_bounds(diag_right) and self.board[diag_right[0]][diag_right[1]] != ".." and self.board[diag_right[0]][diag_right[1]].color != self.color:
                if not self.is_pinned or pin_direction == "down-right":
                    possible_moves.append(c.Move((self.row, self.col), diag_right, self.board))
            if self.in_bounds(diag_left) and self.board[diag_left[0]][diag_left[1]] != ".." and self.board[diag_left[0]][diag_left[1]].color != self.color:
                if not self.is_pinned or pin_direction == "down-left":
                    possible_moves.append(c.Move((self.row, self.col), diag_left, self.board))
            
        if self.color == "white":
            one_forward = (self.row - 1, self.col)
            two_forward = (self.row - 2, self.col)
            diag_right = (self.row - 1, self.col + 1)
            diag_left = (self.row - 1, self.col - 1)

            if self.is_valid_square(one_forward):
                if not self.is_pinned or pin_direction == "up":
                    possible_moves.append(c.Move((self.row, self.col), one_forward, self.board))
                    if self.row == 6 and self.is_valid_square(two_forward):
                        possible_moves.append(c.Move((self.row, self.col), two_forward, self.board))

            if self.in_bounds(diag_right) and self.board[diag_right[0]][diag_right[1]] != ".." and self.board[diag_right[0]][diag_right[1]].color != self.color:
                if not self.is_pinned or pin_direction == "up-right":
                    possible_moves.append(c.Move((self.row, self.col), diag_right, self.board))
            if self.in_bounds(diag_left) and self.board[diag_left[0]][diag_left[1]] != ".." and self.board[diag_left[0]][diag_left[1]].color != self.color:
                if not self.is_pinned or pin_direction == "up-left":
                    possible_moves.append(c.Move((self.row, self.col), diag_left, self.board))
    
        return possible_moves

class Knight(Piece):
    def __init__(self, row, col, board, color):
        super().__init__(row, col, board)
        self.id = uuid.uuid1()
        self.color = color
        self.name = "knight"

    '''
    Returns all possible moves that a knight can take. Not accounting for potential checks or checkmates.
    '''
    def possible_moves(self):
        list_possible_moves = [
            (self.row+2, self.col+1), (self.row+2,self.col-1), (self.row+1, self.col+2), (self.row+1, self.col-2),
            (self.row-2, self.col+1), (self.row-2, self.col-1), (self.row-1,self.col+2), (self.row-1, self.col-2)
            ]
        current_sq = (self.row, self.col)
        valid_moves = []
        for move in list_possible_moves:
            if self.is_valid_square(move) and not self.is_pinned:
                possible_king = self.board[move[0]][move[1]]
                valid_moves.append(c.Move(current_sq, move, self.board))
        return valid_moves


            
class Bishop(Piece):
    def __init__(self, row, col, board, color):
        super().__init__(row, col, board)
        self.id = uuid.uuid1()
        self.color = color
        self.name = "bishop"

    '''
    Returns all possible moves that a bishop can take. Not accounting for potential checks or checkmates.
    '''
    def possible_moves(self):
        possible_moves = []
        current_sq = (self.row, self.col)
        possible_directions = ["up-right", "up-left", "down-right", "down-left"]
        
        for direction in possible_directions:
            self.moves_dict[direction](self.row, self.col, possible_moves, self.moves_dict)

        return possible_moves


class Rook(Piece):
    def __init__(self, row, col, board, color):
        super().__init__(row, col, board)
        self.id = uuid.uuid1()
        self.color = color
        self.is_empty = False
        self.name = "rook"
    
    def possible_moves(self):
        possible_moves = []
        current_sq = (self.row, self.col)
        possible_directions = ["up", "down", "right", "left"]
        
        for direction in possible_directions:
            self.moves_dict[direction](self.row, self.col, possible_moves, self.moves_dict)

        return possible_moves
    
class Queen(Piece):
    def __init__(self, row, col, board, color):
        super().__init__(row, col, board)
        self.id = uuid.uuid1()
        self.color = color
        self.is_empty = False
        self.name = "queen"
    
    def possible_moves(self):
        possible_moves = []
        current_sq = (self.row, self.col)
        possible_directions = ["up", "down", "right", "left", "up-right", "up-left", "down-right", "down-left"]
        
        for direction in possible_directions:
            self.moves_dict[direction](self.row, self.col, possible_moves, self.moves_dict)

        return possible_moves

class King(Piece):
    def __init__(self, row, col, board, color):
        super().__init__(row, col, board)
        self.id = uuid.uuid1()
        self.color = color
        self.is_empty = False
        self.name = "king"
    

    def possible_moves(self):
        possible_moves = []
        current_sq = (self.row, self.col)
        possible_directions = [
            (self.row+1,self.col), (self.row+1, self.col+1), (self.row+1, self.col-1),
            (self.row-1, self.col), (self.row-1, self.col+1), (self.row-1, self.col-1),
            (self.row, self.col-1), (self.row, self.col + 1)
        ]
        
        for direction in possible_directions:
            if(self.in_bounds(direction) and self.has_no_opposing_pieces(direction)):
                self.board.make_move(c.Move(current_sq, direction, self.board))
                in_check, pins, checks = self.board.check_for_pins_and_checks()
                self.board.undo_move()
                if not in_check:
                    possible_moves.append(c.Move(current_sq, direction, self.board))
                
        return possible_moves
