import Pieces
import utils


class GameState():
    def __init__(self):
        # starting position using the FEN notation
        self.board = self.fen_to_board(
            'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
        self.move_log = []
        self.white_to_move = True

    def fen_to_board(self, fen_string):
        """
        Takes a Forsyth-Edwards Notation string and returns the
        corresponding board representation, and other game state
        information
        """
        board = [[Pieces.EmptyPiece(row, col) for col in range(8)]
                 for row in range(8)]
        row, col = 0, 0
        for char in fen_string:
            if char.isnumeric():
                col += int(char)
                if col >= 8:
                    col = 0
            elif char == '/':
                row += 1
                col = 0
            else:
                color = 'white' if char.isupper() else 'black'
                piece = GameState.args_to_piece(self, char.lower(), row, col,
                                                color)
                board[row][col] = piece
                col += 1
        return board

    def args_to_piece(self, key, row, col, color):
        """
        Takes a key and returns a corresponding Piece object.
        """
        letter_to_piece = {
            'p': Pieces.Pawn(row, col, color),
            'r': Pieces.Rook(row, col, color),
            'n': Pieces.Knight(row, col, color),
            'b': Pieces.Bishop(row, col, color),
            'q': Pieces.Queen(row, col, color),
            'k': Pieces.King(row, col, color)
        }
        return letter_to_piece[key]

    def make_move(self, move, switch_turns):
        """
        Moves a piece from the start square to the end square
        """
        start_row, start_col = move.start_sq
        end_row, end_col = move.end_sq
        piece_to_move = self.board[start_row][start_col]
        if piece_to_move.is_empty:
            raise Exception("Piece to move is an empty piece (make_move)")
        elif not utils.in_bounds(move.start_sq) or \
                not utils.in_bounds(move.end_sq):
            raise Exception("Start or end square are not in bounds")
        else:
            piece_to_move.row = end_row
            piece_to_move.col = end_col
            self.board[end_row][end_col] = piece_to_move
            self.board[start_row][start_col] = Pieces.EmptyPiece(start_row,
                                                                 start_col)
            if switch_turns:
                self.white_to_move = not self.white_to_move
                self.move_log.append(move)

    def undo_move(self):
        """
        Undos the last made move
        """
        if self.move_log:
            move = self.move_log.pop()
        else:
            return
        piece_moved = move.piece_to_move
        piece_to_add = move.piece_removed
        ex_start_row, ex_start_col = move.start_sq
        ex_end_row, ex_end_col = move.end_sq
        if piece_moved.is_empty:
            raise Exception("Piece moved is an empty piece (undo_move)")
        elif not utils.in_bounds(move.start_sq) or \
                not utils.in_bounds(move.end_sq):
            raise Exception("Start or end square not in bounds")
        else:
            piece_moved.row = ex_start_row
            piece_moved.col = ex_start_col
            piece_to_add.row = ex_end_row
            piece_to_add.col = ex_end_col

            self.board[ex_start_row][ex_start_col] = piece_moved
            self.board[ex_end_row][ex_end_col] = piece_to_add


class Move():
    def __init__(self, start_sq, end_sq, board):
        self.start_sq = start_sq
        self.end_sq = end_sq
        start_row, start_col = self.start_sq
        end_row, end_col = self.end_sq
        self.piece_to_move = board[start_row][start_col]
        self.piece_removed = board[end_row][end_col]
