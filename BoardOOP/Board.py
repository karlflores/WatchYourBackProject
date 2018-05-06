from Board import constant
class Board(object):

    # a class to represent the board state of the game
    def __init__(self):

        # initialise the board with the corner pieces
        # this dictionary keeps track of the board and the pieces that are currently on the board
        self.cells = {(0,0): constant.CORNER_PIECE, (7,0): constant.CORNER_PIECE,\
                      (7,0): constant.CORNER_PIECE,(7,7): constant.CORNER_PIECE}


