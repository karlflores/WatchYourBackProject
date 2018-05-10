from math import inf
from Constants import constant
from WatchYourBack.Board import Board
from Evaluation.Policies import Evaluation
from DataStructures.Transposition_Table import TranspositionTable
from copy import deepcopy
from time import time
from ErrorHandling.Errors import *

'''
IMPLEMENTED THE NEGASCOUT ALGORITHM TO NEGAMAX-AB-TRANSPOSITION TABLE 
- this works by assuming the first move you will try is the best move you have found so far, 
and testing every other sequential move with a NULL alpha-beta window such that it maximises
pruning. If the cutoff does not fail, it has to do a full research from that specific node as
clearly the move tried was not the best move found so far.

FROM OUR TESTS, THERE IS NO BENEFIT TO RUNNING THIS ALGORITHM, THERE IS NO SIGNIFICANT SPEED UP
IN PERFORMANCE. THIS COULD BE DUE TO THE WAY THAT WE ARE DOING OUR MOVE ORDERING OR THE WAY THAT
WE HAVE IMPLEMENTED THE TRANSPOSITION TABLE. THEORETICALLY, WE SHOULD HAVE SEEN A DECENT INCREASE 
IN SPEEDUP, BUT I BELIEVE DUE TO THE RUN TIME OF NAIVE-MOVE ORDERING, THAT THIS ALGORITHM IS NOT 
PROCUDING ANY NET BENEFIT TO NORMAL NEGAMAX-AB
'''


class Negascout(object):

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

    def itr_negascout(self):
        colour = self.player
        # clear the transposition table every time we make a new move -- this is to ensure that it doesn't grow too big
        # if self.board.phase == constant.MOVING_PHASE and self.board.move_counter == 0:
        if self.board.phase == constant.PLACEMENT_PHASE:
            self.tt.clear()


        MAX_ITER = 20

        # default policy
        available_actions = self.board.update_actions(colour)
        action_set = set(available_actions)
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
        if self.board.phase == constant.PLACEMENT_PHASE:
            self.time_alloc = 1500
        else:
            self.time_alloc = 1200

            # if we have reached 100 moves in the game and the game
            if self.total_time > 90000 or self.board.move_counter > 120:
                self.time_alloc = 500
                # if we are near the final shrinking phase, then we can decrease the time it has to
                # evaluate
                if self.board.move_counter > 150:
                    self.time_alloc = 150


        start_time = Negascout.curr_millisecond_time()
        best_depth = 1
        val, move = 0, None
        best_move = None
        self.time_rem = self.time_alloc
        # iterative deepening begins here
        for depth in range(1, MAX_ITER):
            print(self.tt.size)
            print(depth)
            try:

                self.time_start = self.curr_millisecond_time()
                val, move = self.negascout(depth, -inf, inf, self.player)
                # move = self.negascout(depth,self.player)
                self.time_end = self.curr_millisecond_time()

                self.time_rem = self.time_alloc - (self.time_end-self.time_start)
                print(move)
                best_depth += 1

                if move is not None and move in action_set:
                    best_move = move

            except TimeOut:
                print("TIMEOUT")
                break
        # add the time allocated to the total time
        self.total_time += self.time_alloc
        self.eval_depth = best_depth
        return best_move

    def set_player_colour(self, colour):
        self.player = colour;
        self.opponent = Board.get_opp_piece_type(colour)

    @staticmethod
    def curr_millisecond_time():
        return int(time() * 1000)

    def negascout(self,depth,alpha,beta,colour):
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
            #print(move_to_try)
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
                    return tt_value, tt_best_move

        actions= self.board.update_actions(colour)
        # actions = actions_1
        actions = self.board.sort_actions(actions, colour)
        #actions = actions_1
        # terminal test -- default case
        if self.cutoff_test(depth):
            val = self.evaluate_state(self.board, self.player, actions)*dic[colour]
            return val, None

        # do the minimax search
        best_val = -inf
        best_action = None

        if move_to_try is not None and move_to_try in actions:
            #print("MOVE ORDERING")
            # put the move to try at the first position -- therefore it will be searched first
            actions = [move_to_try] + actions

        i = 0
        if len(actions) <= 10:
            favourable = actions
        else:
            favourable = actions[:len(actions)//2]
        # print(len(actions))

        # start negascout here
        for i, action in enumerate(favourable):
            # skip over the best action in the tt table
            if action == move_to_try and i > 0:
                continue

            elim = self.board.update_board(action, colour)

            # if we are at the first node -- this is the best node we have found so far
            # therefore we do a full search on this node
            if i == 0:
                # do a full search on the best move found so far
                score, _ = self.negascout(depth-1,-beta,-alpha, opponent)
                score = -score

            else:
                # assume that the first move is the best move we have found so far,
                # therefore to see if this is the case we can do a null window search on the
                # rest of the moves, if the search breaks, then we know that the first move is
                # the best move and it will return the best move
                # but if the search "failed high" - i.e. the score is between alpha and beta
                # we need to do a full research of the node to work out the minimax value

                # do the null window search
                score, _ = self.negascout(depth-1,-alpha-1,-alpha,opponent)
                score = -score

                # if it failed high, then we just do a full search to find the actual best move
                if alpha < score < beta:
                    score, _ = self.negascout(depth-1,-beta,-score,opponent)
                    score = -score

            # get the best value and score
            if best_val < score:
                best_val = score
                best_action = action

            # reset alpha
            if alpha < score:
                alpha = score

            # undo the action applied to the board -- we can now apply another move to the board
            self.undo_actions(action,colour,elim)

            # test for alpha beta cutoff
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

    def undo_actions(self,action,colour,elim):
        return self.board.undo_action(action,colour,elim)
        # then we need to recalculate the available moves based on the board representation
        # self.generate_actions()
