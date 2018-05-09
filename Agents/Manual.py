from BoardOOP.Board import Board
from Constants import constant
from copy import deepcopy
class Manual(object):
    def __init__(self,player):
        self.board = Board()
        self.player = player

    def return_actions(self,player, piece_pos):
        if player == constant.WHITE_PIECE:
            my_pieces = self.board.white_pieces
        else:
            my_pieces = self.board.black_pieces

        if piece_pos in my_pieces:
            piece = my_pieces[piece_pos]
            return piece.get_legal_actions()
        else:
            return []

    def choose_action(self,action):
        self.board.update_board(action,self.player)

    def update_board(self,board):
        self.board = deepcopy(board)