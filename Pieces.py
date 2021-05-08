import utils
import ChessEngine
import shortuuid


class EmptyPiece():
    def __init__(self, row, col):
        self.is_empty = True
        self.row = row
        self.col = col
        self.id = shortuuid.uuid()

    def __eqs__(self, other):
        return self.id == other.id


class SlidingPiece(EmptyPiece):
    def __init__(self, row, col, directions, color):
        EmptyPiece.__init__(self, row, col)
        self.is_empty = False
        self.directions = directions
        self.color = color

    def valid_moves(self, board):
        """ Returns the valid moves for sliding pieces """
        row, col = self.row, self.col
        moves = []
        for direction in self.directions:
            d_row, d_col = direction
            end_row, end_col = row, col
            while True:
                end_row += d_row
                end_col += d_col
                end_sq = (end_row, end_col)
                if self.valid_square(board, end_sq):
                    move = ChessEngine.Move((self.row, self.col),
                                            end_sq, board)
                    moves.append(move)
                else:
                    break
        return moves

    def valid_square(self, board, square):
        """ Returns true if the square is a valid square for sliding pieces """
        if utils.in_bounds(square) and (utils.is_empty(board, square) or
                                        utils.has_enemy(self.color,
                                                        board,
                                                        square)):
            return True
        return False


class Pawn(EmptyPiece):
    def __init__(self, row, col, color):
        EmptyPiece.__init__(self, row, col)
        self.is_empty = False
        self.color = color
        self.can_enpassant = True

    def valid_moves(self, board):
        """ Returns a list of valid moves that a piece can make"""
        row, col = self.row, self.col
        moves = []
        end_sqs_dict = {}
        if self.color == 'black':
            end_sqs_dict['one_forward'] = (row + 1, col)
            end_sqs_dict['attack'] = [
                (row + 1, col + 1),
                (row + 1, col - 1)
            ]
        else:
            end_sqs_dict['one_forward'] = (row - 1, col)
            end_sqs_dict['attack'] = [
                (row - 1, col + 1),
                (row - 1, col - 1)
            ]

        for key in end_sqs_dict:
            cur_sq = end_sqs_dict[key]
            if key == 'one_forward':
                row, col = cur_sq
                if utils.in_bounds(cur_sq) and board[row][col].is_empty:
                    move = ChessEngine.Move((self.row, self.col),
                                            cur_sq, board)
                    moves.append(move)
            elif key == 'attack':
                for cur_sq in end_sqs_dict[key]:
                    if utils.in_bounds(cur_sq) and \
                            utils.has_enemy(self.color, board, cur_sq):
                        move = ChessEngine.Move((self.row, self.col),
                                                cur_sq, board)
                        moves.append(move)
        return moves


class Rook(SlidingPiece):
    def __init__(self, row, col, color):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        SlidingPiece.__init__(self, row, col, directions, color)


class Bishop(SlidingPiece):
    def __init__(self, row, col, color):
        directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        SlidingPiece.__init__(self, row, col, directions, color)


class Knight(EmptyPiece):
    def __init__(self, row, col, color):
        EmptyPiece.__init__(self, row, col)
        self.is_empty = False
        self.color = color

    def valid_moves(self, board):
        """ Returns a list of moves that a piece can make """
        row, col = self.row, self.col
        end_sqs = [
            (row + 2, col + 1),
            (row + 2, col - 1),
            (row - 2, col + 1),
            (row - 2, col - 1),
            (row + 1, col + 2),
            (row + 1, col - 2),
            (row - 1, col + 2),
            (row - 1, col - 2)
        ]
        moves = []
        for end_sq in end_sqs:
            if self.valid_square(board, end_sq):
                move = ChessEngine.Move((self.row, self.col), end_sq, board)
                moves.append(move)
        return moves

    def valid_square(self, board, sq):
        row, col = sq
        if utils.in_bounds(sq) and \
                not utils.has_friendly(self.color, board, sq):
            return True
        return False


class Queen(SlidingPiece):
    def __init__(self, row, col, color):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1),
                      (-1, -1), (1, -1), (-1, 1)]
        SlidingPiece.__init__(self, row, col, directions, color)


class King(EmptyPiece):
    def __init__(self, row, col, color):
        EmptyPiece.__init__(self, row, col)
        self.is_empty = False
        self.color = color

    def valid_moves(self, board):
        """ Returns a list of moves that a piece can make """
        return []
