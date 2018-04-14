'''
* Implements the board class for the game
*

'''

import constant
from copy import deepcopy
import math

class Board(object):

    def __init__(self):
        # define the board parameters and constants
        self.board_state = self.init_board_rep()

        # self.piece_pos = {constant.BLACK_PIECE: {-1:}, constant.WHITE_PIECE: []}

        self.piece_counter = {constant.BLACK_PIECE: constant.MAX_NUM_PIECES,
                              constant.WHITE_PIECE: constant.MAX_NUM_PIECES}

        # dictionary storing the available moves of each player
        # in the placement phase the key is just constant.PLACEMENT_PHASE
        # indicating there is no pieces on the board at the moment
        # when we switch from placement to moving phase we get rid of this entry
        # and the keys are the tuples representing the position of the pieces that
        # are the position of pieces on the board so far
        self.available_moves = {constant.BLACK_PIECE: {constant.PLACEMENT_PHASE: []},
                                constant.WHITE_PIECE: {constant.PLACEMENT_PHASE: []}}
        # initialise the board representation
        # LT RT LB RB
        self.corner_pos = [(0, 0), (7, 0), (0, 7), (7, 7)]

        self.move_counter = 0
        self.phase = constant.PLACEMENT_PHASE
        self.num_shrink = 0

        # initialise the start of the game
        self.init_start_moves()

    def init_board_rep(self):
        # store the board representation as a byte_array length 64 (64bytes)
        temp = ''
        for index in range(constant.BOARD_SIZE*constant.BOARD_SIZE):
            temp += constant.FREE_SPACE
        # create a temp string of length 64
        temp = bytearray(temp,'utf-8')

        # set the corner locations on the board representation
        corner_pos = [(0,0),(0,7),(7,0),(7,7)]
        for col,row in corner_pos:
            self.set_array_char(temp,row,col,constant.CORNER_PIECE)

        return temp

    # set up the board for the first time
    def init_start_moves(self):
        # set the initial board parameters
        # no pieces on the board
        # available moves is the entire starting zone for each player

        # set the white pieces available moves
        for row in range(0,constant.BOARD_SIZE-2):
            for col in range(constant.BOARD_SIZE):
                if (row, col) not in self.corner_pos:
                    # append the available move in the list in the form col, row
                    # get the dictionary associated with the white piece
                    white_move_dict = self.available_moves[constant.WHITE_PIECE]

                    white_move_dict[constant.PLACEMENT_PHASE].append((col,row))

        # set the black piece available moves
        for row in range(2, constant.BOARD_SIZE):
            for col in range(constant.BOARD_SIZE):
                if (row, col) not in self.corner_pos:
                    # append the available move in the list in the form col, row
                    black_move_dict = self.available_moves[constant.BLACK_PIECE]
                    black_move_dict[constant.PLACEMENT_PHASE].append((col,row))

    def is_valid_placement(self,piece_place,piece_type):
        # set the valid zones for placement
        if piece_type == constant.WHITE_PIECE:
            start_zone = 0
            end_zone = constant.BOARD_SIZE-2
        else:
            start_zone = 2
            end_zone = constant.BOARD_SIZE-1

        # get the row and col
        pos_col, pos_row = piece_place

        # check the boundary of the board -- if a piece is placed outside
        # of it then return false
        if pos_col < 0 or pos_col > constant.BOARD_SIZE - 1:
            return False
        if pos_row < start_zone or pos_row > end_zone:
            # we can check if the place is placed in the starting zones for each player
            return False

        # now we can check if the placement of the piece is a free space -- if it
        # is then we know it is possible
        if self.get_board_piece(pos_row, pos_col) == constant.FREE_SPACE:
            return True
        else:
            return False

    # returns the type of the cell at a given position
    def return_cell_type(self,my_piece_pos):
        col_min = self.corner_pos[0][1]
        col_max = self.corner_pos[2][1]
        row_min = self.corner_pos[0][0]
        row_max = self.corner_pos[1][0]

        # if the position is outside of the playable bounds
        pos_col, pos_row = my_piece_pos
        if pos_col < col_min or pos_col > col_max:
            return constant.INVALID_SPACE
        if pos_row < row_min or pos_row > row_max:
            return constant.INVALID_SPACE

        # piece is in the playable bounds of the game
        if my_piece_pos in self.available_moves[constant.BLACK_PIECE]:
            return constant.BLACK_PIECE
        elif my_piece_pos in self.available_moves[constant.WHITE_PIECE]:
            return constant.WHITE_PIECE
        elif my_piece_pos in self.corner_pos:
            return constant.CORNER_PIECE
        else:
            return constant.FREE_SPACE
    # helper method for the moving phase of the game
    @staticmethod
    def convert_move_type_to_coord(my_piece_pos, move_type):
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
        if move_type == 0:
            return pos_col + 1, pos_row
        elif move_type == 1:
            return pos_col, pos_row + 1
        elif move_type == 2:
            return pos_col - 1, pos_row
        elif move_type == 3:
            return pos_col, pos_row - 1
        elif move_type == 4:
            return pos_col + 2, pos_row
        elif move_type == 5:
            return pos_col, pos_row + 2
        elif move_type == 6:
            return pos_col - 2, pos_row
        elif move_type == 7:
            return pos_col, pos_row - 2

    @ staticmethod
    def convert_coord_to_move_type(coord_1,coord_2):
        # coord is the stationary piece, coord_2 is the piece we want to move to
        # the move type returned is the movetype to get from coord_1 to coord_2
        coord_1_col, coord_1_row = coord_1
        coord_2_col, coord_2_row = coord_2

        diff_col = coord_2_col-coord_1_col
        diff_row = coord_2_row - coord_1_row

        if diff_col == 0:
            if diff_row == 1:
                return 0
            elif diff_row == -1:
                return 2
            elif diff_row == 2:
                return 4
            elif diff_row == -2:
                return 6
        elif diff_row == 0:
            if diff_col == 1:
                return 1
            elif diff_col == -1:
                return 3
            elif diff_col == 2:
                return 5
            elif diff_col == -2:
                return 7

    # check if a move is legal
    def is_legal_move(self,my_piece_pos,move_type):

        # apply the move to the piece
        new_pos = self.convert_move_type_to_coord(my_piece_pos,move_type)
        my_piece_type = self.return_cell_type(my_piece_pos)

        # check if the piece is actually a piece on the board
        if my_piece_type != constant.BLACK_PIECE and my_piece_type != constant.WHITE_PIECE:
            # then the piece cannot be placed here
            return False

        # at this stage we know the position is a piece on the board

        # get the piece type:
        new_my_piece_type = self.return_cell_type(new_pos)
        # check if the piece is within the current dimensions of the board
        if new_my_piece_type == constant.INVALID_SPACE or \
                    new_my_piece_type == constant.SPACE_NOT_EXIST:
            return False

        # if there is not another piece occupying that space and if it is inside the board
        # then it is a valid move
        # now we can check the move itself
        # if it is an adjacent move
        if move_type >=0 and move_type < 4:
            if new_my_piece_type == constant.FREE_SPACE:
                return True
            else:
                # there is a piece that is occupying this space
                return False
        elif move_type >= 4 and move_type < 8:
            # get the intermediate position
            inter_pos = self.convert_move_type_to_coord(my_piece_pos,move_type-4)
            inter_pos_piece_type = self.return_cell_type(inter_pos)

            # if there is a piece adjacent to that piece then we can make the jump
            if inter_pos_piece_type in (constant.BLACK_PIECE, constant.WHITE_PIECE):
                if new_my_piece_type == constant.FREE_SPACE:
                    # if the space is free then we can move here
                    return True
                else:
                    # if the space is not free then we cannot move here
                    return False
            else:
                # if the intermediate piece is a free space then we cannot perform this move
                return False

    # get the opposite piece type
    @staticmethod
    def get_opp_piece_type(piece_type):
        if piece_type == constant.WHITE_PIECE:
            return constant.BLACK_PIECE
        else:
            return constant.WHITE_PIECE

    # board representation setters and getter methods
    def get_board_piece(self, row, col):
        return self.get_array_element(self.board_state,row,col)

    # change the piece type in the board representation
    def set_board(self, row, col, piece_type):
        piece_types = (constant.CORNER_PIECE,constant.WHITE_PIECE,constant.BLACK_PIECE,
                       constant.FREE_SPACE,constant.INVALID_SPACE)
        # check if the piece_type is valid
        if piece_type not in piece_types:
            return

        # if valid we can set the board position
        self.set_array_char(self.board_state,row,col,piece_type)

    # print board method
    def print_board(self):

        for row in range(constant.BOARD_SIZE):
            for col in range (constant.BOARD_SIZE):
                # get the char to print
                char_index = row*constant.BOARD_SIZE + col

                char = chr(self.board_state[char_index])
                print('{} '.format(char),end='')

            print()

    # elimination checkers

    # TODO -- NEED TO TEST IF THE CHANGES TO MAKE IT HANDLE BOTH PLACEMENT AND MOVING
    # TODO -- WILL WORK CORRECTLY
    def perform_elimination(self,my_piece_pos,my_piece_type):
        # get the opponent piece type
        opp_piece_type = self.get_opp_piece_type(my_piece_type)

        while self.check_one_piece_elimination(my_piece_pos,my_piece_type) is not None:
            piece = self.check_one_piece_elimination(my_piece_pos,my_piece_type)

            # want to eliminate about the opposition's piece
            if piece in self.available_moves[opp_piece_type] and piece is not None:
                # remove this entry from the dictionary if in the moving phase
                # add the free space in to the avaiable moves list we are in the placement
                # phase
                if self.phase == constant.PLACEMENT_PHASE:
                    # add this free space to both the opponent piece and the current player
                    # available player list
                    self.available_moves[opp_piece_type][constant.PLACEMENT_PHASE].append(piece)
                    self.available_moves[my_piece_type][constant.PLACEMENT_PHASE].append(piece)
                else:
                    self.available_moves[opp_piece_type].pop(piece)
                    # recalculate all available moves for pieces around the new free space
                    self.update_near_by_free_space(piece)

                # update the string board representation
                remove_col,remove_row = piece
                self.set_board(remove_row,remove_col,constant.FREE_SPACE)
                # there is now one less piece on the board
                self.piece_counter[opp_piece_type] -= 1

        # check for self elimination if there is not opponent piece to be eliminated
        piece = self.check_self_elimination(my_piece_pos,my_piece_type)
        if piece is not None:
            # removes item from the board
            if self.phase == constant.PLACEMENT_PHASE:
                # add this free space to both the opponent piece and the current player
                # available player list
                self.available_moves[opp_piece_type][constant.PLACEMENT_PHASE].append(piece)
                self.available_moves[my_piece_type][constant.PLACEMENT_PHASE].append(piece)
            else:
                self.available_moves[my_piece_type].pop(piece)

            # when we remove a piece, it creates a free space on the board --
            # this free space needs to be updated to be an available move to those pieces
            # that can move into it -- TODO: NEED TO TEST THIS FUNCTION WELL
            self.update_near_by_free_space(piece)

            remove_col, remove_row = piece
            self.set_board(remove_row,remove_col,constant.FREE_SPACE)

            # there is now one less piece on the board
            self.piece_counter[my_piece_type] -= 1

    # elimination helper function
    def check_one_piece_elimination(self,my_piece_pos,my_piece_type):
        pos_col, pos_row = my_piece_pos
        my_piece_pos_list = list(self.available_moves[my_piece_type].keys())
        opp_piece_type = self.get_opp_piece_type(my_piece_type)
        # append the corner pieces to the list as these act as your own piece
        for corner in self.corner_pos:
            my_piece_pos_list.append(corner)

        # test all the 4 cases for this type of elimination
        # don't need to test for negative indices and positions outside the boundary of the board because there should
        # be no pieces that are placed in these positions and therefore do not exist in these lists

        # check left
        if (pos_col-1,pos_row) in self.available_moves[opp_piece_type] and (pos_col-2,pos_row) in my_piece_pos_list:
            return pos_col-1,pos_row
        # check right
        elif (pos_col+1,pos_row) in self.available_moves[opp_piece_type] and (pos_col+2,pos_row) in my_piece_pos_list:
            return pos_col+1,pos_row
        # check up
        elif (pos_col,pos_row-1) in self.available_moves[opp_piece_type] and (pos_col,pos_row-2) in my_piece_pos_list:
            return pos_col,pos_row-1
        # check down
        elif (pos_col,pos_row+1) in self.available_moves[opp_piece_type] and (pos_col,pos_row+2) in my_piece_pos_list:
            return pos_col, pos_row+1
        else:
            # if it does not exist therefore there is no piece to be eliminated
            return None
    
    def check_self_elimination(self,my_piece_pos,my_piece_type):
        # update piecePos from tuple to pos_row and pos_col
        pos_col,pos_row = my_piece_pos
        
        # if the current piece pos is not the expected piece type then return None
        if self.return_cell_type(my_piece_pos) != my_piece_type:
            return None

        opp_piece_type = self.get_opp_piece_type(my_piece_type)
        # add the location of the corners to the location list of the opponent piece
        opp_piece_pos_list = list(self.available_moves[opp_piece_type].keys())
        
        # now just need to check horizontal and vertical positions to see if they are in the piecePos list
        # horizontal check
        if ((pos_col+1,pos_row) in opp_piece_pos_list) and ((pos_col-1,pos_row) in opp_piece_pos_list):
            return pos_col,pos_row
        # vertical piece position check for self elimination
        elif ((pos_col,pos_row+1) in opp_piece_pos_list) and ((pos_col,pos_row-1) in opp_piece_pos_list):
            return pos_col,pos_row
        else:
            return None

    # call this when we want to make a move -- change the dict and change the board

    # when we want to apply a move to the board -- update the board and the dict associated
    def make_move(self,old_pos,move_type,my_piece_type):
        # check if the move is legal first
        if self.is_legal_move(old_pos,move_type) is False:
            return False

        # we know we can make the move now
        new_pos = self.convert_move_type_to_coord(old_pos,move_type)
        new_col, new_row = new_pos
        old_col, old_row = old_pos

        # first we update the board representation
        self.set_board(old_row,old_col,constant.FREE_SPACE)
        self.set_board(new_row,new_col,my_piece_type)

        # then we can update the dictionaries
        self.available_moves[my_piece_type].pop(old_pos)
        # create a new entry in the dictionary containing the piece on the board
        # and its available moves it can make
        new_entry = self.update_available_moves(new_pos)
        self.available_moves[my_piece_type].update(new_entry)

        # now we can test for elimination at the new position on the board
        self.perform_elimination(new_pos,my_piece_type)

        # increase the number of moves made on the board
        self.move_counter += 1
        # success
        return True

    # updates the available moves a piece can make after it has been moved
    # this way we don;t need to calculate all the available moves on the board
    # as pieces that have been eliminated also get rid of those associated available moves
    def update_available_moves(self, piece):
        # calculate the moves a piece can make
        new_dict = {piece: []}

        for move_type in range(constant.MAX_MOVETYPE):
            if self.is_legal_move(piece,move_type):
                new_dict[piece].append(move_type)

        return new_dict

    def update_near_by_free_space(self,free_space_pos):
        # enum all the possible locations
        possible = []
        for move in range(constant.MAX_MOVETYPE):
            possible.append(self.convert_move_type_to_coord(free_space_pos,move))

        for move in possible:
            type = self.return_cell_type(move)
            if type == constant.BLACK_PIECE:
                # if this possible piece is a black piece, we add this new free
                # space to its available move list
                move_type = self.convert_move_type_to_coord(move,free_space_pos)
                self.available_moves[constant.BLACK_PIECE][move].append(move_type)
            elif type == constant.WHITE_PIECE:
                self.available_moves[constant.WHITE_PIECE][move].append(move_type)

    def make_placement(self,pos, my_piece_type):
        opp_piece_type = self.get_opp_piece_type(my_piece_type)
        col,row = pos
        # check if that placement is legal
        if self.is_valid_placement(pos)is False:
            return False

        # else we know that this piece can be placed on the board

        # first we update the board representation
        self.set_board(row,col,my_piece_type)

        # then we update the counters of the board
        self.piece_counter[my_piece_type]+=1

        # update the board dictionaries -- this space is now occupied
        # therefore remove these entries from both available move dictionaries
        # for each piece
        self.available_moves[my_piece_type][constant.PLACEMENT_PHASE].remove(pos)
        self.available_moves[opp_piece_type][constant.PLACEMENT_PHASE].remove(pos)

        # increment the move counter

        # perform the elimination around the piece that has been placed
        self.perform_elimination(pos,my_piece_type)
        self.move_counter += 1

    # went we want to update the board we call this function
    # move has to be in the form ((row,col),move_type)
    def update_board(self,move,my_piece_type):
        pass

    # string_array helper methods
    @staticmethod
    def get_array_element(byte_array,row,col):
        # we assume that the string array is n x n in dimension

        # get the dimension
        dimension = int(math.sqrt(len(byte_array)))
        # check if row and col are valid
        if row > dimension - 1 or col > dimension - 1:
            return None

        elif row < 0 or col < 0:
            return None
        # get the index to access in the string
        index = row*dimension + col;

        # return the char at position index
        return chr(byte_array[index])

    @staticmethod
    def set_array_char(byte_array, row, col, new_char):
        dimension = int(math.sqrt(len(byte_array)))

        if row > dimension - 1 or col > dimension - 1:
            return
        elif row < 0 or col < 0:
            return

        # set the new char in the string
        # need to turn char into utf-8 encoding first
        byte_array[row * dimension + col] = ord(new_char)
