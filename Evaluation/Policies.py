from math import sqrt #, fabs
from XML.xml_helper import xml_helper

# from Agents.Minimax_Node import *
# from random import randint
# Class to implement all the evaluation functions that we generate throughout
# the development of this project
from DepreciatedBoard.Board import Board
from Evaluation.Features import Features


class Evaluation(object):
    def __init__(self,path,filename):
        self.read_xml = xml_helper(path,filename)

        # read the weights from the XML file
        self.weights = self.read_xml.load()

    # return the policy vector -- this was designed this way such that we could have easily applied machine learning
    # the policy vector is just a vector containing the evaluation of each individual feature of the board-state
    @staticmethod
    def return_policy_vector(board,colour,available_moves):
        opponent = board.get_opp_piece_type(colour)
        diff_pieces = Features.diff_pieces(board,colour)
        dist_cent = Features.total_dist_to_center(board, colour)
        num_actions = Features.num_actions(available_moves)
        self_surrounded = Features.check_board_surrounded_my_piece(board,colour)
        opp_surrounded = Features.check_board_surround_opponent(board,colour)
        middle_occupy = Features.check_middle(board,colour)
        num_cluster = Features.cluster_exists(board,colour)
        sum_min_man_dist = Features.total_min_man_dist(board, colour)
        edge_vuln = Features.diff_edge_vulnerable(board, colour)
        next_to_corner = Features.place_next_to_corner(board,opponent) - Features.place_next_to_corner(board, colour)
        return diff_pieces, dist_cent, num_actions, self_surrounded, opp_surrounded, middle_occupy, num_cluster, \
                    edge_vuln, next_to_corner, sum_min_man_dist

    # get the dot product between the weight and policy vectors -- this is the evaluation value
    @staticmethod
    def dot_prod(policy_vector, weight_vector):
        if len(policy_vector) != len(weight_vector):
            return None

        evaluate = 0

        for i,feature in enumerate(policy_vector):
            evaluate += policy_vector[i]*weight_vector[i]

        return evaluate

    # get the scalar evaluation of the board state
    # note -- load_weights -- this is if we want to use the xml_file to load weights (True) if we dont we set it to
    # False (default value)
    def evaluate(self, board, colour, available_moves, load_weights=False):
        policy_vector = self.return_policy_vector(board,colour,available_moves)
        # print(policy_vector)
        if load_weights is False:
            return self.dot_prod(self.weights, policy_vector)
        else:
            # diff_pieces, dist_cent, num_actions, self_surrounded, opp_surrounded, middle_occupy, num_cluster,
            # edge_vuln, next_to_corner, sum_min_man_dist
            self.weights = [1000, 50, 5, -100, 300, 2000, 500,220,350, 50]

            # to get the evaluation value -- we just need to do the dot product betweeen the policy vector
            # and the weight vector
            return self.dot_prod(self.weights, policy_vector)


