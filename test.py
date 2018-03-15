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
print("\ntest legalType function")
counter = 0

for pos in a.whitePos:
    for i in range(8):

        poscol,posrow = a.convertMoveTypeToCoord(pos,i);
        print(i,pos,(poscol,posrow),a.isLegalMove(pos,i));
        if a.isLegalMove(pos,i):
            counter += 1
    print("")
print(counter)
counter = 0
for pos in a.blackPos:
    for i in range(8):

        poscol,posrow = a.convertMoveTypeToCoord(pos,i);
        # print(i,pos,(poscol,posrow),a.isLegalMove(pos,i));
        if a.isLegalMove(pos,i):
            counter += 1
    # print("")
print(counter)

# test the available moves and the length of each -- this is the functionality of the MOVES function
print("")
print("test availableMoves and MOVES functionality")
a.updateAvailableMoves()
print("WHITE", a.whiteAvailableMoves,"\nLEN: ",len(a.whiteAvailableMoves))
print("BLACK", a.blackAvailableMoves,"\nLEN: ",len(a.blackAvailableMoves))
