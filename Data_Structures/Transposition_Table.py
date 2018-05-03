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
    def __init__(self):

        pass

    @staticmethod
    def add_entry(tt,bytearr, colour,tt_type,best_move,):
        str_rep = bytearr.decode("utf-8")
        tup = (hash, colour)
        temp_dict = {tup: (minmax_val,tt_type,best_move)}
        tt.update(hash)

    @staticmethod
    def contains(tt,tup):
        if tup in tt:
            return True
        else:
            return None

    @staticmethod
    def get_val(tt,tup):
        if TranspositionTable.contains(tt,tup):
            return tt[tup]

    @staticmethod
    def remove(tt, tup):
        if TranspositionTable.contains(tt,tup):
            tt.pop(tup)

    @staticmethod
    def check_placement_sym(tt, board_state):
        # check two transformations for now
        transformation_1 = TranspositionTable.apply_horizontal_reflection(board_state)

        board = copy(board_state)

        if transformation_1.decode("utf-8") in tt:
            return True
        else:
            tt.add(board.decode("utf-8"))
            return False

    @staticmethod
    def check_already_visited(tt,board_state):
        # check two transformations for now
        transformation_1 = TranspositionTable.apply_horizontal_reflection(board_state)
        transformation_2 = TranspositionTable.apply_vertical_reflection(board_state)

        board = copy(board_state)

        if transformation_1.decode("utf-8") in tt or transformation_2.decode("utf-8") in tt:
            return True
        elif board.decode("utf-8") in tt:
            return True

        tt.add(board.decode("utf-8"))
        return False

    @staticmethod
    def apply_horizontal_reflection(board_state):
        temp = ''
        for index in range(constant.BOARD_SIZE ** 2):
            temp += constant.FREE_SPACE

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
        temp = ''
        for index in range(constant.BOARD_SIZE ** 2):
            temp += constant.FREE_SPACE

        temp = bytearray(temp, 'utf-8')

        for row in range(constant.BOARD_SIZE):
            for col in range(constant.BOARD_SIZE):
                Board.set_array_char(temp, 7 - row, col,
                                     Board.get_array_element(board_state, row, col))

        return temp