from Constants import constant
from copy import deepcopy
from math import inf
'''
NODE STRUCTURE FOR THE MCTS GAME TREE -- ALLOWS US TO TRAVERSE DOWN THE TREE AND ALSO 
UPDATE/BACKPROPAGATE ONCE WE REACH TERMINAL STATE 
'''


class Node(object):
    def __init__(self,board,colour,move,parent):
        self.board = deepcopy(board)
        self.colour = colour
        self.parent = parent
        self.move = move
        self.ucb_value = inf

        self.untried_actions = []

        self.wins = 0
        self.visit_num = 0
        self.children = []

    # add a child to this node
    def add_child(self,node):
        self.children.append(node)

    # this updates the available actions that the child node can make
    def update_actions(self):
        self.untried_actions = self.board.update_actions(self.board, self.colour)

    def is_leaf(self):
        # if there are no child nodes at this node then it is a leaf node
        if len(self.children) == 0:
            return True
        else:
            return False

    # compare override -- such taht we can sort node s
    def __lt__(self,other):
        if other is None:
            return False

        return self.ucb_value < other.ucb_value

    # terminal test
    def is_terminal(self):
        return self.board.is_terminal()

    # check if a node is fully expanded, thus we can start to expand its children
    def is_fully_expanded(self):
        # if all the actions have been tried then it has been ully expanded
        if len(self.untried_actions) == 0:
            return True
        else:
            return False
