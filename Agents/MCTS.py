from math import inf,sqrt,log
from Agents.MCTS_Node import Node
from Board.Board import constant
from Board.Board import Board
from Evaluation.Policies import Evaluation
from copy import deepcopy

class MonteCarloTreeSearch(object):
    def __init__(self,root):
        self.root = root

    def MCTS(self,root):
        # is the root a child node
        if len(root.child) == 0:
            self.expand(root)
        pass

    def simulate(self,node):

        node.available_move

    @staticmethod
    def backpropagate_value(node,value):
        while node is not None:
            node.visit_num += 1
            node.wins += value
            node = node.parent

    def expand(self):
        pass

    def UCB1(self,node,explore_param):

        evaluate = node.wins/node.visit_num +\
                   explore_param*sqrt(log(node.parent.visit_num)/node.visit_num)

        node.ucb_value = evaluate


    def best_move(self):
        pass

    def UCB1_traversal(self,explor_param):


    def update_root(self):
        self.root = root

    @staticmethod
    def create_node(board,colour,move,parent):
        node = Node(board,colour)
        node.move = move
        node.parent = parent
        return node
    def make_move(self):


