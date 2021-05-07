

def in_bounds(square):
    """
    Returns true if a square is in bounds of a chess board
    """
    row, col = square
    if 0 <= row < 8 and 0 <= col < 8:
        return True
    return False


def valid_board(board):
    """
    Returns true if the pieces match their position on the board
    """
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece.row != row or piece.col != col:
                return False
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
