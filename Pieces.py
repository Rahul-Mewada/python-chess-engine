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


class Pawn(EmptyPiece):
    def __init__(self, row, col, color):
        EmptyPiece.__init__(self, row, col)
        self.is_empty = False
        self.color = color
        self.can_enpassant = True

    def valid_moves(self, board):
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


class Rook():
    def __init__(self, row, col, color):
        EmptyPiece.__init__(self, row, col)
        self.is_empty = False
        self.color = color

    def valid_moves(self, board):
        return []


class Bishop():
    def __init__(self, row, col, color):
        EmptyPiece.__init__(self, row, col)
        self.is_empty = False
        self.color = color

    def valid_moves(self, board):
        return []


class Knight():
    def __init__(self, row, col, color):
        EmptyPiece.__init__(self, row, col)
        self.is_empty = False
        self.color = color

    def valid_moves(self, board):
        return []


class Queen():
    def __init__(self, row, col, color):
        EmptyPiece.__init__(self, row, col)
        self.is_empty = False
        self.color = color

    def valid_moves(self, board):
        return []


class King():
    def __init__(self, row, col, color):
        EmptyPiece.__init__(self, row, col)
        self.is_empty = False
        self.color = color

    def valid_moves(self, board):
        return []
