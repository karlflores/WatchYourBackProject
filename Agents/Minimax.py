'''
* Implements the mini-max algorithm based on the minimax_mode structure
* and the player file
'''
from math import inf
from Agents.Minimax_Node import Node
from Board.Board import constant
from Board.Board import Board
from Evaluation.Policies import Evaluation
from copy import deepcopy


class Minimax(object):

    def __init__(self,board,available_moves,colour):
        # we want to create a node
        self.node = Minimax.create_node(board,colour,None)
        self.depth = 0
        self.best_move = None
        self.iteration = 0

        self.node.available_moves = available_moves

    @staticmethod
    def alpha_beta_minimax(depth,root):
        evaluate = -inf
        best_move = None
        best_eval = inf
        alpha = -inf
        beta = inf
        # print the available mvoes of the alpha beta call
        #print(root.available_moves)

        #print("*"*20)
        #root.board.print_board()
        #print("*"*20)
        # generate the child nodes of the root node and run minimax  on these
        # nodes -- choose the node that has the best value
        # initially the best move has not been found

        # minimax_val = Minimax.max_value(root,depth,alpha,beta)

        #print("MINIMAX VALUE IS: " + str(minimax_val))
        #print()
        for action in root.available_moves:
            '''
            #print(action)
            # create a child node based on these available moves

            child = Minimax.create_node(root.board, Board.get_opp_piece_type(root.colour),action)
            evaluate = min(evaluate,Minimax.min_value(child,depth-1,-alpha,beta))

            # need to find the maximum of all min values
            if evaluate > best_eval:
                best_move = action
                best_eval = evaluate

            if best_eval >= beta:
                return best_move
            # find the node that equates to the minimax value found and return this
            # this is the best move according to the algorithm
            # print(Minimax.evaluate_node(child))
            alpha = max(best_eval, alpha)
            '''
        return best_move

        # find the action associated with eval


    @staticmethod
    def max_value(node, depth, alpha, beta):
        evaluate = -inf
        if Minimax.cutoff_test(node,depth):
            return Minimax.evaluate_node(node)

        # visit each available move
        # print(node.available_moves)
        for action in node.available_moves:
            # make a new node for each available node -- this child is now the opposite colour
            child = Minimax.create_node(node.board, Board.get_opp_piece_type(node.colour), action)

            # get the minimax value for this node
            evaluate = max(evaluate, Minimax.min_value(child, depth-1, alpha, beta))

            alpha = max(evaluate,alpha)
            if alpha >= beta:
                break

        node.minimax = evaluate
        return evaluate

    @staticmethod
    def min_value(node, depth, alpha, beta):
        # beginning evaluation value
        evaluate = inf

        if Minimax.cutoff_test(node, depth):
            return Minimax.evaluate_node(node)

        # print(node.available_moves)
        for action in node.available_moves:
            # apply the move to the child node, this node is now the opposite colour
            child = Minimax.create_node(node.board, Board.get_opp_piece_type(node.colour), action)
            evaluate = min(evaluate, Minimax.max_value(child, depth-1, alpha, beta))

            beta = min(beta, evaluate)

            if beta <= alpha:
                break

        node.minimax = evaluate
        return evaluate

    @staticmethod
    def create_node(board,colour,move):
        # colour is the colour this player with the move from the previous player applied
        # therefore move is the opposite colour player

        # create a new node object based on the board
        node = Node(board,colour)
        if node is None:
            return None

        eliminated = []
        # apply this move to the node
        if move is not None:
            eliminated = node.board.update_board(move, Board.get_opp_piece_type(colour))
        else:
            pass
            #print("Move is None: WTFFFFFFF")

        # get the available moves based on what phase the board is in

        if node.board.phase == constant.PLACEMENT_PHASE and node.board.move_counter == 24:
            node.board.phase = constant.MOVING_PHASE
            node.board.move_counter = 0

        if node.board.phase == constant.PLACEMENT_PHASE:
            '''
            if len(node.available_moves) == 0:
                # then we have not began the game yet --
                for row in range(constant.BOARD_SIZE):
                    for col in range(constant.BOARD_SIZE):
                        # iterate through all the positions on the board and check if
                        # this poistion is within the starting move of the colour piece
                        if Board.within_starting_area((col,row),node.colour):
                            node.available_moves.append((col,row))
            else:
                # we can just remove the move from the available moves list for that node
                node.available_moves.remove(move)
                print("-"*50)
                print(node.available_moves)
                print("-"*50)
                # add the places to available moves of pieces that have been eliminated due to the
                # piece placement
                for piece in eliminated and eliminated is not None:
                    # check if this piece is within the starting area
                    if Board.within_starting_area(piece, colour):
                        node.available_moves.append(piece)
            '''
            Minimax.update_available_nodes_placement(node)

        elif node.board.phase == constant.MOVING_PHASE:
            if node.board.move_counter == 24:
                node.available_moves = []
            # generate the moves that you can apply to this node
            node.available_moves = Minimax.generate_moves(node, colour)

        return node

    @staticmethod
    def generate_moves(node,colour):
        available_moves = []
        if node.board.phase == constant.MOVING_PHASE :
            for move in node.board.piece_pos[colour]:
                for move_type in range(constant.MAX_MOVETYPE):
                    if node.board.is_legal_move(move,move_type):
                        available_moves.append((move,move_type))
        return available_moves

    @staticmethod
    def cutoff_test(node, depth):
        if depth == 0:
            return True

        if Minimax.is_terminal(node):
            return True

        return False

    @staticmethod
    def evaluate_node(node):
        return Evaluation.basic_policy(node.board,node.colour)

    # update the available moves of the search algorithm after it has been instantiated
    def update_available_moves(self, available_moves):
        self.node.available_moves = available_moves

    def update_board(self, board):
        self.node.board = deepcopy(board)

    @staticmethod
    def is_terminal(node):
        return node.is_leaf()

    @staticmethod
    def update_available_nodes_placement(node):
        Minimax.init_placable_area(node)

        for colour in (constant.BLACK_PIECE,constant.WHITE_PIECE):
            for piece in node.board.piece_pos[colour]:
                if piece in node.available_moves:
                    node.available_moves.remove(piece)

    @staticmethod
    def init_placable_area(node):
        node.available_moves = []
        for row in range(constant.BOARD_SIZE):
            for col in range(constant.BOARD_SIZE):
                if Board.within_starting_area((col,row),node.colour):
                    node.available_moves.append((col,row))
