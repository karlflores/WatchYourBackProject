from Board import constant
from math import sqrt
class Board(object):

    # a class to represent the board state of the game
    def __init__(self):

        # initialise the board with the corner pieces
        # this dictionary keeps track of the board and the pieces that are currently on the board
        # define the board parameters and constants
        self.board_state = self.init_board_rep()

        # self.piece_pos = {constant.BLACK_PIECE: {-1:}, constant.WHITE_PIECE: []}
        # store the current position of pieces on the board

        # key -- the position of the pieces
        # value -- the piece object
        # when we place a piece on the board we update pieces_remaining and we look at any neighbours in a 2 block radius
        # we need to update these pieces neighbour positions to being False -- a
        self.pieces = {constant.WHITE_PIECE: {},
                          constant.BLACK_PIECE: {}}

        self.places_remaining = {constant.WHITE_PIECE: 12, constant.BLACK_PIECE: 12}

        # initialise the board representation
        # LT RT LB RB
        self.corner_pos = [(0, 0), (7, 0), (0, 7), (7, 7)]

        # how many moves have been applied to the board so far
        self.move_counter = 0
        self.phase = constant.PLACEMENT_PHASE
        self.num_shrink = 0

        # initially no one wins
        self.winner = None
        self.terminal = False

        # who is moving first
        self.player_to_move = None

    def init_board_rep(self):
        # store the board representation as a byte_array length 64 (64bytes)
        temp = ''
        for index in range(constant.BOARD_SIZE * constant.BOARD_SIZE):
            temp += constant.FREE_SPACE
        # create a temp string of length 64
        temp = bytearray(temp,'utf-8')

        # set the corner locations on the board representation

        for col,row in self.corner_pos:
            self.set_array_char(temp, row, col, constant.CORNER_PIECE)

        return temp

# string_array helper methods
    @staticmethod
    def get_array_element(byte_array,row,col):
        # we assume that the string array is n x n in dimension

        # get the dimension
        dimension = constant.BOARD_SIZE
        # check if row and col are valid
        if row > dimension - 1 or col > dimension - 1:
            return None

        elif row < 0 or col < 0:
            return None
        # get the index to access in the string
        index = row*dimension + col

        # return the char at position index
        return chr(byte_array[index])

    @staticmethod
    def set_array_char(byte_array, row, col, new_char):
        dimension = constant.BOARD_SIZE

        if row > dimension - 1 or col > dimension - 1:
            return
        elif row < 0 or col < 0:
            return

        # set the new char in the string
        # need to turn char into utf-8 encoding first
        byte_array[row * dimension + col] = ord(new_char)

