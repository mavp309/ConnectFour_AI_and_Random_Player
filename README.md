# ConnectFour_AI_and_Random_Player
This project implements an AI player to play ConnectFour. It also implements a Random player which randomly chooses a move among the valid ones at given point in the game. You can choose to play against AI, Random, or against another human; infact you can even see two AI players play against each other.
## How to run
- Make sure python3 and numpy library is installed in your device.
- run command
  ```Bash
  python3 ConnectFour.py <player1> <player2>
  ```
  where <player1> and <player2> may be among ai, human or random.
  
## Player.py
- Contains classes for running all sorts of players- AI, Human, or Random.
- AI player implementation uses Alpha-Beta Pruning for its move.
- Since it is not possible to explore all outcomes of all valid moves at a given point in game, Iterative Deepening Search is implemented.
- A fixed duration of time is alloted to the AI Player, within which it is explored as many depths as possible and return the best move.

## ConnectFour.py
- Code for simulating the game on a GUI based board, simulate moves on the board each player makes.
