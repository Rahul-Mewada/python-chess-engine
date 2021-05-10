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
    valid_moves = state.get_valid_moves()
    move_made = False
    animate = False
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
                    for m in valid_moves:
                        if m.id == move.id:
                            move_made = True
                            animate = True
                            state.make_move(move, True)
                    sq_selected = ()
                    player_clicks = []
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    state.undo_move()
                    move_made = True
                    animate = False
        if move_made:
            if animate:
                animate_move(state.move_log[-1], screen, state.board, clock)
            valid_moves = state.get_valid_moves()
            move_made = False
            animate = False
        draw_gamestate(screen, state, valid_moves, sq_selected)
        clock.tick(MAX_FPS)
        pygame.display.flip()


def highlight_squares(screen, state, valid_moves, sq_selected):
    """
    Highlights the square selected and valid_moves
    that a piece can make
    """
    if sq_selected:
        r, c = sq_selected
        piece = state.board[r][c]
        if not piece.is_empty and \
                piece.color == ('white' if state.white_to_move else 'black'):
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(pygame.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(pygame.Color('yellow'))
            for move in valid_moves:
                start_row, start_col = move.start_sq
                end_row, end_col = move.end_sq
                if start_row == r and start_col == c:
                    screen.blit(s, (SQ_SIZE * end_col,
                                    SQ_SIZE * end_row))


def animate_move(move, screen, board, clock):
    """ Animates the piece moves """
    colors = [pygame.Color("white"), pygame.Color("gray")]
    start_row, start_col = move.start_sq
    end_row, end_col = move.end_sq
    d_row, d_col = end_row - start_row, end_col - start_col
    frames_per_sq = 10
    frame_count = (abs(d_row) + abs(d_col)) * frames_per_sq
    for frame in range(frame_count + 1):
        row, col = (start_row + (d_row * frame/frame_count),
                    start_col + (d_col * frame/frame_count))
        draw_board_squares(screen)
        draw_pieces(screen, board)
        color = colors[(end_row + end_col) % 2]
        end_square = pygame.Rect(end_col * SQ_SIZE, end_row * SQ_SIZE,
                                 SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(screen, color, end_square)
        if not move.piece_removed.is_empty:
            piece_removed_image = piece_to_image(move.piece_removed)
            screen.blit(piece_removed_image, end_square)
        piece_moved_image = piece_to_image(move.piece_to_move)
        screen.blit(piece_moved_image,
                    pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                    )
        pygame.display.flip()
        clock.tick(60)


def draw_gamestate(screen, state, valid_moves, sq_selected):
    """
    Responsible for all graphics within current gamestate
    """
    draw_board_squares(screen)
    highlight_squares(screen, state, valid_moves, sq_selected)
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
