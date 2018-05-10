from Constants import constant
from WatchYourBack.Board import Board
from Agents.NegamaxTranspositionTable import Negamax
from ActionBook.ActionBook import ActionBook
# from Agents.GreedyAlphaBeta import GreedyAlphaBetaMinimax


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
        self.minimax = Negamax(self.board, self.colour)

        self.opponent = self.board.get_opp_piece_type(self.colour)

        # self.search_algorithm = Minimax(self.board,self.available_moves,self.colour)

        # print(self.opponent)
        self.depth_eval = 0
        self.minimax_val = 0
        self.policy_vector = 0

        self.action_book = ActionBook(self.colour)

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

            move_type = self.board.convert_coord_to_direction(action[0], action[1])

            # update the player board representation with the action
            self.board.update_board((action[0], move_type), self.opponent)

    def action(self, turns):
        self.minimax.update_board(self.board)
        # print(self.board.board_state)
        # print(self.board.piece_pos)
        # if action is called first the board representation move counter will be zero
        # this indicates that this player is the first one to move

        # if update is called before action the board representation counter will be 1,
        # this indicates that the player is the second to move

        if turns == 0 and self.board.phase == constant.MOVING_PHASE:
            self.board.move_counter = 0
            self.board.phase = constant.MOVING_PHASE

        # check the action book to see if there is a state
        board_state = self.board.board_state
        if self.board.phase == constant.PLACEMENT_PHASE:
            action = self.action_book.check_state(board_state)

            if action is not None:
                # return the action found and update the board representations
                self.board.update_board(action, self.colour)
                self.minimax.update_board(self.board)
                return action

        # if there is no found state in the action book, therefore we just do a negamax search

        best_move = self.minimax.itr_negamax()

        self.depth_eval = self.minimax.eval_depth
        self.minimax_val = self.minimax.minimax_val

        # do an alpha beta search on this node
        # once we have found the best move we must apply it to the board representation
        if self.board.phase == constant.PLACEMENT_PHASE:
            # print(best_move)
            self.board.update_board(best_move, self.colour)
            self.minimax.update_board(self.board)
            return best_move
        else:
            if best_move is None:
                return None
            # (best_move is None)
            # print(best_move[0],best_move[1])
            new_pos = Board.convert_direction_to_coord(best_move[0], best_move[1])
            self.board.update_board(best_move, self.colour)
            self.minimax.update_board(self.board)
            return best_move[0], new_pos