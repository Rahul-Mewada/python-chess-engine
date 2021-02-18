import random



def find_random_move(valid_moves):
    rand_index = random.randint(0, len(valid_moves) - 1)
    return valid_moves[rand_index]