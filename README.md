# python-klondike-solver-ai

The first algorithm of solving is a heuristic one. Every possible moves have a number that characterize the best move. The second algorithm, called “rollout algorithm”, try several combination of moves and execute the one that has the most priority.

Klondike's rule

There is different stacks : the pile, the talon, the suits stacks, the build stacks. The game is over when all the cards of the 4 colors are stacked on the 4 suits stacks on the top left, from ace to king. If the game is in a dead-end, the player lost the game. During the game, the player can stack any card on top of a suit stack if that card is of the same color and superior to the one on the suit stack. The player can also put a card on a build stack if this card is inferior and of the opposite color. The talon can give 3 faced up card to the pile, only the one on the top is movable. At the beginning, all the suit stacks and the pile are empty. The 7 build stack have one to seven card, the card at the top is the only one faced up.

Structure of the program

The program is coded in Python 3. It consists of 2 classes :
•	Game : represent the game and contains the 2 algorithms.
•	Window : the definition of the Tkinter UI used to see the evolution of the game, turn by turn.

The game is stored in a list of lists of tuples. Each cells represent one stack, the pile or the talon.
The user can modify the content of main.py to either use the rollout or the heuristic strategy. It is also possible to not display the window in order to play as many games as possible.

The hardest part was to detect whether the game is in a dead end, or not. To do that, the function defeat() of Game, checks if a card or a set of cards is always moved between the two same stacks. It checks also if a card of the build stacks has been recently turned faced up, or for the talon, recently uncovered.
Even though the function detect most of the dead ends, there’s still some undetected ones. In this case, the game is running indefenitly. This is why in the simulations I also counted the games that takes too much time.

Heuristic strategy

With this strategy every possible moves have a heuristic value. This value serve as priority for the computer to choose which move to perform. The value can be found in the article. The possibles moves are: from build to build stack, from build to suit stack, from talon to build stack, from talon to suits stack. Only the move from suit stack to build stack is not considered in my version of the game, to simplify the detection of the defeat.

The algorithm of play with this method is this one :
1.	The computer get every possibles moves
2.	The first priority criterion are applied
3.	If there's several moves at the maximum priority, we apply the second priority criterion
4.	If there's still several moves at the maximum priority, the computer choose a random one. Otherwise, it play the move with the highest priority.

With this heuristic strategy, out of 1000 game, 150 were won, 829 were lost and 21 were taking too much time to be taken into account.

This proportion is close to the proportion obtained by the team of researchers.

Rollout strategy

The rollout strategy can’t really be applied to the klondike game, because it is working with series of trial and restore of the game. But still it’s interesting to now the result and the success rate of this algorithm.

My implementation is using the heuristics of the moves, used in the first part of my project. Let’s consider that the game is at the state n, the computer follow this process:

1.	Find the moves : n
2.	Execute one move : n+1
3.	Find the moves : n+1
4.	Execute one move : n+2, and so on...
5.	If the number of moves has been reached, save the move list and go back to step 1.
6.	If all the possibles series of moves has been checked, execute the one that has the maximum priority

For 2 rollout, out of 1000 games, 130 were won, 851 were lost and 19 took too much time. For 3 rollout, out of 1000 games, 132 were won, 839 were lost and 29 took too much time. In the article, the success rate with 2 rollout is close to 50%, and greater than 50% with 3 rollouts.

The team don’t details how the computer choose which move to perform, so I applied the heuristic of the first algorithm. Each move of a serie is evaluated. The value of the serie is equal to the sum of all values of each move of the serie. The computer play the serie of move that has the maximum value. I also tried to evaluate the serie of move by counting the number of cards on the suits stack, but the ratio of game won was even smaller.

The code part is done, the heuristic algorithm is working and give expected results. Even though the rollout algorithm is working, the evaluation function of the series of moves is not working has expected because the ratio of games won seems to be the same as the one with the heuristic strategy. A more complete evaluation function has to be created.
