# WATCH YOUR BACK

## Project A 

### Moves
* Implemented the backend for the game. This includes the moving mechanics and elimination mechanics.
* Implemented certain methods relating to updating the game and getting information about the game 
* Implemented moves functionality by storing then counting the number of available moves each colour player can make.
* This works for supplied inputs 

### Massacre 
* Implemented the node, Massacre classes 
* node is the structure to store each game board such that we are able to search through different configurations via graph traversal algorithms.
* node also includes certain evaluation functions to evualute which states are better than others. Note currently that the countNum() method is the best evaluation function that has been implemented so far. 
* Implemented the Massacre class. This is the searching class that has implementations of Breadth First Search, an iteration of Greedy First Search using a heap based priority queue, Depth Limited Search and Iterative Deepenign Depth First Search have been fully implemented. Note that Greedy Search has been the most efficient so far, but it does not provide the most optimal path. Since all path calls are of cost 1 (can only move once during a move), therefore both IDDFS and also Breadth first search will return optimal paths, but each has big limitations in terms of time and speed. 
* Still need to implement Depth First Search into this class

#### TODO 
* Need to test with more input cases 
* Work out the edge cases 
* Clean up code and rename some variables such as piecePos and oppPiecePos to something that is relevant. PiecePos is not a good name because it shares an instance variable of the same name where when not used in that context it means the current players piece position instead of the opposition piece colour. 
* Need to implement A* search and to also think of dominant and admissable heuristics to help more effectively search the structure. 
