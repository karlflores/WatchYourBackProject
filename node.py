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

    # evaluation function - counts the number of black pieces on the board
    def countNum(self):
        # print(len(self.board.piecePos[constant.BLACK_PIECE]))
        return len(self.board.piecePos[constant.BLACK_PIECE])

    # evaluation function -- returns the combined manhattan distance of the node
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

    def averageManhattanDist(self):
        return self.totalManhattanDist()/len(self.board.piecePos[constant.BLACK_PIECE])

    @staticmethod
    def eucledianDist(a,b):
        return math.sqrt((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1]))

    def averageEucledDist(self):
        total = 0

        for white in self.board.piecePos[constant.WHITE_PIECE]:
            for black in self.board.piecePos[constant.BLACK_PIECE]:
                total += self.eucledianDist(white,black)

        return total/len(self.board.piecePos[constant.BLACK_PIECE])

    # evaluation function -- returns the depth of the node
    def returnDepth(self):
        return self.depth

    def __lt__(self,other):
        return self.priority < other.priority

    # checks if the board is in a solvable state -- checks if there are more than 2 white pieces on the board
    def isSolveable(self):
        if len(self.board.piecePos[constant.WHITE_PIECE]) >= 2:
            return True
        else:
            return False
