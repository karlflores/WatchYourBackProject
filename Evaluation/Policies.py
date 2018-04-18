from Board.Board import Board
from math import sqrt, fabs
# Class to implement all the evaluation functions that we generate throughout
# the development of this project


class Evaluation(object):
    @staticmethod
    def basic_policy(board,colour):
        # assume that the board is in a byte string representation
        diff_pieces = len(board.piece_pos[colour])-3*len(board.piece_pos[Board.get_opp_piece_type(colour)])
        dist_cent = 0
        for pieces in board.piece_pos[colour]:
            dist_cent+= Evaluation.distance(pieces,(3,3))

        dist_pieces = 0

        return 1/(1+int(dist_cent))+10*diff_pieces
        #print(dist_cent)
        #return diff_pieces

    @staticmethod
    def distance(pos_1,pos_2):
        return sqrt((pos_1[0]-pos_2[0])**2+(pos_1[1]-pos_2[1])**2)

