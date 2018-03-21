from gameBoard import Board
import constant
from Massacre import Massacre
from Node import Node

a = Board()
a.readInitialBoardState();
print("test print board")
a.printBoard();
# a.getPiecePos();

print("\ntest get position fucntion")


# test the movePos cases:
print("\ntest moveType function")
for i in range(8):
    print(i,a.piecePos[constant.WHITE_PIECE][0],a.convertMoveTypeToCoord(a.piecePos[constant.WHITE_PIECE][0],i))

# test the legalMoves function
print("\ntest legalType function")
counter = 0

for pos in a.piecePos[constant.WHITE_PIECE]:
    for i in range(8):

        poscol,posrow = a.convertMoveTypeToCoord(pos,i);
        print(i,pos,(poscol,posrow),a.isLegalMove(pos,i));
        if a.isLegalMove(pos,i):
            counter += 1
    print("")
print(counter)

counter = 0
for pos in a.piecePos[constant.BLACK_PIECE]:
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
for key in a.availableMoves.keys():
    print(key,len(a.availableMoves[key]))
'''

THIS IS THE TEST ELIMINATION CASE FOR THE TESTBOARD.TXT
a.updateBoardState((5,5),1)
print(a.piecePos)
a.printBoard()
a.updateBoardState((5,3),6)
a.printBoard()
a.updateBoardState((5,2),1)
a.printBoard()
a.updateBoardState((3,3),1)
a.printBoard()
a.updateBoardState((3,4),1)
a.printBoard()
a.updateBoardState((3,5),1)
a.printBoard()
a.updateBoardState((5,3),1)
a.printBoard()
a.updateBoardState((5,4),1)
a.printBoard()
a.updateBoardState((5,5),1)
a.printBoard()
a.updateBoardState((6,6),6)
print(a.availableMoves)
print(a.piecePos)
a.printBoard()
'''

# TEST CASE two piece elimination -- testBoard5.txt
a.printBoard()
print()

# a.updateBoardState((5,2),7)
#a.printBoard()

root = Node(a, None)
massacre = Massacre(root)
solution = massacre.BFS(root)

node = solution
solution.board.printBoard()


while(node is not None and node.moveApplied is not None):
    move = node.moveApplied
    coordinates = node.board.convertMoveTypeToCoord(move[0], move[1])
    print(str(move[0]) + " -> " + str(coordinates))
    node = node.parent
