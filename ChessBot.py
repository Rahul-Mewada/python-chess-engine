import random

'''
Picks a random move
'''
def find_random_move(valid_moves):
    rand_index = random.randint(0, len(valid_moves) - 1)
    return valid_moves[rand_index]

'''
Looks 1 move ahead and tries to maximize points per turn
'''
def find_greedy_move(state, valid_moves):
    # white wants to max while black wants to minimize
    turn_multiplier = 1 if state.white_to_move else -1
    max_score = -10000 
    best_move = None
    for player_move in valid_moves:
        state.make_move(player_move)
        opponents_moves = state.get_valid_moves()
        tot_points = state.evaluate_state()  * turn_multiplier
        if tot_points > max_score:
            max_score = tot_points
            best_move = player_move
        state.undo_move()

    return best_move

def find_minimax_move(state, valid_moves):
    # white wants to max while black wants to minimize
    turn_multiplier = 1 if state.white_to_move else -1
    opponent_minmax_score = 10000 
    best_player_move = None
    for player_move in valid_moves:
        state.make_move(player_move)
        opponent_moves = state.get_valid_moves()
        opponent_max_score = -10000

        for opponent_move in opponent_moves:
            state.make_move(opponent_move)
            if state.checkmate:
                tot_points = -turn_multiplier * 10000
            elif state.stalemate:
                tot_points = 0
            else:
                tot_points = state.evaluate_state()  * -turn_multiplier
            if tot_points > opponent_max_score:
                opponent_max_score = tot_points
            state.undo_move()

        if opponent_max_score < opponent_minmax_score:
            opponent_minmax_score = opponent_max_score
            best_player_move = player_move
        state.undo_move()

    return best_player_move
