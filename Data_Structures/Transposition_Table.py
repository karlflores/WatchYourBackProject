from copy import copy
from Board import constant
from Board.Board import Board
'''
We can use a dictionary to store any visited node in the search -- just store the board representation 
as a tuple with the player that made that move and the board representation itself -- this is the key
The value of the search is the minimax value for that search -- therefore if 
we want to evaluate the minimax value for a particular state, we can just look it up in the table if it has 
been visited before, if not we can just evaluate minimax for that state then store this value in the 
transposition table 

Therefore as we play the game we grow the transposition table -- but this will take up a lot of memory, hence we require
a way to discard old states -- thus need to look into using a cache of some sort, which gets rid of items in the cache 
that have not been accessed recently, and therefore can be evicted from the cache 

'''

# we treat a dictionary as a transposition table
class TranspositionTable:
    def __init__(self,MAX_SIZE=100000):
        self.empty = True
        self.size = 0
        self.tt = {}
        self.keys = {}
        self.MAX_SIZE = MAX_SIZE

    def add_entry(self,bytearr, colour, val, tt_type, best_move, depth):
        if self.empty:
            self.empty = False

        str_rep = bytearr.decode("utf-8")
        tup = (str_rep, colour)
        temp_dict = {tup: (val,tt_type,best_move, depth)}
        self.tt.update(temp_dict)
        self.size += 1

    def contains(self, board, colour,phase=constant.MOVING_PHASE):
        boardstr = copy(board)
        key = (boardstr, colour)
        if key in self.tt:
            # print("TRUE")
            return key

        # turn board string into
        temp = bytearray(boardstr, "utf-8")

        '''
                CHECK FOR ROTATIONS/SYMMETRIES AND SHIT 
        '''

        rotation_arr = []
        # check horizontal and vertical symmetry

        rotation_arr.append(TranspositionTable.apply_horizontal_reflection(temp))
        if phase == constant.MOVING_PHASE:
            # check vertical reflection
            rotation_arr.append(TranspositionTable.apply_vertical_reflection(temp))
            # check rotation 90L
            rotation1 = TranspositionTable.apply_90l_rot(temp)
            rotation_arr.append(rotation1)
            # check rotation 180l
            rotation2 = TranspositionTable.apply_90l_rot(rotation1)
            rotation_arr.append(rotation2)
            # check rotation 270L
            rotation3 = TranspositionTable.apply_90l_rot(rotation2)
            rotation_arr.append(rotation3)

        # check all rotations first
        for board in rotation_arr:
            key = (board.decode("utf-8"), colour)
            if key in self.tt:
                # print("FOUND ROTATION")
                return key
            else:
                return None

        # if there are no rotations in the TT and the original key is not in the TT therefore
        # this entry does not exist in the TT
        return None

    def get_entry(self, boardstr, colour):
        tup = (boardstr, colour)
        key = self.contains(boardstr, colour)
        if key is not None:
            return self.tt[tup]

    def remove(self,tt, tup):
        if self.contains(tt,tup):
            tt.pop(tup)
            self.size -= 1

    # clear the dict
    def clear(self):
        self.tt.clear()
        self.empty = True
        self.size = 0
        self.tt = {}

    @staticmethod
    def apply_horizontal_reflection(board_state):
        temp = '-'*64
        temp = bytearray(temp, 'utf-8')

        for row in range(constant.BOARD_SIZE):
            for col in range(constant.BOARD_SIZE):
                Board.set_array_char(temp, row, 7 - col,
                                     Board.get_array_element(board_state, row, col))
        # print(temp)
        # print(board_state)
        return temp

    @staticmethod
    def apply_vertical_reflection(board_state):
        temp = '-'*64
        temp = bytearray(temp, 'utf-8')

        for row in range(constant.BOARD_SIZE):
            for col in range(constant.BOARD_SIZE):
                Board.set_array_char(temp, 7 - row, col,
                                     Board.get_array_element(board_state, row, col))

        return temp

    @staticmethod
    def apply_90r_rot(board_state):
        temp = copy(board_state)
        TranspositionTable.transpose_arr(temp)
        for row in range(constant.BOARD_SIZE):
            TranspositionTable.reverse_row(temp,row)
        return temp


    @staticmethod
    def apply_90l_rot(board_state):
        temp = copy(board_state)
        TranspositionTable.transpose_arr(temp)
        for col in range(constant.BOARD_SIZE):
            TranspositionTable.reverse_col(temp, col)
        return temp

    @staticmethod
    def transpose_arr(arr):
        for row in range(constant.BOARD_SIZE):
            for col in range(constant.BOARD_SIZE):
                temp_ij = Board.get_array_element(arr,row,col)
                temp_ji = Board.get_array_element(arr,col,row)
                Board.set_array_char(arr,row,col,temp_ji)
                Board.set_array_char(arr,col,row,temp_ij)
        return arr

    @staticmethod
    def reverse_row(arr,row):
        for col in range(constant.BOARD_SIZE):
            temp_start = Board.get_array_element(arr,row,col)
            temp_end = Board.get_array_element(arr,row,7-col)
            # swap
            Board.set_array_char(arr, row, col, temp_end)
            Board.set_array_char(arr, row, 7-col, temp_start)
        return arr

    @staticmethod
    def reverse_col(arr, col):
        for row in range(constant.BOARD_SIZE):
            temp_start = Board.get_array_element(arr, row, col)
            temp_end = Board.get_array_element(arr, 7-row, col)
            # swap
            Board.set_array_char(arr, row, col, temp_end)
            Board.set_array_char(arr, 7-row, col, temp_start)
        return arr
