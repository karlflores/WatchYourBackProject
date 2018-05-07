from Board import constant
from Board.Board import Board
from Error_Handling.Errors import *

class Piece(object):
    '''
    When a piece is placed on a board it is alive -- when it is eliminated from the board, it is not
        - this means when undoing a move or several moves you just need to keep track of every piece that
        has been eliminated and return them to their original state

    During placement phase, we add pieces to the board, if we keep track of a pieces neighbours and
    where on the board they can move to, then we can easily generate the boards available moves
    this means that when we are generating moves to make -- this can be done in linear time by just
    iterating through each piece and seeing what locations the piece can move to
    '''

    def __init__(self,pos,colour,board):

        # check if a piece is placed within the defined starting areas of the board
        if colour == constant.WHITE_PIECE:
            min_row = 0
            max_row = constant.BOARD_SIZE-3
        else:
            min_row = 2
            max_row = constant.BOARD_SIZE-1

        col,row = pos

        if col > constant.BOARD_SIZE-1 or col < 0:
            raise IllegalPlacement
        if row > max_row or row < min_row:
            raise IllegalPlacement
        # check if the piece is placed on a corner -- this is illegal
        if pos in board.corner_pos:
            raise IllegalPlacement

        # if we get down here we know that a piece has been placed in a legal position relative to starting positions

        # need to check if the piece is being place on top of another piece before we can set the position
        # of this piece
        # because we are checking if this position is already occupied by another piece, we need to initialise
        # this piece first, before we add it to the corresponding piece dictionary
        if pos in board.white_pieces:
            raise IllegalPlacement

        if pos in board.black_pieces:
            raise IllegalPlacement

        self.pos = pos
        self.colour = colour
        self.board = board

        # a list containing the spaces corresponding to the spaces surrounding this space that
        # we can index into a direction of the board to see if that position is free
        self.neighbours = [True]*8
        self.set_valid_neighbours()
        # when a square is initialised we need to check if

        self.alive = True

    def set_valid_neighbours(self):
        # check all directions, and see if they are occupying a free square
        for direction in range(constant.MAX_MOVETYPE):
            new_pos = self.board.convert_move_type_to_coord(self.pos,direction)

            # check if the new position is within the bounds of the board -- uses the current dimensions of the board
            # this is because when the board is shrinking, the boards dimensions change
            col, row = new_pos
            if col < self.board.get_min_dim() or col > self.board.get_max_dim():
                self.set_neighbour(direction,False)
            elif row < self.board.get_min_dim() or col > self.board.get_max_dim():
                self.set_neighbour(direction, False)

            # check if neighbouring squares are already occupied by another piece
            if new_pos in self.board.white_pieces:
                self.set_neighbour(direction, False)
            elif new_pos in self.board.black_pieces:
                self.set_neighbour(direction, False)
            elif new_pos in self.board.corner_pos:
                self.set_neighbour(direction, False)
            else:
                # if we get down here, we know that the neighbouring square is a free square
                self.set_neighbour(direction, True)

    def set_neighbour(self,direction, bool):
        # if a neighbouring square is a free space -- not
        # necessarily if a neighbouring square is a legal move
        self.neighbours[direction] = bool

    def get_neighbour(self,direction):
        # returns if a square in a specific direction from the perspective of this square
        # if a free square
        return self.neighbours[direction]

    def return_valid_neighbour_directions(self):
        directions = []
        for i,free in enumerate(self.neighbours):
            if free:
                directions.append(i)
        return directions

    def return_valid_neighbour_pos(self):
        positions = []
        for i,free in enumerate(self.neighbours):
            if free:
                positions.append(Board.convert_move_type_to_coord(self.pos, i))
        return positions

    # gets the legal actions that this piece can move into -- these actions are just generated as we see them
    # these are not generated in a greedy was -- TODO: need to implement a way to generate moves/ sort moves
    # TODO - in a greedy way : Optimistic moves??
    def get_legal_actions(self):

        actions = []

        # if we want to test whether an action is legal -- we just need to test if
        # this square is able to move into a free square
        # we need to test if this square is also able to jump into a square

        for direction in range(constant.MAX_MOVETYPE):
            # this represents a one step move
            if self.is_legal_move(direction):
                actions.append((self.pos,direction))

        return actions

    # tests if a piece is able to move in a given direction
    def is_legal_move(self,direction):
        if direction < 4:
            if self.get_neighbour(direction):
                # then this is a free square, hence we can move into it
                return True
            else:
                return False

        else:
            # then this is a jump move, need to see if the adjacent square is occupied
            # NOTE: direction - 4 converts a move of 2 step into a 1 step equivalent
            adj_square = self.get_neighbour(direction - 4)
            if adj_square is False and self.get_neighbour(direction) is True:
                return True
            else:
                return False

    def eliminate(self):
        self.alive = False

    # when we want to revert a piece to being alive -- TODO: Need to establish what this does
    def revert(self):
        self.alive = True

    def is_alive(self):
        return self.alive

    # print a string representation of this piece
    def __str__(self):
        if self.colour == constant.WHITE_PIECE:
            colour = "WHITE"
        else:
            colour = "BLACK"

        # neighbour array
        neighbours = ""
        key = ["RIGHT 1", "DOWN 1", "LEFT 1", "UP 1", "RIGHT 2", "DOWN 2", "LEFT 2", "UP 2"]
        for i in range(constant.MAX_MOVETYPE):
            neighbours+= key[i] + ": " + str(self.neighbours[i]) + "\n"

        return "PIECE AT Position: " + str(self.pos) + "\n" + "Colour: " + colour + "\n" + neighbours + "\n"

        # print a string representation of this piece
    def __repr__(self):
        if self.colour == constant.WHITE_PIECE:
            colour = "WHITE"
        else:
            colour = "BLACK"
        return colour + ": " + str(self.pos) + " -- " + "ALIVE: " + str(self.alive)
