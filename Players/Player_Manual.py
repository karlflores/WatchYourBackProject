from Constants import constant
from WatchYourBack.Board import Board
from ErrorHandling.Errors import *

class Player:

    def __init__(self, colour):
        if colour == 'white':
            self.colour = constant.WHITE_PIECE
        elif colour == 'black':
            self.colour = constant.BLACK_PIECE

        # each players internal board representation
        self.board = Board()

        self.opponent = self.board.get_opp_piece_type(self.colour)

    def update(self, action):

        # update the board based on the action of the opponent
        # get move type
        if self.board.phase == constant.PLACEMENT_PHASE:
            self.board.update_board(action, self.opponent)

        elif self.board.phase == constant.MOVING_PHASE:
            if isinstance(action[0],tuple) is False:
                raise InvalidAction

            direction = self.board.convert_coord_to_direction(action[0], action[1])
            self.board.update_board((action[0], direction), self.opponent)

    def action(self, turns):
        available_actions = self.board.update_actions(self.colour)
        available_actions.sort()

        for i,action in enumerate(available_actions):
            print(str(i) + " : " + str(action))

        print("+"*50)
        index = int(input("Enter move for {}: ".format(self.colour)))
        next_move = available_actions[index]
        print("+" * 50)

        print(self.board.move_counter)
        if self.board.phase == constant.PLACEMENT_PHASE:

            # making moves during the placement phase
            self.board.update_board(next_move, self.colour)
            return next_move
        else:
            new_pos = self.board.convert_direction_to_coord(next_move[0],next_move[1])
            # making moves during the placement phase
            self.board.update_board(next_move, self.colour)
            return next_move[0], new_pos