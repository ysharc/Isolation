## Introduction

Isolation is a deterministic, two-player game of perfect information in which the players alternate turns moving a single piece from one cell to another on a board.  Whenever either player occupies a cell, that cell becomes blocked for the remainder of the game.  The first player with no remaining legal moves loses, and the opponent is declared the winner.  These rules are implemented in the `isolation.Board` class provided in the repository.

This project uses a version of Isolation where each agent is restricted to L-shaped movements (like a knight in chess) on a rectangular grid (like a chess or checkerboard).  The agents can move to any open cell on the board that is 2-rows and 1-column or 2-columns and 1-row away from their current position on the board. Movements are blocked at the edges of the board (the board does not wrap around), however, the player can "jump" blocked or occupied spaces (just like a knight in chess).

Additionally, agents will have a fixed time limit each turn to search for the best move and respond.  If the time limit expires during a player's turn, that player forfeits the match, and the opponent wins.

## Getting Started
Use python3 while following the instructions below.

```
git clone https://github.com/ysharc/Isolation.git
cd Isolation
```

### Testing the Game Agent

1. Run the sample players script and copy the move history at the end of the play.
```
python sample_players.py
```

2. Run the visualization server 
```
cd isoviz
python -m http.server
```

3. Open http://localhost:8000/ and paste the move history here and run game.

### Modifying Game Agent

If you want to implement your own heuristic for the game agent modify `custom_score` in `game_agent.py`

To test your agent against various other agents run the tournament.
```
python tournament.py
``` 

For a single game play follow the instructions in the previous section. 
