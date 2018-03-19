'''
BOARD GAME CLASS -- INCLUDES ALL THE MECHANICS FOR THE GAME

PARAMETERS:
    boardState
    piecePos
    availableMoves
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

    # helper methods
    checkOnePieceEliminations()
    checkSelfEliminations()

'''
import constant
from copy import deepcopy

class Board(object):

    # initialise the class
    def __init__(self):
        # define the board state

        # list to hold the representation of the current board state
        self.boardState = []

        # list to hold what previous moves have been made on the board so far
        self.history = []

        # create dictionaries to hold all the available moves and piece positions
        # on the board
        # map the board symbol types to the list for easy access
        self.piecePos = {constant.BLACK_PIECE: [],constant.WHITE_PIECE: []}
        self.availableMoves = {constant.BLACK_PIECE: [], constant.WHITE_PIECE: []}

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

        # move the piece -- get the piecetype and the oppositePiecetype, update to free space
        fromPosCol,fromPosRow = piecePos
        toPosCol,toPosRow = self.convertMoveTypeToCoord(piecePos,moveType)
        # print(toPosCol,toPosRow)
        pieceType = self.boardState[fromPosRow][fromPosCol]

        if pieceType == constant.WHITE_PIECE:
            # print("white")
            oppPieceType = constant.BLACK_PIECE
        else:
            # print("black")
            oppPieceType = constant.WHITE_PIECE

        # update the 'to' location with the old piecetype, only if the move is valid
        if self.isLegalMove(piecePos,moveType):
            # print("legal",piecePos)
            self.boardState[toPosRow][toPosCol] = pieceType
            self.boardState[fromPosRow][fromPosCol] = constant.FREE_SPACE
        else:
            # return False -- error value, if the move is not valid, i.e a move has not been made
            # print("not legal",piecePos)
            return False

        # update pos dict
        self.piecePos[pieceType].remove(piecePos)
        self.piecePos[pieceType].append((toPosCol,toPosRow))

        # update piecePos to be the new position for elimination checking
        piecePos = toPosCol,toPosRow
        # check for eliminations at this new move - run three on the same piece to simulate three piece elimination
        # if only a two piece elimination, it should sequentially eliminate the pieces around it
        # if
        while self.checkOnePieceElimination(piecePos,pieceType,oppPieceType) is not None:
            piece = self.checkOnePieceElimination(piecePos,pieceType,oppPieceType)
            # want to eliminate the opposition's piece
            if piece in self.piecePos[oppPieceType]:
                # remove from dict
                self.piecePos[oppPieceType].remove(piece)

                # replace with free space on board
                removePosCol,removePosRow = piece
                self.boardState[removePosRow][removePosCol] = constant.FREE_SPACE

        # check for self eliminations if there is no opponent piece to be eliminated
        piece = self.checkSelfElimination(piecePos,pieceType,oppPieceType);
        # print(piece)
        if piece is not None:
            col,row = piece
            # remove if there a piece is self eliminated
            self.piecePos[pieceType].remove(piece);
            self.boardState[row][col] = constant.FREE_SPACE
        # recalculate all the moves
        self.updateAvailableMoves()

        # check nearby locations if a white/black pieces exist -- then check if these pieces
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
            # moveType is related with each other by a constant of 4
            # one space movements are 4 less than the two space movements

            interPosCol,interPosRow = self.convertMoveTypeToCoord(piecePos,moveType-4)
            # test whether the piece that it is jumping over is a board piece and is not free space
            if self.boardState[interPosRow][interPosCol] in (constant.WHITE_PIECE,constant.BLACK_PIECE):
                # test the place that the piece is moving to
                if self.boardState[newCol][newRow] == constant.FREE_SPACE:
                    return True
                else:
                    # if place that it is moving to is not free, then return false
                    return False
            else:
                # if this space is free then you can't jump, therefore return false
                return False



    def convertMoveTypeToCoord(self,piecePos,moveType):
        # piece pos is in the form of a tuple (col,row)
        # moves types
        # 0 - left 1 space
        # 1 - down 1 space
        # 2 - right 1 space
        # 3 - up 1 spaces
        # 4 - left 2 spaces
        # 5 - down 2 spaces
        # 6 - right 2 spaces
        # 7 - up 2 spaces

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
                # get current pieceType
                pieceType = self.boardState[row][col]

                # update the dictionary based on the pieceType it finds
                if pieceType in (constant.BLACK_PIECE,constant.WHITE_PIECE):
                    self.piecePos[pieceType].append((col,row))
        return

    # update the available moves based on the current positions of pieces on the board
    def updateAvailableMoves(self):
        # update the dict for piece positions
        # get the keys of the dict

        newDict = {constant.BLACK_PIECE: [],constant.WHITE_PIECE: []}

        for key in self.piecePos.keys():
            # iterate through each piece position in each position list in the dict
            for piecePos in self.piecePos[key]:
                # test all movetypes to see if they are legal or not
                for moveType in range(constant.MAX_MOVETYPE):
                    if self.isLegalMove(piecePos,moveType):
                        # append all legal moves to the availableMoves dict
                        # store in a tup (tup1,moveType) where tup1 is the original piece position before the movetype
                        # is applied
                        newDict[key].append((piecePos,moveType))

        self.availableMoves = newDict

    # elimination checker helper functions  -- for updateBoard method
    # checks if a move results in a one piece elimination
    # can use this method multiple times to check whether a multiple pieces are eliminated
    # with one move
    def checkOnePieceElimination(self,piecePos,pieceType,oppPieceType):

        # update piecePos from tuple to posRow and posCol
        posCol, posRow = piecePos

        # add the location of the corners to the location list of the current players piece position list
        # create a deep copy of the positions such that you don't alter the original
        piecePosList = deepcopy(self.piecePos[pieceType]);
        piecePosList.append((0,0))
        piecePosList.append((0,constant.BOARD_SIZE-1))
        piecePosList.append((constant.BOARD_SIZE-1,0))
        piecePosList.append((constant.BOARD_SIZE-1,constant.BOARD_SIZE-1))

        # test all the 4 cases for this type of elimination
        # don't need to test for negative indices and positions outside the boundary of the board because there should
        # be no pieces that are placed in these positions and therefore do not exist in these lists

        # check left
        if (posCol-1,posRow) in self.piecePos[oppPieceType] and (posCol-2,posRow) in piecePosList:
            return posCol-1,posRow
        # check right
        elif (posCol+1,posRow) in self.piecePos[oppPieceType] and (posCol+2,posRow) in piecePosList:
            return posCol+1,posRow
        # check up
        elif (posCol,posRow-1) in self.piecePos[oppPieceType] and (posCol,posRow-2) in piecePosList:
            return posCol,posRow-1
        # check down
        elif (posCol,posRow+1) in self.piecePos[oppPieceType] and (posCol,posRow+2) in piecePosList:
            return posCol, posRow+1
        else:
            # if it does not exist therefore there is no piece to be eliminated
            return None

    # helper method to calculate if a piece is to be self eliminated by its own move
    def checkSelfElimination(self,piecePos,pieceType,oppPieceType):
        # update piecePos from tuple to posRow and posCol
        posCol,posRow = piecePos

        # add the location of the corners to the location list of the opponent piece
        oppPosList = deepcopy(self.piecePos[oppPieceType]);
        # print("oppPosList",oppPosList)
        # print("piecePos",piecePos)
        oppPosList.append((0,0))
        oppPosList.append((0,constant.BOARD_SIZE-1))
        oppPosList.append((constant.BOARD_SIZE-1,0))
        oppPosList.append((constant.BOARD_SIZE-1,constant.BOARD_SIZE-1))

        # now just need to check horizontal and vertical positions to see if they are in the piecePos list
        # horizontal check
        if ((posCol+1,posRow) in oppPosList) and ((posCol-1,posRow) in oppPosList):
            return posCol,posRow
        # vertical piece position check for self elimination
        elif ((posCol,posRow+1) in oppPosList) and ((posCol,posRow-1) in oppPosList):
            return posCol,posRow
        else:
            return None
