import ChessEngine
import Pieces


class TestGameState():

    def test_fen_to_board():
        target_boards = [
            [
                [('black', 'r'), '.', '.', '.', ('black', 'r'), '.', ('black', 'k'), '.'],
                [('black', 'p'), ('black', 'p'), '.', '.', '.', ('black', 'n'), ('white', 'p'), ('black', 'p')],
                ['.', ('black', 'b'), '.', ('black', 'p'), '.', ('white', 'b'), '.', '.'],
                ['.', ('black', 'q'), '.', ('white', 'p'), '.', ('white', 'n'), '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                [('white', 'p'), '.', '.', '.', '.', ('black', 'q'), '.', '.'],
                ['.', ('white', 'p'), '.', '.', '.', ('white', 'p'), ('white', 'q'), '.'],
                [('white', 'r'), '.', '.', '.', '.', '.', '.', ('white', 'r')]
            ],

            [
                [('black', 'r'), ('black', 'n'), ('black', 'b'), ('black', 'q'), ('black', 'k'),
                    ('black', 'b'), ('black', 'n'), ('black', 'r')],
                [('black' 'p'), ('black', 'p'), ('black', 'p'), ('black', 'p'), ('black', 'p'),
                    ('black', 'p'), ('black', 'p'), ('black', 'p')],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.'],
                [('white', 'p'), ('white', 'p'), ('white', 'p'), ('white', 'p'), ('white', 'p'),
                    ('white', 'p'), ('white', 'p'), ('white', 'p')],
                [('white', 'r'), ('white', 'n'), ('white', 'b'), ('white', 'q'), ('white', 'k'),
                    ('white', 'b'), ('white', 'n'), ('white', 'r')]
            ]
        ]
        letter_to_piece = {
            'p': Pieces.Pawn,
            'r': Pieces.Rook,
            'n': Pieces.Knight,
            'b': Pieces.Bishop,
            'q': Pieces.Queen,
            'k': Pieces.King
        }
        fen_strings = ['r3r1k1/pp3nPp/1b1p1B2/1q1P1N2/8/P4Q2/1P3PK1/R6R',
                       'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR']

        for index, target_board in target_boards:
            target_fen_string = fen_strings[index]
            result_board = ChessEngine.fen_to_board(target_fen_string)
            for row in range(8):
                for col in range(8):
                    result_piece = result_board[row][col]
                    target_piece = target_board[row][col]
                    if target_piece == '.':
                        if result_piece.type() is not Pieces.EmptyPiece:
                            return False
                    else:
                        target_piece_color, target_piece_type = target_piece
                        if result_piece.color != target_piece_color:
                            return False
                        if result_piece.type() is not \
                                letter_to_piece[target_piece_type]:
                            return False
                    if result_piece.row != row or result_piece.col != col:
                        return False

        return True
