import constant

class Board(object):
    #initialise the class
    def __init__(self):
        # define the board state

        # list to hold the representation of the current board state
        self.boardState = []

        # list to hold what previous moves have been made on the board so far
        self.history = [];

        # list containing the current positions on the board
        self.whitePos = [];
        self.blackPos = [];

        # list containing the different available moves for both white
        # and black pieces they have available on the board
        self.whiteAvailableMoves = [];
        self.blackAvailableMoves = [];

        # phase of the game
        # 0 - placing phase
        # 1 - moving phase
        self.phase = 0;

        # move counter
        self.counter = 0;

    def readInitialBoardState(self):

        # read 8 lines of std in to fulfill the board

        for i in range(constant.BOARD_SIZE):
            temp = input().strip('\n').split(' ');
            self.boardState.append(temp);
        return;

    # update the board state
    def updateBoardState(self,board,piecePosFrom,moveType):
        self.boardState = board;

    # update the phase marker of the board
    def updatePhase(self,phase):
        if(phase>=1):
            # return error value
            return 1

        self.phase = phase;
        # return success value
        return 0

    def isLegalMove(self,piecePos,moveType):
        pass

    def convertMoveTypeToCoord(self,piecePos,moveType):
        # piece pos is in the form of a tuple (col,row)
        # moves types
        # 0 - left 1 space
        # 1 - down 1 space
        # 2 - right 1 space
        # 3 - top 1 spaces

        # 4 - left 2 spaces
        # 5 - down 2 spaces
        # 6 - right 2 spaces
        # 7 - top 2 spaces

        # convert the tuple to row, col variable

        rowPiecePos,colPiecePos = piecePos;

        # do the conversion -- this function does not handle
        if moveType == 0:
            return rowPiecePos,colPiecePos + 1;
        elif moveType == 1:
            return rowPiecePos + 1, colPiecePos;
        elif moveType == 2:
            return rowPiecePos, colPiecePos - 1;
        elif moveType == 3:
            return rowPiecePos - 1, colPiecePos;
        elif moveType == 4:
            return rowPiecePos, colPiecePos + 2;
        elif moveType == 5:
            return rowPiecePos + 2, colPiecePos;
        elif moveType == 6:
            return rowPiecePos, colPiecePos - 2;
        elif moveType == 7:
            return rowPiecePos - 2, colPiecePos;

    def printBoard(self):
        for row in range(constant.BOARD_SIZE):
            for col in range(constant.BOARD_SIZE):
                print("{} ".format(self.boardState[row][col]),end = '')
            print('\n',end = '');

    # get the position of each piece on the board
    def getPiecePos(self):
        # iterate through the boardState and check for pieces, then append to list
        for row in range(constant.BOARD_SIZE):
            for col in range(constant.BOARD_SIZE):
                if self.boardState[row][col] == constant.WHITE_PIECE:
                    self.whitePos.append((col,row));
                elif self.boardState[row][col] == constant.BLACK_PIECE:
                    self.blackPos.append((col,row));
        return;