from DepreciatedBoard.Board import Board
from Constants import constant
from Agents.Minimax import Minimax

# create a new board game
board_game = Board()

board_game.print_board()
print()
print()
# create the starting node -- this node is black
node = Minimax.create_node(board_game, constant.BLACK_PIECE, None)
node.board.print_board()
print(node.available_moves)
print(node.colour)
print()

# to create a child node we apply one of the move from black to the next node

child = Minimax.create_node(node.board,node.colour,(3,2))
child.board.print_board()
print(child.available_moves)
print(child.board.move_counter)
print(child.board.piece_pos)
print(child.board.eliminated_pieces)

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),(3,3))
child.board.print_board()
print(child.available_moves)
print(child.board.move_counter)
print(child.board.piece_pos)
print(child.board.eliminated_pieces)

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),(6,2))
child.board.print_board()
print(child.available_moves)
print(child.board.move_counter)
print(child.board.piece_pos)
print(child.board.eliminated_pieces)

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),(7,2))
child.board.print_board()
print(child.available_moves)
print(child.board.move_counter)
print(child.board.piece_pos)
print(child.board.eliminated_pieces)

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),(3,5))
child.board.print_board()
print(child.available_moves)
print(child.board.move_counter)
print(child.board.piece_pos)
print(child.board.eliminated_pieces)

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),(5,2))
child.board.print_board()
print(child.available_moves)
print("MOVE COUNTER ",end='')
print(child.board.move_counter)
print(child.board.piece_pos)
print()
print("eliminated pieces")
print(child.board.eliminated_pieces)

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),(3,2))
child.board.print_board()
print(child.available_moves)
print("MOVE COUNTER ",end='')
print(child.board.move_counter)
print(child.board.piece_pos)
print()
print("eliminated pieces")
print(child.board.eliminated_pieces)
print()

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),(4,3))
child.board.print_board()
print(child.available_moves)
print("MOVE COUNTER ",end='')
print(child.board.move_counter)
print(child.board.piece_pos)
print()
print("eliminated pieces")
print(child.board.eliminated_pieces)
print()

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),(6,3))
child.board.print_board()
print(child.available_moves)
print("MOVE COUNTER ",end='')
print(child.board.move_counter)
print(child.board.piece_pos)
print()
print("eliminated pieces")
print(child.board.eliminated_pieces)
print()

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),(1,3))
child.board.print_board()
print(child.available_moves)
print("MOVE COUNTER ",end='')
print(child.board.move_counter)
print(child.board.piece_pos)
print()
print("eliminated pieces")
print(child.board.eliminated_pieces)
print()

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),(2,2))
child.board.print_board()
print(child.available_moves)
print("MOVE COUNTER ",end='')
print(child.board.move_counter)
print(child.board.piece_pos)
print()
print("eliminated pieces")
print(child.board.eliminated_pieces)
print()

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),(7,6))
child.board.print_board()
print(child.available_moves)
print("MOVE COUNTER ",end='')
print(child.board.move_counter)
print(child.board.piece_pos)
print()
print("eliminated pieces")
print(child.board.eliminated_pieces)
print()

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),(0,1))
child.board.print_board()
print(child.available_moves)
print("MOVE COUNTER ",end='')
print(child.board.move_counter)
print(child.board.piece_pos)
print()
print("eliminated pieces")
print(child.board.eliminated_pieces)
print()

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),(0,6))
child.board.print_board()
print(child.available_moves)
print("MOVE COUNTER ",end='')
print(child.board.move_counter)
print(child.board.piece_pos)
print()
print("eliminated pieces")
print(child.board.eliminated_pieces)
print()

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),(5,5))
child.board.print_board()
print(child.available_moves)
print("MOVE COUNTER ",end='')
print(child.board.move_counter)
print(child.board.piece_pos)
print()
print("eliminated pieces")
print(child.board.eliminated_pieces)
print()

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),(2,5))
child.board.print_board()
print(child.available_moves)
print("MOVE COUNTER ",end='')
print(child.board.move_counter)
print(child.board.piece_pos)
print()
print("eliminated pieces")
print(child.board.eliminated_pieces)
print()

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),(5,3))
child.board.print_board()
print(child.available_moves)
print("MOVE COUNTER ",end='')
print(child.board.move_counter)
print(child.board.piece_pos)
print()
print("eliminated pieces")
print(child.board.eliminated_pieces)
print()

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),(5,4))
child.board.print_board()
print(child.available_moves)
print("MOVE COUNTER ",end='')
print(child.board.move_counter)
print(child.board.piece_pos)
print()
print("eliminated pieces")
print(child.board.eliminated_pieces)
print()

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),(2,3))
child.board.print_board()
print(child.available_moves)
print("MOVE COUNTER ",end='')
print(child.board.move_counter)
print(child.board.piece_pos)
print()
print("eliminated pieces")
print(child.board.eliminated_pieces)
print()

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),(3,3))
child.board.print_board()
print(child.available_moves)
print("MOVE COUNTER ",end='')
print(child.board.move_counter)
print(child.board.piece_pos)
print()
print("eliminated pieces")
print(child.board.eliminated_pieces)
print()
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),(4,4))
child.board.print_board()
print(child.available_moves)
print("MOVE COUNTER ",end='')
print(child.board.move_counter)
print(child.board.piece_pos)
print()
print("eliminated pieces")
print(child.board.eliminated_pieces)
print()
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),(5,6))
child.board.print_board()
print(child.available_moves)
print("MOVE COUNTER ",end='')
print(child.board.move_counter)
print(child.board.piece_pos)
print()
print("eliminated pieces")
print(child.board.eliminated_pieces)
print()
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),(7,3))
child.board.print_board()
print(child.available_moves)
print("MOVE COUNTER ",end='')
print(child.board.move_counter)
print(child.board.piece_pos)
print()
print("eliminated pieces")
print(child.board.eliminated_pieces)
print()
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),(4,5))
child.board.print_board()
print(child.available_moves)
print("MOVE COUNTER ",end='')
print(child.board.move_counter)
print(child.board.piece_pos)
print()
print("eliminated pieces")
print(child.board.eliminated_pieces)
print()

print("UNDO MOVE")
child.board.undo_move()
child.board.print_board()
print(child.available_moves)
print("MOVE COUNTER ",end='')
print(child.board.move_counter)
print(child.board.piece_pos)
print()
print("eliminated pieces")
print(child.board.eliminated_pieces)
print()

'''
print("UNDO MOVE")
child.board.undo_move()
child.board.print_board()
print(child.available_moves)
print(child.board.move_counter)
print(child.board.piece_pos)
print(child.board.eliminated_pieces)
'''


