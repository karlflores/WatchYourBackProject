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
        self.best_move = None
        self.value = 0
        self.depth = 0
        self.type = None
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

    def contains(self, boardstr, colour):
        key = (boardstr,colour)
        if key in self.tt:
            return True
        else:
            return None

    def get_entry(self, boardstr, colour):
        tup = (boardstr, colour)
        if self.contains(boardstr, colour):
            self.value = self.tt[tup][0]
            self.type = self.tt[tup][1]
            self.best_move = self.tt[tup][2]
            self.depth = self.tt[tup][3]
            return self.tt[tup]

    def remove(self,tt, tup):
        if self.contains(tt,tup):
            tt.pop(tup)
            self.size -= 1

    # clear the dict
    def clear(self):
        self.tt.clear()
        self.empty = True
        self.best_move = None
        self.value = 0
        self.type = None
        self.size = 0
        self.tt = {}

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