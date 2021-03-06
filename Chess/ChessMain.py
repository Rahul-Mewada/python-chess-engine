"""
Main driver file, responsible for handling user input and
 displaying the current Game State object
"""
import pygame as p
import ChessEngine
import ChessBot as bot
import time
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
                if move.start_row == row and move.start_col == col:
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

def draw_text(screen, text):
    font = p.font.SysFont("Helvetica", 35, True, False)
    text_object = font.render(text, 0, p.Color('Orange'))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - text_object.get_width()/2, HEIGHT/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)
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
    piece_moves = []
    state.white_to_move = True
    invalid_sq = ()
    player_one = True # if a human is playing white this will be true. If an AI is playing then this is false
    player_two = False # same as the above but for black
    game_over = False
    move_made = False
    is_undo = False
    list_of_moves = state.get_valid_moves()
    while running: 
        #print(state.white_to_move)
        is_human_turn = (state.white_to_move and player_one) or (not state.white_to_move and player_two)
        for e in p.event.get():
            invalid_sq = ()
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                
                if not game_over and is_human_turn:
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
                        print("...........................")
                        print()
                        print("Inside invalid sq elif")
                        print(state.white_to_move)
                        print(state.board[row][col].color)
                        print()
                        invalid_sq = (row, col)
                        pass
                    else:
                        selected_square = (row, col)
                        player_clicks.append(selected_square)
                        if player_clicks != [] and state.board[player_clicks[0][0]][player_clicks[0][1]] != "..":
                            piece_selected = state.board[player_clicks[0][0]][player_clicks[0][1]]
                            # LIST OF MOVES HERE
                            piece_moves = []
                            for move in list_of_moves:
                                if move.start_row == piece_selected.row and move.start_col == piece_selected.col:
                                    piece_moves.append(move)
                            if len(piece_moves) == 0:
                                for move in list_of_moves:
                                    piece_moved = move.piece_moved
                                invalid_sq = (player_clicks[0][0], player_clicks[0][1])
                                selected_sqaure = ()
                                player_clicks = []
                        if len(player_clicks) == 2:
                            if player_clicks[0] == player_clicks[1]:
                                pass
                            else:
                                move = ChessEngine.Move(player_clicks[0], player_clicks[1], state.board)
                                #piece_selected = state.board[player_clicks[0][0]][player_clicks[0][1]]
                                #list_of_moves = piece_selected.possible_moves()
                                for element in piece_moves:
                                    if move == element:
                                        state.make_move(element)
                                        move_made = True
                                        break
                            selected_square = ()
                            player_clicks = []
                            invalid_sq = ()
            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo when key 'z' is pressed
                    i = 0
                    state.undo_move()
                    move_made = True
                    is_undo = True
                if e.key == p.K_x: # redo when key 'x' is pressed
                    state.redo_move()

        # AI Move finder logic
        if not game_over and not is_human_turn and not is_undo:
            ai_move = bot.find_minimax_move(state, list_of_moves)
            state.make_move(ai_move)
            move_made = True

        if move_made:
            list_of_moves = state.get_valid_moves()
            move_made = False
            is_undo = False

        #draw_game_state(screen, state)
        draw_board(screen)               # draw squares on the board
        highlight_squares(screen, state, piece_moves, selected_square, invalid_sq)
        draw_pieces(screen, state.board)
        
        if state.checkmate:
            game_over = True
            if state.white_to_move:
                draw_text(screen, "Black Wins")
            else:
                draw_text(screen, "White Wins")
        elif state.stalemate:
            game_over = True
            draw_text(screen, "Stalemate")

        clock.tick(MAX_FPS)
        p.display.flip()

if __name__ == "__main__":
    main()
    