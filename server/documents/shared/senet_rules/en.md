# Rules Of Senet
PlayPalace team, 2026.

## TL;DR
Senet is an ancient Egyptian board game, possibly the oldest board game still played today, with origins dating back over 5,000 years. The famous pharaoh Tutankhamun was buried with Senet boards in his tomb.

Two players race five pieces each along a 30-square S-shaped track, trying to bear them all off the board. Movement is determined by throwing four sticks, and certain rolls grant bonus throws. The board features several special squares with unique effects, including one that sends your piece backward and others that require exact rolls to leave.

## Gameplay
PlayPalace Senet supports **exactly 2 players**.

### Setup
Each player starts with 5 pieces, placed alternately on squares 1 through 10:
* Player 1: squares 1, 3, 5, 7, 9
* Player 2: squares 2, 4, 6, 8, 10

Players are assigned randomly at the start of the game. Player 1 always goes first.

### The Board
The board is a 3-row by 10-column grid. Pieces travel along an S-shaped path:
* Row 1 (top): squares 1 to 10, moving left to right.
* Row 2 (middle): squares 11 to 20, moving right to left.
* Row 3 (bottom): squares 21 to 30, moving left to right.

Both players move in the same direction, from square 1 toward square 30. The board is displayed as a physical grid, so row 2 appears reversed (square 20 on the left, square 11 on the right) to reflect the S-shaped path.

### Throwing Sticks
Instead of dice, Senet uses four throwing sticks, each with a colored side and a black side. On your turn, press Enter on any square to throw. The result depends on how many sticks land colored-side up:

* **1 colored up:** Move 1 square. **Bonus throw!**
* **2 colored up:** Move 2 squares.
* **3 colored up:** Move 3 squares.
* **4 colored up:** Move 4 squares. **Bonus throw!**
* **0 colored up (all black):** Move 5 squares. **Bonus throw!**

When you earn a bonus throw, you move a piece for your current roll, then throw again immediately. Bonus throws can chain: you keep throwing as long as you keep rolling 1, 4, or 5.

### Moving Pieces
After throwing, click on one of your pieces to move it. Each piece has at most one legal destination for a given roll, so clicking your piece moves it immediately.

Movement rules:
* Pieces move forward along the path (toward square 30).
* You may jump over any pieces in your way.
* You cannot land on a square occupied by one of your own pieces.
* If you land on a square occupied by a single opponent piece, you **swap** positions: your piece takes their square, and their piece goes back to where yours came from.
* If you have no legal moves for a roll, you lose that move (but still get a bonus throw if the roll was 1, 4, or 5).

### Protection
Two or more of the same player's pieces on adjacent squares form a protected group. Protected pieces **cannot be captured** (swapped). You cannot land on an opponent piece that is part of a protected group.

Additionally, a line of three or more consecutive opponent pieces completely **blocks passage**. You cannot jump over such a formation.

### Special Squares
Five squares on the board have special properties:

* **Square 15 -- House of Rebirth:** This is the destination for pieces sent back from the House of Water. It has no other special effect.

* **Square 26 -- House of Happiness:** Every piece **must** land here on its way to the end. You cannot jump over square 26. If a roll would carry a piece past square 26 without landing on it, that move is illegal. Once a piece has stopped on square 26, it can move forward normally on a later turn.

* **Square 27 -- House of Water:** Landing here is bad luck. Your piece is immediately sent back to the House of Rebirth (square 15). If square 15 is occupied, your piece goes to the first empty square before it.

* **Square 28 -- House of Three Truths:** Once a piece lands here, it is locked in place and safe from capture. The only way to move it is to bear it off by throwing exactly **3**.

* **Square 29 -- House of Re-Atum:** Same as square 28, but the piece can only be borne off by throwing exactly **2**.

* **Square 30:** A piece here can only be borne off by throwing exactly **1**.

### Bearing Off
Pieces are removed from the board (borne off) from the final squares. Each locked square requires a specific roll:
* From square 28: exactly 3
* From square 29: exactly 2
* From square 30: exactly 1

You cannot bear off from any other square. Pieces must reach these final squares and wait for the correct roll.

### Winning
The first player to bear off all 5 of their pieces wins the game.

## Game Options
* **Bot Difficulty:** The AI difficulty level when playing against a bot. Options are:
    * Random: The bot makes completely random legal moves.
    * Simple: The bot uses heuristic evaluation to pick moves (default).

## Keyboard Shortcuts
Shortcuts specific to Senet:

* **Enter (on any grid square):** Throw sticks (before throwing) or move a piece (during movement).
* **Ctrl+Arrow (Up/Down/Left/Right):** Cycle between your pieces that have legal moves.
* **Alt+Arrow:** Jump to the edge of the current grid row or column.
* **Home / End:** Equivalent to Alt+Left / Right.
* **E:** Check game status (pieces off, current roll).
* **C:** Check current stick throw result.
* **S:** Check score (pieces borne off per player).
* **T:** Check whose turn it is.

## Game Theory / Tips
* **Get through the House of Happiness early.** Every piece must stop on square 26, creating a bottleneck. Moving pieces there sooner gives you more flexibility later.
* **Watch out for the House of Water.** Landing on square 27 sends your piece all the way back to square 15. Plan your moves to avoid it when possible, especially with pieces that have already traveled far.
* **Form protective pairs.** Two adjacent pieces protect each other from capture. Try to advance pieces together rather than spreading them out, especially in areas where your opponent has nearby pieces.
* **Use bonus throws wisely.** Rolls of 1, 4, and 5 grant extra throws. A chain of bonus throws can move a piece a long distance in a single turn. Consider which piece benefits most from each roll in a chain.
* **Block your opponent.** Three or more consecutive pieces form an impassable wall. If you can build a blockade in a strategic location, your opponent's pieces may be stuck for several turns.
* **Swaps can be strategic.** Capturing an opponent's piece sends it to where yours was. If your piece was far behind, the swap hurts your opponent more. Conversely, avoid leaving lone pieces in positions where a swap would benefit your opponent.
* **The endgame is about exact rolls.** Pieces on squares 28, 29, and 30 each need a specific roll to bear off. Having multiple pieces waiting on different locked squares increases your chances of using any given throw productively.
