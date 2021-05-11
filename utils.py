import Pieces


def type_to_direction(typee):
    direction_dict = {
        Pieces.Rook: [(1, 0), (-1, 0), (0, 1), (0, -1)],
        Pieces.Bishop: [(1, 1), (-1, -1), (1, -1), (-1, 1)],
        Pieces.Queen: [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1),
                       (-1, -1), (1, -1), (-1, 1)],
    }
    return direction_dict[typee]


def in_bounds(square):
    """
    Returns true if a square is in bounds of a chess board
    """
    row, col = square
    if 0 <= row < 8 and 0 <= col < 8:
        return True
    return False


def validate_state(state):
    """
    Returns true if the pieces match their position on the board
    """
    print('Validate state called')
    board = state.board
    white_pieces = state.white_pieces
    black_pieces = state.black_pieces
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece.row != row or piece.col != col:
                raise Exception('Coords dont match')

    for piece in black_pieces:
        board_piece = board[piece.row][piece.col]
        if type(board_piece) != type(piece):
            raise Exception('Types dont match')
        elif board_piece.color != piece.color:
            raise Exception('Piece colors dont match')
        elif board_piece.row != piece.row or board_piece.col != piece.col:
            raise Exception('Coords dont match')

    for piece in white_pieces:
        board_piece = board[piece.row][piece.col]
        if type(board_piece) != type(piece):
            raise Exception('Types dont match')
        elif board_piece.color != piece.color:
            raise Exception('Piece colors dont match')
        elif board_piece.row != piece.row or board_piece.col != piece.col:
            raise Exception('Coords dont match')

    return True


def has_enemy(color, board, square):
    """
    Returns true if there is an enemy piece on the square
    """
    row, col = square
    return (not board[row][col].is_empty and color != board[row][col].color)


def is_empty(board, square):
    """
    Returns true if the square on the board has no pieces
    """
    row, col = square
    if board[row][col].is_empty:
        return True


def has_friendly(color, board, square):
    """
    Returns true if the square has a piece of the same color
    """
    return not is_empty(board, square) and not has_enemy(color, board, square)


def find_king(pieces):
    """ Return the king from a list of pieces """
    for piece in pieces:
        if type(piece) == Pieces.King:
            return piece
    raise Exception("Couldn't find king")


def reverse_direction(direction):
    """ Returns the reverse of the direction provided """
    row, col = direction
    return (row * -1, col * -1)
