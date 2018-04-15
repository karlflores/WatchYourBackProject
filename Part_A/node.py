from Part_A import constant
from copy import deepcopy


class Node(object):
    def __init__(self,board,move):
        # deep copy the board such that any changes that are made
        # to this instance of board are only made to this node and not the original.
        self.board = deepcopy(board)
        self.depth = 0
        self.parent = None

        # this stores the move applied to a certain node to bring it to the state that it is in
        # move should be in the form (tup1,moveType) where tup1 is the original location
        self.moveApplied = move

        # priority of the node -- could be the cost + heuristic -- used for greedy search
        self.priority = 0

    def isGoalState(self):
        # checks if the node is at the goal state, for this to occur test whether the
        # there are less than 2 black pieces on the board
        if len(self.board.piecePos[constant.BLACK_PIECE]) == 0:
            return True
        else:
            return False

    # HELPER FUNCTIONS FOR GREEDY SEARCH
    # evaluation function - counts the number of black pieces on the board
    def countBlackPieces(self):
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

    # evaluation function -- returns the depth of the node
    def returnDepth(self):
        return self.depth

    # comparision method for nodes -- used in heapq ordering
    def __lt__(self,other):
        return self.priority < other.priority

    # checks if the board is in a solvable state -- checks if there are more than 2 white pieces on the board
    def isSolveable(self):
        # next to corner pieces

        # if there are no black pieces on the board -- no solution
        if len(self.board.piecePos[constant.WHITE_PIECE]) == 0:
            return False

        # if there is one white piece on the board need to check if there are pieces next
        # to the corner pieces of the board
        elif len(self.board.piecePos[constant.WHITE_PIECE]) == 1:
            # enumerate all corner pieces
            nextToCornerPos = [(0, 1), (1, 0), (7, 1), (6, 0), (0, 6), (1, 7), (6, 7), (7, 6)]
            numNextToCornerPos = 0
            # count the number of black pieces next to the corner positions
            for piece in self.board.piecePos[constant.BLACK_PIECE]:
                if piece in nextToCornerPos:
                    numNextToCornerPos += 1
                    print(numNextToCornerPos)

            # if there are no pieces next to the corner pieces -- not solvable
            if numNextToCornerPos == 0:
                return False
            else:
                return True
        else:
            return True
