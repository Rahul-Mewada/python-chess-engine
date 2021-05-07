import pygame
import ChessEngine
import Pieces
pygame.init()
WIDTH = HEIGHT = 400
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def load_images():
    """
    Loads the images into pygame
    """
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ',
              'bK']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/"
                                               + piece + ".png"),
                                               (SQ_SIZE, SQ_SIZE))


def piece_to_image(piece):
    """
    Takes a Piece and returns its corresponding image
    """
    type_to_string = {
        Pieces.Pawn: 'P',
        Pieces.Rook: 'R',
        Pieces.Knight: 'N',
        Pieces.Bishop: 'B',
        Pieces.Queen: 'Q',
        Pieces.King: 'K'
    }
    if piece.is_empty:
        raise Exception('Piece is empty when it shouldnt be')
    else:
        color = 'w' if piece.color == 'white' else 'b'
        piece_type = type(piece)
        return IMAGES[color + type_to_string[piece_type]]


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    state = ChessEngine.GameState()
    load_images()
    # keeps track of the last click of the user
    sq_selected = ()
    # keeps track of the player clicks [(), ()]
    player_clicks = []
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sq_selected == (row, col):
                    # the user clicked the same square twice
                    sq_selected = ()
                    player_clicks = []
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)
                if len(player_clicks) == 2:
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1],
                                            state.board)
                    state.make_move(move, True)
                    sq_selected = ()
                    player_clicks = []
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    state.undo_move()
        draw_gamestate(screen, state)
        clock.tick(MAX_FPS)
        pygame.display.flip()


def draw_gamestate(screen, state):
    """
    Responsible for all graphics within current gamestate
    """
    draw_board_squares(screen)
    draw_pieces(screen, state.board)


def draw_board_squares(screen):
    """
    Draws the squares of the board
    """
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color,
                             pygame.Rect(col * SQ_SIZE, row * SQ_SIZE,
                                         SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    """
    Draws the pieces on the board
    """
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if not piece.is_empty:
                piece_image = piece_to_image(piece)
                screen.blit(piece_image,
                            pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE,
                                        SQ_SIZE))


if __name__ == '__main__':
    main()
