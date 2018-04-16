'''
* Implements the mini-max algorithm based on the minimax_mode structure
* and the player file
'''
from math import inf
from Agents.Minimax_Node import Node
from Board.Board import constant
from Board.Board import Board


class Minimax(object):

    def __init__(self,board,available_moves,colour):

        self.node = Minimax.create_node(board,colour,None)
        self.depth = 0
        self.best_move = None
        self.iteration = 0
        self.available_moves = available_moves


    def alpha_beta_minimax(self,depth,root):
        evaluate = self.max_value(root,-inf,inf)

        # find the action associated with eval
        return action


    @staticmethod
    def max_value(node,depth,alpha,beta):
        evaluate = -inf
        if Minimax.cutoff_test(node,depth):
            return node.eval

        # visit each available move
        for action in node.available_moves:

            # make a new node for each available node
            child = Minimax.create_node(node.board,Board.get_opp_piece_type(node.colour),action)

            evaluate = max(evaluate,Minimax.min_value(child,depth-1,alpha,beta))

            if evaluate >=beta:
                return evaluate

            alpha = min(evaluate,alpha)

        return eval

    @staticmethod
    def min_value(node,depth,alpha,beta):
        evaluate = inf

        if Minimax.cutoff_test(node,depth):
            return node.eval

        for action in node.available_moves:
            child = Minimax.create_node(node.board,Board.get_opp_piece_type(node.colour),action)
            evaluate = min(evaluate,Minimax.max_value(child,depth-1,alpha,beta))

            if evaluate <= alpha:
                return evaluate
            beta = min(beta, evaluate)

        return evaluate

    def create_node(board,colour,move):
        node = Node(board,colour)
        if node is None:
            return None

        # apply this move to the node
        if move is not None:
            eliminated = node.board.update_board(move,colour)

        # get the available moves based on what phase the board is in
        if node.board.phase == constant.PLACEMENT_PHASE:
            if len(available_moves) == 0:
                # then we have not began the game yet --

                if colour == constant.WHITE_PIECE:
                    for row in range(constant.BOARD_SIZE-2):
                        for col in range(constant.BLACK_PIECE):
                            if (col, row) not in node.board.piece_pos[colour] or\
                                    (col, row) not in node.board.piece_pos[Board.get_opp_piece_type(colour)] or\
                                    (col, row) not in node.board.corner_pos:
                                node.available_moves.append((col,row))
                elif colour == constant.BLACK_PIECE:
                    for row in range(2,constant.BOARD_SIZE):
                        for col in range(constant.BLACK_PIECE):
                            if (col, row) not in node.board.piece_pos[colour] or \
                                    (col, row) not in node.board.piece_pos[Board.get_opp_piece_type(colour)] or \
                                    (col, row) not in node.board.corner_pos:
                                node.available_moves.append((col,row))
            else:
                # we can just remove the move from the available moves list for that node
                node.available_moves.remove(move)
                # add the places to available moves of pieces that have been eliminated due to the
                # piece placement
                for piece in eliminated:

                    if colour == constant.WHITE_PIECE:
                        min_row = 0
                        max_row = 6
                    elif colour == constant.BLACK_PIECE:
                        min_row = 2
                        max_row = 8
                    col,row = piece

                    if min_row <= row <= max_row and min_col <= col <= max_col:
                        node.available_moves.append(piece)

        elif node.board.phase == constant.MOVING_PHASE:
            # generate the moves that you can apply to this node
            node.available_moves = Minimax.generate_moves(node,colour)

        # apply the evaluation function to this node
        node.evaluate()

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
    def cutoff_test(node,depth):
        if depth == 0:
            return node.eval

        if node.is_leaf():
            return node.eval