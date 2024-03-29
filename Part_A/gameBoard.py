'''
BOARD GAME CLASS -- INCLUDES ALL THE MECHANICS FOR THE GAME

PARAMETERS:
    boardState
    piecePos
    availableMoves
    counter


METHODS:
    readInitialBoardState()
    updateBoardState(myPiecePos,moveType)
    isLegalMove(myPiecePos,moveType)
    convertMoveTypeToCoords(myPiecePos,moveType)
    printBoard()
    getPiecePos()
    updateAvailableMoves()

    # helper methods
    checkOnePieceEliminations()
    checkSelfEliminations()

'''

from Part_A import constant
from copy import deepcopy


class Board(object):
    # initialise the class
    def __init__(self):
        # define the board state

        # 2D list to hold the representation of the current board state
        self.boardState = []

        # create dictionaries to hold all the available moves and piece positions
        # on the board
        # map the board symbol types to the list for easy access
        self.piecePos = {constant.BLACK_PIECE: [], constant.WHITE_PIECE: []}
        self.availableMoves = {constant.BLACK_PIECE: [], constant.WHITE_PIECE: []}

        # track the position of the corner pieces in the game
        self.cornerPos = [(0, 0), (7, 0), (0, 7), (7, 7)]

        # move counter
        self.moveCounter = 0
        self.phase = 0
        # number of shrinks made so far
        self.numShrink = 0
    # reads in stdin and converts it to boardState, gets the piece positions and available
    # moves
    def readInitialBoardState(self):
        # read 8 lines of std in to fulfill the board
        for i in range(constant.BOARD_SIZE):
            temp = input().strip('\n').split(' ')
            self.boardState.append(temp)

        # update the position of the pieces and its available moves
        self.getPiecePos()
        self.updateAvailableMoves()
        return

    # update the board state based on a move applied to a particular piece
    def updateBoardState(self,myPiecePos,moveType):
        # update the position on the board and check whether a piece/pieces are to be eliminated
        # move the piece -- get the myPieceType and the oppPieceType, update to free space
        fromPosCol,fromPosRow = myPiecePos
        toPosCol,toPosRow = self.convertMoveTypeToCoord(myPiecePos,moveType)
        myPieceType = self.boardState[fromPosRow][fromPosCol]

        # update the 'to' location with the old piecetype, only if the move is valid
        if self.isLegalMove(myPiecePos,moveType):
            self.boardState[toPosRow][toPosCol] = myPieceType
            self.boardState[fromPosRow][fromPosCol] = constant.FREE_SPACE
        else:
            # return False -- error value, if the move is not valid, i.e a move has not been made
            return False

        # update pos dict with new position, remove the old position
        self.piecePos[myPieceType].remove(myPiecePos)
        self.piecePos[myPieceType].append((toPosCol,toPosRow))

        # update piecePos to be the new position for elimination checking
        myPiecePos = toPosCol,toPosRow
        self.performPieceElimination(myPiecePos, myPieceType)
        # recalculate all the moves
        self.updateAvailableMoves()

    def isLegalMove(self,myPiecePos,moveType):
        # get the new position from moveType
        oldCol,oldRow = myPiecePos;
        newCol,newRow = self.convertMoveTypeToCoord(myPiecePos,moveType)

        # get the board dimensions based on the current corner positions (LT, RT, LB, RR)
        colIndexMin = self.cornerPos[0][0]
        colIndexMax = self.cornerPos[1][0]
        rowIndexMin = self.cornerPos[0][1]
        rowIndexMax = self.cornerPos[3][1]
        # check if the piecePos is actually a piece, if not return false
        if self.boardState[oldRow][oldCol] not in (constant.WHITE_PIECE, constant.BLACK_PIECE):
            return False
        # need to test if the newCol, newRow are in the boundaries of the board based on
        # the corner locations
        if newCol < colIndexMin or newCol > colIndexMax:
            return False
        if newRow < rowIndexMin or newRow > rowIndexMax:
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
            # the relationship between one space moveTypes and two space moveTypes is a difference of 4
            # get the one space position based on the moveType entered
            # one space movements are 4 less than the two space movements

            interPosCol,interPosRow = self.convertMoveTypeToCoord(myPiecePos,moveType-4)
            # test whether the piece that it is jumping over is a board piece and is not free space
            if self.boardState[interPosRow][interPosCol] in (constant.WHITE_PIECE, constant.BLACK_PIECE):
                # test the place that the piece is moving to
                if self.boardState[newRow][newCol] == constant.FREE_SPACE:
                    return True
                else:
                    # if place that it is moving to is not free, then return false
                    return False
            else:
                # if this space is free then you can't jump, therefore return false
                return False

    # checks whether placing a piece is legal or not based on the rules of the game
    def isLegalPlace(self,position):
        posCol,posRow = position

        # get the board dimensions based on the current corner positions (LT, RT, LB, RB)
        colIndexMin = self.cornerPos[0][0]
        colIndexMax = self.cornerPos[1][0]
        rowIndexMin = self.cornerPos[0][1]
        rowIndexMax = self.cornerPos[3][1]
        # check if the position is out bounds of the board
        if posCol < colIndexMin or posCol > colIndexMax:
            return False
        if posRow < rowIndexMin or posRow > rowIndexMax:
            return False

        # check if the piece is on free spot on the board
        if self.boardState[posRow][posCol] == constant.FREE_SPACE:
            return True
        else:
            return False

    def convertMoveTypeToCoord(self,myPiecePos,moveType):
        # piece pos is in the form of a tuple (col,row)
        # moves types
        # 0 - right 1 space
        # 1 - down 1 space
        # 2 - left 1 space
        # 3 - up 1 spaces
        # 4 - right 2 spaces
        # 5 - down 2 spaces
        # 6 - left 2 spaces
        # 7 - up 2 spaces

        # convert the tuple to row, col variable
        colPiecePos,rowPiecePos = myPiecePos;

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
                # get current myPieceType
                myPieceType = self.boardState[row][col]

                # update the dictionary based on the myPieceType it finds
                if myPieceType in (constant.BLACK_PIECE, constant.WHITE_PIECE):
                    self.piecePos[myPieceType].append((col,row))
        return

    # update the available moves based on the current positions of pieces on the board
    def updateAvailableMoves(self):
        # update the dict for piece positions
        # get the keys of the dict

        newDict = {constant.BLACK_PIECE: [], constant.WHITE_PIECE: []}

        for key in self.piecePos.keys():
            # iterate through each piece position in each position list in the dict
            for myPiecePos in self.piecePos[key]:
                # test all movetypes to see if they are legal or not
                for moveType in range(constant.MAX_MOVETYPE):
                    if self.isLegalMove(myPiecePos,moveType):
                        # append all legal moves to the availableMoves dict
                        # store in a tup (tup1,moveType) where tup1 is the original piece position before the movetype
                        # is applied
                        newDict[key].append((myPiecePos,moveType))

        self.availableMoves = newDict

        # when an update has been made we increment the move counter of the board
        self.moveCounter = self.moveCounter+1

    # elimination checker helper functions  -- for updateBoard method
    # checks if a move results in a one piece elimination
    # can use this method multiple times to check whether a multiple pieces are eliminated
    # with one move
    def checkOnePieceElimination(self,myPiecePos,myPieceType,oppPieceType):

        # update piecePos from tuple to posRow and posCol
        posCol, posRow = myPiecePos

        # add the location of the corners to the location list of the current players piece position list
        # create a deep copy of the positions such that you don't alter the original
        myPiecePosList = deepcopy(self.piecePos[myPieceType]);
        myPiecePosList.append((0,0))
        myPiecePosList.append((0, constant.BOARD_SIZE - 1))
        myPiecePosList.append((constant.BOARD_SIZE - 1, 0))
        myPiecePosList.append((constant.BOARD_SIZE - 1, constant.BOARD_SIZE - 1))

        # test all the 4 cases for this type of elimination
        # don't need to test for negative indices and positions outside the boundary of the board because there should
        # be no pieces that are placed in these positions and therefore do not exist in these lists

        # check left
        if (posCol-1,posRow) in self.piecePos[oppPieceType] and (posCol-2,posRow) in myPiecePosList:
            return posCol-1,posRow
        # check right
        elif (posCol+1,posRow) in self.piecePos[oppPieceType] and (posCol+2,posRow) in myPiecePosList:
            return posCol+1,posRow
        # check up
        elif (posCol,posRow-1) in self.piecePos[oppPieceType] and (posCol,posRow-2) in myPiecePosList:
            return posCol,posRow-1
        # check down
        elif (posCol,posRow+1) in self.piecePos[oppPieceType] and (posCol,posRow+2) in myPiecePosList:
            return posCol, posRow+1
        else:
            # if it does not exist therefore there is no piece to be eliminated
            return None

    # helper method to calculate if a piece is to be self eliminated by its own move
    def checkSelfElimination(self,myPiecePos,myPieceType,oppPieceType):
        # update piecePos from tuple to posRow and posCol
        posCol,posRow = myPiecePos

        # if the current piece pos is not the expected piece type then return None
        if self.boardState[posRow][posCol] != myPieceType:
            return None

        # add the location of the corners to the location list of the opponent piece
        oppPiecePosList = deepcopy(self.piecePos[oppPieceType]);
        oppPiecePosList.append((0,0))
        oppPiecePosList.append((0, constant.BOARD_SIZE - 1))
        oppPiecePosList.append((constant.BOARD_SIZE - 1, 0))
        oppPiecePosList.append((constant.BOARD_SIZE - 1, constant.BOARD_SIZE - 1))

        # now just need to check horizontal and vertical positions to see if they are in the piecePos list
        # horizontal check
        if ((posCol+1,posRow) in oppPiecePosList) and ((posCol-1,posRow) in oppPiecePosList):
            return posCol,posRow
        # vertical piece position check for self elimination
        elif ((posCol,posRow+1) in oppPiecePosList) and ((posCol,posRow-1) in oppPiecePosList):
            return posCol,posRow
        else:
            return None

    def shrinkBoard(self):
        # we can shrink the board upto 2 times per game -- one at 64 moves in total and one at 128 moves
        pass
        # first we need to remove the edges of the board

        # after we remove the edges we remove the pieces at the corner of the board

    def checkWin(self):
        # check if an opponent has won or drew -- an opponent has won if the other opponent has no
        pass

    @staticmethod
    def returnOppPieceType(myPieceType):
        if myPieceType not in (constant.BLACK_PIECE, constant.WHITE_PIECE):
            return None

        if myPieceType == constant.WHITE_PIECE:
            return constant.BLACK_PIECE
        else:
            return constant.WHITE_PIECE

    def performPieceElimination(self,myPiecePos,myPieceType):

        oppPieceType = self.returnOppPieceType(myPieceType)
        # check for eliminations at this new move - run three on the same piece to simulate three piece elimination
        # if only a two piece elimination, it should sequentially eliminate the pieces around it
        while self.checkOnePieceElimination(myPiecePos, myPieceType, oppPieceType) is not None:
            piece = self.checkOnePieceElimination(myPiecePos, myPieceType, oppPieceType)
            # want to eliminate the opposition's piece
            if piece in self.piecePos[oppPieceType]:
                # remove from dict
                self.piecePos[oppPieceType].remove(piece)

                # replace with free space on board
                removePosCol, removePosRow = piece
                self.boardState[removePosRow][removePosCol] = constant.FREE_SPACE

        # check for self eliminations if there is no opponent piece to be eliminated
        piece = self.checkSelfElimination(myPiecePos, myPieceType, oppPieceType)
        if piece is not None:
            col, row = piece
            # remove if there a piece is self eliminated
            self.piecePos[myPieceType].remove(piece)
            self.boardState[row][col] = constant.FREE_SPACE