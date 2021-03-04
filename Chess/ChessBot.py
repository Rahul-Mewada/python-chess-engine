import random



def find_random_move(valid_moves):
    rand_index = random.randint(0, len(valid_moves) - 1)
    return valid_moves[rand_index]

def find_greedy_move(state, valid_moves):
    turn_multiplier = 1 if state.white_to_move else -1
    max_score = -10000 
    best_move = None
    for player_move in valid_moves:
        print()
        print("Before making: " + str(state.white_to_move))
        state.make_move(player_move)
        tot_points = state.evaluate_state()  * turn_multiplier
        if tot_points > max_score:
            max_score = tot_points
            best_move = player_move
        state.undo_move()
        move = player_move
        piece = move.piece_moved
        print("Piece Moved: " + str(piece.color) + str(piece.name))
        print("Moved from " + str((move.start_row, move.start_col)) + " to " + str((move.end_row, move.end_col)))
        print("After undoing: " + str(state.white_to_move))
        print()
    return best_move

def find_minimax_move(state):
    if depth == 0 or state.checkmate or state.stalemate:
        return 

    for move in valid_moves:
        state.make_move(move)
        total_points = state.evaluate_state()