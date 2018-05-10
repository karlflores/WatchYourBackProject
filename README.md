# Watch Your Back
------------------------------------------/Watch Your Back\-----------------------------------------

## 1. Program Description
Our program can be split up into four main parts:
    1. The board/ board rules
    2. The player
    3. The search strategy
    4. Evaluation function

In terms of the files used in our submission, the structure is as follows:
```
	> WatchYourBack -----------------------------------------------------------------------
		> Board.py
			 |__ Implementation of the board 
		> Piece.py
			 |__ Implementation of the board pieces 
	> Agents ------------------------------------------------------------------------------
		> NegamaxTranspositionTable.py
					     |__ Implementation of the Negamax algorithm with a
						 transposition table
	> Data_Structures ---------------------------------------------------------------------
		> TranspositionTable.py
				      |__Implementation of the Transposition Table 
	> Constants ---------------------------------------------------------------------------
		> constants.py
			     |__ All constants used by the files in the submission
	> Error_Handling ----------------------------------------------------------------------
		> Errors.py
			  |__ Custom exceptions created for debugging and error handling 
	> Evaluation --------------------------------------------------------------------------
		> Features.py
			    |__ Implementation of all the features that we have come up with 
		> Policies.py
			    |__ The actual evaluation function implementation 
	> XML ---------------------------------------------------------------------------------
		> xml_helper.py
			      |__ Class that helps us save, load and update weights for the 
			   	  evaluation function. This was intended to be used with 
				  Machine Learning.
	> Player_Negamax.py 
			  |__ Our final player submission.
```
		


### 1.1 The board/board rules
* We decided to implement the board game using two main classes -- Board and Piece.

#### Piece.py

* The Piece class models the behaviour that a piece (black or white) on the board. This class implements several methods that govern how the piece is able to move on the board, and also stores if any neighbouring squares surrounding itself is FREE. We store the neighbour "free" positions as a list, where the index represents the direction that that piece needs to take to occupy that square. This allows for constant time operation to find whether a neighbouring square is already occupied or not, and also allows us to update in constant time the occupancy state of this pieces neighbours. This approach allows us to efficiently allow us to generate the legal directions the piece can move by just checking whether the neighbours are free or not.

#### Board.py
* The Board class structure consists of a dictionary storing all the pieces on the board, a bytearray board representation that is use for the key in the Transposition Table data structure used in our search algorithms (more on this later...) and a dictionary that stores all FREE-spaces on the board during the placement phase. We decided to use a byte array to represent the board in string format as it allowed for the lightweight properties of a string, with constant time access to piece types but unlike a string, it was mutable. This allowed us to easily convert between a bytearray and a string using encode and decode methods. The byte array is only updated when we apply an action to the board or we undo an action from the board. For the board's purpose it allows an easy way to print the board. Dictionaries were used to store the pieces on the board as it allowed for average-case O(1) constant time access and checking, allowing for quick updates to the board.

* The board class methods deal with the following features of the board game:

	- Updating the board, which consisted of switching from placing to moving phases, shrinking the board and performing eliminations:

		- Adding pieces to the board during the placement phase of the game.
            		- This is handled by the apply_placement method which allows for a player to place a piece on the board

        	- Moving a piece during the moving phase
            		- This is handled by the apply_action method

        	- Elimination of pieces is handled by the perform_elimination method

        	- Shrinking the board is handled by the shrink_board method

            	- This both eliminates any pieces near the corners according tp the rules of the game, as well as updating the bytearray representation of the board.

    	- The board class is also responsible for generating a list of legal actions such that our searching algorithm is able to search on the board. This method utilises the information of the state of the neighbouring squares of a piece.
        	- The sort actions method is able to take in a set of legal actions, and use a light evaluation function to sort those actions based on features of the game (more on this later...)
    	
- Most importantly, this Watch Your Back implementation also implements an undo_action method which takes in the action applied to the board and the list of eliminated pieces that resulted from applying that action. It then puts back all eliminated pieces on the board, undoes the action applied to the board and also updates the neighbouring square information of each "affected" piece from that action. By "affected piece" we mean pieces that have been eliminated, pieces that have been moved/placed and also neighbouring pieces of pieces that have been eliminated/moved/ placed on the board as well as neighbouring squares of newly-freed squares. By doing so we only update the attributes of pieces who have been affected by an action, thus eliminated any extra computation by not re-comupting any attributes of pieces that have been unaffected by an action. Furthermore, this undo_action method allows us to use the one board representation during the search thereby minimising any memory that we are using. This means we are able to store more information in the board structure as we are not deep-copying the board every time we explore a new path in a search.

- Originally we were implementing the board using lists instead of dictionaries, and whenever we wanted to obtain a list of available actions it had to generate that list from scratch by looking if a square was empty or test if a piece was able to move in the each direction. Because accessing and testing membership in a list is an O(N) operation in the average case, whereas when using a dictionary accessing and testing membership is O(1) in the average case, there was a dramatic increase in speed when we compare the two models. Furthermore in the original board representation our undo function was quite a bit more complicated and used two seperate stacks to store the eliminated pieces (along with what turn they were eliminated on) and also the move applied to the game. When we wanted to undo an action, we just needed to pop the most recent element off the stack that corresponed to the most recent action and most recent eliminated pieces. Therefore this implementation required a bit more overhead in terms of memory but also because we were using more function calls to update and store these actions/pieces it did impact on the running time as well. There was one advantage to this implementation of the board is that we could do multiple undo-action calls in a row, where as with our current implementation it requires a list of eliminated pieces and the last move to be passed in.

Overall, because we did re-implement the board game using different data structures, we also did notice an increase in performance in negamax calls. We were able to reach depth 2 within 200ms compared to taking around ~1s to do so previously.

### 1.2 The player/s

* Our method implements a range of players that can play the game -- one for each search method we have created. The ones of note are the following:

	*PLAYERS THAT WORK WITH THE CURRENT IMPLEMENTATION*:

	1. Player_Random.py -- a player that just chooses random moves
	2. Player_Manual.py -- a player that accepts user input to what move it is able to make
	3. Player_Negamax.py -- a player that implements the negamax algorithm with greedy heuristics on move evaluation and ordering. This also implements the ActionBook, and transposition tables to help inform decisions.
	5. Player_Negascout.py -- implementation of the negascout algorithm with the greedy heuristics on move evaluation and ordering.
	6. Player_MCTS.py -- Implementation of Monte Carlo Tree Search applied to Watch Your Back 

* The players listed above guided the creation of our final player agent -- Player_Negamax.py which implements the iterative deepening version of negamax (with transposition table) with an opening book of moves.

### 1.3 The search strategy

#### Negamax 

The final search strategy that we chose to implement was the negamax variant of minimax search with alpha beta pruning. We also used iterative deepening combined with a time-cutoff to ensure that we can return the best available move in a given amount of time.

At the start of the game we chose to implement a short "action book" for opening moves of the game to cut down search times and also to maximise the search times for later in the game. We chose to implement this as a dictionary where the key is the board-array string and the value is the position of the piece placement.

Negamax is equivalent to alpha beta but it assumes that the game is a zero-sum two player game such that the following property is held:
```
	max(alpha,beta) = -min(-alpha,-beta)
```

This means we are able to use one function call instead of creating two calls to min_player and max_player, thus simplifying the code implementation, and allows for easier implementation of addition features such are move ordering and transposition tables. 

Negamax also has the same running time as naive alpha beta minimax O(b^d/2). For the game, we realised that the branching factor of the game is quite high (starting at 46 at the beginning of the game and can still be at around 30-35 during mid game assuming you still have most your pieces on the board). This meant that evaluating every move using minimax became unfeasable as even evaluating a move to depth 2 was originally taking 2-3 seconds per turn. Therefore we had to come up with a way to heavily prune the available moves to do search on. To do this we first implemented alpha-beta pruning with the original minimax function that we wrote, which still did not improve the performance of the algorithm significantly. We thought that this was partly because we were just evaluating moves as we saw them (no move ordering). Since alpha-beta pruning works best when you have good move ordering we knew that we needed to try to develop ways to prune out bad moves from the search space. 

In the end we implemented a method which was able to take in the list of legal action, and we applied a light "action"-evaluation function to each of the legal actions and from this we were able to produce a sorted list of moves which we could then iterate on. To our surprise this method of ordering the moves did not produce any noticeable increase in performance. In part, we thought that this was because the cost of sorting a list of actions was O(Nlog(N)), and when combined with evaluating the moves which we assumed to be a O(1) operation, that the total cost of obtaining a list of sorted moves became a [O(Nlog(N)) + O(1)*N ~ O(Nlog(N))] operation. But because negamax/minimax variants are still exponential functions, and that we were doing this trivial ordering at every new state that we searched on, that the added computation of sorting the available moves negates any performance increase from move ordering in alpha-beta-negamax. 

To counteract this we decided to split up the sorted actions list into a list of "favourable" and unfavourable moves. We achei by just taking the first len(actions)/2 or so of the list to evaluate (if there is greater than 16 actions) or the first 10 actions if there is between 10-16 legal actions to make, if the number of legal actions is less than 10 we just evaluate every action. This means that we effective just choose the best moves that we think are good so far and do a search on these actions to pick our best action to make. Effectively this is a greedy approach to reduce the branching factor of the game to make the search more feasible to complete in a reasonable amount of time. When playing an agent that makes random moves we were able to evaluate to depth 3-4 on average in a 900ms time-cutoff. Ideally we thought that we would have gotten to a deeper depth but we thought that due to our board implementation and the cost of move-ordering that this would have been the best strategy we could have come up with in this period of time. Furthermore because we applied this greedy nature of only looing at the best moves you think without looking any further in the game, negamax is no longer an optimal search and transitions into something more in line of a greedy search. 

To help prune more nodes in the tree we also implemented a transposition table inside of negamax. The transposition table is explained below:

#### Transposition table:

- The transposition table is a dictionary in python that stores different board-state, minimax-value/best move key-value pairs such that when we come across a board state, before we evaluate using minimax search we are able to query the table to check whether or not we have seen that state before.
 
- The entry of the transposition table is as follows: 
```
	{(board_bytearray, player_colour): (minimax_value, tt_type, best_move, depth)}

	-> board_bytearray: the byte array representation of that board state 		
	-> tt_type: whether the minimax_value returned was an upper bound, lower bound or an exact value 
	-> best_move: the best move found my minimax to get to that particular state 
	-> depth: depth at which minimax was evaluated at. If we got to a deeper search on the next iteration of iterative deepening, we can rewrite the entry of this board representation 
		

```

- By storing whether the minimax was an alpha, beta cut-off or an PV_node value we are able to either just return the best move/best minimax value from the table for any future serach (if the board state matches an entry), or it can update the values of alpha and beta based on whether the value stored in the transposition table was a beta or alpha cut-off value.

- To maximise the use and efficiency of the table we incrementally fill up the table using iterative deepening search. When we increase the depth of search we always just try the best move that we have found so far to direct our search to deeper levels.

- To reduce branching factor we also attempted to apply symmetries to the byte-array board representation. We did so by the following: when a symmetry was applied to a board representation we checked if the resultant board was in the transposition table. We originally tested for horizontal reflection in both placement and moving phases, and tested vertical, horizontal and rotation in the moving phases. We found that for most cases there was no point in testing for symmetries and reflections in the moving phases as through our simulations we found that it was very rare that we would be able to generate states that were symmetries of other states already in the table. Since the cost of applying a symmetry is O(n^2) and that we would be checking for symmetries at every state, that this was not worth it. We found that we were only finding symmetries in the first few moves of the board game, and hardly any, if any symmetries were found in the moving phase. We decided to not check for any symmetries when checking in the transposition table. The code supplied has the symmetry checking commented out. The relavent methods used for rotation, reflection are still provided.

- We clear the transposition table after every call to find the next move in the placement phase of the game. This is to stop it from growing too big. In the placement phase we do not clear the table. From our tests, the table does not exceed the memory limits of the game when it is not cleared during the moving phase. 


#### Other Search Algorithms That We Explored 

The following describes the other algorithms that we have implemented and trialed: 

* Minimax and Alpha-Beta (Minimax.py, AlphaBetaOptimised.py):

    - This was the starting point of our algorithm. We decided to compact the implementation of minimax using negamax therefore we stopped using this class.

    - Before we switched to using the negamax algorithm, we tried to use the built in python lru_cache to memoize negamax calls. The problem with this was that we did not know if the negamax value returned was an alpha beta cutoff or a PV-node therefore the resulting move returned by the negamax call was not known to be optimal or not. To replace this we decided to implement the transposition table. 

* Negascout / Principal variation search (PVS)

* Monte Carlo Tree Search (MCTS.py)

- Originally we thought that we would use monte carlo tree search as our algorithm for decision making. It works by creating a game-tree on the fly by randomly simulating games and calculating the resultant chance of winning the game by taking a particular action. The algorithm progresses in 4 distinct phases:

	1. Selection: Select the child node that looks the most promising according to a default policy. Here the policy used was the UCB1 (upper confidence bound 1) to select the most promising child node.
	2. Expansion: Once we have selected the child node, we expand that child node by choosing a random action from that childs available actions to make. It creates a new node that corresponds to this action and adds it to this leaf nodes children list.
	3. Simulation: From the newly created node we then simulate the game from this state until we reach terminal state. The winner from this simulation is recorded.
	4. Backpropagation: The values from the simulation are backpropagated back up to the parent node, adjusting every node in the path to the parent along the way.

- This four step process is run multiple times, starting at the root node, until a game tree is built. Then, to choose the action to make, we pick the child of the root node which maxmimses the UCB1 value. I.e. from our current simulation which of the moves are we most comfortable making such that our chances of winning from these board states is maximised. 

- What we discovered was that this MCTS algorithm is dependent on how fast your are able to simulate a game until terminal state, as well as the time that the MCTS algorithm is allowed to run. The longer that the MCTS can take to create a game tree, the better the resulting move should be. What we found, that for a one-second move evaluation, that we were only able to create 10-12 child nodes. 

- The bottleneck in this implementation we found to be the time it takes to simulate the game. When we were using our original board implementation, it took roughly 0.08s to simulate a game to terminal state, therefore 12 nodes were able to be created. This board game at the start has a branching factor of 46, therefore we were not able to create a game tree even to evaluate to one complete layer. Therefore effectively we were just choosing a random move to make. To try improve this, we tried to rewrite the original board implementation to take advantage of dictionaries and sets to update/access the board. By doing so we decreased the amount of time to simulate a game down to 0.04s on average. But this was still way too slow for the generation of decent game tree. Therefore, we stopped exploring this algorithm in favour for negamax and its variants.

- We planned on implementing different rollouts of the game -- i.e. a minimax evaluation to a shallow depth vs a random player to help inform which moves are the best to make, but because the random simluation was taking too long, that we did not even bother with this since this would be taking much longer to evaluate. Maybe if we had 1 hour per move to evaluate we could generate a good enough game tree to inform decision, but sadly this is not feasible. 

### 1.4 Evaluation function

#### BOARD STATE EVALUATION FUNCTION

- Our evaluation function works by returning two vectors that correspond to the number of features that we wish to evaluate. To get the evaluation value we just take the dot product between the weight vector for that function together with the resulting vector of the feature values for the board.

- The features we have implemented in our evaluation are as follows:
    	1. The difference in the number of pieces on the board (EG. WHITE-BLACK)
    	2. Combined distance of all pieces to the centre of the board 
		- This is because we want to be closer to the centre due to the shrinking nature of the board 
	3. The difference in the number of actions a piece can make 
	4. If a piece is surrounded such that it cannot move without being eliminated by an enemy piece 
	5. If an enemy is surround such that it cannot move without being eliminated by our piece 
		- for 4,5 the patterns are shown the comments of the Features.py file 
	6. If we occupy the middle positions
	7. The number of clusters of pieces on the board -- this is defined as being a "block" of 4 pieces in a 2x2 format, therefore we count a 3x3 arrangement of pieces as being 4 contiguous overlapping clusters on the board. 
	8. Edge piece vulnerability -- If pieces are near an edge close to board shrinking, or if it is on a space where it would be eliminated due to board shrinking
		- We try to move out of these situations when this is the case as we need to keep the maximum number of pieces alive 
	9. The difference in the number of pieces of our pieces vs the opponent's that are next to a corner position on the board 
		- We want to maximise the number of enemy pieces next to corners and minimise the number of our pieces next to the corner. This is because being next to a corner puts your piece in a vulnerable position. 
	10. The sum of the minimum manhattan distances of our pieces to an opponent piece 
		- This is a value that represents how close our pieces are to the opponents. Later in the game we want to move our pieces as close as we can to the opponent pieces such that we can play are more offensive game such that we put ourselves in a position to capture them, if we are far away from the opponent we are not able to easily capture the opponet pieces. This function is only evaluated towards the end of the game. 
	11. The difference number of patterns between the two players, of pieces on the board that correspond to guaranteed captures. These specific patters are shown in the comments of the Features.py file. 


#### ACTION EVALUATION FUNCTION FOR GREEDY/NAIVE MOVE ORDERING
- In order to order the legal actions from most favourable to least we applied a "action evaluation to each of the legal actions once generated, we then used those values to order the actions in decreasing values of evaluation. 
- The action evaluation function took the following features into consideration: 
	1. The minimum manhattan distance of that piece being moved is to a opponent piece -- we want to move only the pieces that are close to the enemy piece 
	2. If an action is able to be placed closer to the centre of the board, the higher the weighting will be
	3. If an action can capture an opponent piece -- this is weighted highly
	4. If an action results in self elimination -- this is weighted negatively
	5. If an action can "surround" a piece such that the opponent can't move without being eliminated 
	6. If an action results in a cluster forming on the board 
	7. If an action results in us occupying part of the middle squares -- this is weighted highly as we try to occupy these squares first 
	8. If, in the moving phase we move one of the middle pieces -- ideally we do not want to do this as, therefore we decrease the weight of that action if this occurs 
	9. If we are able to form a pattern that ensures that we can capture a piece on the next move -- i.e. does not matter where the opponent moves or places their piece, we can always capture a piece

#### Machine Learning: 
- We did not successfully implement machine learning to train the weights of our evaluation function as we ran out of time. We implemented the basis for TD-Leaf(Lambda) in the file Learning/Learners.py, although it has not been fully tested yet 

- We actually have created a separate class called xml_helper to help save weights and load weights from an XML file. This class is actually used in our final submission to load the weights for our evaluation function. This allows to easily store and create different weights for our evaluation functions such that we can change it by just changing the file path to the weight-xml file.

- Furthermore by using an XML file to load the weights, we can easily update and save weights generated by machine learning and "incrementally" update the weights as we wish. 

- This technique also would have allowed us to have multiple agents that use the same search strategy with essentially the same evaluation function, except with different weights (via the weight xml files). We could then verse the same agent with each other with two different weights and see whether one function is better than the other. This was we can effectively create slowly refine our evaluation function through machine learning techniques. 

- Sadly we did not have time to fully implement the TD-Leaf(Lambda) algorithm, all that was left to do was to try and return the "best policy vector" from the PV node found in the negamax algorithm such that we could extract the ith-feature for the partial derivative of the reward function, but we did not have time to do this sadly. 
		

### Other creative aspects

- We implemented a simple GUI boardgame app to help visualise the game better -- App.py. This was implemented using tkinter and currently only supports visualising the turn by turn action of AI players. We planned on implementing a feature that allowed for human input such that we could verse our own AI, but we did not have any time to complete this. 



___________________________________________________________________________________________
*COMMENTS.TXT ENDS HERE*
___________________________________________________________________________________________

# PROJECT PART B -- LOG COMMENTS 

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
* Instead of using ML to find the weights for our function -- or before we apply ML, we could create different players whos evaluation function weights are all randomised, we then face them off in a competition, whoever wins we keep their weights, and they verse each other. Ultimately we should end up with a rough idea of what the weights should be. Then we can apply ML to fine-tune those weights.
### TODO 
* Implement 3 types of roll outs for MCTS -- random rollout, light roll out (greedy), medium roll-out (2-ply negamax/ab-minimax)
    - Need to speed up the simulation of the board game because this is the factor that is stopping us from creating a deep game tree in 1 second. 
    - Currently it takes 0.07s to do one game iteration, this is bad because we can theoretically only create 14 nodes in one move iteration. This is not good. 
* We could switch up the search strategy for each phase of the game -- e.g. MCTS for moving phase and AB-Minimax for Placement phase.  
* Need to work out how to use Machine Learning to train the evaluation function 
* Need to work out what the dominant feature of the game are 
* Features to implement:                    
    - Guaranteed capture position patters 
    ```
            W     :----|
            B B   :----|{ this is an example of a guaranteed capture position -- need to scan the entire board for this kind of thing }
              W   :----|
    ```
    - "heat map" of the board -- each location on the board has a weight associated with it -- when our piece is on that position the weight is positive
                - when the enemy is on that position the weight is negative
                - therefore we can get a single number that represents the overall net-state of the board 
* Could implement a different strategy for moving phase vs placing 
    - in placing phase we could put ourselves in a position that is more defensive -- right now we are striving for the middle of the board
* Need to work out if a piece is in an attacking position or defending position 
    - this is important to our evaluation function -- need to classify our pieces into attacking and defending 

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
* Implemented negamax and transposition tables within negamax 