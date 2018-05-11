from Constants import constant
from DepreciatedBoard.Board import Board
from Agents.MCTS import MonteCarloTreeSearch

'''
A PLAYER WHICH IMPLEMENTS MCTS TO INFORM ITS NEXT MOVE -- THIS DOES NOT WORK AS WELL AS WE LIKED 

EFFECTIVELY IT JUST CHOOSES A RANDOM MOVE TO MAKE AS IT DOES NOT HAVE ENOUGH TIME TO EVALUATE AND CREATE 
ENOUGH NODES FOR THE SEARCH TREE

FURTHERMORE DUE TO MEMORY LIMITATIONS THIS MIGHT NOT BE FEASIBLE AS THE SEACH TREE WOULD EASILY OUTGROW THE 
ALLOCATED MEMORY AS WE ARE DEEP-sCOPYING THE BOARD EACH TIME WE MAKE A NEW NODE
'''

class Player:

    def __init__(self, colour):
        if colour == 'white':
            self.colour = constant.WHITE_PIECE
        elif colour == 'black':
            self.colour = constant.BLACK_PIECE

        self.available_moves = []

        # each players internal board representation
        self.board = Board()

        # TODO -- need to see if this works correctly

        self.strategy = MonteCarloTreeSearch(self.board,self.colour)

        self.opponent = self.board.get_opp_piece_type(self.colour)

    def update(self, action):
        # update the board based on the action of the opponent
        if self.board.phase == constant.PLACEMENT_PHASE:
            # update board also returns the pieces of the board that will be eliminated
            self.board.update_board(action, self.opponent)
            # self.board.eliminated_pieces[self.opponent]

        elif self.board.phase == constant.MOVING_PHASE:
            if isinstance(action[0], tuple) is False:
                print("ERROR: action is not a tuple")
                return

            move_type = self.board.convert_coord_to_move_type(action[0], action[1])

            # update the player board representation with the action
            self.board.update_board((action[0], move_type), self.opponent)

    def action(self, turns):
        self.strategy.num_nodes = 0
        self.strategy.update_board(self.board)

        if turns == 0 and self.board.phase == constant.MOVING_PHASE:
            self.board.move_counter = 0
            self.board.phase = constant.MOVING_PHASE

        best_move = self.strategy.MCTS()
        # print("NUM NODE IN THIS TREE: " + str(self.strategy.num_nodes))

        # once we have found the best move we must apply it to the board representation
        if self.board.phase == constant.PLACEMENT_PHASE:
            self.board.update_board(best_move, self.colour)
            return best_move
        else:

            new_pos = Board.convert_move_type_to_coord(best_move[0], best_move[1])
            self.board.update_board(best_move, self.colour)
            return best_move[0], new_pos