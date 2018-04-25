from Board import constant
from copy import deepcopy
from math import inf


class Node(object):
    def __init__(self,board,colour,move,parent):
        self.board = deepcopy(board)
        self.colour = colour
        self.parent = parent
        self.move = move
        self.ucb_value = inf

        self.untried_actions = []
        # test the dictionary for the available moves
        # each piece has their available able
        # self.available_actions = {constant.WHITE_PIECE: {}, constant.BLACK_PIECE: {}}
        # initialise the available actions
        # self.init_available_actions()

        self.wins = 0
        self.visit_num = 0
        self.children = []

    def add_child(self,node):
        self.children.append(node)

    def init_available_actions(self):
        for row in range(constant.BOARD_SIZE):
            for col in range(constant.BOARD_SIZE):
                pass

    def update_available_moves(self,action):
        pass
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
        pass
        # read in the available

    # this updates the available actions that the child node can make
    def update_actions(self):
        self.untried_actions = self.board.update_actions(self.board, self.colour)

    def is_leaf(self):
        # if there are no child nodes at this node then it is a leaf node
        if len(self.child) == 0:
            return True
        else:
            return False

    def __lt__(self,other):
        if other is None:
            return False

        return self.ucb_value < other.ucb_value

    def is_terminal(self):
        return self.board.is_terminal()

    def is_fully_expanded(self):
        # TODO -- NEED TO IMPLEMENT THIS FUNCTION
        # if all the actions have been tried then it has been
        # fully expanded
        if len(self.untried_actions) == 0:
            return True
        else:
            return False
