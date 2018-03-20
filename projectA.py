from gameBoard import Board
import constant

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
        massacre()


def moves(boardState):
    print(len(boardState.availableMoves[constant.WHITE_PIECE]))
    print(len(boardState.availableMoves[constant.BLACK_PIECE]))
    return

def massacre():
    pass


if __name__ == "__main__":
    main()