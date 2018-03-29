# WATCH YOUR BACK

## Project A 
### Running the program: 
* To run the program: 
```
    python3 projectA,py < path_to_file
```
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
* Implemented IDDFS search and DLS, now DLS checks for visited nodes in its current call

