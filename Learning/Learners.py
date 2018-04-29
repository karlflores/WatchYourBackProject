from xml import etree as et
from Board.Board import Board
from copy import deepcopy,copy
from Player import Player as rand_player
from Player_AB_LRU import Player as ab_player
from Player_MCTS import Player as mcts_player
from Board import constant
from math import *


class Learner(object):
    def __init__(self, name, feature, weights, learning_rate=0.7):
        self.weights = weights
        self.learning_rate = learning_rate
        self.weights_len = len(weights)
        self.eval_name = name

        self.game_state = []
        self.eval_depths = []
        self.minimax_eval = []

        # when we are evaluating the weight update -- we only need the
        # policy vector to evaluate the derivative
        # we don't actually evaluate the state -- we just get the feature of the
        # policy vector

        self.policy_vectors = []
        self.temporal_diff = []
        self.reward = []

        self.player = ab_player('white')
        self.opponent = rand_player('black')

    def td_leaf_lambda(self, eval_value, result):
        pass

    def playgame(self, first_player=True):
        game = Board()

        state_index = 0
        if first_player:
            # this player makes the move first
            self.game_state.append(deepcopy(game))

        while game.is_terminal() is False:
            turns = game.move_counter

            action = self.player.action(turns)
            # append the depth at which the action was evaluated at -- this is so we can find the best child node later
            # we require r(s_i^l,w) -- now is s_i^l the minimax value that evaluated?
            self.eval_depths.append(self.player.depth_eval)
            self.minimax_eval.append(self.player.minimax_val)
            self.policy_vectors.append(self.player.policy_vector)

            # update the board
            game.update_board(action, self.player.colour)
            self.opponent.update(action)

            turns = game.move_counter
            # opponent makes a move
            action = self.opponent.action(turns)
            game.update_board(action,self.opponent.colour)
            self.player.update(action)

            # add the game state to the game state array
            self.game_state.append(deepcopy(game))

        # return the outcome of the game
        if game.winner == constant.WHITE_PIECE:
            return 1
        elif game.winner == constant.BLACK_PIECE:
            return -1
        elif game.winner is None:
            return 0

    def get_temporal_diff(self):
        for i in range(len(self.minimax_eval)-1):
            self.temporal_diff.append(self.minimax_eval[i+1]-self.minimax_eval[i])

    @staticmethod
    def reward_dx(evaluation,feature_eval):
        return Learner.tanh_dx(evaluation)*feature_eval

    @staticmethod
    def tanh_dx(val):
        return 1 - pow(tanh(val),2)

    # once we play a game we can call update weights to update the weight parameters
    # of the evaluation function according to the TDLead-Lambda formula
    def update_weights(self,l_ambda=0.7,learning_rate=0.7):
        for j in range(len(self.weights)):
            outer_sum = 0
            for i in range(len(self.game_state)-1):
                inner_sum = 0

                # calculate the inner sum
                for m in range(len(self.game_state)-1):
                    inner_sum += pow(l_ambda,m-i)*self.temporal_diff[m]

                # get the game state for this value
                state = self.game_state[i]
                feature_val = state.feature_val[i]

                outer_sum += Learner.reward_dx(self.minimax_eval[i],feature_val)