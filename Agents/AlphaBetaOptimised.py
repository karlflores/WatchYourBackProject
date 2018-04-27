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

class MinimaxABOptimised(object):

    def __init__(self, board):
        # we want to create a node

        self.transposition_table = set()

        # only use this board to complete the search
        # save memory
        self.board = deepcopy(board)

        # test the dictionary for the available moves
        # each piece has their available able
        self.available_actions = {constant.WHITE_PIECE: {}, constant.BLACK_PIECE: {}}
        # initialise the available actions
        self.init_available_placement_actions()
        # print(self.available_actions)

        # for alpha beta search -- instead of passing it into the function calls we can use this
        self.alpha = -inf
        self.beta = inf

        # defines the colours of min and max
        self.player = constant.WHITE_PIECE
        self.opponent = Board.get_opp_piece_type(self.player)

        # default depth
        self.depth = inf

    '''
    * Alpha Beta - Minimax Driver Function 
    '''

    def iterative_deepening_alpha_beta(self, root):
        MAX_ITER = 20

        # default policy
        if len(root.available_moves) == 0:
            return None
        else:
            move = root.available_moves[0]

        # time allocated per move in ms
        time_alloc = 1000

        # get time
        start_time = MinimaxAB.curr_millisecond_time()

        # iterative deepening begins here
        for depth in range(1, MAX_ITER):
            print(depth)
            move = self.alpha_beta_minimax(depth, root)
            sleep(0.05)

            if MinimaxAB.curr_millisecond_time() - start_time > time_alloc:
                break
        return move

    @staticmethod
    def curr_millisecond_time():
        return int(time() * 1000)

    def alpha_beta_minimax(self, depth):
        if self.board.phase == constant.MOVING_PHASE and self.board.move_counter == 0:
            self.min_value.cache_clear()
        # print the available mvoes of the alpha beta call
        # print(root.available_moves)
        # generate the child nodes of the root node and run minimax  on these
        # nodes -- choose the node that has the best value
        # initially the best move has not been found
        # essentially we just need to do a min search on the child nodes
        # of the root -- do this week alpha-beta pruning

        best_move = None
        alpha = -inf
        evaluate = -inf
        beta = inf

        # update the minimax depth counter
        self.depth = depth


        i = 0
        # get the available moves of the board (based on the current board representation)
        # we can generate the actions as we wish -- this can easily change -- TODO : OPTIMISATION/ PRUNING OF ACTION __ CAN BE GREEDY __ favoured moves and unfavoured moves
        available_actions = self.board.update_actions(self.board, self.player)


        for action in available_actions:
            # print("{} Action AB call".format(i))
            # update the minimax board representation with the action
            self.board.update_board(action, self.player)

            board_string = self.board.board_state.decode("utf-8")
            '''
            if self.board.phase == constant.PLACEMENT_PHASE:
                if TranspositionTable.check_placement_sym(self.transposition_table,self.board.board_state) is True:
                    continue
            elif self.board.phase == constant.MOVING_PHASE:
                if TranspositionTable.check_already_visited(self.transposition_table, self.board.board_state):
                    continue
            '''
            # decrease the depth counter
            self.depth -= 1

            ab_evaluate = self.min_value(board_string, self.opponent, self.board.phase)
            # print(ab_evaluate)
            # print(self.min_value.cache_info())

            if ab_evaluate > evaluate:
                best_move = action
                evaluate = ab_evaluate

            self.undo_move()
            self.depth += 1

            if evaluate >= beta:
                # print(evaluate)
                # print("AB Best Value: ",end='')
                # rint(evaluate, best_move)
                return best_move

            alpha = max(alpha, evaluate)

        # print(best_move)
        # print(evaluate)
        # print("AB Best Value: ",end='')
        # print(evaluate, best_move)
        return best_move

    # memoize the function call -- opitimisation
    # @lru_cache(maxsize=100000)
    def max_value(self,board_string, colour, phase):

        evaluate = -inf

        if self.cutoff_test(self.depth):
            return self.evaluate_state(self.board,colour)

        # visit each available move
        available_actions = self.board.update_actions(self.board, colour)

        for action in available_actions:

            # update the board representation with the move
            self.board.update_board(action, colour)
            self.depth -= 1
            # create an immutable object for board_string such that we can call lru_cache on the max function call
            board_string = self.board.board_state.decode("utf-8")

            # get the minimax value for this state

            evaluate = max(evaluate, self.min_value(board_string, self.opponent, self.board.phase))
            # print(self.board.action_applied)

            # undo the move so that we can apply another action
            self.undo_move()
            self.depth += 1

            if evaluate >= self.beta:
                return evaluate

            self.alpha = max(evaluate, self.alpha)

        return evaluate

    # memoize the min value results -- optimisation of its function call
    @lru_cache(maxsize=10000)
    def min_value(self, board_string, colour, phase):
        # print("CALLED MIN")
        # beginning evaluation value
        evaluate = inf

        if self.cutoff_test(self.depth):
            # val = self.evaluate_node(node)
            # print("MIN NODE VAL: ",end='')
            # print(val)
            # return val
            # print(self.evaluate_node(node))
            return self.evaluate_state(self.board,colour)
        # print("MIN MOVES: ",end='')
        # print(node.available_moves)

        # generate the actions to search on
        available_actions = self.board.update_actions(self.board, colour)

        for action in available_actions:

            # update the board representation -- this action is the min nodes's action
            self.board.update_board(action, colour)
            # when we apply a move we do down a level so we have to decrease depth
            self.depth -= 1

            board_string = self.board.board_state.decode("utf-8")

            # find the value of the max node
            evaluate = min(evaluate, self.max_value(board_string, self.player, self.board.phase))

            # undo the board move so that we can apply another move
            # -- we also go up a level therefore we need to increment depth
            self.undo_move()
            self.depth += 1

            '''
            if beta <= alpha:
                # when we break from the loop make sure to undo the move
                break
            '''

            if evaluate <= self.alpha:

                # print("MIN Best Value: ",end='')
                # print(evaluate)
                return evaluate

            self.beta = min(self.beta, evaluate)

        return evaluate

    def update_minimax_board(self, move, node, start_node=False):

        # if the move is None -- this could be a forfeit of a move or it could be a start of a search
        # apply this move to the node

        if move is not None:
            self.board.update_board(move, Board.get_opp_piece_type(node.colour))
        elif move is None and self.board.move_counter is not 0:
            # if the move is none and the counter is not zero this is a forfeit
            self.board.move_counter += 1
            self.board.set_player_to_move(self.board.get_opp_piece_type(self.board.player_to_move))

        # update minimax board represents the start of the minimax search then we need to initalise
        # the available moves
        # print("Move is None: WTFFFFFFF")

        # get the available moves based on what phase the board is in
        '''
        if self.board.phase == constant.PLACEMENT_PHASE and self.board.move_counter == 24:
            self.board.phase = constant.MOVING_PHASE
            self.board.move_counter = 0
        '''
        # print(self.board.phase,self.board.move_counter)

        if self.board.phase == constant.PLACEMENT_PHASE:
            self.update_available_nodes_placement(node)
            # if the move is none then we need to initalise the available moves of the board
            '''
            if move is None and start_node is True:
                # then this is the first node in the search -- initialise the placement actions
                if self.board.move_counter == 0 or self.board.move_counter == 1:
                    self.start_available_actions_placement()
                    return
            elif start_node is False:
                # this is a start node but a move has been applied, therefore we just need to update the available
                # moves list
                #print(move)
                self.update_available_placement(move)
                #print(self.available_actions)
                return
            '''
        elif self.board.phase == constant.MOVING_PHASE:
            # generate the moves that you can apply to this node
            node.available_moves = self.generate_moves(node.colour)
            # this is the start to the search -- we don't want to update the available_moves list
            '''
            if start_node is True and move is None:
                # if it is the start to the moving phase -- need to initialise
                self.init_available_moving_actions()
                return

            elif start_node is False:
                self.update_available_moves(move, node.colour)
                return
            '''

    def generate_moves(self, colour):
        available_moves = []
        if self.board.phase == constant.MOVING_PHASE:
            for move in self.board.piece_pos[colour]:
                for move_type in range(constant.MAX_MOVETYPE):
                    if self.board.is_legal_move(move, move_type):
                        available_moves.append((move, move_type))
        return available_moves

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
    @staticmethod
    def evaluate_state(board, colour):
        return Evaluation.basic_policy(board, colour)

    # update the available moves of the search algorithm after it has been instantiated
    #
    # def update_available_moves(self, node, available_moves):
    #    node.available_moves = available_moves

    def update_board(self, board):
        self.board = deepcopy(board)


    def is_terminal(self):
        return self.board.is_terminal()

    def update_available_nodes_placement(self, node):
        MinimaxABUndo.init_placable_area(node)

        for colour in (constant.BLACK_PIECE, constant.WHITE_PIECE):
            for piece in self.board.piece_pos[colour]:
                if piece in node.available_moves:
                    node.available_moves.remove(piece)

    @staticmethod
    def init_placable_area(node):
        node.available_moves = []
        for row in range(constant.BOARD_SIZE):
            for col in range(constant.BOARD_SIZE):
                if Board.within_starting_area((col, row), node.colour):
                    node.available_moves.append((col, row))

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
        self.board.undo_move()
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
            self.init_available_moving_actions()

    def init_available_placement_actions(self):
        # initialise the dictionary with the available placements on the board
        for row in range(constant.BOARD_SIZE):
            for col in range(constant.BOARD_SIZE):
                piece = col, row
                # print(col,row)
                for colour in (constant.WHITE_PIECE, constant.BLACK_PIECE):
                    if Board.within_starting_area(piece, colour):
                        temp = {piece: constant.PLACEMENT_PHASE}
                        # print(temp)
                        self.available_actions[colour].update(temp)

    def start_available_actions_placement(self):
        # get rid of all pieces that exist on the board
        for colour in (constant.BLACK_PIECE, constant.WHITE_PIECE):
            for piece in self.board.piece_pos[colour]:
                if piece in self.available_actions[colour]:
                    if Board.within_starting_area(piece, colour):
                        self.available_actions[colour].pop(piece)

    def init_available_moving_actions(self):
        for colour in (constant.WHITE_PIECE, constant.BLACK_PIECE):
            for piece in self.available_actions[colour].keys():
                self.update_actions_dict_entry(piece, colour)

    # need to ensure that we call this after an update to the minimax board representation
    def update_available_moves(self, action, colour):

        # if there were any eliminated pieces last move retrieve them from the stack -- but make sure not to pop them
        # off the stack completely
        eliminated_pieces = self.board.eliminated_pieces_last_move(self.board.phase, self.board.move_counter, pop=False)

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
            self.available_actions[colour].pop(old_pos)
        else:
            pass
            # need to raise an error saying

        # then add an entry into the dictionary corresponding to the new location of the piece
        # after the move has been applied
        if new_pos not in self.available_actions[colour]:
            temp_list = self.get_piece_legal_moves(new_pos)
            temp_dict = {new_pos: temp_list}
            self.available_actions.update(temp_dict)
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
            piece = Board.convert_move_type_to_coord(old_pos, move_type)
            for piece_colour in (constant.WHITE_PIECE, constant.BLACK_PIECE):
                if piece in self.available_actions[piece_colour]:
                    if move_type < 4:
                        self.update_actions_dict_entry(piece, piece_colour)
                    else:
                        if self.board.can_jump_into_position(old_pos, move_type):
                            self.update_actions_dict_entry(piece, piece_colour)

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
                    piece = Board.convert_move_type_to_coord(elim_piece, move_type)
                    # if this piece corresponds to an entry in the dictionary, then there is a piece at this location
                    if piece in self.available_actions[piece_colour]:
                        # one step moves
                        if move_type < 4:
                            self.update_actions_dict_entry(piece, piece_colour)
                        else:
                            # need to check if a jump is available into the free space
                            # if the piece at the jump location is in the available_action dict
                            if self.board.can_jump_into_position(elim_piece, move_type):
                                self.update_actions_dict_entry(piece, piece_colour)

            # update the available moves of the pieces that surround where the
            # new position of the piece is -- this is no longer an occupied space therefore pieces surrounding
            # it cannot move into this space anymore
            piece = Board.convert_move_type_to_coord(new_pos, move_type)
            for piece_colour in (constant.WHITE_PIECE, constant.BLACK_PIECE):
                if piece in self.available_actions[piece_colour]:
                    if move_type < 4:
                        self.update_actions_dict_entry(piece, piece_colour)
                    else:
                        # treat this old position as a free space -- if there are pieces
                        # that can jump into this piece we have to update these pieces available
                        # actions because this space is no longer free
                        if self.board.can_jump_into_position(new_pos, move_type):
                            self.update_actions_dict_entry(piece, piece_colour)

    # HELPER METHOD THAT ALLOWS TO UPDATE A PARTICULAR PIECES AVAILABLE ACTIONS IN THE DICTIONARY
    def update_actions_dict_entry(self, piece, colour):
        temp_list = self.get_piece_legal_moves(piece)
        update_entry = {piece: temp_list}
        self.available_actions[colour].update(update_entry)

    # get a list of the legal moves of a particular piece
    def get_piece_legal_moves(self, piece):
        available_moves = []
        for move_type in range(constant.MAX_MOVETYPE):
            if self.board.is_legal_move(piece, move_type):
                available_moves.append(move_type)

        return available_moves

    def update_available_placement(self, action):
        # to update the available actions in the placement phase we just need to read in the action made
        # remove this entry from the dictionary
        # add the entries of any eliminated positions in the dictionary
        eliminated_pieces = self.board.eliminated_pieces_last_move(self.board.phase, self.board.move_counter, pop=False)
        print("ELIMINATED: ", end='')
        print(eliminated_pieces)
        print("AVAILABLE: ", end='')
        print(self.available_actions)
        for colour in (constant.WHITE_PIECE, constant.BLACK_PIECE):
            if Board.within_starting_area(action, colour):
                # remove the action from the entry of the dictionary
                if action in self.available_actions[colour]:
                    self.available_actions[colour].pop(action)

            # add all the eliminated pieces to the available moves of the dictionary
            for piece in eliminated_pieces[colour]:
                if Board.within_starting_area(piece, colour):
                    if piece not in self.available_actions[colour]:
                        update_entry = {piece: constant.PLACEMENT_PHASE}
                        self.available_actions[colour].update(update_entry)

    # return a list of actions corresponding to a particular board state
    def get_actions(self, colour):
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
                    actions.append((key, move_type))
            return actions
