from Agents.MCTS import MonteCarloTreeSearch
from Board.Board import Board
from Board import constant
# create a new board

board = Board()

colour = constant.WHITE_PIECE

while(board.is_terminal() is False):
    agent = MonteCarloTreeSearch(board, colour)
    move = agent.MCTS()
    print(move)
    board.update_board(move,colour)
    board.print_board()
    colour = Board.get_opp_piece_type(colour)

