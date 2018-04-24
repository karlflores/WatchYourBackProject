from Board import constant
from Board.Board import Board
from Agents.MCTS import MonteCarloTreeSearch
from copy import deepcopy

class Node(object):
    def __init__(self,board,colour):
        self.board = deepcopy(board)
        self.colour = colour
        self.parent = None
        self.move = None
        self.ucb_value = 0
        self.wins = 0
        self.available_moves = []

        # test the dictionary for the available moves
        # each piece has their available able
        self.available_actions = {constant.WHITE_PIECE: {}, constant.BLACK_PIECE: {}}
        # initialise the available actions
        self.init_available_actions()

        self.wins = 0
        self.visit_num = 0
        self.child = []

    def add_child(self,node):
        self.child.append(node)
    def init_available_actions(self):

        for row in range(constant.BOARD_SIZE):
            for col in range(constant.BOARD_SIZE):

    def update_available_moves(self,action):
        # read in the pieces on the board -- if they already exist in the dictionary
        # then we dont need to do anything -- if they don't exist in the dictionary
        # need to look at all the eliminated pieces on the board
        #   -- look for pieces in the vicinity of that space
        #   -- delete keys associated with those eliminated pieces as these are pieces on the board
        #   -- that do not exists anymore, therefore there are no associated moves with this piece
        #   -- update the available moves of the pieces that can move into that square
        # need to update the available moves of the piece at its new location
        # delete entry in the dictionary that corresponds to the old position

    def update_available_placement(self,action):

        # read in the available

    def get_action_list(self):
        if board.phase == constant.PLACEMENT_PHASE:
            pass
        elif board.phase == constant.MOVING_PHASE:
            pass

