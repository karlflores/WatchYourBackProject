# this class is a book of opening moves for each player -- we only use this in the placement phase of the game.
from Constants import constant
from Data_Structures.Transposition_Table import TranspositionTable


class ActionBook(object):

    def __init__(self,colour):
        self.action_book_start = {}

        # IMPLEMENT THESE LATER ...
        self.action_book_mid = {}
        self.aciton_bood_end = {}

        if colour == constant.WHITE_PIECE:
            self.placement_book_white()
        else:
            self.placement_book_black()

    def placement_book_white(self):

        action_book = {}
        action_book.update({'X------X------------------------------------------------X------X': (3,3)})
        action_book.update({'X------X-------------------O--------@-------------------X------X': (2,4)})
        action_book.update({'X------X-------------------O@---------------------------X------X': (5,3)})
        action_book.update({'X------X-----------@-------O----------------------------X------X': (3,4)})
        action_book.update({'X------X-----------@-------O----------------------------X------X': (3,4)})
        action_book.update({'X------X-----------O--------@------O--------@-----------X------X': (2,3)})
        action_book.update({'X------X-----------O--------@------O--------@-----------X------X': (2,3)})
        action_book.update({'X------X-----------O-------O@-------@-------------------X------X': (5,3)})
        action_book.update({'X------X-----------O-------@-------@O-------------------X------X': (2,4)})
        action_book.update({'X------X-----------O--------@-O----O------@-@-----------X------X': (5,3)})
        action_book.update({'X------X-----------O------@-@OO----O------@-@-----------X------X': (3,3)})
        action_book.update({'X------X-----------O------@O-OO----O------@-@-@---------X------X': (4,3)})
        action_book.update({'X------X-----------O------@OOOO----O------@-@-@---------X------X': (4,4)})
        self.action_book_start = action_book

    def placement_book_black(self):
        action_book = {}
        action_book.update({'X------X-------------------O----------------------------X------X': (4,4)})
        action_book.update({'X------X--------------------O---------------------------X------X': (3,4)})
        action_book.update({'X------X---------------------------O--------------------X------X': (4,3)})
        action_book.update({'X------X----------------------------O-------------------X------X': (3,3)})
        action_book.update({'X------X-------------------OO-------@-------------------X------X': (4,2)})
        action_book.update({'X------X-------------------O------O-@-------------------X------X': (5,3)})
        action_book.update({'X------X-------------------O--------@------O------------X------X': (5,3)})
        action_book.update({'X------X------------------OO--------@-------------------X------X': (3,5)})
        action_book.update({'X------X------------------OO------O-@------@------------X------X': (3,4)})
        action_book.update({'X------X------------------OO-------O@------@------------X------X': (2,4)})
        action_book.update({'X------X------------------OO--------@-----O@------------X------X': (1,5)})
        action_book.update({'X------X------------------O-@------O--------------------X------X': (5,4)})
        action_book.update({'X------X-------------------O@------O--------------------X------X': (2,3)})
        action_book.update({'X------X--------------------@------OO-------------------X------X': (4,5)})
        action_book.update({'X------X-----------O------O-@------O-@------------------X------X': (5,2)})
        self.action_book_start = action_book

    def check_state(self,board_arr):
        board_str = board_arr.decode("utf-8")

        if board_str in self.action_book_start:
            # return the move corresponding to the state
            return self.action_book_start[board_str]

        # check for symmetries -- we will only check for horizontal symmetries
        new_board = TranspositionTable.apply_horizontal_reflection(board_arr)
        new_board_str = new_board.decode("utf-8")
        if new_board_str in self.action_book_start:
            action = self.action_book_start[new_board_str]

            # apply move rotation - just need to reflect the move horizontally
            col,row = action

            # (0,1) --> (0,6) or (4,3) -> (4,4) ...
            return col, 7 - row

        return None
