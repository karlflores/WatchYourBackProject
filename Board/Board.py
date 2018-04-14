'''
* Implements the board class for the game
*

'''

import constant
from copy import deepcopy
import math

class Board(object):

    def __init__(self):
        # define the board parameters and constants
        self.board_state = self.init_board_rep()

        self.piece_pos = {constant.BLACK_PIECE:[], constant.WHITE_PIECE: []}
        self.available_moves = {constant.BLACK_PIECE: [], constant.WHITE_PIECE: []}
        # initialise the board representation
        self.corner_pos = [(0, 0),(7, 0), (0, 7), (7, 7)]

        self.move_counter = 0
        self.phase = constant.PLACEMENT_PHASE
        self.num_shrink = 0

    def init_board_rep(self):
        # store the board representation as a byte_array length 64 (64bytes)
        temp = ''
        for index in range(constant.BOARD_SIZE*constant.BOARD_SIZE):
            temp += constant.FREE_SPACE
        # create a temp string of length 64
        temp = bytearray(temp,'utf-8')

        # set the corner locations on the board representation
        corner_pos = [(0,0),(0,7),(7,0),(7,7)]
        for col,row in corner_pos:
            self.set_array_char(temp,row,col,constant.CORNER_PIECE)

        return temp

    # board representation setters and getter methods
    def get_board_piece(self,row,col):
        return self.get_array_element(self.board_state,row,col)

    # change the piece type in the board representation
    def set_board(self,row,col,piece_type):
        piece_types = (constant.CORNER_PIECE,constant.WHITE_PIECE,constant.BLACK_PIECE,
                       constant.FREE_SPACE,constant.INVALID_SPACE)
        # check if the piece_rype is valid
        if piece_type not in piece_types:
            return

        # if valid we can set the board position
        self.set_array_char(self.board_state,row,col,piece_type)

    # print board method
    def print_board(self):

        for row in range(constant.BOARD_SIZE):
            for col in range (constant.BOARD_SIZE):
                # get the char to print
                char_index = row*constant.BOARD_SIZE + col

                char = chr(self.board_state[char_index])
                print('{} '.format(char),end='')

            print()

    # string_array helper methods
    @staticmethod
    def get_array_element(byte_array,row,col):
        # we assume that the string array is n x n in dimension

        # get the dimension
        dimension = int(math.sqrt(len(byte_array)))
        # check if row and col are valid
        if row > dimension - 1 or col > dimension - 1:
            return None

        elif row < 0 or col < 0:
            return None
        # get the index to access in the string
        index = row*dimension + col;

        # return the char at position index
        return chr(byte_array[index])

    @staticmethod
    def set_array_char(byte_array, row, col, new_char):
        dimension = int(math.sqrt(len(byte_array)))

        if row > dimension - 1 or col > dimension - 1:
            return
        elif row < 0 or col < 0:
            return

        # set the new char in the string
        # need to turn char into utf-8 encoding first
        byte_array[row * dimension + col] = ord(new_char)
