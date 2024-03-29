'''
* Implements the mini-max algorithm based on the minimax_mode structure
* and the player file
'''
from math import inf
from Constants import constant
from DepreciatedBoard.Board import Board
from Evaluation.Policies import Evaluation
from DataStructures.Transposition_Table import TranspositionTable
from copy import deepcopy
from time import time
from ErrorHandling.Errors import *

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

        self.evaluation = Evaluation("./XML","/eval_weights")

    '''
    * Alpha Beta - Minimax Driver Function 
    '''

    def itr_negamax(self):
        # clear the transposition table every time we make a new move -- this is to ensure that it doesn't grow too big
        # if self.board.phase == constant.MOVING_PHASE and self.board.move_counter == 0:
        #if self.board.phase == constant.PLACEMENT_PHASE:
        self.tt.clear()

        MAX_ITER = 10

        # default policy
        available_actions = self.board.update_actions(self.board, self.player)
        # self.actions_leftover = self.board.update_actions(self.board, self.player)

        if len(available_actions) == 0:
            return None
        #else:
            # lets just set the default to the first move
        #    move = available_actions[0]

        # time allocated per move in ms
        '''
        self.time_alloc = 0
        if self.board.phase == constant.PLACEMENT_PHASE:
            self.time_alloc = (30000 - self.time_alloc) / (24 - self.board.move_counter)
        else:
            self.time_alloc = (30000 - self.time_alloc) / (100 - self.board.move_counter)
        '''

        # self.time_alloc = 5000
        # time allocated per move in ms
        self.time_alloc = 0
        total = 120000
        if self.board.phase == constant.PLACEMENT_PHASE:
            #self.time_alloc = (total/2 - self.time_alloc) / (24 - self.board.move_counter)
            total -= self.time_alloc
            self.time_alloc = 1000
        else:
            #self.time_alloc = (total - self.time_alloc) / (100 - self.board.move_counter)
            total -= self.time_alloc
            self.time_alloc = 1000
        # get time
        start_time = Negamax.curr_millisecond_time()
        best_depth = 1
        val, move = 0, None
        # iterative deepening begins here
        for depth in range(1, MAX_ITER):
            print(self.tt.size)
            print(depth)
            try:
                self.time_rem = self.time_alloc
                self.time_start = self.curr_millisecond_time()
                val, move = self.negamax(depth,-inf,inf,self.player)
                self.time_end = self.curr_millisecond_time()

                self.time_rem = self.time_alloc - (self.time_end-self.time_start)
                print(move)
                best_depth += 1
            except TimeOut:
                print("TIMEOUT")
                break

            if Negamax.curr_millisecond_time() - start_time > self.time_alloc:
                break

        self.eval_depth = best_depth
        return move

    def set_player_colour(self, colour):
        self.player = colour;
        self.opponent = Board.get_opp_piece_type(colour)

    @staticmethod
    def curr_millisecond_time():
        return int(time() * 1000)

    def negamax(self,depth,alpha,beta,colour):
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

        key = self.tt.contains(board_str,colour,phase=self.board.phase)
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

            #print("FOUND ENTRY IN TT")
            if tt_depth >= depth:
                if tt_type == constant.TT_EXACT:
                    #print("FOUND PV")
                    return tt_value, tt_best_move
                elif tt_type == constant.TT_LOWER:
                    if tt_value > alpha:
                        #print("FOUND FAIL SOFT")
                        alpha = tt_value

                elif tt_type == constant.TT_UPPER:
                    if tt_value < beta:
                        #print("FOUND FAIL HARD")
                        beta = tt_value

                if alpha >= beta:
                    return tt_value, None

        actions_1 = self.board.update_actions(self.board, colour)

        actions = self.board.sort_actions(actions_1,colour)

        # terminal test -- default case
        if self.cutoff_test(depth):
            val = self.evaluate_state(self.board, self.player, actions_1)*dic[colour]
            return val, None

        # do the minimax search
        best_val = -inf
        best_action = None

        if move_to_try is not None and move_to_try in actions:
            #print("MOVE ORDERING")
            # put the move to try at the first position -- therefore it will be searched first
            actions = [move_to_try] + actions
        i = 0
        if len(actions) <= 8:
            favourable = actions
        else:
            favourable = actions[:8]
        # print(len(actions))
        for action in favourable:
            # skip over the best action in the tt table
            if action == move_to_try and i!= 0:
                continue
            i+=1

            self.board.update_board(action, colour)
            score, temp = self.negamax(depth-1, -beta, -alpha, opponent)
            score = -score

            if score > best_val:
                best_val = score
                best_action = action

            if best_val > alpha:
                alpha = best_val

            self.undo_move()

            if alpha >= beta:
                break

        # store the values in the transposition table
        if best_val <= original_alpha:
            # then this is an upperbound -FAILHARD
            tt_type = constant.TT_UPPER
        elif best_val >= beta:
            tt_type = constant.TT_LOWER
            # print("LOWER")
        else:
            tt_type = constant.TT_EXACT
            # print("EXACT")

        # add the entry to the transposition table
        self.tt.add_entry(self.board.board_state,colour,best_val,tt_type,best_action, depth)
        return best_val, best_action

    def cutoff_test(self, depth):
        if depth == 0:
            return True

        if self.is_terminal():
            return True

        return False
    '''
    * NEED TO THINK ABOUT IF THIS FUNCTION JUST EVALUATES THE NODES AT THE ROOT STATE DUE TO THE UNDO MOVES 
            -- NEED TO TEST THIS OUT SOMEHOW, because other than that the algorithm is working as intended 
            -- Need to work out some optimisations of the algorithm though 

    '''

    def evaluate_state(self, board, colour, actions):
        #return Evaluation.basic_policy(board,colour)
        return self.evaluation.evaluate(board, colour, actions)

    # update the available moves of the search algorithm after it has been instantiated
    #
    # def update_available_moves(self, node, available_moves):
    #    node.available_moves = available_moves

    def update_board(self, board):
        self.board = deepcopy(board)

    def is_terminal(self):
        return self.board.is_terminal()

    def undo_move(self):
        return self.board.undo_move()
        # then we need to recalculate the available moves based on the board representation
        # self.generate_actions()
