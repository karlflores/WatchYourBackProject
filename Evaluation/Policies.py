from math import sqrt #, fabs
from XML.xml_helper import xml_helper

# from Agents.Minimax_Node import *
# from random import randint
# Class to implement all the evaluation functions that we generate throughout
# the development of this project
from DepreciatedBoard.Board import Board
from Evaluation.FeaturesOOP import Features


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
    def return_policy_vector(board,colour,available_moves):

        diff_pieces = Features.diff_pieces(board,colour)
        dist_cent = Features.total_dist_to_center(board, colour)
        num_actions = Features.num_actions(available_moves)
        self_surrounded = Features.check_board_surrounded_my_piece(board,colour)
        opp_surrounded = Features.check_board_surround_opponent(board,colour)
        middle_occupy = Features.check_middle(board,colour)
        num_cluster = Features.cluster_exists(board,colour)
        sum_min_man_dist = Features.total_min_man_dist(board, colour)
        edge_vuln = Features.diff_edge_vulnerable(board, colour)
        next_to_corner = Features.place_next_to_corner(board, colour)
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

    def evaluate(self, board, colour, available_moves, load_weights=False):
        policy_vector = self.return_policy_vector(board,colour,available_moves)
        # print(policy_vector)
        if load_weights is False:
            return self.dot_prod(self.weights, policy_vector)
        else:
            # diff_pieces, dist_cent, num_actions, self_surrounded, opp_surrounded, middle_occupy, num_cluster,
            # edge_vuln, next_to_corner, sum_min_man_dist
            self.weights = [1000, 50, 5, -100, 300, 1000, 500,220,100,50]
            return self.dot_prod(self.weights, policy_vector)


