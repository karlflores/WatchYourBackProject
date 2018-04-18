from Board.Board import Board
from Board.Board import constant
from Evaluation.Policies import Evaluation
from Agents.Minimax import Minimax
from Agents.Minimax_Node import Node

# create a new board game
board_game = Board()

board_game.print_board()

# create the starting node -- this node is black
node = Minimax.create_node(board_game,constant.BLACK_PIECE,None)
node.board.print_board()
print(node.available_moves)
print(node.colour)
print()

# to create a child node we apply one of the move from black to the next node
child = Minimax.create_node(node.board,Board.get_opp_piece_type(node.colour),node.available_moves[0])
child.board.print_board()
print(len(child.available_moves))
print(child.colour)
print()

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(len(child.available_moves))
print(child.colour)
print(child.board.piece_pos)



child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(len(child.available_moves))
print(child.board.piece_pos)

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(len(child.available_moves))
print(child.colour)
print(child.board.move_counter)

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(len(child.available_moves))
print(child.colour)
print(child.board.move_counter)

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(len(child.available_moves))
print(child.colour)
print(child.board.move_counter)

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(len(child.available_moves))
print(child.colour)
print(child.board.move_counter)

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(len(child.available_moves))
print(child.colour)
print(child.board.move_counter)

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(len(child.available_moves))
print(child.colour)
print(child.board.move_counter)

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)
print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)
print(child.board.phase)
print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)
print(str(child.board.phase)+ "THIS")
print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)


print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)


print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)


print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)


print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)
print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)
print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)
print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)

print()
print(child.available_moves[1])
child = Minimax.create_node(child.board,Board.get_opp_piece_type(child.colour),child.available_moves[1])
child.board.print_board()
print(child.available_moves)
print(child.colour)
print(child.board.move_counter)





