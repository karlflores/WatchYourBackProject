from Board import constant
from Board.Board import Board

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
        self.pos = pos
        self.colour = colour
        self.board = board

        # a list containing the spaces corresponding to the spaces surrounding this space that
        # we can index into a direction of the board to see if that position is free
        self.neighbours = [True]*8

        self.is_alive = True

    def set_neighboour(self,direction, bool):
        self.neighbours[direction] = bool

    def get_neighbour(self,direction):
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

