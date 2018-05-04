from math import sqrt #, fabs
from XML.xml_helper import xml_helper

# from Agents.Minimax_Node import *
# from random import randint
# Class to implement all the evaluation functions that we generate throughout
# the development of this project
from Board.Board import Board

class Evaluation(object):
    def __init__(self,path,filename):
        self.read_xml = xml_helper(path,filename)

        # read the weights from the XML file
        self.weights = self.read_xml.load()

    @staticmethod
    def distance(pos_1,pos_2):
        return sqrt((pos_1[0]-pos_2[0])**2+(pos_1[1]-pos_2[1])**2)

    @staticmethod
    def eval(board,weights):
        for weight in weights:
            pass

    @staticmethod
    def return_policy_vector(board,colour):

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
        return diff_pieces, 1/(1+dist_cent), num_moves

    # get the dot product between the weight and policy vectors -- this is the evaluation value
    @staticmethod
    def dot_prod(policy_vector, weight_vector):
        if len(policy_vector) != len(weight_vector):
            return None

        evaluate = 0

        for i in range(len(policy_vector)):
            evaluate += policy_vector[i]*weight_vector[i]

        return evaluate

    def evaluate(self,board,colour):
        policy_vector = self.return_policy_vector(board,colour)
        return self.dot_prod(self.weights,policy_vector)
