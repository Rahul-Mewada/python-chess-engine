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
import pdb

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
        #self.captured_pieces = []
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
        self.checkmate = False
        self.stalemate = False
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
    Takes a move as a param and executes it. 
    '''
    def make_move(self, move, is_test=False):
        piece_moved = self.board[move.start_row][move.start_col]
        if piece_moved == "..":
            print("something is wrong")
            raise NameError("Piece moved is empty")
        piece_captured = self.board[move.end_row][move.end_col]
        self.board[move.start_row][move.start_col] = ".." # adds an empty piece to the starting row and col of the move
        if piece_captured != "..":                                  # if the square where the piece wants to go has another piece
            self.change_cords(piece_captured, 8, 8, True)           # change the co-ordinates of the piece and mark it as being captured
            if piece_captured.color == "black":                     # appends the non-empty piece to the captured_pieces list
                self.black_playable_pieces.remove(piece_captured)
            else:
                self.white_playable_pieces.remove(piece_captured)
        self.board[move.end_row][move.end_col] = piece_moved
        self.change_cords(piece_moved, move.end_row, move.end_col, False) 
        self.move_log.append(move)
        


        if move.is_pawn_promotion:
            # add a queen in it's place
            replacement_piece = p.Queen(move.end_row, move.end_col, self.board, piece_moved.color)
            self.board[move.end_row][move.end_col] = replacement_piece

            # adds the replacement piece to the playable pieces array and removes the replaced piece
            if replacement_piece.color == "white":
                self.white_playable_pieces.append(replacement_piece)
                self.white_playable_pieces.remove(piece_moved)
                
            else:
                self.black_playable_pieces.append(replacement_piece)
                self.black_playable_pieces.remove(piece_moved)

            self.change_cords(piece_moved, 8, 8, True)


        if move.is_enpassant == True: 
            piece_captured = self.board[move.start_row][move.end_col]
            if piece_captured == "..":
                print("Piece captured in pawn promo is empty")

            self.change_cords(piece_captured, 8, 8, True)           # change the co-ordinates of the piece and mark it as being captured
            if piece_captured.color == "black":                     # appends the non-empty piece to the captured_pieces list
                self.black_playable_pieces.remove(piece_captured)
            else:
                self.white_playable_pieces.remove(piece_captured)
            self.board[move.start_row][move.end_col] = ".."
            move.piece_captured = piece_captured

        # update the enpassant square if a pawn is moved
        if piece_moved.name == "pawn" and abs(move.start_row - move.end_row) == 2:
            self.special_move_mem.enpassant_sq = ((move.start_row + move.end_row)//2, move.end_col)
        else: # reset the enpassant square
            self.special_move_mem.enpassant_sq = ()

        # if move.is_castle:
        #     if move.end_col - move.start_col == 2: # kingside castle move
        #         new_rook = p.Rook(move.end_row, move.end_col-1, self.board, piece_moved.color) # create a new rook piece

        #         old_rook = self.board[move.start_row][move.start_col + 3] # remove the old rook piece and reset it's coords

        #         if piece_moved.color == "black":
        #             self.black_playable_pieces.remove(old_rook)
        #             self.black_playable_pieces.append(new_rook)
        #         else:
        #             self.white_playable_pieces.remove(old_rook)
        #             self.white_playable_pieces.append(new_rook)
        #         self.change_cords(old_rook, 8, 8, True)

        #         self.board[move.start_row][move.start_col+3] = ".." # assign the square on the board as empty
        #         self.board[move.end_row][move.end_col-1] = new_rook # update the board with the new rook

        #     else: # queenside castle move
        #         old_rook = self.board[move.end_row][move.start_col-4]
        #         new_rook = p.Rook(move.start_row, move.end_col + 1, self.board, piece_moved.color)

        #         if piece_moved.color == "black":
        #             self.black_playable_pieces.append(new_rook)
        #             self.black_playable_pieces.remove(old_rook)
        #         else:
        #             self.white_playable_pieces.append(new_rook)
        #             self.white_playable_pieces.remove(old_rook)
        #         self.change_cords(old_rook, 8, 8, True)

        #         self.board[move.end_row][move.start_col-4] = ".." # assign the square on the board as empty
        #         self.board[move.end_row][move.end_col+1] = new_rook # update the board with the new rook
                

        self.update_castle_rights(move)
        self.castling_log.append(CastlingRights(
                                                self.current_castle_state.white_kingside,
                                                self.current_castle_state.white_queenside, 
                                                self.current_castle_state.black_kingside,
                                                self.current_castle_state.black_queenside
                                                )
                                )
        if not is_test:
            self.white_to_move = not self.white_to_move
            self.is_first_move = False


    def debug_print(self, move):
        piece_moved = move.piece_moved
        piece_captured = move.piece_captured
        print()
        print()
        print("Piece Moved: " + str(piece_moved) + str(piece_moved.color))
        print("Piece Captured: " + str(piece_captured))
        i = 0
        j = 0
        print("White Pieces")
        for piece in self.white_playable_pieces:
            i += 1
            print(piece.name + " " + str(i) + " " + str((piece.row, piece.col)))
        print()
        print("Black Pieces")
        for piece in self.black_playable_pieces:
            j += 1
            print(piece.name + " " + str(j) + " " + str((piece.row, piece.col)))
        print()
        print("Do coords match? " + str(self.do_coords_match()))
        print()
        print()

    '''
    Reverses the last action and adds the reveresed moved to the redo move stack
    '''
    def undo_move(self, is_test = False):

        if len(self.move_log) >= 1:
            undo = self.move_log.pop()
            piece_moved = undo.piece_moved
            piece_captured = undo.piece_captured
            self.board[undo.start_row][undo.start_col] = piece_moved
            self.change_cords(piece_moved, undo.start_row, undo.start_col, False)
            self.board[undo.end_row][undo.end_col] = piece_captured


            if piece_captured != "..":
                self.change_cords(piece_captured, undo.end_row, undo.end_col, False)
                if piece_captured.color == "black":
                    self.black_playable_pieces.append(piece_captured)
                else:
                    self.white_playable_pieces.append(piece_captured)
            

            if len(self.move_log) == 0:
                self.is_first_move = True

            if not is_test:
                self.white_to_move = not self.white_to_move
                self.redo_move_log.append(undo)

            # update pawn promotion move
            if undo.is_pawn_promotion:
                replacement_piece = p.Pawn(undo.start_row, undo.start_col, self.board, piece_moved.color, self.special_move_mem)
                self.board[undo.start_row][undo.start_col] = replacement_piece
                # adding the pawn to the pieces on the board
                if replacement_piece.color == "white":
                    self.white_playable_pieces.append(replacement_piece)
                    self.white_playable_pieces.remove(piece_moved)
                else:
                    self.black_playable_pieces.append(replacement_piece)
                    self.white_playable_pieces.remove(piece_moved)
                # removing the queen from the board
                self.change_cords(piece_moved, 8,8, True)

            # update en_passnt move
            if undo.is_enpassant:
                self.board[undo.end_row][undo.end_col] = ".."
                self.board[undo.start_row][undo.end_col] = undo.piece_captured
                self.change_cords(piece_captured, undo.start_row, undo.end_col, False)
            
            # # update castling move
            # if undo.is_castle:
            #     if undo.end_col - undo.start_col == 2: #kingside castle
            #         old_rook = self.board[undo.end_row][undo.end_col - 1]
            #         new_rook = p.Rook(undo.start_row, undo.end_col+1, self.board, piece_moved.color)
            #         if old_rook.color == "black":
            #             self.black_playable_pieces.remove(old_rook)
            #             self.black_playable_pieces.append(new_rook)
            #         else:
            #             self.white_playable_pieces.remove(old_rook)
            #             self.white_playable_pieces.append(new_rook)
                    
            #         self.change_cords(old_rook, 8, 8, True)
            #         self.board[undo.end_row][undo.end_col-1] = ".."
            #         self.board[undo.end_row][undo.end_col+1] = new_rook

            #     elif undo.start_col - undo.end_col == 2: # queenside castle
            #         old_rook = self.board[undo.end_row][undo.end_col+1]
            #         new_rook = p.Rook(undo.end_row, undo.start_col -4, self.board, piece_moved.color)
            #         if old_rook.color == "black":
            #             self.black_playable_pieces.remove(old_rook)
            #             self.black_playable_pieces.append(new_rook)
            #         else:
            #             self.white_playable_pieces.remove(old_rook)
            #             self.white_playable_pieces.append(new_rook)

            #         self.change_cords(old_rook, 8, 8, True)
            #         self.board[undo.end_row][undo.end_col+1] = ".."
            #         self.board[undo.end_row][undo.start_col-4] = new_rook

            #undo castle log

            self.castling_log.pop()
            self.current_castle_state.white_kingside = self.castling_log[-1].white_kingside
            self.current_castle_state.white_queenside = self.castling_log[-1].white_queenside
            self.current_castle_state.black_kingside = self.castling_log[-1].black_kingside
            self.current_castle_state.black_queenside = self.castling_log[-1].black_queenside
            self.checkmate = False
            self.stalemate = False

    '''
    Updates whether or not a player is allowed/can make a queenside or kingside castling move
    '''
    def update_castle_rights(self, move):
        piece_moved = move.piece_moved
        piece_captured = move.piece_captured
        if piece_moved.name == "king":
            if piece_moved.color == "black":
                self.current_castle_state.black_kingside = False
                self.current_castle_state.black_queenside = False
            else:
                self.current_castle_state.white_kingside = False
                self.current_castle_state.white_queenside = False

        elif piece_moved.name == "rook":
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

        if piece_captured != ".." and piece_captured.name == "rook":
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
    Removes and returns a particular piece from a list
    '''
    def pop_piece(self, piece, arr):
        found_piece = False
        for element in arr:
            if element.id == piece.id:
                return arr.pop(arr.index(element))
    
    '''
    Returns the position of a king
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

    '''
    Recursive helper function that searches outwards from the player's king to detect checks and pins
    '''
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
                    in_check = True
                    pieces_that_check.append((pot_piece, direction))
                else:
                    for element in possible_pinned:
                        piece = element[0]
                        piece.is_pinned = True
                        piece.pin_direction = direction
                    pinned_pieces += possible_pinned
                return in_check, pinned_pieces, pieces_that_check
            if (count <=1 and pot_piece.name == "pawn" and pot_piece.color == "black" and (direction == "up-right" or direction == "up-left")) or \
                (count <= 1 and pot_piece.name == "pawn" and pot_piece.color == "white" and (direction == "down-right" or direction == "down-left")): # if the piece is a pawn
                if possible_pinned == []:
                    in_check = True
                    pieces_that_check.append((pot_piece, direction))
                else:
                    for element in possible_pinned:
                        piece = element[0]
                        piece.is_pinned = True
                        piece.pin_direction = direction
                    pinned_pieces += possible_pinned
                return in_check, pinned_pieces, pieces_that_check
            else:  # if there are no enemy pieces or if the enemy pieces are not in a position to check or pin
                return in_check, pinned_pieces, pieces_that_check

        return self.direc_dict[direction](row, col, count, color, pinned_pieces, possible_pinned, pieces_that_check, in_check, direction)
            
    '''
    Returns all the possible moves that a player can make accounting for checks and pins
    '''       
    def get_valid_moves(self):
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
        for pin in pins:
            pin_piece = pin[0]
            pin_direction = pin[1]
            if self.white_to_move:
                for piece in self.white_playable_pieces:
                    if piece.id == pin_piece.id:
                        piece.is_pinned = True
                        piece.pin_direction = pin_direction
            else:
                for piece in self.black_playable_pieces:
                    if piece.id == pin_piece.id:
                        piece.is_pinned = True
                        piece.pin_direciton = pin_direction

    
        if self.white_to_move:
            king_row, king_col = self.find_king_pos("white")
            for piece in self.white_playable_pieces:
                if piece.name == "king":
                    moves += self.get_king_moves(piece)
                else:
                    moves += piece.possible_moves()
        else:
            king_row, king_col = self.find_king_pos("black")
            for piece in self.black_playable_pieces:
                if piece.name == "king":
                    moves += self.get_king_moves(piece)
                else:
                    moves += piece.possible_moves()

        #moves = self.get_possible_moves()

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

                for i in range(len(moves) - 1, -1, -1): # traversal backwards to facilitate removal
                    if moves[i].piece_moved.name != "king":
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                            moves.remove(moves[i])
                if len(moves) == 0:
                    self.checkmate = True
            else: # if there are 1+ checks only return moves if the piece selected is a king
                if piece.name == "king":
                    if len(moves) == 0:
                        self.checkmate = True
                    return moves
                else:
                    return []

        elif len(moves) == 0:
            self.stalemate = True

        return moves


    '''
    Returns all the possible moves that a player can make, not accounting for checks and pins etc
    '''
    def get_possible_moves(self):
        moves = []
        in_check, pins, checks = self.check_for_pins_and_checks()

        if self.white_to_move:
            for piece in self.white_playable_pieces: 
                if piece.name == "king":
                    king_moves = self.get_king_moves(piece)
                    moves += king_moves
                else:
                    moves += piece.possible_moves()
        else:
            for piece in self.black_playable_pieces:
                if piece.name == "king":
                    king_moves = self.get_king_moves(piece)
                    moves += king_moves
                else:
                    moves += piece.possible_moves()
        return moves

    '''
    Returns all the possible moves that a king can make
    '''
    def get_king_moves(self, king):
        moves = []
        if king.name == "king": # filters moves that would lead to a king into a check
            possible_moves = king.possible_moves() # gets "regular" king moves
            castle_moves = self.get_castle_moves(king) # gets castling moves
            if castle_moves != None:
                for move in castle_moves:
                    if move != None:
                        possible_moves.append(move)

            for move in possible_moves: # for every possible move, make it and check if it results in a check or not
                self.make_move(move, is_test = True)
                future_in_check, future_pins, future_checks = self.check_for_pins_and_checks()
                self.undo_move(is_test = True)
                if not future_in_check:
                    moves.append(move)
                
        else:
            print("NOT A KING")

        in_check, pins, checks = self.check_for_pins_and_checks()
        return moves

    '''
    Returns an array of all the possible castle moves that a king can make
    '''
    def get_castle_moves(self, king):
        row = king.row
        col = king.col
        castle_moves = []

        # checking for kingside castling moves
        if self.white_to_move and self.current_castle_state.white_kingside or \
            not self.white_to_move and self.current_castle_state.black_kingside:
            right_move = self.get_kingside_moves(row, col, king)
            if right_move:
                castle_moves.append(right_move)
        
        # checking for queenside castling moves
        if self.white_to_move and self.current_castle_state.white_queenside or \
            not self.white_to_move and self.current_castle_state.black_queenside:
            left_move = self.get_queenside_moves(row, col, king)
            if left_move:
                castle_moves.append(left_move)

        in_check, pins, checks = self.check_for_pins_and_checks()
        if in_check:
            return []

        return castle_moves

    '''
    Gets the kingside castling moves of a king piece
    '''
    def get_kingside_moves(self, row, col, king):
        if self.board[row][col+1] == ".." and self.board[row][col+2] == "..":
            one_right = Move((row, col), (row, col+1), self.board)
            two_right = Move((row, col), (row, col+2), self.board)
            if not (self.is_attacked(one_right) or self.is_attacked(two_right)):
                return Move((row, col), (row, col+2), self.board, is_castle = True)
        return 

    '''
    Detects if a king move results in it walking into a check
    '''
    def is_attacked(self, move):
        self.make_move(move, is_test = True)
        in_check, pins, checks = self.check_for_pins_and_checks()
        self.undo_move(is_test = True)
        if not in_check:
            return False
        return True
        
    '''
    Gets the queenside castling moves of a king piece
    '''
    def get_queenside_moves(self, row, col, king):
        if self.board[row][col-1] == ".." and self.board[row][col-2] == ".." \
            and self.board[row][col-3] == "..":
            one_left = Move((row, col), (row, col-1), self.board)
            two_left = Move((row, col), (row, col-2), self.board)
            if not(self.is_attacked(one_left) or self.is_attacked(two_left)):
                return Move((row, col), (row, col-2), self.board, is_castle = True)
        return 
    
    '''
    Returns the total number of points attributed to a player for a particular board state
    '''
    def evaluate_state(self):
        tot_points = 0
        # tuning variable for piece value
        a = 1  
        # tuning variable for positional value
        b = 0.1

        for piece in self.white_playable_pieces:
            pos_value = piece.pos_value()
            tot_points += (a * piece.value + b * pos_value)

        for piece in self.black_playable_pieces:
            pos_value = piece.pos_value()
            tot_points -= (a * piece.value + b * pos_value)

        return tot_points

class Move():
    rank_to_row = {"8": 0, "7": 1, "6": 2, "5": 3, "4": 4, "3": 5, "2": 6, "1": 7}
    row_to_rank = {val: key for key, val in rank_to_row.items()}
    file_to_col = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    col_to_file = {val: key for key, val in file_to_col.items()}

    def __init__(self, start_sq, end_sq, board, is_enpassant = False, is_castle = False):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.id = self.start_row*1000 + self.start_col*100 + self.end_row*10 + self.end_col
        self.is_enpassant = is_enpassant
        self.is_pawn_promotion = self.is_pawn_promo()
        self.is_castle = is_castle
        if self.piece_moved == "..":
            raise Exception("Piece moved is empty")
    
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
        is_promotion = False
        if self.piece_moved.name == "pawn" and self.piece_moved.color == "white" and self.end_row == 0:
            is_promotion = True
        elif self.piece_moved.name == "pawn" and self.piece_moved.color == "black" and self.end_row == 7:
            is_promotion = True
        return is_promotion
        


    


class Memory(): #TODO: Change the name to represent enpassant
    def __init__(self):
        self.enpassant_sq = () # co-ordinates of a square where an en passant move is possible

class CastlingRights():
    def __init__(self, wks, wqs, bks, bqs):
        self.white_kingside = wks # stores the castling rights for each side of the king
        self.white_queenside = wqs
        self.black_kingside = bks
        self.black_queenside = bqs





