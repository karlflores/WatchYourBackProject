'''
* Implements the mini-max algorithm based on the minimax_mode structure
* and the player file
'''
from math import inf
from Constants import constant
from WatchYourBack.Board import Board
from Evaluation.Policies import Evaluation
from Data_Structures.Transposition_Table import TranspositionTable
from copy import deepcopy
from time import time
from Error_Handling.Errors import *

'''
NEGAMAX WITH A PURPOSE BUILT TRANSPOSITION TABLE FOR MEMOISATION OF BOARDSTATES/AB CUTOFFS/BEST MOVES
FUNCTIONALITY IS THE SAME AS WHAT IS IN NEGAMAX.PY
'''

class Negamax(object):

    def __init__(self, board, colour):
        # we want to create a node

        self.tt = TranspositionTable()

        # only use this board to complete the search
        # save memory
        self.board = deepcopy(board)

        # for alpha beta search -- instead of passing it into the function calls we can use this
        self.alpha = -inf
        self.beta = inf

        # defines the colours of min and max
        self.player = colour
        self.opponent = Board.get_opp_piece_type(self.player)

        # default depth
        self.depth = inf

        # default move ordering with iterative deepening
        self.actions_evaluated = []
        self.actions_leftover = []

        # data structures for machine learning
        self.eval_depth = 0
        self.minimax_val = 0
        self.policy_vector = []

        # dictionary storing the available moves of the board
        self.available_actions = {constant.WHITE_PIECE: {}, constant.BLACK_PIECE: {}}

        # generate the actions for the start of the game
        # self.generate_actions()

        self.undo_effected = []
        self.time_alloc = 0
        self.time_rem = 0
        self.time_start = 0
        self.time_end = 0
        self.total_time = 0
        self.evaluation = Evaluation("./XML","/eval_weights")

    '''
    * Alpha Beta - Minimax Driver Function 
    '''

    def itr_negamax(self):
        # clear the transposition table every time we make a new move -- this is to ensure that it doesn't grow too big
        # if self.board.phase == constant.MOVING_PHASE and self.board.move_counter == 0:
        if self.board.phase == constant.PLACEMENT_PHASE:
            self.tt.clear()

            # set the max depth iterations based on the phase
            MAX_ITER = 5
        else:
            MAX_ITER = 11

        # default policy
        available_actions = self.board.update_actions(self.player)

        # if there are no available actions to make, therefore we just return None -- this is a forfeit
        if len(available_actions) == 0:
            return None

        if self.board.phase == constant.PLACEMENT_PHASE:
            self.time_alloc = 1500
        else:
            self.time_alloc = 900

            # if we have reached 100 moves in the game and the game
            if self.total_time > 100000 and self.board.move_counter > 120:
                self.time_alloc = 500

        # get time

        best_depth = 1
        val, move = 0, None

        # iterative deepening begins here
        for depth in range(1, MAX_ITER):
            # get the best move until cut off is reached
            try:
                self.time_rem = self.time_alloc

                self.time_start = self.curr_millisecond_time()
                val, move = self.negamax(depth, -inf, inf, self.player)
                self.time_end = self.curr_millisecond_time()

                self.time_rem = self.time_alloc - (self.time_end-self.time_start)

                best_depth += 1
            except TimeOut:
                break

        print(best_depth - 1)
        self.eval_depth = best_depth - 1
        return move

    def set_player_colour(self, colour):
        self.player = colour;
        self.opponent = Board.get_opp_piece_type(colour)

    @staticmethod
    def curr_millisecond_time():
        return int(time() * 1000)

    def negamax(self,depth,alpha,beta,colour):

        # print(self.board.board_state)

        # Timeout handling
        self.time_end = self.curr_millisecond_time()
        if self.time_end - self.time_start > self.time_rem:
            raise TimeOut

        opponent = Board.get_opp_piece_type(colour)
        original_alpha = alpha
        dic = {self.player: 1, self.opponent: -1}

        move_to_try = None
        # check if the current board state is in the transposition table
        board_str = self.board.board_state.decode("utf-8")

        key = self.tt.contains(board_str, colour, phase=self.board.phase)
        if key is not None:
            board_str = key[0]
            entry = self.tt.get_entry(board_str,colour)
            tt_value = entry[0]
            tt_type = entry[1]
            tt_best_move = entry[2]
            tt_depth = entry[3]

            # if we have found an entry in the transposition table, then the move
            # we should try first is this best move
            move_to_try = tt_best_move

            if tt_depth >= depth:
                # this is the PV node therefore this is the best move that we have found so far
                if tt_type == constant.TT_EXACT:
                    return tt_value, tt_best_move

                # the minimax value in the transposition table is a lower bound to the search
                elif tt_type == constant.TT_LOWER:
                    if tt_value > alpha:
                        alpha = tt_value

                # the value in the table corresponds to a beta cutoff and therefore it is an upper bound for beta
                elif tt_type == constant.TT_UPPER:
                    if tt_value < beta:
                        beta = tt_value

                # test for cutoff -- return the best move found so far
                if alpha >= beta:
                    return tt_value, tt_best_move

        # obtain the actions and sort them
        actions = self.board.update_actions(colour)
        actions = self.board.sort_actions(actions,colour)

        # terminal test -- default case
        if self.cutoff_test(depth):
            val = self.evaluate_state(self.board, self.player, actions)*dic[colour]
            return val, None

        # do the negamax search  search
        best_val = -inf
        best_action = None

        # if we have found a best action to take in the transposition table, this should be the first
        # move we should try -- put this at the start of the list of actions
        if move_to_try is not None and move_to_try in actions:
            # put the move to try at the first position -- therefore it will be searched first
            actions = [move_to_try] + actions

        i = 0
        # split the list of actions into favourable and unfavourable actions
        # we only consider to search teh favourable actions if the action list is long enough
        if len(actions) <= 10:
            favourable = actions
        elif 10 < len(actions) < 16:
            favourable = actions[:10]
        else:
            favourable = actions[:len(actions)//2]

        for action in favourable:

            # skip over the best action in the tt table -- this action has already be searched
            if action == move_to_try and i != 0:
                continue
            i += 1

            # update the board, record the eliminated pieces from that update
            elim = self.board.update_board(action, colour)
            score, temp = self.negamax(depth-1, -beta, -alpha, opponent)
            score = -score
            # undo the action applied to the board
            self.undo_action(action,colour,elim)

            # get the best score and action so far
            if score > best_val:
                best_val = score
                best_action = action

            # update alpha if needed
            if best_val > alpha:
                alpha = best_val

            if alpha >= beta:
                break

        # store the values in the transposition table
        if best_val <= original_alpha:
            # then this is an upper bound
            tt_type = constant.TT_UPPER
        elif best_val >= beta:
            # if the best value we have found is a lower bound
            tt_type = constant.TT_LOWER
            # print("LOWER")
        else:
            # this is the PV node value
            tt_type = constant.TT_EXACT

        # add the entry to the transposition table
        self.tt.add_entry(self.board.board_state,colour,best_val,tt_type,best_action, depth)

        return best_val, best_action

    def cutoff_test(self, depth):
        if depth == 0:
            return True

        if self.is_terminal():
            return True

        return False

    # evaluate the game state
    def evaluate_state(self, board, colour, actions):
        return self.evaluation.evaluate(board, colour, actions)

    # update the negamax board representation for another search
    def update_board(self, board):
        self.board = deepcopy(board)

    # terminal state check
    def is_terminal(self):
        return self.board.is_terminal()

    # undo board wrapper
    def undo_action(self,action,colour,elim):
        return self.board.undo_action(action,colour,elim)