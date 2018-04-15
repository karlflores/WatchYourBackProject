from Board import constant
from Board.Board import Board


class Player(object):
    def __init__(self, colour):
        if colour == 'white':
            self.colour = constant.WHITE_PIECE
        else:
            self.colour = constant.BLACK_PIECE

        self.available_moves = []

        # each players internal board representation
        self.board = Board()

        # initialise the available moves
        self.init_start_moves()

        self.opponent = self.board.get_opp_piece_type(colour)

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

    def update(self, turns):
        pass

    def action(self, action):
        pass

    # updates the available moves a piece can make after it has been moved
    # this way we don;t need to calculate all the available moves on the board
    # as pieces that have been eliminated also get rid of those associated available moves
    def update_available_moves(self):
        # calculate the moves a piece can make
        for piece in self.board.piece_pos[self.colour]:
            for move_type in range(constant.MAX_MOVETYPE):
                if self.board.is_legal_move(piece,move_type):
                    self.available_moves.append((piece,move_type))
