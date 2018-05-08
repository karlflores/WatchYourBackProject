from Constants import constant
from BoardOOP.Piece import Piece
from Error_Handling.Errors import *
from copy import copy


class Board(object):

    # a class to represent the board state of the game
    def __init__(self):

        # key -- the position of the pieces
        # value -- the piece object
        # when we place a piece on the board we update pieces_remaining and we look at any neighbours in a 2 block radius
        # we need to update these pieces neighbour positions to being False -- a
        self.white_pieces = {}
        self.white_eliminate_pieces = []

        self.black_pieces = {}
        self.black_eliminate_pieces = []

        self.free_sqaures = {}

        self.places_remaining = {constant.WHITE_PIECE: 12, constant.BLACK_PIECE: 12}

        # initialise the board representation
        # LT RT LB RB
        self.corner_pos = [(0, 0), (7, 0), (0, 7), (7, 7)]

        # how many moves have been applied to the board so far
        self.move_counter = 0
        self.phase = constant.PLACEMENT_PHASE
        self.num_shrink = 0

        # initially no one wins
        self.winner = None
        self.terminal = False

        # who is moving first
        self.player_to_move = None

        # current size of the board
        self.min_dim = 0
        self.max_dim = constant.BOARD_SIZE-1

        # initialise the board with the corner pieces
        # this dictionary keeps track of the board and the pieces that are currently on the board
        # define the board parameters and constants
        self.board_state = self.init_board_rep()

    @staticmethod
    def init_board_rep():
        # store the board representation as a byte_array length 64 (64bytes)
        # create a temp string of length 64

        # set the corner locations on the board representation

        return bytearray(constant.START_BOARD_STR,"utf-8")

# string_array helper methods
    @staticmethod
    def get_array_element(byte_array,row,col):
        # we assume that the string array is n x n in dimension

        # get the dimension
        dimension = constant.BOARD_SIZE
        # check if row and col are valid
        if row > dimension - 1 or col > dimension - 1:
            return None

        elif row < 0 or col < 0:
            return None
        # get the index to access in the string
        index = row*dimension + col

        # return the char at position index
        return chr(byte_array[index])

    @staticmethod
    def set_array_char(byte_array, row, col, new_char):
        dimension = constant.BOARD_SIZE

        if row > dimension - 1 or col > dimension - 1:
            return
        elif row < 0 or col < 0:
            return

        # set the new char in the string
        # need to turn char into utf-8 encoding first
        byte_array[row * dimension + col] = ord(new_char)

    # return the current size of the board
    def get_min_dim(self):
        return self.min_dim

    def get_max_dim(self):
        return self.max_dim

    # board representation setters and getter methods
    def get_board_piece(self, row, col):
        return self.get_array_element(self.board_state, row, col)

    # change the piece type in the board representation
    def set_board(self, row, col, piece_type):
        piece_types = (constant.CORNER_PIECE, constant.WHITE_PIECE, constant.BLACK_PIECE,
                       constant.FREE_SPACE, constant.INVALID_SPACE)
        # check if the piece_type is valid
        if piece_type not in piece_types:
            return

        # if valid we can set the board position
        self.set_array_char(self.board_state, row, col, piece_type)

    # print board method
    def print_board(self):

        for row in range(constant.BOARD_SIZE):
            for col in range(constant.BOARD_SIZE):
                # get the char to print
                char_index = row * constant.BOARD_SIZE + col

                char = chr(self.board_state[char_index])
                print('{} '.format(char), end='')

            print()

    # when we add a piece back to the board -- this will automatically take care of updating the neighbour
    # therefore move generation should still happen in constant time -- we don't need to test if squares are free
    # or not as this should handle it
    def add_piece(self,pos,colour):
        try:
            new_piece = Piece(pos,colour,self)
            col, row = pos
            new_piece_entry = {pos: new_piece}

            if colour == constant.WHITE_PIECE:
                self.white_pieces.update(new_piece_entry)
                # update the board representation string
                self.set_board(row,col,constant.WHITE_PIECE)
            else:
                self.black_pieces.update(new_piece_entry)
                self.set_board(row,col,constant.BLACK_PIECE)

            # once we add ths piece to the board, we need to update its neighbours
            for direction in range(constant.MAX_MOVETYPE):
                # check if there are any pieces that are occupying nearby squares
                new_pos = self.convert_direction_to_coord(pos,direction)

                # get the direction for the new_position from the old position
                opp_direction = self.get_opposite_direction(direction)

                if new_pos in self.black_pieces:
                    # update this pieces neighbour list
                    piece = self.black_pieces[new_pos]
                    # this space is now occupied therefore set the neighbour to false -- can no longer move here
                    piece.set_neighbour(opp_direction, False)
                elif new_pos in self.white_pieces:
                    piece = self.white_pieces[new_pos]
                    piece.set_neighbour(opp_direction, False)

        except IllegalPlacement:
            print("Illegal Piece Placement... at ({}, {})".format(pos[1],pos[0]))
            return

    # when we want to apply a move to the board -- update the board and the dict associated
    # return the eliminated pieces when we apply a move to the board
    def apply_move(self, pos, direction, colour):
        if colour == constant.WHITE_PIECE:
            my_pieces = self.white_pieces
            opponent_pieces = self.black_pieces
        else:
            my_pieces = self.black_pieces
            opponent_pieces = self.white_pieces

        # get the piece we are trying to move
        try:
            piece = self.get_piece(pos)
        except PieceNotExist:
            print("No piece at this location... ")
            exit(1)

        # check if the move is legal first
        if piece.is_legal_move(direction) is False:
            return

        # we know we can make the move now
        new_pos = self.convert_direction_to_coord(pos, direction)

        new_col, new_row = new_pos
        old_col, old_row = pos

        # update the pieces positoin
        piece.set_position(new_pos)

        # update the pieces neighbours
        piece.set_valid_neighbours()

        # update the neighbours of that piece to False as these pieces can no longer move into this sqaure
        self.update_neighbouring_squares(pos,False)

        # update the board representation
        self.set_board(old_row, old_col, constant.FREE_SPACE)
        self.set_board(new_row, new_col, colour)

        # then we can update the dictionaries
        piece = my_pieces.pop(pos)
        # map it to the new position of the board
        new_piece = {new_pos: piece}
        my_pieces.update(new_piece)

        # now we can test for elimination at the new position on the board
        eliminated_pieces = self.perform_elimination(new_pos, colour)

        if len(eliminated_pieces) > 0:
            # then there are pieces that have been eliminated, therefore we must update the
            # neighbouring pieces free neighbour list
            for piece in eliminated_pieces:
                elim_pos = piece.get_position()
                self.update_neighbouring_squares(elim_pos,True)
        # increase the number of moves made on the board
        # self.move_counter += 1
        # success
        return eliminated_pieces

    # place a piece on the board and return the eliminated piece if there are any
    def apply_placement(self, pos, colour):
        col, row = pos
        if colour == constant.WHITE_PIECE:
            my_pieces = self.white_pieces
            opponent_pieces = self.black_pieces
        else:
            my_pieces = self.black_pieces
            opponent_pieces = self.white_pieces

        # add the piece to the board
        try:
            new_piece = {pos: Piece(pos,colour,self)}
            my_pieces.update(new_piece)

            # for this position we must check if there are any pieces that are neighbouring this piece
            # if there are, we must update those pieces free neighbours
            # since we have placed a piece on the board, this location is no longer free
            self.update_neighbouring_squares(pos,False)

        except IllegalPlacement:
            print("Piece created at illegal position on board")
            return

        # first we update the board representation
        self.set_board(row, col, colour)

        # perform the elimination around the piece that has been placed
        eliminated_pieces = self.perform_elimination(pos, colour)

        # for each eliminated piece we must update the neighbouring sqaures of that piece
        if len(eliminated_pieces) > 0:
            for piece in eliminated_pieces:
                elim_pos = piece.get_position()
                self.update_neighbouring_squares(elim_pos,True)

        # update the number of pieces the player is able to place
        self.places_remaining[colour] -= 1

        return eliminated_pieces

    # update the pieces neighbour free list --
    # if we are wanting to indicate that the current square that we are on is no longer free we set the
    # value to False,
    # if the sqaure we are currently on is free, we set the value to true, indicating that this is a possible
    # square that the neighboring sqaure can possibly move int o
    def update_neighbouring_squares(self,pos, bool_value):
        # for the eliminated piece we must also update any neighboutrs
        for direction in range(constant.MAX_MOVETYPE):
            # get the position of any possible neighbouring squares
            neighbour_pos = self.convert_direction_to_coord(pos, direction)

            # get the direction that is pointing from from neighbour to reference square
            opp_dir = self.get_opposite_direction(direction)

            # if a neighbouring square is occupied by this piece, we must update its free-neighbour list
            if neighbour_pos in self.white_pieces:
                neighbour = self.white_pieces[neighbour_pos]
                neighbour.set_neighbour(opp_dir, bool_value)
                print(neighbour)

            # if a neighbour is occupied by the opponent piece, we need to update its free-neighbour list
            elif neighbour_pos in self.black_pieces:
                neighbour = self.black_pieces[neighbour_pos]
                neighbour.set_neighbour(opp_dir, bool_value)
                print(neighbour)

    # went we want to update the board we call this function
    # move has to be in the form ((row,col),direction)
    def update_board(self, move, colour):
        eliminated_pieces = []
        # we no longer reset the eliminated moves dictionary
        # make the action
        if self.phase == constant.PLACEMENT_PHASE:
            # make the placement -- this should take care of the update to the piece position list
            # as well as the move counter
            eliminated_pieces = self.apply_placement(move, colour)

        elif self.phase == constant.MOVING_PHASE:
            # move is in the form (pos, direction)
            pos = move[0]
            direction = move[1]
            # print(pos)
            # make the move
            eliminated_pieces = self.apply_move(pos, direction, colour)

        # after an action is applied we can increment the move counter of the board
        self.move_counter += 1

        # test if we need to switch from placement to moving
        if self.move_counter == 24 and self.phase == constant.PLACEMENT_PHASE:
            # change the phase from placement to moving
            self.phase = constant.MOVING_PHASE
            self.move_counter = 0
            # all 24 pieces have been placed on the board

        if self.phase == constant.MOVING_PHASE:
            # do we need to shrink the board
            if self.move_counter in (128, 192):
                # add the eliminated pieces from the shrink board to this
                eliminated_pieces += self.shrink_board()

            # check if the move passed in was a forfeit move
            if move is None:
                self.move_counter += 1

    # check if there is a winner terminal states can only occur in the final phase
    def is_terminal(self):

        # use the referee code for this
        white_num = len(self.white_pieces)
        black_num = len(self.black_pieces)

        if self.phase == constant.MOVING_PHASE:

            if black_num >= 2 and white_num >= 2:
                return False
            elif black_num >= 2 and white_num < 2:
                self.winner = constant.BLACK_PIECE
                # self.phase = constant.TERMINAL
                self.terminal = True
                return True
            elif black_num < 2 and white_num >= 2:
                self.winner = constant.WHITE_PIECE
                # self.phase = constant.TERMINAL
                self.terminal = True
                return True
            elif black_num < 2 and white_num < 2:
                self.winner = None
                # self.phase = constant.TERMINAL
                self.terminal = True
                return True
        else:
            # we have not reached a terminal state
            return False

    # elimination checkers -- TODO: need to change this to work with this board representation
    def perform_elimination(self, my_piece_pos, colour):
        eliminated_pieces = []

        # get the opponent piece type
        opponent = self.get_opp_piece_type(colour)

        if colour == constant.WHITE_PIECE:
            my_pieces = self.white_pieces
            my_elim_pieces = self.white_eliminate_pieces
            opponent_pieces = self.black_pieces
            opp_elim_pieces = self.black_eliminate_pieces
        elif colour == constant.BLACK_PIECE:
            my_pieces = copy(self.black_pieces)
            my_elim_pieces = self.black_eliminate_pieces
            opponent_pieces = copy(self.white_pieces)
            opp_elim_pieces = self.white_eliminate_pieces

        while self.check_one_piece_elimination(my_piece_pos, colour) is not None:
            # check if this piece has eliminated an opponent
            elim_pos = self.check_one_piece_elimination(my_piece_pos, colour)

            # want to eliminate about the opposition's piece
            if elim_pos in opponent_pieces:
                # get the eliminated piece
                elim_piece = opponent_pieces.pop(elim_pos)

                # eliminate that piece from the board
                elim_piece.eliminate()

                # add to the opponent eliminated pieces
                opp_elim_pieces.append(elim_piece)

                # update the string board representation
                remove_col, remove_row = elim_pos
                self.set_board(remove_row, remove_col, constant.FREE_SPACE)

                # update the eliminated piece list
                eliminated_pieces.append(elim_piece)

                # for the eliminated piece we must also update any neighboutrs
                for direction in range(constant.MAX_MOVETYPE):
                    neighbour_pos = self.convert_direction_to_coord(elim_pos,direction)
                    opp_dir = self.get_opposite_direction(direction)

                    # if a neighbouring square is occupied by this piece, we must update its free-neighbour list
                    if neighbour_pos in my_pieces:
                        neighbour = my_pieces[neighbour_pos]
                        neighbour.set_neighbour(opp_dir, True)
                        print(neighbour)

                    # if a neighbour is occupied by the opponent piece, we need to update its free-neighbour list
                    elif neighbour_pos in opponent_pieces:
                        neighbour = opponent_pieces[neighbour_pos]
                        neighbour.set_neighbour(opp_dir, True)
                        print(neighbour)

        # check for self elimination if there is not opponent piece to be eliminated
        elim_pos = self.check_self_elimination(my_piece_pos, colour)
        if elim_pos is not None:
            # removes item from the board and list
            elim_piece = my_pieces.pop(elim_pos)
            elim_piece.eliminate()

            # add to this players eliminated piece list
            my_elim_pieces.append(elim_piece)

            remove_col, remove_row = elim_pos
            self.set_board(remove_row, remove_col, constant.FREE_SPACE)

            # update the eliminated piece dictionary
            eliminated_pieces.append(elim_piece)

            # for the eliminated piece we must also update any neighbour
            for direction in range(constant.MAX_MOVETYPE):
                neighbour_pos = self.convert_direction_to_coord(elim_pos, direction)
                opp_dir = self.get_opposite_direction(direction)

                # if a neighbouring square is occupied by this piece, we must update its free-neighbour list
                if neighbour_pos in my_pieces:
                    neighbour = my_pieces[neighbour_pos]
                    neighbour.set_neighbour(opp_dir, True)
                    print(neighbour)

                # if a neighbour is occupied by the opponent piece, we need to update its free-neighbour list
                elif neighbour_pos in opponent_pieces:
                    neighbour = opponent_pieces[neighbour_pos]
                    neighbour.set_neighbour(opp_dir, True)
                    print(neighbour)

        print(eliminated_pieces)
        print(my_elim_pieces)
        print(opp_elim_pieces)
        print(self)
        return eliminated_pieces

    # elimination helper function
    def check_one_piece_elimination(self, my_piece_pos, colour):
        pos_col, pos_row = my_piece_pos

        if colour == constant.WHITE_PIECE:
            my_pieces = copy(self.white_pieces)
            opponent_pieces = copy(self.black_pieces)
        elif colour == constant.BLACK_PIECE:
            my_pieces = copy(self.black_pieces)
            opponent_pieces = copy(self.white_pieces)

        # append the corner pieces to the list as these act as your own piece
        for corner in self.corner_pos:
            my_pieces.update({corner: None})

        # test all the 4 cases for this type of elimination
        # don't need to test for negative indices and positions outside the boundary of the board because there should
        # be no pieces that are placed in these positions and therefore do not exist in these lists

        # check left
        if (pos_col - 1, pos_row) in opponent_pieces and (pos_col - 2, pos_row) in my_pieces:
            if opponent_pieces[(pos_col - 1, pos_row)].is_alive():
                return pos_col - 1, pos_row
        # check right
        if (pos_col + 1, pos_row) in opponent_pieces and (pos_col + 2, pos_row) in my_pieces:
            if opponent_pieces[(pos_col + 1, pos_row)].is_alive():
                return pos_col + 1, pos_row
        # check up
        if (pos_col, pos_row - 1) in opponent_pieces and (pos_col, pos_row - 2) in my_pieces:
            if opponent_pieces[(pos_col, pos_row - 1)].is_alive():
                return pos_col, pos_row - 1
        # check down
        if (pos_col, pos_row + 1) in opponent_pieces and (pos_col, pos_row + 2) in my_pieces:
            if opponent_pieces[(pos_col, pos_row + 1)].is_alive():
                return pos_col, pos_row + 1

        # if it does not exist therefore there is no piece to be eliminated
        return None

    def check_self_elimination(self, my_piece_pos, colour):
        # update piecePos from tuple to pos_row and pos_col
        pos_col, pos_row = my_piece_pos

        if colour == constant.WHITE_PIECE:
            opponent_pieces = copy(self.black_pieces)
            my_pieces = self.white_pieces
        elif colour == constant.BLACK_PIECE:
            opponent_pieces = copy(self.white_pieces)
            my_pieces = self.black_pieces

        # append the corner pieces to the list as these act as your own piece
        for corner in self.corner_pos:
            opponent_pieces.update({corner: None})

        # now just need to check horizontal and vertical positions to see if they are in the piecePos list
        # horizontal check
        if ((pos_col + 1, pos_row) in opponent_pieces) and ((pos_col - 1, pos_row) in opponent_pieces):
            if my_pieces[(pos_col, pos_row)].is_alive():
                return pos_col, pos_row
        # vertical piece position check for self elimination
        elif ((pos_col, pos_row + 1) in opponent_pieces) and ((pos_col, pos_row - 1) in opponent_pieces):
            if my_pieces[(pos_col, pos_row)].is_alive():
                return pos_col, pos_row
        else:
            return None

    # helper method for the moving phase of the game
    @staticmethod
    def convert_direction_to_coord(my_piece_pos, direction):
        # piece pos is in the form of a tuple (col,row)
        # moves types
        # 0 - right 1 space
        # 1 - down 1 space
        # 2 - left 1 space
        # 3 - up 1 spaces
        # 4 - right 2 spaces
        # 5 - down 2 spaces
        # 6 - left 2 spaces
        # 7 - up 2 spaces

        # convert the tuple to row, col variable
        pos_col, pos_row = my_piece_pos

        # do the conversion -- this function does not handle
        if direction == constant.RIGHT_1:
            return pos_col + 1, pos_row
        elif direction == constant.DOWN_1:
            return pos_col, pos_row + 1
        elif direction == constant.LEFT_1:
            return pos_col - 1, pos_row
        elif direction == constant.UP_1:
            return pos_col, pos_row - 1
        elif direction == constant.RIGHT_2:
            return pos_col + 2, pos_row
        elif direction == constant.DOWN_2:
            return pos_col, pos_row + 2
        elif direction == constant.LEFT_2:
            return pos_col - 2, pos_row
        elif direction == constant.UP_2:
            return pos_col, pos_row - 2

    @staticmethod
    def convert_coord_to_direction(coord_1, coord_2):
        # coord is the stationary piece, coord_2 is the piece we want to move to
        # the move type returned is the move type to get from coord_1 to coord_2
        coord_1_col, coord_1_row = coord_1
        # print(coord_1_col, coord_1_row)
        coord_2_col, coord_2_row = coord_2

        # check left and right first
        # check left
        if coord_1_col + 1 == coord_2_col and coord_1_row == coord_2_row:
            return constant.RIGHT_1
        elif coord_1_col == coord_2_col and coord_1_row + 1 == coord_2_row:
            return constant.DOWN_1
        elif coord_1_col - 1 == coord_2_col and coord_1_row == coord_2_row:
            return constant.LEFT_1
        elif coord_1_col == coord_2_col and coord_1_row - 1 == coord_2_row:
            return constant.UP_1
        elif coord_1_col + 2 == coord_2_col and coord_1_row == coord_2_row:
            return constant.RIGHT_2
        elif coord_1_col == coord_2_col and coord_1_row + 2 == coord_2_row:
            return constant.DOWN_2
        elif coord_1_col - 2 == coord_2_col and coord_1_row == coord_2_row:
            return constant.LEFT_2
        elif coord_1_col == coord_2_col and coord_1_row - 2 == coord_2_row:
            return constant.UP_2

    @staticmethod
    def get_opposite_direction(direction):
        if direction == constant.UP_1:
            return constant.DOWN_1
        elif direction == constant.LEFT_1:
            return constant.RIGHT_1
        elif direction == constant.DOWN_1:
            return constant.UP_1
        elif direction == constant.RIGHT_1:
            return constant.LEFT_1
        elif direction == constant.UP_2:
            return constant.DOWN_2
        elif direction == constant.LEFT_2:
            return constant.RIGHT_2
        elif direction == constant.DOWN_2:
            return constant.UP_2
        elif direction == constant.RIGHT_2:
            return constant.LEFT_2

    # shrink the board
    def shrink_board(self):
        eliminated_pieces = []

        # use the referee code for the shrinking of the board
        offset = self.num_shrink
        for i in range(offset, constant.BOARD_SIZE - offset):
            # list storing the row and column we need to shrink
            shrink = [(i, offset), (offset, i), (i, 7 - offset), (7 - offset, i)]
            for (col, row) in shrink:
                # update the board representation
                # set the row to invalid spaces
                self.set_board(row, col, constant.INVALID_SPACE)

                # remove any piece that is eliminated from the position lists
                if (col, row) in self.black_pieces:
                    piece = self.black_pieces.pop((col, row))
                    piece.eliminate()
                    self.black_eliminate_pieces.append(piece)
                    eliminated_pieces.append(piece)
                elif (col, row) in self.white_pieces:
                    piece = self.white_pieces.pop((col, row))
                    piece.eliminate()
                    self.white_eliminate_pieces.append(piece)
                    eliminated_pieces.append(piece)

                # set the column to invalid spaces
                self.set_board(col, row, constant.INVALID_SPACE)

        self.num_shrink += 1
        offset += 1
        # set the new corner
        self.corner_pos[0] = (offset, offset)
        self.corner_pos[1] = (7 - offset, offset)
        self.corner_pos[2] = (offset, 7 - offset)
        self.corner_pos[3] = (7 - offset, 7 - offset)

        # if a corner is on top of a piece , eliminate that piece
        for corner in self.corner_pos:

            if corner in self.white_pieces:
                piece = self.white_pieces.pop(corner)
                piece.eliminate()
                self.white_eliminate_pieces.append(piece)
                eliminated_pieces.append(piece)
            elif corner in self.black_pieces:
                piece = self.black_pieces.pop(corner)
                piece.eliminate()
                self.black_eliminate_pieces.append(piece)
                eliminated_pieces.append(piece)

        # update the board representations
        for corner_col, corner_row in self.corner_pos:
            self.set_board(corner_row, corner_col, constant.CORNER_PIECE)

        # check for one space eliminations about the corner pieces
        for i in (0, 2, 3, 1):
            corner = self.corner_pos[i]
            pieces = self.corner_elimination(corner)

            # add the eliminated pieces from corner elimination to the list of eliminated pieces
            eliminated_pieces += pieces

    # helper function for elimination of pieces at a corner -- for board shrinks
    def corner_elimination(self, corner):
        eliminated_pieces = []
        # print("CALLED CORNER ELIMINATION")
        # print("*"*50)
        # self.print_board()
        # print("*"*50)
        # types of players
        player_types = (constant.WHITE_PIECE, constant.BLACK_PIECE)

        # the corner piece can act as the player piece -- therefore we can eliminate
        # the white pieces around the corner first, then the black pieces
        for player in player_types:

            if player == constant.WHITE_PIECE:
                opponent_pieces = self.black_pieces
                opp_elim_pieces = self.black_eliminate_pieces
            elif player == constant.BLACK_PIECE:

                opponent_pieces = self.white_pieces
                opp_elim_pieces = self.white_eliminate_pieces

            opp_player = self.get_opp_piece_type(player)
            # there can be more than one elimination or there can be None
            while self.check_one_piece_elimination(corner, player) is not None:
                eliminated_pos = self.check_one_piece_elimination(corner, player)

                # remove from the oppenent players piece pos list
                # print("ELIMINATED: " + str(eliminated_piece))
                elim_piece = opponent_pieces.pop(eliminated_pos)
                elim_piece.eliminate()
                opp_elim_pieces.append(elim_piece)

                eliminated_pieces[opp_player].append(elim_piece)
                col, row = eliminated_pos
                # update the board representation
                self.set_board(row, col, constant.FREE_SPACE)

        return eliminated_pieces

    # get the piece at a given position on the board
    # returns -- the piece object or None if there is no piece corresponding to that position
    def get_piece(self, pos):
        if pos in self.white_pieces:
            return self.white_pieces[pos]
        elif pos in self.black_pieces:
            return self.black_pieces[pos]
        else:
            raise PieceNotExist

    # get the opposite piece type
    @staticmethod
    def get_opp_piece_type(piece_type):
        if piece_type == constant.WHITE_PIECE:
            return constant.BLACK_PIECE
        else:
            return constant.WHITE_PIECE

    def undo_move(self, action_applied, eliminated_pieces):

        colour_tup = (constant.BLACK_PIECE, constant.WHITE_PIECE)
        # then we need to update the board to being in the state where it originally was in
        # first we need to see if the board has just recently been shrunk

        if self.move_counter == 128:
            # the board has just been shrunk once
            # clear the board
            self.board_state = self.init_board_rep()
            # put the original corners back on the board
            self.corner_pos = [(0,0),(7,0),(0,7),(7,7)]
            for (col,row) in self.corner_pos:
                self.set_board(row, col, constant.CORNER_PIECE)

            # place all the pieces back on the board
            for colour in colour_tup:
                for i in range(len(self.piece_pos[colour])):
                    col, row = self.piece_pos[colour][i]
                    self.set_board(row,col,colour)

            # place all the eliminated pieces back on the board
            for colour in colour_tup:
                for (col,row) in eliminated_pieces[colour]:
                    # print((col,row))
                    self.set_board(row,col,colour)
                    self.piece_pos[colour].append((col,row))

                    # these pieces are affected by the change so then we can add these pieces to the
                    # affected piece list
                    pieces_effected.append(((col, row), colour))
            # self.print_board()

        elif self.move_counter == 192:
            # reinitialise the board state then reset the corner pieces
            self.board_state = self.init_board_rep()
            # outer edges still invalid
            for i in range(constant.BOARD_SIZE):
                # set the outer edges to invalid
                self.set_board(0, i, constant.INVALID_SPACE)
                self.set_board(7, i, constant.INVALID_SPACE)
                self.set_board(i, 7, constant.INVALID_SPACE)
                self.set_board(i, 0, constant.INVALID_SPACE)

            # set the corner positions to be at the old corners
            self.corner_pos = [(1,1),(6,1),(1,6),(6,6)]
            for (col,row) in self.corner_pos:
                self.set_board(row, col, constant.CORNER_PIECE)

            # place all the pieces back on the board
            for colour in colour_tup:
                for (col,row) in self.piece_pos[colour]:
                    self.set_board(row,col,colour)

            # place all the eliminated pieces back on the board
            for colour in colour_tup:
                for (col,row) in eliminated_pieces[colour]:
                    self.set_board(row,col,colour)
                    self.piece_pos[colour].append((col,row))

                    # these pieces are affected by the change so then we can add these pieces to the
                    # affected piece list
                    pieces_effected.append(((col, row), colour, constant.ELIMINATED_PIECE))

        # now we just need to deal the with action applied to the board

        # if there was no action applied to the board, all we need to do
        # is to decrease the move counter
        # print("GOT HERE")

        if action_applied is None:
            self.move_counter-=1
            return

        # if there was an action applied, need to determine if it was in placement or moving
        # phase
        if self.phase == constant.PLACEMENT_PHASE:
            # put the eliminated pieces back on the board, then move the piece
            for colour in colour_tup:
                for (col,row) in eliminated_pieces[colour]:
                    self.set_board(row,col,colour)
                    self.piece_pos[colour].append((col,row))

                    # these pieces are affected by the change so then we can add these pieces to the
                    # affected piece list
                    pieces_effected.append(((col, row), colour, constant.ELIMINATED_PIECE))



            # print("TEST")
            # self.print_board()

            # reverse the move that was placed on the board
            pos = action_applied[0]
            col,row = pos
            colour = action_applied[1]
            # print(pos)
            if pos in self.piece_pos[colour]:
                self.piece_pos[colour].remove(pos)
            self.set_board(row, col, constant.FREE_SPACE)

            # this piece is affected by the change so then we can add these pieces to the
            # affected piece list
            pieces_effected.append(((col, row), colour, constant.PLACE_LOC))


            # decrease the moving counter
            self.move_counter-=1
            return pieces_effected

        elif self.phase == constant.MOVING_PHASE:
            # need to check if it is the first move of moving phase
            if self.move_counter == 0:
                # print("MOVE COUNTER IS NOW 0")
                # this is the first move, then the action applied to the
                # board is a placement
                for colour in colour_tup:
                    for (col,row) in eliminated_pieces[colour]:
                        self.set_board(row,col,colour)
                        self.piece_pos[colour].append((col,row))

                        # these pieces are affected by the change so then we can add these pieces to the
                        # affected piece list
                        pieces_effected.append(((col, row), colour, constant.ELIMINATED_PIECE))

                # reverse the move that was placed on the board
                pos = action_applied[0]
                col,row = pos
                colour = action_applied[1]
                # print(pos)
                if pos in self.piece_pos[colour]:
                    self.piece_pos[colour].remove(pos)
                self.set_board(row, col, constant.FREE_SPACE)
                # these pieces are affected by the change so then we can add these pieces to the
                # affected piece list
                pieces_effected.append(((col, row), colour, constant.PLACE_LOC))

                # decrease the move counter
                self.move_counter = 24
                self.phase = constant.PLACEMENT_PHASE
                return pieces_effected
            else:
                # if the move counter was not 128,192 we need to place
                # the eliminated pieces back on the board
                # print("started here")
                if self.move_counter not in (0, 128, 192):
                    for colour in colour_tup:
                        for (col,row) in eliminated_pieces[colour]:
                            self.set_board(row,col,colour)
                            self.piece_pos[colour].append((col,row))

                            # these pieces are affected by the change so then we can add these pieces to the
                            # affected piece list
                            pieces_effected.append(((col, row), colour, constant.ELIMINATED_PIECE))

                # print("eliminated pieces")
                # we just need to undo the move that was made
                old_pos = action_applied[0][0]
                move_type = action_applied[0][1]
                colour = action_applied[1][0]

                curr_pos = self.convert_move_type_to_coord(old_pos, move_type)
                # reset the new location to being free
                self.set_board(curr_pos[1], curr_pos[0], constant.FREE_SPACE)
                if curr_pos in self.piece_pos[colour]:
                    self.piece_pos[colour].remove(curr_pos)

                    # these pieces are affected by the change so then we can add these pieces to the
                    # affected piece list
                    pieces_effected.append((curr_pos, colour, constant.PIECE_NEW_LOC))

                # put the piece back to its old location
                self.set_board(old_pos[1],old_pos[0], colour)
                self.piece_pos[colour].append(old_pos)

                # these pieces are affected by the change so then we can add these pieces to the
                # affected piece list
                #
                pieces_effected.append((old_pos, colour, constant.PIECE_OLD_LOC))
                # decrease the move counter
                self.move_counter -= 1

                # return the pieces_effected by the undo move
                return pieces_effected

    '''
    STANDARD METHODS OVERRIDDEN FOR THIS CLASS
    '''
    def __str__(self):
        board = ""
        for row in range(constant.BOARD_SIZE):
            for col in range(constant.BOARD_SIZE):
                # get the char to print
                char_index = row * constant.BOARD_SIZE + col

                char = chr(self.board_state[char_index])
                board+=char + " "
            board+="\n"

        return "THIS BOARD: \n" + board + "\n"
