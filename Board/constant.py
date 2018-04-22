'''
THIS FILE CONTAINS THE GLOBAL VARIABLES FOR THE GAME BOARD
INCLUDE IN Board.py
'''

# GLOBAL VARIABLES
BOARD_SIZE = 8
MAX_MOVETYPE = 8
MAX_NUM_PIECES = 12
# space types
FREE_SPACE = '-'
CORNER_PIECE = 'X'
WHITE_PIECE = 'O'
BLACK_PIECE = '@'
INVALID_SPACE = '.'
SPACE_NOT_EXIST = -1

# phases
PLACEMENT_PHASE = 0
MOVING_PHASE = 1
TERMINAL = 2

# move types

# to the get the reverse move add 2
# to get a 2 square move -- add 4

RIGHT_1 = 0
DOWN_1 = 1
LEFT_1 = 2
UP_1 = 3
RIGHT_2 = 4
DOWN_2 = 5
LEFT_2 = 6
UP_2 = 7


# search constants

# IDDFS and DLS
FAILURE = None
CUTOFF = -2
NO_SOLUTION = -3
MAX_DEPTH = 100
