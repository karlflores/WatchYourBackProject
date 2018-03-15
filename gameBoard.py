'''
BOARD GAME CLASS -- INCLUDES ALL THE MECHANICS FOR THE GAME

PARAMETERS:
    boardState
    history
    whitePos
    blackPos
    whiteAvailableMoves
    blackAvailableMoves
    phase
    counter

METHODS:
    readInitalBoardState()
    updateBoardState(piecePos,moveType)
    updatePhase(phase)
    isLegalMove(piecePos,moveType)
    convertMoveTypeToCoords(piecePos,moveType)
    printBoard()
    getPiecePos()
    updateAvailableMoves()

'''
import constant


class Board(object):

    # initialise the class
    def __init__(self):
        # define the board state

        # list to hold the representation of the current board state
        self.boardState = []

        # list to hold what previous moves have been made on the board so far
        self.history = []

        # list containing the current positions on the board
        self.whitePos = []
        self.blackPos = []

        # list containing the different available moves for both white
        # and black pieces they have available on the board
        self.whiteAvailableMoves = []
        self.blackAvailableMoves = []

        # phase of the game
        # 0 - placing phase
        # 1 - moving phase
        self.phase = constant.PLACEMENT_PHASE

        # move counter
        self.counter = 0

    def readInitialBoardState(self):

        # read 8 lines of std in to fulfill the board

        for i in range(constant.BOARD_SIZE):
            temp = input().strip('\n').split(' ')
            self.boardState.append(temp)

        # update the position of the pieces and its available moves
        self.getPiecePos()
        self.updateAvailableMoves()
        return

    # update the board state
    def updateBoardState(self,piecePos,moveType):
        # update the position on the board and check whether a piece/pieces are to be eliminated

        # move the piece -- get the piecetype, update to free space
        fromPosCol,fromPosRow = piecePos
        toPosCol,toPosRow = self.convertMoveTypeToCoord(piecePos,moveType)

        pieceType = self.boardState[fromPosRow][fromPosCol]
        self.boardState[fromPosRow][fromPosCol] = constant.FREE_SPACE

        # update the 'to' location with the old piecetype, only if the move is valid
        if self.isLegalMove(piecePos,moveType):
            self.boardState[toPosRow][toPosCol] = pieceType
        else:
            # return False -- error value, if the move is not valid, i.e a move has not been made
            return False

        # check nearby locations if a black/black pieces exist -- then check if these pieces
        # have been eliminated by the move that has been made

    # update the phase marker of the board
    def updatePhase(self,phase):
        if phase>=1:
            # return error value
            return 1

        self.phase = phase;
        # return success value
        return 0

    def isLegalMove(self,piecePos,moveType):

        # get the new position from moveType
        oldCol,oldRow = piecePos;
        newCol,newRow = self.convertMoveTypeToCoord(piecePos,moveType)

        # check if the piecePos is actually a piece, if not return false
        if self.boardState[oldRow][oldCol] not in (constant.WHITE_PIECE,constant.BLACK_PIECE):
            return False
        # need to test if the newCol, newRow are in the boundaries of the board
        if newCol < 0 or newCol > constant.BOARD_SIZE - 1:
            return False
        if newRow < 0 or newRow > constant.BOARD_SIZE - 1:
            return False

        # now need to test whether the new position on board is an free space on the board
        # if not, it is an invalid position, therefore cannot move to it then return false ;

        # first test one space moves
        if moveType <4 and moveType >=0:
            if self.boardState[newRow][newCol] == constant.FREE_SPACE:
                return True
            else:
                return False
        # test two step moves
        elif moveType >=4 and moveType <8:
            # need to test if the intermediate space is a player piece -- if true
            # return true
            # the relationship between one spaxe moveTypes and two space moveTypes is a difference of 4

            # get the one space position based on the moveType entered
            interPosCol,interPosRow = self.convertMoveTypeToCoord(piecePos,moveType-4)
            if self.boardState[interPosRow][interPosCol] in (constant.WHITE_PIECE,constant.BLACK_PIECE):
                return True
            else:
                return False



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
        colPiecePos,rowPiecePos = piecePos;

        # do the conversion -- this function does not handle
        if moveType == 0:
            return colPiecePos + 1, rowPiecePos
        elif moveType == 1:
            return colPiecePos, rowPiecePos + 1
        elif moveType == 2:
            return colPiecePos - 1, rowPiecePos
        elif moveType == 3:
            return colPiecePos, rowPiecePos - 1
        elif moveType == 4:
            return colPiecePos + 2, rowPiecePos
        elif moveType == 5:
            return colPiecePos, rowPiecePos + 2
        elif moveType == 6:
            return colPiecePos - 2, rowPiecePos
        elif moveType == 7:
            return colPiecePos, rowPiecePos - 2

    def printBoard(self):
        # iterate through the array representing the boardState and
        # print each element
        for row in range(constant.BOARD_SIZE):
            for col in range(constant.BOARD_SIZE):
                print("{} ".format(self.boardState[row][col]),end = '')
            print('\n',end = '')
        return

    # get the position of each piece on the board
    def getPiecePos(self):
        # iterate through the boardState and check for pieces, then append to list
        for row in range(constant.BOARD_SIZE):
            for col in range(constant.BOARD_SIZE):
                if self.boardState[row][col] == constant.WHITE_PIECE:
                    self.whitePos.append((col,row))
                elif self.boardState[row][col] == constant.BLACK_PIECE:
                    self.blackPos.append((col,row))
        return

    # update the available moves based on the current positions of pieces on the board
    def updateAvailableMoves(self):
        # update the white piece available positions
        for piecePos in self.whitePos:
            for moveType in range(constant.MAX_MOVETYPE):
                if self.isLegalMove(piecePos,moveType):
                    # append to available moves if moveType is legal -- this is in the form of
                    # a tuple (piecePos,newPos)
                    # both piecePos and newPos are tuples
                    self.whiteAvailableMoves.append((piecePos,self.convertMoveTypeToCoord(piecePos,moveType)))

        # update the black piece available positions
        for piecePos in self.blackPos:
            for moveType in range(constant.MAX_MOVETYPE):
                if self.isLegalMove(piecePos,moveType):
                    # append to available moves if moveType is legal -- this is in the form of
                    # a tuple (piecePos,newPos)
                    # both piecePos and newPos are tuples
                    self.blackAvailableMoves.append((piecePos,self.convertMoveTypeToCoord(piecePos,moveType)))