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
        self.evaluation = 0
        self.expand = True
        self.available_moves = []
        self.wins = 0
        self.visit_num = 0

