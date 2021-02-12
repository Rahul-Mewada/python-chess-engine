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
        self.white_king_sq = self.find_king_pos("white")
        self.black_king_sq = self.find_king_pos("black")
        self.special_move_mem = Memory()
        self.board = self.init_board()
        self.direc_dict = {
            "up": lambda row, col, count, color, pinned_pieces, possible_pinned, pieces_that_check, in_check, direction: \
                self.direction_search(row-1, col, count, color, pinned_pieces, possible_pinned, pieces_that_check, in_check, "up"),
            "down": lambda row, col, count, color, pinned_pieces, possible_pinned, pieces_that_check, in_check, direction: \
                 self.direction_search(row+1, col, count, color, pinned_pieces, possible_pinned, pieces_that_check, in_check, "down"),
            "left": lambda row, col, count, color, pinned_pieces, possible_pinned, pieces_that_check, in_check, direction: \
                self.direction_search(row, col-1, count, color, pinned_pieces, possible_pinned, pieces_that_check, in_check, "left"),
            "right": lambda row, col, count, color, pinned_pieces, possible_pinned, pieces_that_check, in_check, direction: \
                self.direction_search(row, col+1, count, color, pinned_pieces, possible_pinned, pieces_that_check, in_check, "right"),
            "down-left": lambda row, col, count, color, pinned_pieces, possible_pinned, pieces_that_check, in_check, direction: \
                self.direction_search(row+1, col-1, count, color, pinned_pieces, possible_pinned, pieces_that_check, in_check, "down-left"),
            "down-right": lambda row, col, count, color, pinned_pieces, possible_pinned, pieces_that_check, in_check, direction: \
                 self.direction_search(row+1, col+1, count, color, pinned_pieces, possible_pinned, pieces_that_check, in_check, "down-right"),
            "up-left": lambda row, col, count, color, pinned_pieces, possible_pinned, pieces_that_check, in_check, direction: \
                self.direction_search(row-1, col-1, count, color, pinned_pieces, possible_pinned, pieces_that_check, in_check, "up-left"),
            "up-right": lambda row, col, count, color, pinned_pieces, possible_pinned, pieces_that_check, in_check, direction: \
                self.direction_search(row-1, col+1, count, color, pinned_pieces, possible_pinned, pieces_that_check, in_check, "up-right")
        }
        self.current_castle_state = CastlingRights(True, True, True, True)
        self.castling_log = [CastlingRights(True, True, True, True)]
 # def direction_search(self, row, col, count, color, pinned_pieces, possible_pinned, pieces_that_check, in_check, direction):
    '''
    Converts a board of strings into a board of Pieces and populates the white and black piece arrays
    '''
    def init_board(self):
        piece_dict = {
            "P": lambda row, col, board, color: p.Pawn(row, col, board, color, self.special_move_mem),
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
    
    def gen_all_possible_moves(self):
        pass

    def gen_all_valid_moves(self):
        moves = []
        if self.white_to_move:
            for piece in self.white_playable_pieces:
                moves.append(piece.valid_moves)

    '''
    Helper function that changes a particular pieces variables
    '''
    def change_cords(self, piece, row, col, to_capture):
        piece.row = row
        piece.col = col
        piece.current_sq = (row, col)
        if to_capture:
            piece.is_captured = True

    '''
    Checks if the board state representation and the piece's coordinates match
    '''
    def do_coords_match(self):
        for row in range(len(self.board)):
            for col in range(len(self.board)):
                piece = self.board[row][col]
                if piece != "..":
                    if piece.row != row and piece.col != col:
                        print(piece.name)
                        return False
        return True
    '''
    Takes a move as a param and executes it. Will not work for castling, en passant, or pawn promotion
    '''
    def make_move(self, move):
        piece_moved = self.board[move.start_row][move.start_col]
        if piece_moved == "..":
            print("something is wrong")
        piece_captured = self.board[move.end_row][move.end_col]
        self.board[move.start_row][move.start_col] = ".." # adds an empty piece to the starting row and col of the move
        if piece_captured != "..":                                  # if the square where the piece wants to go has another piece
            self.change_cords(piece_captured, 8, 8, True)           # change the co-ordinates of the piece and mark it as being captured
            if piece_captured.color == "black":                     # appends the non-empty piece to the captured_pieces list
                self.captured_pieces.append(self.pop_piece(piece_captured, self.black_playable_pieces))
                print("black piece captured: " + piece_captured.name)
            else:
                self.captured_pieces.append(self.pop_piece(piece_captured, self.white_playable_pieces))
                print("white piece captured: " + str(piece_captured.name))
        self.board[move.end_row][move.end_col] = piece_moved
        print(piece_moved)
        self.change_cords(piece_moved, move.end_row, move.end_col, False) 
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move
        self.is_first_move = False

        if move.is_pawn_promo:
            # add a queen in it's place
            replacement_piece = p.Queen(move.end_row, move.end_col, self.board, piece_moved.color)
            self.board[move.end_row][move.end_col] = replacement_piece

            # adding the replacement piece to the playable pieces array 
            if replacement_piece.color == "white":
                self.white_playable_pieces.append(replacement_piece)
            else:
                self.black_playable_pieces.append(replacement_piece)

            # remove the pawn from the board
            temp_piece = piece_moved
            self.change_cords(temp_piece, 8, 8, True)

        if move.is_enpassant == True: 
            piece_captured = self.board[move.start_row][move.end_col]
            self.change_cords(piece_captured, 8, 8, True)           # change the co-ordinates of the piece and mark it as being captured
            if piece_captured.color == "black":                     # appends the non-empty piece to the captured_pieces list
                self.captured_pieces.append(self.pop_piece(piece_captured, self.black_playable_pieces))
                print("black piece captured: " + piece_captured.name)
            else:
                self.captured_pieces.append(self.pop_piece(piece_captured, self.white_playable_pieces))
                print("white piece captured: " + str(piece_captured.name))
            self.board[move.start_row][move.end_col] = ".."
            move.piece_captured = piece_captured

        
        # update the enpassant square if a pawn is moved
        if piece_moved.name == "pawn" and abs(move.start_row - move.end_row) == 2:
            self.special_move_mem.enpassant_sq = ((move.start_row + move.end_row)//2, move.end_col)
        else: # reset the enpassant square
            self.special_move_mem.enpassant_sq = ()

        self.update_castling_rights(move)
        self.castling_log.append(CastlingRights(
                                                self.current_castle_state.white_kingside,
                                                self.current_castle_state.white_queenside, 
                                                self.current_castle_state.black_kingside,
                                                self.current_castle_state.black_queenside
                                                )
                                )

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

            if piece_captured != "..":
                self.change_cords(piece_captured, undo.end_row, undo.end_col, False)
            if len(self.captured_pieces) != 0:
                piece_removed = self.captured_pieces.pop() 
                if piece_removed.color == "black":
                    self.black_playable_pieces.append(piece_removed)
                else:
                    self.white_playable_pieces.append(piece_removed)

            if len(self.move_log) == 0:
                self.is_first_move = True
            self.white_to_move = not self.white_to_move
            self.redo_move_log.append(undo)

            if undo.is_pawn_promo:
                replacement_piece = p.Pawn(undo.start_row, undo.start_col, self.board, piece_moved.color)
                self.board[undo.start_row][undo.start_col] = replacement_piece
                
                # adding the pawn to the pieces on the board
                if replacement_piece.color == "white":
                    self.white_playable_pieces.append(replacement_piece)
                else:
                    self.black_playable_pieces.append(replacement_piece)

                # removing the queen from the board
                temp_piece = piece_moved
                self.change_cords(piece_moved, 8,8, True)

            if undo.is_enpassant:
                self.board[undo.end_row][undo.end_col] = ".."
                self.board[undo.start_row][undo.end_col] = undo.piece_captured
                self.change_cords(piece_captured, undo.start_row, undo.end_col, False)
            
            # undo castle log
            self.castling_log.pop()
            self.current_castle_state.white_kingside = self.castling_log[-1].white_kingside
            self.current_castle_state.white_queenside = self.castling_log[-1].white_queenside
            self.current_castle_state.black_kingside = self.castling_log[-1].black_kingside
            self.current_castle_state.black_queenside = self.castling_log[-1].black_queenside

    def update_castle_rights(self, move):
        piece_moved = move.piece_moved
        if piece_moved.name == "king":
            if piece_moved.color == "black":
                self.current_castle_state.black_kingside = False
                self.current_castle_state.black_queenside = False
            else:
                self.current_castle_state.white_kingside = False
                self.current_castle_state.white_queenside = False

        elif piece_moved.name = "rook":
            if piece_moved.color == "black":
                if move.start_row == 0:
                    if move.start_col == 0:
                        self.current_castle_state.black_queenside = False
                    elif move.start_col == 7:
                        self.current_castle_state.black_kingside = False
            else:
                if move.start_row == 7:
                    if move.start_col == 0:
                        self.current_castle_state.white_queenside = False
                    elif move.start_col ==7:
                        self.current_castle_state.white_kingside = False

        if piece_captured.name == "rook":
                if piece_captured.color == "black":
                    if move.end_row == 0:
                        if move.end_col == 0:
                            self.current_castle_state.black_queenside = False
                        elif move.end_col == 7:
                            self.current_castle_state.black_kingside = False
                else:
                    if move.end_row == 7:
                        if move.end_col == 0:
                            self.current_castle_state.white_queenside = False
                        elif move.end_col == 7:
                            self.current_castle_state.white_kingside = False



            
    '''
    Reverses the last undo move
    '''
    def redo_move(self):
        if len(self.redo_move_log) >= 1:
            redo = self.redo_move_log.pop()
            self.make_move(redo)
        else:
            pass

    '''
    Removes and returns a particular piece from a list
    '''
    def pop_piece(self, piece, arr):
        found_piece = False
        for element in arr:
            if element.id == piece.id:
                return arr.pop(arr.index(element))
    
    '''
    Returns the position of the white king
    '''
    def find_king_pos(self, color):
        if color == "white":
            for piece in self.white_playable_pieces:
                if piece.name == "king":
                    return (piece.row, piece.col)
        elif color == "black":
            for piece in self.black_playable_pieces:
                if piece.name == "king":
                    return (piece.row, piece.col)

    '''
    Returns the pieces that are pinned and checked and the direction from which they are being attacked
    '''
    def check_for_pins_and_checks(self):
        if self.white_to_move:
            start_row, start_col = self.find_king_pos("white")
            color = "white"
            for piece in self.white_playable_pieces:
                piece.is_pinned = False
                piece.pin_direction = ()
                if piece.name == "king":
                    self.is_checked = False
                    self.check_direction = ()
        else:
            start_row, start_col = self.find_king_pos("black")
            color = "black"
            for piece in self.black_playable_pieces:
                piece.is_pinned = False
                piece.pin_direction = ()
                if piece.name == "king":
                    self.is_checked = False
                    self.check_direction = ()

        possible_directions = ["up", "down", "left", "right", "down-right", "down-left", "up-right", "up-left"] # relative to the king being considered
        pins = []
        checks = []
        in_check = False
        for direction in possible_directions:
            in_check, pins, checks = self.direc_dict[direction](start_row, start_col, 0, color, pins, [], checks, in_check, direction)

        possible_knight_directions = [
            (start_row+2, start_col+1), (start_row+2, start_col-1), (start_row+1, start_col+2), (start_row+1, start_col-2),
            (start_row-2, start_col+1), (start_row-2, start_col-1), (start_row-1, start_col+2), (start_row-1, start_col-2)
        ]

        for direction in possible_knight_directions:
            row, col = direction
            if (0 <= row < 8 and 0 <= col < 8):
                possible_piece = self.board[row][col]
                if possible_piece != ".." and possible_piece.color != color and possible_piece.name == "knight":
                    in_check = True
                    checks.append((possible_piece, direction))
        
        if in_check:
            self.board[start_row][start_col].is_checked = True
            for check in checks:
                self.board[start_row][start_col].check_direction = check[1]

        return in_check, pins, checks

    def direction_search(self, row, col, count, color, pinned_pieces, possible_pinned, pieces_that_check, in_check, direction):
        if not (0 <= row < 8 and 0 <= col < 8): # return if out of bounds
            return in_check, pinned_pieces, pieces_that_check

        count += 1
        pot_piece = self.board[row][col]
        if pot_piece != ".." and pot_piece.color == color: # if the piece is of the same color, then it might be a pinned piece
            if possible_pinned == []:
                possible_pinned.append((pot_piece, direction))
            else: # if it is the second piece 
                return in_check, pinned_pieces, pieces_that_check

        elif pot_piece != ".." and pot_piece.color != color: # if the piece is an enemy piece
            if (pot_piece.name == "rook" and (direction == "up" or direction == "down" or direction == "right" or direction == "left")) or \
                (pot_piece.name == "bishop" and (direction == "up-right" or direction == "up-left" or direction == "down-right" or direction == "down-left")) or \
                    pot_piece.name == "queen" or (pot_piece.name == "king" and count <=1):
                if possible_pinned == []:
                    is_check = True
                    pieces_that_check.append((pot_piece, direction))
                else:
                    for element in possible_pinned:
                        piece = element[0]
                        piece.is_pinned = True
                        piece.pin_direction = direction
                    pinned_pieces.append(possible_pinned)
                return in_check, pinned_pieces, pieces_that_check
            if (count <=1 and pot_piece.name == "pawn" and pot_piece.color == "black" and (direction == "up-right" or direction == "up-left")) or \
                (count <= 1 and pot_piece.name == "pawn" and pot_piece.color == "white" and (direction == "down-right" or direction == "down-left")): # if the piece is a pawn
                if possible_pinned == []:
                    is_check = True
                    pieces_that_check.append((pot_piece, direction))
                else:
                    for piece in possible_pinned:
                        piece.is_pinned = True
                        piece.pin_direction = direction
                    pinned_pieces.append(possible_pinned)
                return in_check, pinned_pieces, pieces_that_check
            else:  # if there are no enemy pieces or if the enemy pieces are not in a position to check or pin
                return in_check, pinned_pieces, pieces_that_check

        return self.direc_dict[direction](row, col, count, color, pinned_pieces, possible_pinned, pieces_that_check, in_check, direction)
            
                
    def get_valid_moves(self, piece):
        moves = []
        in_check, pins, checks = self.check_for_pins_and_checks()
        dir_to_tuple = {
            "up": (-1,0),
            "down": (1, 0),
            "left": (0,-1),
            "right": (1, 1),
            "up-right": (-1, 1),
            "up-left": (-1, -1),
            "down-right": (1, 1),
            "down-left": (1, -1)
        }
        if self.white_to_move:
            king_row, king_col = self.find_king_pos("white")
        else:
            king_row, king_col = self.find_king_pos("black")

        if piece.name == "king": # filters moves that would lead to a king into a check
            possible_moves = piece.possible_moves()
            for move in possible_moves: # for every possible move, make it and check if it results in a check or not
                self.make_move(move)
                future_in_check, future_pins, future_checks = self.check_for_pins_and_checks()
                self.undo_move()
                if not future_in_check:    
                    moves.append(move)
        else: # if not a king then add all possible moves it can make
            moves = piece.possible_moves()

        if in_check:
            if len(checks) == 1: # only 1 check, block check or move king
                check_piece = checks[0][0]
                check_direction = checks[0][1]
                check_row = check_piece.row
                check_col = check_piece.col
                valid_squares = []

                if check_piece.name == "knight":
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1,8):
                        valid_square = (king_row + dir_to_tuple[check_direction][0] * i, \
                             king_col + dir_to_tuple[check_direction][1] * i)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break

                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].piece_moved.name != "king":
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                            moves.remove(moves[i])
                if len(moves) == 0:
                    pass #checkmate
            else: # if there are 1+ checks only return moves if the piece selected is a king
                if piece.name == "king":
                    if len(moves) == 0:
                        pass #checkmate
                    return moves
                else:
                    return []
        elif len(moves) == 0:
            pass
            # stalemate
        return moves

    def create_pawn_promo_move(self, start_sq, end_sq, board):
        pass


    def get_possible_moves(self):
        moves = []
        if self.white_to_moves:
            for piece in self.white_playable_pieces:
                moves.append(piece.valid_moves)
        else:
            for piece in self.black_playable_pieces:
                moves.append(piece.valid_moves)
        return moves

class Move():
    rank_to_row = {"8": 0, "7": 1, "6": 2, "5": 3, "4": 4, "3": 5, "2": 6, "1": 7}
    row_to_rank = {val: key for key, val in rank_to_row.items()}
    file_to_col = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    col_to_file = {val: key for key, val in file_to_col.items()}

    def __init__(self, start_sq, end_sq, board, is_enpassant = False):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.id = self.start_row*1000 + self.start_col*100 + self.end_row*10 + self.end_col
        self.is_enpassant = is_enpassant
        self.is_pawn_promo = self.is_pawn_promo()
        self.is_castle = False

    
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.id == other.id
        return False

    def get_simple_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        return self.col_to_file[col] + self.row_to_rank[row]

        
    '''
    Returns true if a move is a pawn promotion
    '''    
    def is_pawn_promo(self):
        if self.piece_moved.name == "pawn" and self.piece_moved.color == "white" and self.end_row == 0:
            self.is_pawn_promo = True
        elif self.piece_moved.name == "pawn" and self.piece_moved.color == "black" and self.end_row == 7:
            self.is_pawn_promo = True


def get_castle_moves(self, king):
    



class Memory(): #TODO: Change the name to represent enpassant
    def __init__(self):
        self.enpassant_sq = () # co-ordinates of a square where an en passant move is possible

class CastlingRights()
    def __init__(self, wks, wqs, bks, bqs):
        self.white_kingside = wks # stores the castling rights for each side of the king
        self.white_queenside = wqs
        self.black_kingside = bks
        self.black_queenside = bqs





