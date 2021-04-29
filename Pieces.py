
class EmptyPiece():
    def __init__(self, row, col):
        self.is_empty = True
        self.row = row
        self.col = col


class Pawn(EmptyPiece):
    def __init__(self, row, col, color):
        super().__init__(row, col)
        self.is_empty = False
        self.color = color


class Rook():
    def __init__(self, row, col, color):
        super().__init__(row, col)
        self.is_empty = False
        self.color = color


class Bishop():
    def __init__(self, row, col, color):
        super().__init__(row, col)
        self.is_empty = False
        self.color = color


class Knight():
    def __init__(self, row, col, color):
        super().__init__(row, col)
        self.is_empty = False
        self.color = color


class Queen():
    def __init__(self, row, col, color):
        super().__init__(row, col)
        self.is_empty = False
        self.color = color


class King():
    def __init__(self, row, col, color):
        super().__init__(row, col)
        self.is_empty = False
