from Constants import constant
from WatchYourBack.Board import Board
from Agents.NegascoutTranspositionTable import Negascout
'''
A PLAYER THAT USES THE NEGASCOUT ALGORITHM TO FIND ITS NEXT MOVE TO MAKE 
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

        self.minimax = Negascout(self.board, self.colour)

        self.opponent = self.board.get_opp_piece_type(self.colour)

        self.depth_eval = 0
        self.minimax_val = 0
        self.policy_vector = 0

    def update(self, action):
        # update the board based on the action of the opponent
        if self.board.phase == constant.PLACEMENT_PHASE:
            # update board also returns the pieces of the board that will be eliminated
            self.board.update_board(action, self.opponent)
            # self.board.eliminated_pieces[self.opponent]
            self.minimax.update_board(self.board)

        elif self.board.phase == constant.MOVING_PHASE:
            if isinstance(action[0], tuple) is False:
                print("ERROR: action is not a tuple")
                return

            direction = self.board.convert_coord_to_direction(action[0], action[1])

            # update the player board representation with the action
            self.board.update_board((action[0], direction), self.opponent)
            self.minimax.update_board(self.board)

    def action(self, turns):
        self.minimax.update_board(self.board)

        if turns == 0 and self.board.phase == constant.MOVING_PHASE:
            self.board.move_counter = 0
            self.board.phase = constant.MOVING_PHASE

        # find the best move
        best_move = self.minimax.itr_negascout()
        # if the best move we have found so far is a Forfeit -- return this
        if best_move is None:
            self.board.update_board(best_move, self.colour)
            self.minimax.update_board(self.board)
            return None

        self.depth_eval = self.minimax.eval_depth
        self.minimax_val = self.minimax.minimax_val

        # once we have found the best move we must apply it to the board representation
        if self.board.phase == constant.PLACEMENT_PHASE:
            # print(best_move)
            self.board.update_board(best_move, self.colour)
            self.minimax.update_board(self.board)
            return best_move
        else:
            # (best_move is None)
            # print(best_move[0],best_move[1])
            new_pos = Board.convert_direction_to_coord(best_move[0], best_move[1])
            self.board.update_board(best_move, self.colour)
            self.minimax.update_board(self.board)
            return best_move[0], new_pos