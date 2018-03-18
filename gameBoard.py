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

        #TODO -- need to change this later on, need to change all methods use this dict instead of two seperate lists
        self.piecePos = {constant.BLACK_PIECE: [],constant.WHITE_PIECE: []}
        # list containing the different available moves for both white
        # and black pieces they have available on the board
        self.whiteAvailableMoves = []
        self.blackAvailableMoves = []

        #TODO -- need to change this later on, need to change all methods use this dict instead of two seperate lists
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

        pieceType = self.boardState[fromPosRow][fromPosCol]
        self.boardState[fromPosRow][fromPosCol] = constant.FREE_SPACE

        if pieceType == constant.WHITE_PIECE:
            oppPieceType = constant.BLACK_PIECE
        else:
            oppPieceType = constant.WHITE_PIECE

        # update the 'to' location with the old piecetype, only if the move is valid
        if self.isLegalMove(piecePos,moveType):
            self.boardState[toPosRow][toPosCol] = pieceType
        else:
            # return False -- error value, if the move is not valid, i.e a move has not been made
            return False

        # remove position from the list, and append its new position
        if pieceType == constant.WHITE_PIECE:
            self.whitePos.remove(piecePos)
            self.whitePos.append((toPosCol,toPosRow))
        elif:
            self.blackPos.remove(piecePos)
            self.blackPos.remove((toPosCol,toPosRow))

        # update pos dict
        self.piecePos[pieceType].remove(piecePos)
        self.piecePos[pieceType].append((toPosCol,toPosRow))

        #check for eliminations at this new move - run twice on the same piece to simulate two piece elimination
        # if only one piece elimination, the second time checkElimination runs, it should return None
        for i in range(2):
            if self.checkElimination(piecePos,pieceType,oppPieceType) is not None:
                # if a piece is found to be eliminated remove it from the dict
                for piece in self.checkElimination(piecePos):
                    for key in self.piecePos:
                        if piece in self.piecePos[pieceType]:
                            # remove from dict
                            self.piecePos[pieceType].remove(piece)

                            # replace with free space on board
                            removePosCol,removePosRow = piece
                            self.boardState[removePosRow][removePosCol] = constant.FREE_SPACE

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
                #update the dictionaries of the piece positions
                self.piecePos[self.boardState[row][col]].append((col,row))

                #update the position lists
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

        # update the dict for piece positions
        for key in self.piecePos.keys():
            for piecePos in self.piecePos[key]:
                for moveType in range(constant.MAX_MOVETYPE):
                    if self.isLegalMove(piecePos,moveType):
                        self.availableMoves[key].append(piecePos,self.convertMoveTypeToCoord(piecePos,moveType))


    def checkElimination(self,piecePos,pieceType,oppPieceType):
        # returns the piece to be eliminated from the board, if there is no piece that is going
        # if there is no piece that is eliminated it returns NULL
        # need to check if the current piece is placed in a position where itself is eliminated

        # check through the two piece eliminations first then check through the one piece eliminations then self eliminations
        if self.checkTwoSpaceElmination(piecePos,pieceType,oppPieceType) is not None:
            return self.checkTwoSpaceElmination(piecePos,pieceType,oppPieceType)
        if self.checkOneSpaceElimination(piecePos,pieceType,oppPieceType) is not None:
            return [self.checkOneSpaceElimination(piecePos,pieceType,oppPieceType)]
        elif self.checkSelfElimination(piecePos,pieceType,oppPieceType) is not None:
            return [self.checkSelfElimination(piecePos,pieceType,oppPieceType)]

    # checkElimination helper methods

    def checkOneSpaceElimination(self,piecePos,pieceType,oppPieceType):
        # update piecePos from tuple to posRow and posCol
        posCol, posRow = piecePos

        #create a tuple containing the pieceType and also the corner piece, since the corner piece acts as pieceType
        pieceType_tup =(pieceType,constant.CORNER_PIECE)
        pieceType = pieceType_tup

        # check if two spaces from the current position of the board are in the coordinate space of the board
        if posCol -2 >=0 and posCol +2 <= constant.BOARD_SIZE-1 and posRow -2 >= 0 and posRow +2 <= constant.BOARD_SIZE-1:
        # can check every configuration
            if self.boardState[posRow+2][posCol] in pieceType and self.boardState[posRow+1][posCol] == oppPieceType:
                return posCol,posRow+1
            elif self.boardState[posRow-2][posCol] in pieceType and self.boardState[posRow-1][posCol] == oppPieceType:
                return posCol,posRow-1
            elif self.boardState[posRow][posCol-2] in pieceType and self.boardState[posRow][posCol-1] == oppPieceType:
                return posCol-2,posRow
            elif self.boardState[posRow][posCol+2] in pieceType and self.boardState[posRow][posCol+1] == oppPieceType:
                return posCol+1,posRow
            else:
                return None

        elif posRow == 1:
            # if the two piece away position is outside the board coordinates can only check
            if posCol == 1:
                if self.boardState[posRow][posCol+2] in pieceType and self.boardState[posRow][posCol+1] == oppPieceType:
                    return posCol+1,posRow
                elif self.boardState[posRow+2][posCol] in pieceType and self.boardState[posRow+1][posCol] == oppPieceType:
                    return posCol,posRow+1
                else:
                    return None
            if posCol == constant.BOARD_SIZE -2:
                if self.boardState[posRow][posCol-2] in pieceType and self.boardState[posRow][posCol-1] == oppPieceType:
                    return posCol-1,posRow
                elif self.boardState[posRow+2][posCol] in pieceType and self.boardState[posRow+1][posCol] == oppPieceType:
                    return posCol,posRow+1
                else:
                    return None
            # if the piece is placed in the top row and not at the corners -- can check both vertical and horizontal
            else:
                # can check every configuration except if there are two pieces above the current piece
                if self.boardState[posRow+2][posCol] in pieceType and self.boardState[posRow+1][posCol] == oppPieceType:
                    return posCol,posRow+1
                elif self.boardState[posRow][posCol-2] in pieceType and self.boardState[posRow][posCol-1] == oppPieceType:
                    return posCol-1,posRow
                elif self.boardState[posRow][posCol+2] in pieceType and self.boardState[posRow][posCol+1] == oppPieceType:
                    return posCol+1,posRow
                else:
                    return None


        elif posRow == constant.BOARD_SIZE -2:
            if posCol == 1:
                if self.boardState[posRow][posCol+2] in pieceType and self.boardState[posRow][posCol+1] == oppPieceType:
                    return posCol+1,posRow
                elif self.boardState[posRow-2][posCol] in pieceType and self.boardState[posRow-1][posCol] == oppPieceType:
                    return posCol,posRow-1
                else:
                    return None
            if posCol == constant.BOARD_SIZE -2:
                if self.boardState[posRow][posCol-2] in pieceType and self.boardState[posRow][posCol-1] == oppPieceType:
                    return posCol-1,posRow
                elif self.boardState[posRow-2][posCol] in pieceType and self.boardState[posRow-1][posCol] == oppPieceType:
                    return posCol,posRow-1
                else:
                    return None
            # if the piece is placed in the top row and not at the corners -- can check both vertical and horizontal
            else:
                # can check every configuration except if there are two pieces above the current piece
                if self.boardState[posRow-2][posCol] in pieceType and self.boardState[posRow-1][posCol] == oppPieceType:
                    return posCol,posRow-1
                elif self.boardState[posRow][posCol-2] in pieceType and self.boardState[posRow][posCol-1] == oppPieceType:
                    return posCol-1,posRow
                elif self.boardState[posRow][posCol+2] in pieceType and self.boardState[posRow][posCol+1] == oppPieceType:
                    return posCol+1,posRow
                else:
                    return None

        elif posCol == 1:
            # if the two piece away position is outside the board coordinates can only check
            # can check every configuration except if there are two pieces above the current piece
            if self.boardState[posRow + 2][posCol] in pieceType and self.boardState[posRow + 1][posCol] == oppPieceType:
                return posCol,posRow+1
            elif self.boardState[posRow - 2][posCol] in pieceType and self.boardState[posRow][posCol - 1] == oppPieceType:
                return posCol-1,posRow
            elif self.boardState[posRow][posCol + 2] in pieceType and self.boardState[posRow][posCol + 1] == oppPieceType:
                return posCol+1,posRow
            else:
                return None
        elif posCol == constant.BOARD_SIZE -2:
            if self.boardState[posRow + 2][posCol] in pieceType and self.boardState[posRow + 1][posCol] == oppPieceType:
                return posCol,posRow+1
            elif self.boardState[posRow - 2][posCol] in pieceType and self.boardState[posRow - 1][posCol] == oppPieceType:
                return posCol,posRow-1
            elif self.boardState[posRow][posCol - 2] in pieceType and self.boardState[posRow][posCol - 1] == oppPieceType:
                return posCol-1,posRow
            else:
                return None
        elif posRow == 0:
            # a piece can't be placed in the corner positions therefore do not need to check these positions -- therefore return none
            if posCol == 0 or posCol == constant.BOARD_SIZE-1:
                return None
            elif posCol == 1:
                # don't need to check to the right because if a opposition piece is here, this piece is eliminated
                # just check down
                if self.boardState[posRow+2][posCol] in pieceType and self.boardState[posRow+1][posCol] == oppPieceType:
                    return posCol,posRow+1
                else:
                    return None

            elif posCol == constant.BOARD_SIZE-1:
                if self.boardState[posRow][posCol+2] in pieceType and self.boardState[posRow][posCol+1] == oppPieceType:
                    return posCol+1, posRow
                else:
                    return None
            else:
                # can check down, left and right for eliminated pieces
                if self.boardState[posRow+2][posCol] in pieceType and self.boardState[posRow+1][posCol] == oppPieceType:
                    return posCol,posRow+1
                elif self.boardState[posRow][posCol-2] in pieceType and self.boardState[posRow][posCol -1] == oppPieceType:
                    return  posCol-1,posRow
                elif self.boardState[posRow][posCol+2] in pieceType and self.boardState[posRow][posCol+1] == oppPieceType:
                    return posCol+1,posRow
                else:
                    return None

                # if the piece is placed in the top row and not at the corners -- can check both vertical and horizontal
        elif posRow == constant.BOARD_SIZE -1:
         # a piece can't be placed in the corner positions therefore do not need to check these positions -- therefore return none
            if posCol == 0 or posCol == constant.BOARD_SIZE-1:
                return None
            # check if a piece is placed next to an opponent piece, but the next piece to that is the current player's piece
            elif posCol == 1:
                if self.boardState[posRow][posCol-2] in pieceType and self.boardState[posRow][posCol-1] == oppPieceType:
                    return posCol-1,posRow
                else:
                    return None
            elif posCol == constant.BOARD_SIZE-1:
                if self.boardState[posRow - 2][posCol] in pieceType and self.boardState[posRow - 1][posCol] == oppPieceType:
                    return posCol, posRow - 1
                else:
                    return None
            else:
                # can check up, left and right for eliminated pieces
                if self.boardState[posRow-2][posCol] in pieceType and self.boardState[posRow-1][posCol] == oppPieceType:
                    return posCol,posRow-1
                elif self.boardState[posRow][posCol-2] in pieceType and self.boardState[posRow][posCol -1] == oppPieceType:
                    return posCol-1,posRow
                elif self.boardState[posRow][posCol+2] in pieceType and self.boardState[posRow][posCol+1] == oppPieceType:
                    return posCol+1,posRow
                else:
                    return None
        elif posCol == 0:
            # no need to check corner pieces and next to corner piece since it has been handled by earlier cases
            # just need to check right up and down
            if self.boardState[posRow - 2][posCol] in pieceType and self.boardState[posRow - 1][posCol] == oppPieceType:
                return posCol,posRow-1
            elif self.boardState[posRow + 2][posCol] in pieceType and self.boardState[posRow + 1][posCol] == oppPieceType:
                return posCol,posRow+1
            elif self.boardState[posRow][posCol+2] in pieceType and self.boardState[posRow][posCol+1] == oppPieceType:
                return posCol+1,posRow
            else:
                return None
        elif posCol == constant.BOARD_SIZE -1:
            # no need to check corner pieces and next to corner piece since it has been handled by earlier cases
            # just need to check left up and down
            if self.boardState[posRow - 2][posCol] in pieceType and self.boardState[posRow - 1][posCol] == oppPieceType:
                return posCol,posRow-1
            elif self.boardState[posRow + 2][posCol] in pieceType and self.boardState[posRow + 1][posCol] == oppPieceType:
                return posCol,posRow+1
            elif self.boardState[posRow][posCol - 2] in pieceType and self.boardState[posRow][posCol - 1] == oppPieceType:
                return posCol-1,posRow;
            else:
                return None

    def checkTwoSpaceElmination(self,piecePos,pieceType,oppPieceType):
        # convert piecePos to row and col
        posCol,posRow = piecePos

        if piecePos in ((0,0),(0,constant.BOARD_SIZE-1),(constant.BOARD_SIZE-1,0),(constant.BOARD_SIZE-1,constant.BOARD_SIZE-1)):
            return None
        # TODO - NEED TO COMPLETE THIS FUNCTION -- work out the boundaries of this checker
        # FOR TWO PIECE ELIMINATION JUST NEED TO RUN ONE PIECE ELIMINATION TWICE< BUT NEED TO REMOVE THE FIRST INSTANCE SUCH THAT IT DOES NOT RETURN THE SAME THING
    def checkSelfElimination(self,piecePos,pieceType,oppPieceType):
        #update piecePos from tuple to posRow and posCol
        posCol,posRow = piecePos

        #update the opponent piece to be either a tuple of corner piece or the actual opponent piece
        oppPieceType_tup = (oppPieceType,constant.CORNER_PIECE)
        oppPieceType = oppPieceType_tup

        # FORM: X
        #       O
        #       X
        # if the position of the pieces next to the current piece is between the bounds of the board:
        if posCol -1 >=0 and posCol +1 <= constant.BOARD_SIZE-1 and posRow -1 >= 0 and posRow +1 <= constant.BOARD_SIZE-1:
            if self.boardState[posRow - 1][posCol] in oppPieceType and self.boardState[posRow + 1][posCol] in oppPieceType:
                return piecePos

        # FORM: XOX
            elif self.boardState[posRow][posCol-1] in oppPieceType and self.boardState[posRow][posCol+1] in oppPieceType:
                return piecePos

        elif posCol - 1 < 0 or posCol +1 > constant.BOARD_SIZE-1:
            # can only check the vertical format
            if self.boardState[posRow -1][posCol] in oppPieceType and self.boardState[posRow +1][posCol] in oppPieceType:
                return piecePos

        elif posRow -1 < 0 or posRow +1 > constant.BOARD_SIZE -1:
            # can only check the horizontal format
            if self.boardState[posRow][posCol-1] in oppPieceType and self.boardState[posRow][posCol+1] in oppPieceType:
                return piecePos

        #if the piece is not placed in such a way that it is not eliminated therefore return NOne
        else:
            return None



