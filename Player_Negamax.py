from Constants import constant
from WatchYourBack.Board import Board
from Agents.NegamaxTranspositionTable import Negamax
from ActionBook.ActionBook import ActionBook

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
        self.minimax = Negamax(self.board, self.colour)

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