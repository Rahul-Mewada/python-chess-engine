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
Highlights the square selected and moves for piece selected
'''
def highlight_squares(screen, state, valid_moves, selected_square, invalid_sq):
    if selected_square != () and valid_moves != []:
        row, col = selected_square
        if state.board[row][col] != "..": # add the color stuff 
            # highlight the selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # transparency value -> 0 transparent, 255 opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (col*SQ_SIZE, row*SQ_SIZE))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                screen.blit(s, (move.end_col * SQ_SIZE, move.end_row * SQ_SIZE))

    if invalid_sq != ():
        row, col = invalid_sq
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100) # transparency value -> 0 transparent, 255 opaque
        s.fill(p.Color('red'))
        screen.blit(s, (col*SQ_SIZE, row*SQ_SIZE))
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
    list_of_moves = []
    state.white_to_move = True
    invalid_sq = ()
    while running: 
        for e in p.event.get():
            
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:

                white_pinned = 0
                black_pinned = 0
                for piece in state.white_playable_pieces:
                    if piece.is_pinned:
                        white_pinned += 1
                for piece in state.black_playable_pieces:
                    if piece.is_pinned:
                        black_pinned +=1 
                
                in_check, pins, checks = state.check_for_pins_and_checks()

                
                location = p.mouse.get_pos() # (x,y) location of mouse
                col = location[0]//SQ_SIZE   # double / ensures that row and col are ints
                row =  location[1]//SQ_SIZE
                if state.board[row][col] == ".." and len(player_clicks) == 0: # user selected an empty square first
                    pass
                elif len(player_clicks) == 0 and ((not state.white_to_move and state.board[row][col].color == "white") or \
                    (state.white_to_move and state.board[row][col].color == "black")):
                    invalid_sq = (row, col)
                    pass
                else:
                    invalid_sq = ()
                    selected_square = (row, col)
                    player_clicks.append(selected_square)
                    if player_clicks != [] and state.board[player_clicks[0][0]][player_clicks[0][1]] != "..":
                        piece_selected = state.board[player_clicks[0][0]][player_clicks[0][1]]
                        print(piece_selected)
                        list_of_moves = state.get_valid_moves(piece_selected)
                        if len(list_of_moves) == 0:
                            invalid_sq = (player_clicks[0][0], player_clicks[0][1])

                    if len(player_clicks) == 2:
                        if player_clicks[0] == player_clicks[1]:
                            pass
                        else:
                            move = ChessEngine.Move(player_clicks[0], player_clicks[1], state.board)
                            #piece_selected = state.board[player_clicks[0][0]][player_clicks[0][1]]
                            #list_of_moves = piece_selected.possible_moves()
                            for element in list_of_moves:
                                if move == element:
                                    state.make_move(element)
                                    break
                        selected_square = ()
                        player_clicks = []


            #ket handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo when key 'z' is pressed
                    state.undo_move()
                if e.key == p.K_x: # redo when key 'x' is pressed
                    state.redo_move()
                    
        
        #draw_game_state(screen, state)
        draw_board(screen)               # draw squares on the board
        highlight_squares(screen, state, list_of_moves, selected_square, invalid_sq)
        draw_pieces(screen, state.board)
        
        clock.tick(MAX_FPS)
        p.display.flip()

if __name__ == "__main__":
    main()
    