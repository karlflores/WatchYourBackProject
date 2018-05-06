class Piece(object):
    '''
    When a piece is placed on a board it is alive -- when it is eliminated from the board, it is not
        - this means when undoing a move or several moves you just need to keep track of every piece that
        has been eliminated and return them to their original state

    During placement phase, we add pieces to the board, if we keep track of a pieces neighbours and
    where on the board they can move to, then we can easily generate the boards available moves
    '''

    def __init__(self,pos,colour):
        self.pos = pos
        self.colour = colour

        # a dictionary containing the neighbours of
        self.neighbours = {}


