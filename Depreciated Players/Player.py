from Constants import constant
from DepreciatedBoard.Board import Board
from Agents.Random import Random


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

        self.opponent = self.board.get_opp_piece_type(self.colour)

        # print(self.opponent)
    # set up the board for the first time
    def init_start_moves(self):
        # set the initial board parameters
        # no pieces on the board
        # available moves is the entire starting zone for each player

        if self.colour == constant.WHITE_PIECE:
            # set the white pieces available moves
            for row in range(0, constant.BOARD_SIZE - 2):
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
            eliminated_pieces = self.board.eliminated_pieces[self.opponent]
            # remove the eliminated pieces from the available moves of this player
            for piece in eliminated_pieces:
                if piece in self.available_moves and Player.within_starting_area(piece,self.colour):
                    # self.available_moves.remove(piece)
                    self.available_moves.append(piece)
            # remove the opponent piece from the available moves list
            if action in self.available_moves:
                self.available_moves.remove(action)

            # print(self.available_moves)
        elif self.board.phase == constant.MOVING_PHASE:
            if isinstance(action[0],tuple) is False:
                # print("WHYYYYYYYY")
                return

            move_type = self.board.convert_coord_to_move_type(action[0], action[1])
            # print("MOVETYPE: " + str(move_type))
            # print(action[0])
            self.board.update_board((action[0], move_type), self.opponent)

    def action(self, turns):
        # print("TURNS SO FAR ---------- " + str(turns))
        # print("ACTION CALLED: BOARD REPRESENTATION COUNTER: " + str(self.board.move_counter))
        if turns == 0 and self.board.phase == constant.PLACEMENT_PHASE:
            # then we are first person to move
            self.board.set_player_to_move(self.colour)

        if turns < 24 and self.board.phase == constant.PLACEMENT_PHASE:

            # then we pick the best move to make based on a search algorithm
            search_algorithm = Random(len(self.available_moves))
            next_move = self.available_moves[search_algorithm.choose_move()]

            # making moves during the placement phase
            self.board.update_board(next_move, self.colour)
            eliminated_pieces = self.board.eliminated_pieces[self.colour]
            # remove the move made from the available moves
            self.available_moves.remove(next_move)
            if len(eliminated_pieces) != 0:
                for piece in eliminated_pieces:
                    if piece in self.available_moves:
                        self.available_moves.remove(piece)
            return next_move

        elif self.board.phase == constant.MOVING_PHASE:
            if turns == 0 or turns == 1:
                # if the turns is 0 or 1 and the board is in moving phase then the
                # all players have placed their pieces on the board, we can call update_available_moves to update the
                # available moves available to this player
                # clear the list
                self.available_moves = []
                # update the lists available moves -- now in the form ((col,row),move_type)
                # self.update_available_moves()
                # print(self.available_moves)
            # we are making a move in the moving phase
            #print(self.available_moves)

            self.update_available_moves()
            # if there are no available moves to be made we can return None:
            if len(self.available_moves) == 0:
                return None
            # print("AVAILABLE MOVES: " + str(self.colour) + " " + str(self.available_moves))
            # if there is a move to be made we can return the best move

            # TODO : THIS IS WHERE WE CARRY OUT OUR SEARCH ALGORITHM
            # then we pick the best move to make based on a search algorithm
            search_algorithm = Random(len(self.available_moves))
            next_move = self.available_moves[search_algorithm.choose_move()]

            self.board.update_board(next_move,self.colour)

            new_pos = self.board.convert_move_type_to_coord(next_move[0],next_move[1])
            # print(self.colour + "  " + str(self.board.piece_pos))

            # TODO - need to double check if this update_available_moves is necessary
            self.update_available_moves()

            #print(getsizeof(self.board.piece_pos))
            #print(getsizeof(self.board.board_state))
            #print(getsizeof(self.available_moves))
            return next_move[0], new_pos

    # updates the available moves a piece can make after it has been moved
    # this way we don;t need to calculate all the available moves on the board
    # as pieces that have been eliminated also get rid of those associated available moves
    def update_available_moves(self):
        # clear the available moves
        available_moves = []
        self.available_moves = []

        # recalculate the moves a piece can make based on the available pieces on the board
        # print(self.colour)
        # print("-"*20)
        # self.board.print_board()
        # print("-"*20)
        # print("THIS PLAYERS CURRENT PIECES: " + str(self.colour) + str(self.board.piece_pos[self.colour]))
        for piece in self.board.piece_pos[self.colour]:
            for move_type in range(constant.MAX_MOVETYPE):
                if self.board.is_legal_move(piece, move_type):
                    available_moves.append((piece, move_type))

        self.available_moves = available_moves

    @staticmethod
    def within_starting_area(move,colour):
        if colour == constant.WHITE_PIECE:
            # update the starting rows based off the player colour
            if colour == constant.WHITE_PIECE:
                min_row = 0
                max_row = 6
            elif colour == constant.BLACK_PIECE:
                min_row = 2
                max_row = 8
            col,row = move

            if min_row <= row <= max_row:
                return True
            else:
                return False

