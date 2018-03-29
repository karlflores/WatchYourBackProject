from gameBoard import Board
import constant
from Massacre import Massacre
from node import Node
from time import time

def main():

    # create board instance
    root = Board()

    # read in initial board state from stdin
    root.readInitialBoardState()

    # input specifying whether to execute Moves or Massacre
    analysisType = input().strip('\n')
    if analysisType == 'Moves':
        moves(root)
    elif analysisType == 'Massacre':
        startTime = time()
        massacre(root)
        print("TIME ELAPSED: " + str(time()-startTime))


def moves(boardState):
    print(len(boardState.availableMoves[constant.WHITE_PIECE]))
    print(len(boardState.availableMoves[constant.BLACK_PIECE]))
    return


def massacre(board):
    # create the root of the search
    root = Node(board, None)

    # create the massacre instance
    search = Massacre(root)

    # do the search using IDDFS
    # IDDFS ensures an optimal solution since it will terminate the the least moves
    # possible
    solution = search.IDDFS(root)

    # if the solution is None, therefore no solution exists and we print no Solution
    if solution is None:
        print("NO SOLUTION: CUTOFF REACHED")
        return
    elif solution is constant.FAILURE:
        print("SEARCH FAILED")
        return
    elif solution is constant.NO_SOLUTION:
        print("NO SOLUTION FOR INPUT BOARD STATE")
        return

    # get the sequence of modes from the terminal node
    reconstructPath(solution)
    return

# helper method for massacre to reconstruct the path from the solution node
def reconstructPath(node):
    # create a list called moves applied
    movesApplied = []

    # trace through the parent nodes to print the solution
    while node is not None and node.moveApplied is not None:
        move = node.moveApplied
        moveCoordinates = node.board.convertMoveTypeToCoord(move[0],move[1])
        movesApplied.append(str(move[0]) + " -> " + str(moveCoordinates))

        # update the node to be the parent
        node = node.parent

    # reverse the move list such that the first element is the first move to be made
    movesApplied.reverse()

    # print the solution
    for move in movesApplied:
        print(move)
    return


if __name__ == "__main__":
    main()