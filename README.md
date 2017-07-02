Genetic Algorithm that learns to identify various signals

genetic.py is a handler script which generates neural network players, execute signal tests, records the winners, ranks the players, generates new players
from the 'genes', in this case net weights, of the top players and then starts this process again. The player class sets up a neural network
player initialised with either random or provided weights. The neural networks have been designed so that the number and width of layers
can be increased as desired. 'Children' are created by uniform crossover with a probabilty of 0.5 and with a mutation probibility of
1/length(weights)


graph.py is a script that plots out the results of the currently stored data. Current graphs show interesting progression with new generations of players consistently beating their older counterparts.

