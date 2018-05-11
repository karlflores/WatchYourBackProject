from math import inf
from Constants import constant
from WatchYourBack.Board import Board
from Evaluation.Policies import Evaluation
from DataStructures.Transposition_Table import TranspositionTable
from copy import deepcopy
from time import time
from ErrorHandling.Errors import *

'''
NEGAMAX WITH A PURPOSE BUILT TRANSPOSITION TABLE FOR MEMOIzATION OF BOARDSTATES/AB CUTOFFS/BEST MOVES

THIS HAS THE SAME FUNCTIONALITY AND METHOD SIGNATURES AS NEGAMAX.PY -- THEREFORE CAN BE USED INTERCHANGEABLY 
FOR COMPARISON 


'''


class Negamax(object):

    def __init__(self, board, colour, file_name):
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

        # data structures for machine learning
        self.eval_depth = 0
        self.minimax_val = 0
        self.policy_vector = []

        # dictionary storing the available moves of the board
        self.available_actions = {constant.WHITE_PIECE: {}, constant.BLACK_PIECE: {}}

        # timing attributes
        self.undo_effected = []
        self.time_alloc = 0
        self.time_rem = 0
        self.time_start = 0
        self.time_end = 0
        self.total_time = 0

        # load the evaluation function based on the colour of the player
        if self.player == constant.WHITE_PIECE:
            self.evaluation = Evaluation("./XML", "/white_weights")
        else:
            self.evaluation = Evaluation("./XML", "/black_weights")

    '''
    Iterative Deepening Negamax 
    
    This implements a time-cutoff such that search is terminated once we have reached the allocated time for evaluation.
    
    IT RETURNS THE BEST MOVE IT HAS FOUND IN THE TIME ALLOCATED 
    '''
    def itr_negamax(self):
        # clear the transposition table every time we make a new move -- this is to ensure that it doesn't grow too big
        # if self.board.phase == constant.MOVING_PHASE and self.board.move_counter == 0:
        if self.board.phase == constant.PLACEMENT_PHASE:
            # clear the transposition table every time we want to evaluate a move in placement phase
            # this is to limit the size of growth
            self.tt.clear()

            # set the max depth iterations based on the phase that we are in
            MAX_ITER = 5
        else:
            MAX_ITER = 11

        # update the root number of pieces every time we do a search on a new node
        self.board.root_num_black = len(self.board.black_pieces)
        self.board.root_num_white = len(self.board.white_pieces)

        # default policy
        available_actions = self.board.update_actions(self.player)

        # if there are no available actions to make, therefore we just return None -- this is a forfeit
        if len(available_actions) == 0:
            return None

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
                    self.time_alloc = 190


        best_depth = 1
        val, move = 0, None

        # set the time remaining for each move evaluation
        self.time_rem = self.time_alloc

        # iterative deepening begins here
        for depth in range(1, MAX_ITER):
            # get the best move until cut off is reached
            try:

                self.time_start = self.curr_millisecond_time()
                val, move = self.negamax(depth, -inf, inf, self.player)
                self.time_end = self.curr_millisecond_time()

                # update the time remaining
                self.time_rem = self.time_alloc - (self.time_end-self.time_start)

                best_depth += 1
            except TimeOut:
                break

        # add the total time to the time allocated
        self.total_time += self.time_alloc

        # print(self.total_time)
        print(best_depth - 1)

        self.eval_depth = best_depth - 1
        return move

    def set_player_colour(self, colour):
        self.player = colour;
        self.opponent = Board.get_opp_piece_type(colour)


    # get the current time in milliseconds
    @staticmethod
    def curr_millisecond_time():
        return int(time() * 1000)


    '''
    NEGAMAX DRIVER FUNCTION -- THIS IMPLEMENTS THE FOLLOWING:
        - NEGAMAX WITH A TRANSPOSITION TABLE 
        - MOVE ORDERING USING THE BEST MOVE WE HAVE FOUND SO FAR (IF IT EXISTS IN THE TRANSPOSITION TABLE) 
        - MOVE ORDERING OF THE MOVES WE THINK TO BE FAVOURABLE USING A LIGHTWEIGHT EVALUATION FUNCTION 
        - SELECTING ONLY THE TOP FAVOURABLE MOVES TO EVALUATE USING MINIMAX -- THIS IS HEAVY GREEDY PRUNING 
          APPLIED TO NEGAMAX DESIGNED SUCH THAT WE ONLY LOOK AT MOVES THAT WE THINK WILL PRODUCE A GOOD OUTCOME,
          THUS PRUNING ANY MOVES THAT HAVE A HIGH CHANGE OF HAVING NO EFFECT ON THE GAME-STATE UTILITY.
    '''
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

            # get the value mappings from the dictionary
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
        if len(actions) <= 12:
            favourable = actions
        elif 12 < len(actions) < 20:
            favourable = actions[:12]
        else:
            favourable = actions[:len(actions)//2]

        # iterate only through the favourable moves, ensuring that the number of moves is not too big
        # the aim is to reduce the branching factor as much as we can, but also having enough moves to
        # evaluate such that we get the part of the optimality decision making  from negamax/minimax
        # rather than a purely greedy approach.
        # print(len(favourable))
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

            # test for cut off
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

    # cut-off test -- either depth is zero or the board is at terminal state
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
