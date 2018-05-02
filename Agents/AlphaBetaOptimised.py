'''
* Implements the mini-max algorithm based on the minimax_mode structure
* and the player file
'''
from math import inf
from Board.Board import constant
from Board.Board import Board
from Evaluation.Policies import Evaluation
from copy import deepcopy
from time import time, sleep
from functools import lru_cache
import heapq

class MinimaxABOptimised(object):

    def __init__(self, board, colour):
        # we want to create a node

        self.transposition_table = set()

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
    '''
    * Alpha Beta - Minimax Driver Function 
    '''

    def iterative_deepening_alpha_beta(self):
        '''
        I dont think this is working correctly -- i believe when things are getting cached because it doesnt take in consideration the depth of the call of that minimax evaluation
        we need to take into consideration the depth for it to call correctly

        need to change this
        '''
        MAX_ITER = 100

        # default policy
        available_actions = self.board.update_actions(self.board,self.player)
        # self.actions_leftover = self.board.update_actions(self.board, self.player)

        if len(available_actions) == 0:
            return None
        else:
            # lets just set the default to the first move
            move = available_actions[0]

        # time allocated per move in ms
        time_alloc = constant.TIME_CUTOFF_AB

        # get time
        start_time = MinimaxABOptimised.curr_millisecond_time()
        best_depth = 1
        # iterative deepening begins here
        for depth in range(1, MAX_ITER):
            print(depth)
            # invalidate / clear the cache when increasing the search depth cutoff
            self.min_value.cache_clear()
            #self.max_value.cache_clear()
            # peform the search
            move = self.alpha_beta_minimax(depth, available_actions)

            # after one iteration of ab search we can order the moves based on the actions that
            # the previous depth evaluated the actions at
            available_actions = []
            while len(self.actions_evaluated) > 0:
                (val, action) = heapq._heappop_max(self.actions_evaluated)
                available_actions.append(action)
            # transform the heap into a max heap
            heapq._heapify_max(self.actions_evaluated)

            # update the available_actions list
            available_actions = available_actions + self.actions_leftover

            best_depth += 1

            if MinimaxABOptimised.curr_millisecond_time() - start_time > time_alloc:
                break

        self.eval_depth = best_depth
        return move

    def set_player_colour(self,colour):
        self.player = colour;
        self.opponent = Board.get_opp_piece_type(colour)

    @staticmethod
    def curr_millisecond_time():
        return int(time() * 1000)

    def alpha_beta_minimax(self, depth, available_actions):
        self.actions_evaluated = []
        if self.board.phase == constant.MOVING_PHASE and self.board.move_counter == 0:
            self.min_value.cache_clear()
            # self.max_value.cache_clear()

        best_move = None
        alpha = -inf
        evaluate = -inf
        beta = inf

        # get the available moves of the board (based on the current board representation)
        # we can generate the actions as we wish -- this can easily change -- TODO : OPTIMISATION/ PRUNING OF ACTION __ CAN BE GREEDY __ favoured moves and unfavoured moves
        self.actions_leftover = self.board.update_actions(self.board, self.player)
        # self.actions_leftover = self.board.update_actions(self.board,self.player)

        for action in available_actions:
            # update the minimax board representation with the action
            self.board.update_board(action, self.player)

            # get the board representation for caching
            board_string = self.board.board_state.decode("utf-8")

            ab_evaluate = self.min_value(board_string, self.opponent, self.board.phase, depth - 1)

            heapq.heappush(self.actions_evaluated, (ab_evaluate, action))
            self.actions_leftover.remove(action)

            if ab_evaluate > evaluate:
                best_move = action
                evaluate = ab_evaluate

            # undo the move
            self.undo_effected = self.undo_move()

            if evaluate >= beta:
                self.minimax_val = evaluate
                return best_move

            alpha = max(alpha, evaluate)

        self.minimax_val = evaluate
        return best_move

    # memoize the function call -- opitimisation
    #@lru_cache(maxsize=10000)
    def max_value(self,board_string, colour, phase, depth):

        evaluate = -inf

        if self.cutoff_test(depth):
            return self.evaluate_state(self.board)

        # visit each available move
        available_actions = self.board.update_actions(self.board, colour)

        for action in available_actions:

            # update the board representation with the move
            self.board.update_board(action, colour)

            # create an immutable object for board_string such that we can call lru_cache on the max function call
            board_string = self.board.board_state.decode("utf-8")

            # get the minimax value for this state
            evaluate = max(evaluate, self.min_value(board_string, self.opponent, self.board.phase, depth-1))

            # undo the move so that we can apply another action
            self.undo_effected = self.undo_move()

            if evaluate >= self.beta:
                return evaluate

            self.alpha = max(evaluate, self.alpha)

        return evaluate

    # memoize the min value results -- optimisation of its function call
    @lru_cache(maxsize=100000)
    def min_value(self, board_string, colour, phase, depth):

        # beginning evaluation value
        evaluate = inf

        if self.cutoff_test(depth):
            return self.evaluate_state(self.board)

        # generate the actions to search on
        available_actions = self.board.update_actions(self.board, colour)

        for action in available_actions:

            # update the board representation -- this action is the min nodes's action
            self.board.update_board(action, colour)

            board_string = self.board.board_state.decode("utf-8")

            # find the value of the max node
            evaluate = min(evaluate, self.max_value(board_string, self.player, self.board.phase, depth - 1))

            # undo the board move so that we can apply another move
            # -- we also go up a level therefore we need to increment depth
            self.undo_effected = self.undo_move()

            '''
            if beta <= alpha:
                # when we break from the loop make sure to undo the move
                break
            '''

            if evaluate <= self.alpha:
                return evaluate

            self.beta = min(self.beta, evaluate)

        return evaluate

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

    def evaluate_state(self, board):
        return Evaluation.basic_policy(board, self.player)

    # update the available moves of the search algorithm after it has been instantiated
    #
    # def update_available_moves(self, node, available_moves):
    #    node.available_moves = available_moves

    def update_board(self, board):
        self.board = deepcopy(board)


    def is_terminal(self):
        return self.board.is_terminal()

    def check_symmetry(self, board_state):
        transformation = MinimaxABUndo.apply_horizontal_reflection(board_state)
        board = deepcopy(board_state)
        if transformation.decode("utf-8") in self.visited:
            return True
        else:
            self.visited.add(board.decode("utf-8"))
            return False

    @staticmethod
    def apply_horizontal_reflection(board_state):
        temp = ''
        for index in range(constant.BOARD_SIZE ** 2):
            temp += constant.FREE_SPACE

        temp = bytearray(temp, 'utf-8')

        for row in range(constant.BOARD_SIZE):
            for col in range(constant.BOARD_SIZE):
                Board.set_array_char(temp, 7 - row, 7 - col,
                                     Board.get_array_element(board_state, row, col))
        # print(temp)
        # print(board_state)
        return temp

    def undo_move(self):
        return self.board.undo_move()
        # then we need to recalculate the available moves based on the board representation
        # self.generate_actions()


    '''
    #################################################################################
    # METHODS FOR THE DICTIONARY REPRESENTATION OF THE AVAILABLE MOVES ON THE BOARD #
    #
    #
    #
    #
    ################################################################################
    '''
    # we update the available actions when we update the board representation
    def generate_actions(self):
        if self.board.phase == constant.PLACEMENT_PHASE:
            self.init_available_placement_actions()
            self.start_available_actions_placement()
        elif self.board.phase == constant.MOVING_PHASE:
            print(self.board.piece_pos)
            print("dsfsf")
            self.init_available_moving_actions()

    def init_available_placement_actions(self):
        # initialise the dictionary with the available placements on the board
        for row in range(constant.BOARD_SIZE):
            for col in range(constant.BOARD_SIZE):
                piece = col,row
                # print(col,row)
                for colour in (constant.WHITE_PIECE, constant.BLACK_PIECE):
                    if Board.within_starting_area(piece, colour):
                        temp = {piece: constant.PLACEMENT_PHASE}
                        # print(temp)
                        self.available_actions[colour].update(temp)

    def start_available_actions_placement(self):
        # get rid of all pieces that exist on the board
        for colour in (constant.BLACK_PIECE,constant.WHITE_PIECE):
            for piece in self.board.piece_pos[colour]:
                if piece in self.available_actions[colour]:
                    if Board.within_starting_area(piece,colour):
                        self.available_actions[colour].pop(piece)

    def init_available_moving_actions(self):
        for colour in (constant.WHITE_PIECE, constant.BLACK_PIECE):
            for piece in self.board.piece_pos[colour]:
                print(piece)
                self.update_actions_dict_entry(piece, colour)

    # need to ensure that we call this after an update to the minimax board representation
    def update_available_moves(self,action,colour):

        # if there were any eliminated pieces last move retrieve them from the stack -- but make sure not to pop them
        # off the stack completely
        eliminated_pieces = self.board.eliminated_pieces_last_move(self.board.phase,self.board.move_counter,pop=False)

        # action is in the form (position, movetype)
        #       -- i,e. we are moving the piece at position by the movetype
        #       -- when an action is called we have move that piece already and we need to change
        #       -- the entries in the dictionary according to that move
        # colour is the colour of the piece we have moved
        # read in the pieces on the board -- if they already exist in the dictionary
        # then we dont need to do anything -- if they don't exist in the dictionary
        # need to look at all the eliminated pieces on the board
        #   -- look for pieces in the vicinity of that space
        #   -- delete keys associated with those eliminated pieces as these are pieces on the board
        #   -- that do not exists anymore, therefore there are no associated moves with this piece
        #   -- update the available moves of the pieces that can move into that square
        # need to update the available moves of the piece at its new location
        # delete entry in the dictionary that corresponds to the old position
        old_pos = action[0]
        print(old_pos)
        print(action)
        new_pos = Board.convert_move_type_to_coord(old_pos, action[1])

        # first we need to update the dictionary by removing the old piece from the
        # dictionary -- as this is not an available move anymore
        if old_pos in self.available_actions[colour]:
            print("old")
            self.available_actions[colour].pop(old_pos)
        else:
            pass
            # need to raise an error saying

        # then add an entry into the dictionary corresponding to the new location of the piece
        # after the move has been applied
        if new_pos not in self.available_actions[colour]:
            self.update_actions_dict_entry(new_pos, colour)
        else:
            pass
            # need to raise an error

        # remove all eliminated pieces from the dictionary
        for piece_type in (constant.WHITE_PIECE, constant.BLACK_PIECE):
            for piece in eliminated_pieces[piece_type]:
                if piece in self.available_actions[piece_type]:
                    self.available_actions[piece_type].pop(piece)
                else:
                    pass
                    # need to raise an error

        # update any piece that is surrounding the old position but also any eliminated pieces and update
        # their available moves by adding the corresponding move type to that list
        # this old position is now a free space on the board and therefore pieces are able to now move into it
        # need to test all positions surround this newly freed space and update their available actions
        for move_type in range(constant.MAX_MOVETYPE):
            # iterate through all the possible moves at the old location, checking
            # whether or not there is a piece there
            # if there is a piece at that location we can update that piece's available moves
            piece = Board.convert_move_type_to_coord(old_pos,move_type)
            for piece_colour in (constant.WHITE_PIECE, constant.BLACK_PIECE):
                if piece in self.available_actions[piece_colour]:
                    if move_type < 4:
                        self.update_actions_dict_entry(piece,piece_colour)
                    else:
                        if self.board.can_jump_into_position(old_pos,move_type):
                            self.update_actions_dict_entry(piece,piece_colour)

            # update the pieces around any eliminated pieces
            for piece_colour in (constant.WHITE_PIECE, constant.BLACK_PIECE):
                # iterate through all the eliminated pieces on the board
                for elim_piece in eliminated_pieces[piece_colour]:
                    # for each eliminated piece we apply a move (move_type to it), checking if there is a piece
                    # at this position on the board, we do this by checking the available moves dictionary
                    # if there is a piece associated with that position on the board then if it is a one step move
                    # we just need to update that pieces available moves, if it is a jump, then we need to test if there
                    # is an adjacent piece between the jump and the free space -- do this by calling
                    # can_jump_into_position -- for a given space, if we apply a move_type corresponding to a
                    # two piece move, can we jump into this free spot
                    # if we can then we just need to update this pieces available actions

                    piece = Board.convert_move_type_to_coord(elim_piece,move_type)
                    '''
                    # if this piece corresponds to an entry in the dictionary, then there is a piece at this location
                    if piece in self.available_actions[piece_colour]:
                        # one step moves
                        if move_type < 4:
                            self.update_actions_dict_entry(piece,piece_colour)
                        else:
                            # need to check if a jump is available into the free space
                            # if the piece at the jump location is in the available_action dict
                            if self.board.can_jump_into_position(elim_piece,move_type):
                                self.update_actions_dict_entry(piece,piece_colour)
                    '''
                    self.update_surrounding_pieces(piece)
            # update the available moves of the pieces that surround where the
            # new position of the piece is -- this is no longer an occupied space therefore pieces surrounding
            # it cannot move into this space anymore
            piece = Board.convert_move_type_to_coord(new_pos,move_type)
            for piece_colour in (constant.WHITE_PIECE, constant.BLACK_PIECE):
                if piece in self.available_actions[piece_colour]:
                    '''
                    if move_type < 4:
                        self.update_actions_dict_entry(piece,piece_colour)
                    else:
                        # treat this old position as a free space -- if there are pieces
                        # that can jump into this piece we have to update these pieces available
                        # actions because this space is no longer free
                        if self.board.can_jump_into_position(new_pos,move_type):
                            self.update_actions_dict_entry(piece,piece_colour)
                    '''
                    self.update_surrounding_pieces(piece)

    # HELPER METHOD THAT ALLOWS TO UPDATE A PARTICULAR PIECES AVAILABLE ACTIONS IN THE DICTIONARY
    def update_actions_dict_entry(self,piece,colour):
        temp_list = self.get_piece_legal_moves(piece)
        update_entry = {piece: temp_list}
        self.available_actions[colour].update(update_entry)

    # get a list of the legal moves of a particular piece
    def get_piece_legal_moves(self,piece):
        available_moves = []
        for move_type in range(constant.MAX_MOVETYPE):
            if self.board.is_legal_move(piece, move_type):
                available_moves.append(move_type)
        print(available_moves)
        return available_moves

    def update_available_placement(self, action):
        # to update the available actions in the placement phase we just need to read in the action made
        # remove this entry from the dictionary
        # add the entries of any eliminated positions in the dictionary

        elim = []
        eliminated_pieces = self.board.eliminated_pieces_last_move(self.board.phase,self.board.move_counter,pop=False)
        print("ELIMINATED: ",end='')
        print(eliminated_pieces)
        print("AVAILABLE: ",end='')
        print(self.available_actions)
        for colour in (constant.WHITE_PIECE, constant.BLACK_PIECE):
            if Board.within_starting_area(action, colour):
                # remove the action from the entry of the dictionary
                if action in self.available_actions[colour]:
                    self.available_actions[colour].pop(action)
            # add all the eliminated pieces to the available moves of the dictionary
            for piece in eliminated_pieces[colour]:
                elim.append(piece)

        for colour in (constant.WHITE_PIECE, constant.BLACK_PIECE):
            for piece in elim:
                if Board.within_starting_area(piece, colour):
                    update_entry = {piece: constant.PLACEMENT_PHASE}
                    self.available_actions[colour].update(update_entry)

    def update_available_actions(self,action, colour):
        if self.board.phase == constant.PLACEMENT_PHASE:
            self.update_available_placement(action)
        elif self.board.phase == constant.MOVING_PHASE:
            self.update_available_moves(action,colour)

    # return a list of actions corresponding to a particular board state
    def get_actions(self,colour):
        actions = []
        if self.board.phase == constant.PLACEMENT_PHASE:
            for key in self.available_actions[colour].keys():
                # return a list containing the free spaces on the board that a player can place a piece into
                actions.append(key)

            return actions
        elif self.board.phase == constant.MOVING_PHASE:

            for key in self.available_actions[colour].keys():
                for move_type in self.available_actions[colour][key]:
                    # return a list of the piece_position and the move it can make
                    actions.append((key,move_type))
            return actions

    '''
    This method is only called after an undo_move call -- this is because undo move will set the pieces_effected_undo 
    attribute to being a list 
    
    This list will contain all pieces that have been effected when the undo move is called 
    Therefore when we are restoring the available actions lists after the undo_move call, we just need to 
    update the entries that have been affected by the undo move 
    
    pieces that have been effected by an undo move are: 
        - any eliminated piece -- this position is now a free space on the board 
            - therefore after an undo call is made -- these pieces should now be placed back onto the available actions list 
        - The list is in the form (action, colour, undo_type)
            - Undo type tells us what type of piece has been effected by an undo -- and what was that location of the 
              board before an undo 
                - constant.PLACE_LOC -- we have placed a piece here, therefore to establish the old state,
                  when we called undo move, we got rid of this piece from this board, thus to reestablish the old available
                  moves we just need to add this position (if valid) into the dictionary of the pieces 
                  
                - constant.ELIMINATED_LOC -- a piece has been eliminated at this location previously, therefore when we undo
                  a move, this piece is now occupied again. Therefore we need to update the pieces that surround it (if in 
                  the moving phase) or remove this piece from the dictionary if we are in the placement phase. 
                  
                - constant.PIECE_OLD_LOC -- relates to the moving phase: we have moved a piece from this position to a new 
                  position therefore in the original available actions list, this action should be removed from the dictionary
                  and we need to update any pieces that surround this piece 
                  
                - constant.PIECE_NEW_LOC -- this relates to the moving phase: we have moved a piece from an old location to
                  this location, therefore this position should not exist in the old dictionary, thus we need to add it back
                  to the old dictionary and update any surrounding pieces 
    
    considering the edge cases -- 
        - shrinking corners: this should already be handled by the undo_move function 
            - all pieces that have been eliminated due to a shrink should be in the effected list
        - PLACEMENT->MOVING transition 
            - treat the effected pieces as placement phase pieces -- might be worth just revaluating the board completely 
            here 
            - when we are undoing a change from moving to placement phase -- undo already changes the phase and moving counter
              so this should not be an issue 
    '''

    def undo_available_placement(self):
        # we just need to pop each piece from the undo_moves effected pieces
        while len(self.undo_effected) > 0:
            action = self.undo_effected.pop()
            print("POP")
            print(action)
            loc = action[0]
            print(loc)
            colour = action[1]
            undo_type = action[2]
            opponent = Board.get_opp_piece_type(colour)

            if undo_type == constant.ELIMINATED_PIECE:
                # this piece was eliminated before the undo move, now we have placed it back on the board with undo
                if loc in self.available_actions[colour]:
                    # remove the action from the dictionary of the corresponding colour
                    self.available_actions[colour].pop(loc)
                if loc in self.available_actions[opponent]:
                    self.available_actions[opponent].pop(loc)

            elif undo_type == constant.PLACE_LOC:
                # a piece was was placed at this location at prior to calling undo move
                # therefore to reestablish the original available moves list, then we need to add
                # this piece to the corresponding dict
                if loc not in self.available_actions[colour] and loc not in\
                        self.available_actions[opponent]:
                    # if we can place a piece at this location again -- then this piece corresponds to a free space
                    if self.board.within_starting_area(loc, colour):
                        temp = {loc: constant.PLACEMENT_PHASE}
                        self.available_actions[colour].update(temp)

                    if self.board.within_starting_area(loc,opponent):
                        temp = {loc: constant.PLACEMENT_PHASE}
                        self.available_actions[opponent].update(temp)

    def undo_available_moves(self):

        for tup in self.undo_effected:
            print(tup)
            loc = tup[0]
            colour = tup[1]
            undo_type = tup[2]

            # get rid of relevent entries in the dictionary
            if undo_type == constant.PIECE_OLD_LOC:
                # if it is an old location it currently does not exist in the dictionary since it was deleted when
                # it was updated
                # add it back
                self.update_actions_dict_entry(loc,colour)
                self.update_surrounding_pieces(loc)
            elif undo_type == constant.PIECE_NEW_LOC:
                print(loc)
                # if it is a new location it currently exists in the dictionary, and we must remove it
                if loc in self.available_actions[colour]:
                    self.available_actions[colour].pop(loc)
                    self.update_surrounding_pieces(loc)
            elif undo_type == constant.ELIMINATED_PIECE:
                # if there were eliminated pieces that were put back onto the board in the undo move -- then these
                # pieces would not exist in the current available move dictionary
                self.update_actions_dict_entry(loc,colour)
                self.update_surrounding_pieces(loc)

        # clear the undo-effected list
        self.undo_effected = []

    # given a center_position -- update the pieces that surround that centre position if they exist
    def update_surrounding_pieces(self,center_pos):
        for move_type in range(constant.MAX_MOVETYPE):
            potential_piece = Board.convert_move_type_to_coord(center_pos,move_type)

            # check if the potential piece is a piece
            if potential_piece in self.available_actions[constant.WHITE_PIECE]:
                # then it is a piece on the board
                # update this piece
                self.update_actions_dict_entry(potential_piece,constant.WHITE_PIECE)
            elif potential_piece in self.available_actions[constant.BLACK_PIECE]:
                self.update_actions_dict_entry(potential_piece,constant.BLACK_PIECE)

    def restore_available_actions(self):
        if self.board.phase == constant.PLACEMENT_PHASE:
            self.undo_available_placement()
        elif self.board.phase == constant.MOVING_PHASE:
            self.undo_available_moves()

