from BoardOOP.Board import Board
from Board import constant
board = Board()
board.print_board()
board.add_piece((3,3),constant.WHITE_PIECE)
board.print_board()
print(board.white_pieces[(3,3)])

board.add_piece((3,4),constant.BLACK_PIECE)
board.print_board()
print(board.black_pieces[(3,4)])
print(board.white_pieces[(3,3)])

board.add_piece((3,5),constant.WHITE_PIECE)
board.print_board()
print(board.white_pieces[(3,5)])
print(board.black_pieces[(3,4)])
print(board.white_pieces[(3,3)])

board.add_piece((4,4),constant.BLACK_PIECE)
board.print_board()
print(board.black_pieces[(4,4)])
print(board.white_pieces[(3,5)])
print(board.black_pieces[(3,4)])
print(board.white_pieces[(3,3)])

board.add_piece((2,5),constant.BLACK_PIECE)
board.add_piece((4,5),constant.BLACK_PIECE)
print(board.check_one_piece_elimination((3,5),constant.WHITE_PIECE))
board.perform_elimination((3,5),constant.WHITE_PIECE)
board.add_piece((10,10),constant.WHITE_PIECE)
print(board.white_pieces)
print(board.black_pieces)