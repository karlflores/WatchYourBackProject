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

    def __init__(self):
        # we want to create a node
        self.visited = set()

    '''
    * Alpha Beta - Minimax Driver Function 
    '''

    def alpha_beta_minimax(self,depth,root):
        self.visited = set()
        # print the available mvoes of the alpha beta call
        #print(root.available_moves)

        #print("*"*20)
        #root.board.print_board()
        #print("*"*20)
        # generate the child nodes of the root node and run minimax  on these
        # nodes -- choose the node that has the best value
        # initially the best move has not been found
        # essentially we just need to do a min search on the child nodes
        # of the root -- do this week alpha-beta pruning

        best_move = None
        alpha = -inf
        beta = inf
        child_nodes = []
        for action in root.available_moves:
            child_nodes.append(Minimax.create_node(root.board, Board.get_opp_piece_type(root.colour),action))

        child_nodes.sort(reverse=False)

        for child in child_nodes:
            # if there is a symmetry of the board state that matches a visited state
            # then we can skip this node -- don't need to explore it anymore
            if self.check_symmetry(child.board.board_state) is True:
                continue

            evaluate = self.min_value(child,depth-1,alpha,beta)

            if evaluate > alpha:
                best_move = child.move_applied
                alpha = evaluate

            if beta < alpha:
                break

        return best_move

        # find the action associated with eval

    def max_value(self,node, depth, alpha, beta):
        evaluate = -inf
        if Minimax.cutoff_test(node,depth):
            return Minimax.evaluate_node(node)

        # visit each available move
        # print(node.available_moves)
        child_nodes = []
        for action in node.available_moves:
            child_nodes.append(Minimax.create_node(node.board, Board.get_opp_piece_type(node.colour),action))

        child_nodes.sort(reverse=False)
        for child in child_nodes:

            #if self.check_symmetry(child.board.board_state) is True:
                #continue
            # make a new node for each available node -- this child is now the opposite colour
            # child = Minimax.create_node(node.board, Board.get_opp_piece_type(node.colour), action)

            # get the minimax value for this node
            evaluate = max(evaluate, self.min_value(child, depth-1, alpha, beta))

            alpha = max(evaluate,alpha)
            if alpha >= beta:
                break

        node.minimax = evaluate
        return evaluate

    def min_value(self,node, depth, alpha, beta):
        # beginning evaluation value
        evaluate = inf

        if Minimax.cutoff_test(node, depth):
            return Minimax.evaluate_node(node)

        # print(node.available_moves)
        child_nodes = []

        for action in node.available_moves:
            # apply the move to the child node, this node is now the opposite colour
            child_nodes.append(Minimax.create_node(node.board, Board.get_opp_piece_type(node.colour), action))

        child_nodes.sort(reverse=True)
        for child in child_nodes:
            # need to check if this is valid -- skip over all previously visied symmetric nodes
            #if self.check_symmetry(child.board.board_state) is True:
            #    print("xxxxxx")
            #    continue
            evaluate = min(evaluate, self.max_value(child, depth-1, alpha, beta))

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
        node.move_applied = move
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

    def check_symmetry(self,board_state):

        transformation = Minimax.apply_horizontal_reflection(board_state)
        board = deepcopy(board_state)
        if transformation.decode("utf-8") in self.visited:
            return True
        else:
            self.visited.add(board.decode("utf-8"))
            return False

    @staticmethod
    def apply_horizontal_reflection(board_state):
        temp = ''
        for index in range(constant.BOARD_SIZE**2):
            temp+=constant.FREE_SPACE

        temp = bytearray(temp,'utf-8')

        for row in range(constant.BOARD_SIZE):
            for col in range(constant.BOARD_SIZE):
                Board.set_array_char(temp,7-row,7-col,
                                     Board.get_array_element(board_state,row,col))
        #print(temp)
        #print(board_state)
        return temp