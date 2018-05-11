'''
THIS FILE CONTAINS THE GLOBAL VARIABLES FOR THE GAME BOARD, agents and players
'''

# GLOBAL VARIABLES
BOARD_SIZE = 8
MAX_MOVETYPE = 8
MAX_NUM_PIECES = 12
START_BOARD_STR = 'X------X------------------------------------------------X------X'

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

# UNDO ACTIONS CONSTANTS
ELIMINATED_PIECE = 'E'
PLACE_LOC = 'P'
PIECE_OLD_LOC = 'O'
PIECE_NEW_LOC = 'N'

# TRANSPOSITION ENTRY TABLE CONSTANTS
# PV Nodes -
TT_EXACT = 'E'
# Cut-Nodes - Fail-high
TT_UPPER = 'U'
#All-Nodes - Fail-low
TT_LOWER = 'L'


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
TIME_CUTOFF = 20000
TIME_CUTOFF_AB_PLACE = 600
TIME_CUTOFF_MOVING = 1500

# IDDFS and DLS
FAILURE = None
CUTOFF = -2
NO_SOLUTION = -3
MAX_DEPTH = 100