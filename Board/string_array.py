from Board import Board
import constant
board = Board()

'''
board.update_board((0,2),constant.BLACK_PIECE)
board.print_board()
#board.set_board(1,1,constant.BLACK_PIECE)
#board.set_board(3,3,constant.INVALID_SPACE)
print()

board.update_board((3,3),constant.BLACK_PIECE)
board.update_board((3,4),constant.WHITE_PIECE)
board.update_board((3,2),constant.WHITE_PIECE)
print(board.piece_pos)
print(board.move_counter)
board.print_board()
board.update_board((0,1),constant.BLACK_PIECE)
board.update_board((0,2),constant.WHITE_PIECE)
board.print_board()
'''
'''
board.phase = constant.MOVING_PHASE
for i in range(200):
    board.update_board(None, constant.BLACK_PIECE)
    board.print_board()
    print()
'''

board.update_board((1, 0),constant.WHITE_PIECE)
board.update_board((2, 0),constant.WHITE_PIECE)
board.update_board((3, 0),constant.WHITE_PIECE)
board.update_board((4, 0),constant.WHITE_PIECE)
board.update_board((5, 0),constant.WHITE_PIECE)
board.update_board((6, 0),constant.WHITE_PIECE)
board.update_board((1,1),constant.WHITE_PIECE)
board.update_board((2,1),constant.WHITE_PIECE)
board.update_board((3,1),constant.WHITE_PIECE)
board.update_board((4,1),constant.WHITE_PIECE)
board.update_board((5,1),constant.WHITE_PIECE)
board.update_board((6,1),constant.WHITE_PIECE)
board.update_board((1,7),constant.BLACK_PIECE)
board.update_board((2,7),constant.BLACK_PIECE)
board.update_board((3,7),constant.BLACK_PIECE)
board.update_board((4,7),constant.BLACK_PIECE)
board.update_board((5,7),constant.BLACK_PIECE)
board.update_board((6,7),constant.BLACK_PIECE)
board.update_board((1,6),constant.BLACK_PIECE)
board.update_board((2,6),constant.BLACK_PIECE)
board.update_board((3,6),constant.BLACK_PIECE)
board.update_board((4,6),constant.BLACK_PIECE)
board.update_board((5,6),constant.BLACK_PIECE)
board.update_board((6,6),constant.BLACK_PIECE)

board.print_board()
print(board.phase)
print(board.piece_pos)
