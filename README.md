# Watch Your Back

## PROJECT PART B

### Board.py
* Implemented the backend of the game board using the class Board. Currently it stores a bytearray representation of the game state as well as the positions of pieces on the board in that game state. It also stores a move counter and phase indicator 
* update_board handles updates to the board -- if you want to move a piece on the board you use this method. When it is called, it places/moves a pieces, checks for eliminations and returns the pieces that have been eliminated. It also updates the move counter and phase of the board game. This is useful for searching 
* **TODO**: Need to work out a way to minimise the size of this structure as it is still taking up quite a lot of space so far. This is because of the lists that store the position of the pieces. Also need to work out if it is best to evaluate available moves for pieces here or is it best to do it out of the class.
    - Think about storing the eliminated pieces a stack of lists that represent the eliminated pieces
    - When we want to undo a move we just pop the latest eliminated pieces of the stack and use that to reconstruct the board 
    - This means added space complexity -- but since we are only using one board it might not matter too much 
    
    * Other way of doing it is to store the eliminated pieces at each node -- then when undoing a move we just need to look at the eliminated pieces at that node (these are the pieces that have been eliminated to get to that particular state)
    
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

### Alpha-Beta Minimax Time and Space Optimisations 
#### Issues Fixed 
* Fixed an issue relating to the evaluation of the moves -- noticed that the evaluation function was being evaluate with respect to the colour of the min or max nodes. Therefore for a max node, it would return the utility for the max player, and for the min player it would return the utility of that board state for that min player. This meant that if we were searching at an odd depth, we would evaluate the cut-off nodes at the min player and hence minimax would actually return the best move for that MIN player instead of the best player for the MAX player. Therefore to fix this we are using the colours of the game defined as instance variables for the AB class. This means that we are always evaluating the board with respect to the MAX player. This explained why previously we noticed that the algorithm was constantly loosing against the random player (when the depth was odd).
* Fixed issue relating the the LRU-caching of the min_value function -- now it takes depth into account and we clear the cache at every depth iteration. Hence we only cache values at the current iteration.

#### Time Optimisation
* We are using an LRU-cache to store recently evaluated minimax evaluations. There is a built in LRU-cache in python3 which we were able to use. As a result we noticed that we were able to get a significant increase in performance from 2-ply to 3-ply for a 0.5 second action evaluation. The only thing with using this is that we have added extra space complexity to store the function call and their values. But by doing so we get a significant increase in performance as we don't have to evaluate nodes that we have come across before as we can just query the cache for the value. We thought about using this with an iterative deepening method applied to minimax depth limited search, but the problem we ran into was that because we were not caching the depth at which the function was being evaluated at, when iterating through deeper depths it was just evaluating the first layer. Hence we needed to clear the cache every time we increase the depth we want to search to. 
* Attempted to use move ordering in iterative deepening to inform deeper searches of moves that the algorithm thinks is better. Since AB-pruning works best when nodes are ordered we implemented this simple static move-ordering to do so. Next thing we should do is to evaluate good-moves from bad-moves before doing the search itself, such that the left-over moves after the AB function call finishes (assuming that it does not search every action) are in some order as well. By doing this trivial method of move-ordering we were able to increase the search depth to 4-ply in a 1 second move evaluation. 
* TODO -- need to implement killer move heuristic -- store moves that cause a beta cutoff and check if these moves are valid in later depth searches: LOOK THIS UP 
* Implement some sort of symmetry checking/ mapping -- this would be good 
    - since in the cache we are only storing the board_state (but we are not doing anything with it in the function -- it is only an argument for storing in the cache), therefore we can apply a symmetry to a board_state, then we can just pass that in the function -- this should be able to decrease the serach space, and hence we should be able to search deeper in a reasonable amount of time.

#### Memory Optimisation
* We are using a bytearray string representation for the board itself. This means we can store the entire board in as little as 121 bytes. Whereas if we had a 2-D nested list that represented the board, it would take up 576 bytes. 
* We are only use a single board to complete the search on, when we want to apply a new move to the board, all we have to do is to undo the previous move, then apply the new move. This means we save space as we don't need to create a node structure to search on, as the structure we search on is the board itself. Previously, we had a node structure, and everytime we wanted to create a new node with an action applied to it, we would deepcopy the board to the new node, and then apply the move in that node. Deepcopying is very inefficent in terms of time, therefore we save some time by not doing that. Furthermore due to the exponential nature of this search and the high branching factor of the game itself, it would mean that we would have a large number of board representations exsisting. Therefore we cut down the amount of space we have. This means that we can store more information about the board as we only have one instance of that board and we don't need to copy these to other nodes in order to be able to search using a given strategy. 

### Monte Carlo Tree Search 
* This was implemented, but it was determined to be inefficent in both time and space compared on minimax given our memory and time constraints. Since we were only able to use 100MB of memory and a total of 60s for the game itself, this means that we could only build a small search tree which was the equivalent to one layer in the minimax tree.
* In order to improve efficency of the game we must improve the simulation algorithm of the game -- currently it takes 0.07s to simulate the game from move 0, and therefore in one second we would only be able to make 14 nodes in the tree. This is not good.
* Maybe in the later phases of the game we can use this technique to inform us of good moves to play in the game, but not at the start of the game as the branching factor and the actual length of the game is too long and we can't build a good game tree to search on. 

### Machine Learning 
#### TD-Leaf(λ) 
* Attempted to implement TD-Leaf(λ) to train our weight update function 
* Need to confirm that the 'best leaf found at max depth' is equivalent to the minimax value of evaluating an action
    * If this is the case we just need to return the best policy vector such that we can extract the weight component for the derivative of that evaluation 
* Added various data structures in the minimax class and the board class to keep track of evaluation values, evaluation vectors for machine learning 
* Added a method to simulate a game between two people, the first being the player we want to train. This returns lists which contain the evaluation values and the corresponding evaluation vector
* Need to figure out what exactly the partial derivative is equal to -- because this is not an entirely differentiable function, hence we need to work out how we can approximate this 
* Need to work out how to train our function 

### Evaluation 
* Need to work out good evaluation functions so that minimax works efficently -- currently we do not have any evaluation functions.
* Need to work out more features of the game -- we need at least 7 features of the game, including some clever heuristics 

### TODO 
* Implement 3 types of roll outs for MCTS -- random rollout, light roll out (greedy), medium roll-out (2-ply negamax/ab-minimax)
    - Need to speed up the simulation of the board game because this is the factor that is stopping us from creating a deep game tree in 1 second. 
    - Currently it takes 0.07s to do one game iteration, this is bad because we can theoretically only create 14 nodes in one move iteration. This is not good. 
* We could switch up the search strategy for each phase of the game -- e.g. MCTS for moving phase and AB-Minimax for Placement phase. 
* Implement negamax
* Need to work out how to use Machine Learning to train the evaluation function 
* Need to work out what the dominant feature of the game are 


### COMPLETED TODO's
* Need to work out how to use a cache to store recent board-state-Minimax value pairs (possibly using an LRU cache or something similar such that we can limit the size of the cache -- keep recently used items and expell least used items -- these items will be added back to the cache if they are visited again)
    - For the LRU cache -- think about using a double ended linked list -- when we add to the cache we add to the head of the cache, but we only add until the cache is below a certain size, when we reach the size and we want to add more, we need to get rid an element at the tail of the cache -- these are the least frequently used items 
    - Or we can use a dictionary to store the entries of the items up until a fixed size, then we can get rid of elements of the dictionary that are old to reduce space in the dictionary 
        - by doing so we limit the size of the cache
    
    - Restructure Minimax such that we dont use a child node to store the move applied to the board state -- instead we can use put that in the function call itself 
        - therfore we should be able to use functools_lrucache to memoize minimax 
        - for lrucache to work the arguments of a function have to be immutable 
            -- prototype: min/max(board_state, depth, move, colour ) -- we need a way to store alpha and beta not in the function call but possibly as a static instance variable -- therefore when updates are being made 
            -- we can just call self.alpha, self.beta to do the work 
                -- therefore by doing so we get rid of the create node part in the min and max nodes -- because we are just using update_board, and undo_move to change the board state, therefore we would not need the node 
* Need to work out a way to use the available moves function I wrote earlier with the undo moves functionality 
* Implement Monte Carlo Tree Search ----- THIS IS MOST IMPORTANT (first we will do it with a random rollout)