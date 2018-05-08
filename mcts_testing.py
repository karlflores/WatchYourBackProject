from Agents.Negamax import Negamax
from Board.Board import Board
from Constants import constant

# create a new board

board = Board()

colour = constant.WHITE_PIECE

#agent = MonteCarloTreeSearch(board,colour)

agent2 = Negamax(board,colour)
actions = agent2.board.update_actions(agent2.board,agent2.player)
print(actions)
print(agent2.board.sort_actions(actions,agent2.player))
#node = agent.create_node(board,colour,None,None)
#agent.simulate(node)
# agent2.itr_negamax()
'''
while(board.is_terminal() is False):
    agent = MonteCarloTreeSearch(board, colour)
    move = agent.MCTS()
    print(move)
    board.update_board(move,colour)
    board.print_board()
    colour = Board.get_opp_piece_type(colour)
'''
