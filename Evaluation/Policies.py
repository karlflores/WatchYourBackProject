from math import sqrt #, fabs
# from Agents.Minimax_Node import *
# from random import randint
# Class to implement all the evaluation functions that we generate throughout
# the development of this project
from Board.Board import Board

class Evaluation(object):

    @staticmethod
    def basic_policy(board, colour):

        # assume that the board is in a byte string representation
        diff_pieces = len(board.piece_pos[colour])-3*len(board.piece_pos[Board.get_opp_piece_type(colour)])
        dist_cent = 0
        for pieces in board.piece_pos[colour]:
            dist_cent += Evaluation.distance(pieces, (3.5,3.5) )

        # number of pieces of the opponent eliminated
        available_actions = board.update_actions(board,colour)

        num_moves = len(available_actions)

        # RANDOM MOVES FOR TESTING IF MINIMAX IS WORKING CORRECTLY
        # return randint(0,5)

        return diff_pieces + 100/(1+10*dist_cent) + 0.3*num_moves

    @staticmethod
    def distance(pos_1,pos_2):
        return sqrt((pos_1[0]-pos_2[0])**2+(pos_1[1]-pos_2[1])**2)

    @staticmethod
    def eval(board,weights):
        for weight in weights:
            pass
