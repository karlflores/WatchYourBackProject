from Agents.Minimax import MinimaxABUndo
from DepreciatedBoard.Board import Board
from Constants import constant

board = Board()
colour = constant.WHITE_PIECE
board.print_board()
agent = MinimaxABUndo(board)

root = agent.create_node(colour, None)

agent.update_minimax_board(None, root, start_node=True)

action = agent.alpha_beta_minimax(3, root)

print(action)