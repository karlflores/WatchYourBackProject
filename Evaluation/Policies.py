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
        # find the values of each of the features

        # get the opponent colour
        opponent = board.get_opp_piece_type(colour)

        # Index 0
        diff_pieces = Features.diff_pieces(board,colour)
        # Index 1
        dist_cent = Features.total_dist_to_center(board, colour)
        # Index 2
        # num_actions = Features.num_actions(available_moves)
        # we want to minimise the number of vulnerable pieces we have
        num_vulnerable = Features.num_vulnerable_pieces(board, colour)
        # Index 3
        self_surrounded = Features.check_board_surrounded_my_piece(board,colour)
        # Index 4
        opp_surrounded = Features.check_board_surround_opponent(board,colour)
        # Index 5
        middle_occupy = Features.check_middle(board,colour)
        # Index 6
        num_cluster = Features.cluster_exists(board,colour)

        # Index 7 -- minimise our total minimum distance to the opponent pieces such that we remain somewhat offensive
        sum_min_man_dist = Features.total_min_man_dist(board, colour)
        # Index 8 -- Minimise the number of vulnerable pieces we have on the edge of the board, but max the opponents
        edge_vuln = Features.diff_edge_vulnerable(board, colour)
        # Index 9 -- We want to minimise our places next to the corner but maximise the opponents pieces at a corner
        next_to_corner = Features.place_next_to_corner(board,opponent) - 2*Features.place_next_to_corner(board, colour)
        # Index 10 -- We want to maxmimse the number of patterns we have compared to the number of patters the
        # opponent has
        diff_elim_pattern = Features.check_elim_pattern(board,colour) - Features.check_elim_pattern(board, opponent)

        # Index 11 -- We want to minimise the difference in pieces between the root node and the current depth we
        # are evaluating at -- we want to reduce the amount of pieces that we loose from the root
        diff_root_pieces = Features.diff_pieces_from_root(board,colour)
        # sprint(diff_root_pieces)

        # return the policy vectors with the features in the right index
        return diff_pieces, dist_cent, num_vulnerable, self_surrounded, opp_surrounded, middle_occupy, num_cluster, \
            edge_vuln, next_to_corner, sum_min_man_dist, diff_elim_pattern, diff_root_pieces

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
    def evaluate(self, board, colour, available_moves, load_weights=True):
        policy_vector = self.return_policy_vector(board,colour,available_moves)
        # print(policy_vector)
        if load_weights is True:
            return self.dot_prod(self.weights, policy_vector)
        else:
            # diff_pieces, dist_cent, num_actions, self_surrounded, opp_surrounded, middle_occupy, num_cluster,
            # edge_vuln, next_to_corner, sum_min_man_dist, diff_elim_pattern, diff_root_pieces
            self.weights = [1000, 500, 5, -100, 300, 2000, 100, 700, 550, 50, 500, 350]
            # self.weights = [100, 80, 5, -50, 60, 150, 130, 95, 80, 45, 50, 90]

            # to get the evaluation value -- we just need to do the dot product betweeen the policy vector
            # and the weight vector
            return self.dot_prod(self.weights, policy_vector)


