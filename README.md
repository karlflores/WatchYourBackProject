# Watch Your Back

## PROJECT PART B

### Board.py
* Implemented the backend of the game board using the class Board. Currently it stores a bytearray representation of the game state as well as the positions of pieces on the board in that game state. It also stores a move counter and phase indicator 
* update_board handles updates to the board -- if you want to move a piece on the board you use this method. When it is called, it places/moves a pieces, checks for eliminations and returns the pieces that have been eliminated. It also updates the move counter and phase of the board game. This is useful for searching 
* **TODO**: Need to work out a way to minimise the size of this structure as it is still taking up quite a lot of space so far. This is because of the lists that store the position of the pieces. Also need to work out if it is best to evaluate available moves for pieces here or is it best to do it out of the class.

### Player.py 
* Player.py -- this is a random player who chooses its next move according to the Random Agent file. 
* Player_AB.py -- this is a player who chooses moves based on the alpha-beta pruning minimax algorithm 
* All three methods are defined in each 

### Minimax.py Minimax_Node.py
* Minimax implements the alpha beta minimax algorithm -- currently it is not optimised and available moves are generated as we create nodes. This is very inefficient as we are always calculating available moves where in reality only some moves need to be changed/added or removed from the pre-existing available moves list.
    - Might be worth looking at using a dictionary to store available moves for a player 
        - When we are updating available moves we just need to at spaces that have recently been freed because a piece has been eliminated, and to look at the pieces around (2 spaces) away and to recalculate those available moves instead.
        - But this implemenation means that we need a dict to store the available moves for each player -- because when minimax is running we need a way to pass these available moves to the next node because both players available moves are affected. 
* Tried to implement move ordering -- this is something that we need to investigate 
* Minimax_Node implements a searchable and expandable node structure for minimax -- we need to look at how this can be compressed, what information do we actually need for the search to occur 

### Evaluation 
* Need to work out good evaluation functions so that minimax works efficently -- currently we do not have any evaluation functions 

