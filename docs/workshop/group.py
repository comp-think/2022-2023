# This is a fake (i.e. it fails) implementation of the 'do_move' 
# function, that does always select an invalid couple of coordinates
# as next move to run. Change the body of the function to provide 
# better instructions to play The Cracked Chess.
def do_move(board, current, exit, notebook):
    new_move = (-1, -1)
    return new_move, notebook