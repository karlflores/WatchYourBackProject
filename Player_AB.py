from Board import constant
from Board.Board import Board
from Agents.Minimax import MinimaxAB, MinimaxABUndo

class Player:

    def __init__(self, colour):
        if colour == 'white':
            self.colour = constant.WHITE_PIECE
        elif colour == 'black':
            self.colour = constant.BLACK_PIECE

        self.available_moves = []

        # each players internal board representation
        self.board = Board()

        # initialise the available moves
        self.init_start_moves()

        # TODO -- need to see if this works correctly

        self.minimax = MinimaxABUndo(self.board)

        self.opponent = self.board.get_opp_piece_type(self.colour)

        # self.search_algorithm = Minimax(self.board,self.available_moves,self.colour)

        # print(self.opponent)

    # set up the board for the first time
    def init_start_moves(self):
        # set the initial board parameters
        # no pieces on the board
        # available moves is the entire starting zone for each player

        if self.colour == constant.WHITE_PIECE:
            # set the white pieces available moves
            for row in range(0,constant.BOARD_SIZE-2):
                for col in range(constant.BOARD_SIZE):
                    if (row, col) not in self.board.corner_pos:
                        self.available_moves.append((col, row))
        else:
            # set the black piece available moves
            for row in range(2, constant.BOARD_SIZE):
                for col in range(constant.BOARD_SIZE):
                    if (row, col) not in self.board.corner_pos:
                        # append the available move in the list in the form col, row
                        self.available_moves.append((col, row))

    def update(self, action):
        # print("UPDATING THIS ACTION : " + str(action))
        if self.board.move_counter == 0:
            # then the opponent is the first person to move
            self.board.set_player_to_move(self.opponent)

        # update the board based on the action of the opponent
        # get move type
        if self.board.phase == constant.PLACEMENT_PHASE:

            # update board also returns the pieces of the board that will be eliminated
            self.board.update_board(action, self.opponent)
            # self.board.eliminated_pieces[self.opponent]
            self.minimax.update_board(self.board)

            # remove the opponent piece from the available moves list
        elif self.board.phase == constant.MOVING_PHASE:
            if isinstance(action[0],tuple) is False:
                print("asdfasf")
                return

            move_type = self.board.convert_coord_to_move_type(action[0], action[1])
            # print("MOVETYPE: " + str(move_type))
            # print(action[0])
            self.board.update_board((action[0], move_type), self.opponent)

            #self.minimax.update_available_actions(action,self.opponent)

    def action(self, turns):

        if turns == 0 and self.board.phase == constant.PLACEMENT_PHASE:
            self.board.set_player_to_move(self.colour)

        if turns == 24 and self.board.phase == constant.PLACEMENT_PHASE:
            self.board.move_counter = 0
            self.board.phase = constant.MOVING_PHASE

        root = self.minimax.create_node(self.colour, None)
        self.minimax.update_minimax_board(None,root)
        # self.minimax.update_available_actions(None)
        # best_move = self.minimax.alpha_beta_minimax(2,root)
        # best_move = self.minimax.iterative_deepening_alpha_beta(root)
        best_move = self.minimax.alpha_beta_minimax(3,root)

        # do an alpha beta search on this node
        if self.board.phase == constant.PLACEMENT_PHASE:
            # print(best_move)
            self.board.update_board(best_move,self.colour)
            self.minimax.update_board(self.board)
            return best_move
        else:
            # (best_move is None)
            # print(best_move[0],best_move[1])
            new_pos = Board.convert_move_type_to_coord(best_move[0],best_move[1])
            self.board.update_board(best_move,self.colour)
            self.minimax.update_board(self.board)
            return best_move[0], new_pos
