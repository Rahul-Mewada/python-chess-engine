import pygame
import ChessEngine
pygame.init()
WIDTH = HEIGHT = 512
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


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    state = ChessEngine.GameState()
    load_images()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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


if __name__ == '__main__':
    main()
