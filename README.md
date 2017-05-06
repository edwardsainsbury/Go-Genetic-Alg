Genetic Algorithm that learns to play the game of GO.

genetic.py is a handler script which generates neural network players, execute rounds of go, records the winners, ranks the players, generates new players
from the 'genes', in this case net weights, of the top players and then starts this process again. The player class sets up a neural network
player initialised with either random or provided weights. The neural networks have been designed so that the number and width of layers
can be increased as desired. 'Children' are created by uniform crossover with a probabilty of 0.5 and with a mutation probibility of
1/length(weights)

go.py is a script found on the internet - 
(all credit to http://www.codercaste.com/2013/02/22/read-set-go-how-to-create-a-go-board-game-in-python/) - that takes an keyboard input
to play a game of go. I have adapted this script to allow the neural network players interface with this script. I have added logic to 
ignore valid moves and scroll though the players output until a valid move is found.

Current Limitations:
- With 4 players and two players and two children being carried over to the next generation, result coverages to the point where players 
  are identical except for their single mutation. Could remedy by increasing number of players and including a 'wildcard' each round
- Runtime is pretty slow with one generation taking significant time even with only 4 players. Number of rounds per era = n!/(n-2)! = n^2-n
  so runtime will explode as number of players increases. More players is obviously prefereable so runtime/round must be addressed.

Future Improvements:
- Addition of sql server to store scores and weights of players. This would allow an standalone script to graph results more effectively 
  and to allow the saving and loading of players. This would allow progress to continue over multiple executions rather than starting fresh
  each exectuion.
- Rewriting go.py and genetic.py in C/C++. This will dramatic increase runtime which is a current issue.
