

def is_in_bounds(square):
    """
    Returns true if a square is in bounds of a chess board
    """
    row, col = square
    if 0 <= row < 8 and 0 <= col < 8:
        return True
    return False

