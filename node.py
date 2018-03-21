import constant
from copy import deepcopy
import math
class Node(object):
    def __init__(self,board,move):
        # deep copy the board such that any changes that are made
        # to this instance of board are only made to this instance of the board
        self.board = deepcopy(board)
        self.depth = 0
        self.parent = None
        self.counter = 0

        # this stores the move applied to a certain node to bring it to the state that it is in
        # move should be in the form (tup1,tup2) where tup1 is the original location and tup2 is the
        # location where the piece has moved to
        self.moveApplied = move

        self.priority = 0

    def updateCounter(self):
        self.counter+=1
        return

    def updateDepth(self):
        self.depth+=1
        return

    def isGoalState(self):
        # checks if the node is at the goal state, for this to occur test whether the
        # there are less than 2 black pieces on the board
        if len(self.board.piecePos[constant.BLACK_PIECE]) == 0:
            return True
        else:
            return False

    def countNum(self):
        # print(len(self.board.piecePos[constant.BLACK_PIECE]))
        return len(self.board.piecePos[constant.BLACK_PIECE])

    def totalManhattanDist(self):
        dist = 0
        for white in self.board.piecePos[constant.WHITE_PIECE]:
            for black in self.board.piecePos[constant.BLACK_PIECE]:
                x = white[0] - black[0]
                y = white[1] - black[1]
                if x < 0:
                    x = -x
                if y < 0:
                    y = -y
                dist += x+y

        return dist

    def returnDepth(self):
        return self.depth

    def __lt__(self,other):
        return self.priority < other.priority

