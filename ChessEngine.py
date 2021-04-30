import Pieces


class GameState():
    def __init__(self):
        # starting position using the FEN notation
        self.board = self.fen_to_board(
            'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

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
                row += int(char)
                if row >= 8:
                    row = 0
            elif char == '/':
                col += 1
                row = 0
            else:
                color = 'white' if char.isupper() else 'black'
                piece = self.args_to_piece(char.lower(), row, col, color)
                board[row][col] = piece
                row += 1
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
