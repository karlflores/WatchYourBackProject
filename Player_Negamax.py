from Constants import constant
from WatchYourBack.Board import Board
from Agents.NegamaxTranspositionTable import Negamax
from ActionBook.ActionBook import ActionBook
from random import randint

'''
THIS IS THE FINAL SUBMISSION: 

THIS PLAYER IMPLEMENTS THE FOLLOWING TO INFORM ITSELF ON WHAT MOVE TO MAKE NEXT: 
    - NEGAMAX WITH TRANSPOSITION TABLE AS ITS MAIN SEARCH STRATEGY
    - GREEDY MOVE ORDERING USING A LIGHT EVALUATION FUNCTION AND SELECTION OF THE BEST MOVES TO COMPLETE THE 
      SEARCH ON 
    - MOVE ORDERING USING THE TRANSPOSITION TABLE IN MINIMAX -- WE TRY THE BEST MOVE FOUND SO FAR AT EARLIER 
      DEPTH ITERATIONS FIRST, BECAUSE CHANCES ARE, THIS MOVE MAY BE THE BEST MOVE FOR THE NEXT DEPTH AS WELL 
    - AN OPENING BOOK OF MOVES TO CUT DOWN SEARCH TIME AT THE START OF THE GAME WHERE THERE ARE POSITIONS THAT
      WE SHOULDN'T NEED TO SEARCH ON. 
'''
class Player:

    def __init__(self, colour):
        # set the colour of the player
        if colour == 'white':
            self.colour = constant.WHITE_PIECE
        elif colour == 'black':
            self.colour = constant.BLACK_PIECE

        # each players internal board representation
        self.board = Board()

        # set up the minimax search strategy -- NEGAMAX
        self.minimax = Negamax(self.board, self.colour, "/eval_weights")

        # set the colour of the opponent
        self.opponent = self.board.get_opp_piece_type(self.colour)

        # set up the mini-max return values
        self.depth_eval = 0
        self.minimax_val = 0
        self.policy_vector = 0

        # initialise the action book
        self.action_book = ActionBook(self.colour)

    def update(self, action):
        # update the board based on the action of the opponent
        if self.board.phase == constant.PLACEMENT_PHASE:
            # update board also returns the pieces of the board that will be eliminated
            self.board.update_board(action, self.opponent)
            self.minimax.update_board(self.board)

        elif self.board.phase == constant.MOVING_PHASE:
            if isinstance(action[0], tuple) is False:
                print("ERROR: action is not a tuple")
                return

            # get the "to" square direction using the provided positions
            move_type = self.board.convert_coord_to_direction(action[0], action[1])

            # update the player board representation with the action
            self.board.update_board((action[0], move_type), self.opponent)

    def action(self, turns):

        # update the negamax/minimax board representation
        self.minimax.update_board(self.board)

        # reset the move counter of the board
        if turns == 0 and self.board.phase == constant.MOVING_PHASE:
            self.board.move_counter = 0
            self.board.phase = constant.MOVING_PHASE

        # check the action book to see if there is a state
        board_state = self.board.board_state
        if self.board.phase == constant.PLACEMENT_PHASE:
            action = self.action_book.check_state(board_state)

            if action is not None:
                # return the action found and update the board representations
                self.board.update_board(action, self.colour)
                self.minimax.update_board(self.board)
                return action
            '''
            # if there is no state in the action book we can see if there are any middle squares free
            action = self.get_middle()
            if action is not None:
                # return the action found and update the board representations
                self.board.update_board(action, self.colour)
                self.minimax.update_board(self.board)
                return action
            '''

        # if there is no found state in the action book, therefore we just do a negamax search
        best_move = self.minimax.itr_negamax()

        self.depth_eval = self.minimax.eval_depth
        self.minimax_val = self.minimax.minimax_val

        # do an alpha beta search on this node
        # once we have found the best move we must apply it to the board representation
        if self.board.phase == constant.PLACEMENT_PHASE:
            self.board.update_board(best_move, self.colour)
            self.minimax.update_board(self.board)
            return best_move
        else:
            # if we are in moving phase, return the correctly formatted positions
            if best_move is None:
                return None
            new_pos = Board.convert_direction_to_coord(best_move[0], best_move[1])
            self.board.update_board(best_move, self.colour)
            self.minimax.update_board(self.board)
            return best_move[0], new_pos

    # BOOKLEARNING APPROACH TO GETTING THE MIDDLE PIECES IF POSSIBLE -- THIS IS INSTEAD OF ENUMERATING ALL POSSIBLE
    # BOARD STATES AND ADDING IT TO THE ACTION BOOK

    '''
    TODO -- THIS DOES NOT WORK CORRECTLY 
    
    NEED TO UPDATE IT 
    '''
    def get_middle(self):
        print(self.board.free_squares)
        if self.colour == constant.WHITE_PIECE:
            my_pieces = self.board.white_pieces
            opponent_pieces = self.board.black_pieces
        else:
            my_pieces = self.board.black_pieces
            opponent_pieces = self.board.white_pieces

        # if the middle locations of the board are free and there are no nearby enemy pieces in a one square radius
        # around the middle pieces, we should be taking one of these places
        middle = [(3,3), (4,3), (3,4), (4,4)]
        # check if the middle squares are free
        num_free = 0
        num_close = 0
        for pos in middle:
            print(pos)
            if pos in self.board.free_squares:
                num_free += 1

            # then the middle squares are free, now just need to see if there are any opponent pieces in neighbouring
            # squares to the centre
            for adj in middle:
                # check if there are neighbouring squares in these positions
                for direction in range(4, constant.MAX_MOVETYPE):
                    new_pos = self.board.convert_direction_to_coord(adj, direction)
                    if new_pos in opponent_pieces:
                        num_close += 1

        if num_close == 0 and num_free == 4:
            # if there are no opponent pieces near the middle we can just place our piece in a random location
            # in the middle of the board
            print("This")
            index = randint(0,3)
            print(middle[index])
            print(self.board)
            return middle[index]

        # if we are occupying three of the middle squares and there is a free sqaure, we should just place our
        # piece in the free square
        occupy_middle = 0
        free_index = -1
        for i, pos in enumerate(middle):
            if pos in my_pieces:
                occupy_middle += 1
            elif pos in self.board.free_squares:
                free_index = i
                print(free_index)

        # if we have 3 pieces in the middle and also there is a free square, just return the location
        # of that free square -- this is where we should place our piece
        if occupy_middle == 3 and free_index > -1:
            print(middle[free_index])
            return middle[free_index]

        # if it is not safe to occupy the middle, then don't do it -- we will need to do a minimax search to find
        # out if it is optimal to occupy the middle or not
        return None
