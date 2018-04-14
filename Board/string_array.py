from Board import Board
import constant
board = Board()

board.print_board()
board.set_board(1,1,constant.BLACK_PIECE)
board.set_board(3,3,constant.INVALID_SPACE)
print()
board.print_board()