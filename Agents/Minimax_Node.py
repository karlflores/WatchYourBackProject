'''
* SEARCHABLE NODE STRUCTURE FOR MINIMAX / ALPHABETA SEARCH
'''


from Evaluation.Policies import Evaluation
from Board.Board import Board
from copy import deepcopy


class Node(object):
    def __init__(self, board, colour):
        self.board = deepcopy(board)
        self.depth = 0
        self.move_applied = None
        self.parent = None
        self.colour = colour
        self.available_moves = []

    # it is a leaf node if terminal
    def is_leaf(self):
        return self.board.is_terminal()

    # set the next colour
    def next_colour(self):
        self.colour = Board.get_opp_piece_type(self.colour)

    def evaluate(self):
        self.eval = Evaluation.basic_policy(self.board.board_state)