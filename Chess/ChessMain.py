"""
Main driver file, responsible for handling user input and
 displaying the current Game State object
"""
import pygame as p
import ChessEngine

p.init()                # initializing pygame
WIDTH = HEIGHT = 400
DIMENSION = 8           # dimension of the board is 8 x 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 30
IMAGES = {
    ("white", "pawn"): p.transform.scale(p.image.load("images/" + "wP" + ".png"), (SQ_SIZE, SQ_SIZE)),
    ("black", "pawn"): p.transform.scale(p.image.load("images/" + "bP" + ".png"), (SQ_SIZE, SQ_SIZE)),
    ("white", "rook"): p.transform.scale(p.image.load("images/" + "wR" + ".png"), (SQ_SIZE, SQ_SIZE)),
    ("black", "rook"): p.transform.scale(p.image.load("images/" + "bR" + ".png"), (SQ_SIZE, SQ_SIZE)),
    ("white", "knight"): p.transform.scale(p.image.load("images/" + "wN" + ".png"), (SQ_SIZE, SQ_SIZE)),
    ("black", "knight"): p.transform.scale(p.image.load("images/" + "bN" + ".png"), (SQ_SIZE, SQ_SIZE)),
    ("white", "bishop"): p.transform.scale(p.image.load("images/" + "wB" + ".png"), (SQ_SIZE, SQ_SIZE)),
    ("black", "bishop"): p.transform.scale(p.image.load("images/" + "bB" + ".png"), (SQ_SIZE, SQ_SIZE)),
    ("white", "queen"): p.transform.scale(p.image.load("images/" + "wQ" + ".png"), (SQ_SIZE, SQ_SIZE)),
    ("black", "queen"): p.transform.scale(p.image.load("images/" + "bQ" + ".png"), (SQ_SIZE, SQ_SIZE)),
    ("white", "king"): p.transform.scale(p.image.load("images/" + "wK" + ".png"), (SQ_SIZE, SQ_SIZE)),
    ("black", "king"): p.transform.scale(p.image.load("images/" + "bK" + ".png"), (SQ_SIZE, SQ_SIZE))
}   # dictionary that maps a color and type of a piece to a func that loads the corrosponding image

'''
Initialize a global dictionary of images, this will be called only once per game
'''
def load_images():
    # pieces = ['wP', 'bP', 'wR', 'bR', 'wN', 'bN', 'wB', 'bB', 'wQ', 'bQ', 'wK', 'bK']
    # for piece in pieces:
    #     IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    for key in IMAGES:
        IMAGES[key]

'''
Responsible for all the graphics on the current game state
'''
def draw_game_state(screen, state):
    draw_board(screen)               # draw squares on the board
    draw_pieces(screen, state.board) # draw pieces on the board

'''
Draws the white and gray squares on the board
'''
def draw_board(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[((row + col) % 2)]
            p.draw.rect(screen, color, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
Draw the pieces on the board using the current GameState.board
'''
def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "..": # not an empty square
                screen.blit(IMAGES[(piece.color, piece.name)], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
The main driver for our code, this will handle user input and updating the process
'''
def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    state = ChessEngine.GameState()
    load_images()
    running = True
    selected_square = () # no square selected, keep track of the last click of theuser (tuple: (row, col))
    player_clicks = []   # keep track of the player clicks (two tuples: [(row, col) -> (row, col)])
    while running: 
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x,y) location of mouse
                col = location[0]//SQ_SIZE   # double / ensures that row and col are ints
                row =  location[1]//SQ_SIZE
                if selected_square == (row, col): # the user clicked the same square twice
                    selected_square = ()
                    player_clicks = []
                else:
                    selected_square = (row, col)
                    player_clicks.append(selected_square) # append for both 1st and 2nd clock
                if len(player_clicks) == 2:
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], state.board)
                    print(move.get_simple_chess_notation())
                    state.make_move(move)
                    selected_square = ()
                    player_clicks = []

                selected_square = (row, col)

            #ket handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo when key 'z' is pressed
                    state.undo_move()
                if e.key == p.K_x: # redo when key 'x' is pressed
                    state.redo_move()
                    
        draw_game_state(screen, state)
        clock.tick(MAX_FPS)
        p.display.flip()

if __name__ == "__main__":
    main()
    