from gameBoard import Board

a = Board()
a.readInitialBoardState();
print("test print board")
a.printBoard();
a.getPiecePos();
print("\ntest get position fucntion")
print(a.whitePos,a.blackPos);

# test the movePos cases:
print("\ntest moveType function")
for i in range(8):
    print(i,a.whitePos[0],a.convertMoveTypeToCoord(a.whitePos[0],i))

# test the legalMoves function
print("\ntest moveType function")
for i in range(8):
    poscol,posrow = a.convertMoveTypeToCoord(a.whitePos[0],i);
    print(i,a.whitePos[0],(poscol,posrow),a.isLegalMove(a.whitePos[0],i),a.boardState[posrow][poscol]);