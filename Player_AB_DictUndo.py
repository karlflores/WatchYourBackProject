from Board import constant
from Board.Board import Board
from Agents.Minimax import MinimaxAB, MinimaxABUndo, MinimaxUndo


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

        self.minimax = MinimaxABUndo(self.board)

        self.opponent = self.board.get_opp_piece_type(self.colour)

        # self.search_algorithm = Minimax(self.board,self.available_moves,self.colour)

        # print(self.opponent)

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

            move_type = self.board.convert_coord_to_move_type(action[0], action[1])

            # update the player board representation with the action
            self.board.update_board((action[0], move_type), self.opponent)
            self.minimax.update_board(self.board)

    def action(self, turns):
        self.minimax.update_board(self.board)
        # if action is called first the board representation move counter will be zero
        # this indicates that this player is the first one to move

        # if update is called before action the board representation counter will be 1,
        # this indicates that the player is the second to move

        if turns == 0 and self.board.phase == constant.MOVING_PHASE:
            self.board.move_counter = 0
            self.board.phase = constant.MOVING_PHASE

        # create the node to search on
        root = self.minimax.create_node(self.colour, None)
        # update the board representation and the available moves
        self.minimax.update_minimax_board(None, root, start_node=True)
        # print(self.minimax.available_actions)
        best_move = self.minimax.alpha_beta_minimax(2, root)

        # do an alpha beta search on this node
        # once we have found the best move we must apply it to the board representation
        if self.board.phase == constant.PLACEMENT_PHASE:
            # print(best_move)
            self.board.update_board(best_move, self.colour)
            self.minimax.update_board(self.board)
            return best_move
        else:
            # (best_move is None)
            # print(best_move[0],best_move[1])
            new_pos = Board.convert_move_type_to_coord(best_move[0], best_move[1])
            self.board.update_board(best_move, self.colour)
            self.minimax.update_board(self.board)
            return best_move[0], new_pos