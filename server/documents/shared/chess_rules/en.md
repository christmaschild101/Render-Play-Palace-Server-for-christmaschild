# Rules Of Chess
PlayPalace team, 2026.

## TL;DR
Chess is the classic two-player strategy board game. Each player commands an army of 16 pieces on an 8-by-8 board. The goal is to checkmate your opponent's king, meaning their king is under attack and cannot escape. PlayPalace's implementation uses an accessible grid mode so you can navigate the board spatially with arrow keys, and every piece, move, and game event is announced through speech output.

## Gameplay
Chess is played between two players. One plays white, the other plays black. Colors are assigned randomly at the start of each game. White always moves first.

### The Board
The board is an 8-by-8 grid. Columns are called files and are labeled A through H from left to right. Rows are called ranks and are numbered 1 through 8 from bottom to top. Each square is identified by its file letter and rank number, for example E4 or A1. White's pieces start on ranks 1 and 2; black's pieces start on ranks 7 and 8.

### The Pieces
Each player starts with 16 pieces:

* **King** -- The most important piece. It can move one square in any direction: horizontally, vertically, or diagonally. If your king is checkmated, you lose.
* **Queen** -- The most powerful piece. It can move any number of squares horizontally, vertically, or diagonally, as long as no piece blocks its path.
* **Rook** -- Moves any number of squares horizontally or vertically, as long as no piece blocks its path. Each player starts with two rooks.
* **Bishop** -- Moves any number of squares diagonally, as long as no piece blocks its path. Each player starts with two bishops. One bishop starts on a light square and one on a dark square, so they always cover different colors.
* **Knight** -- Moves in an L-shape: two squares in one direction and one square perpendicular, or vice versa. The knight is the only piece that can jump over other pieces. Each player starts with two knights.
* **Pawn** -- Moves forward one square, but captures diagonally one square forward. On its first move, a pawn may advance two squares. Pawns cannot move backward. Each player starts with eight pawns.

### Starting Position
Rank 1 (white) and rank 8 (black) hold the major pieces from left to right: rook, knight, bishop, queen, king, bishop, knight, rook. The queen starts on her own color (white queen on a light square, black queen on a dark square). All pawns line up on rank 2 (white) and rank 7 (black).

### Making a Move
Moves use a two-click system. First, select the piece you want to move by clicking on its square. You will hear a confirmation announcing which piece you selected and its location. Then, click the destination square. If the move is legal, the piece moves and the appropriate sound plays. If the move is illegal, you hear a notification and can try again.

To cancel a selection, click the same square again. You will hear a cancellation confirmation and can start over.

### Capturing
When you move a piece to a square occupied by an opponent's piece, you capture that piece and remove it from the board. The game announces what you captured and plays a capture sound.

### Special Moves

**Castling:** A special move involving the king and one rook. The king moves two squares toward a rook, and the rook jumps to the square the king crossed. Castling is only legal when:
* Neither the king nor the rook involved has moved previously.
* There are no pieces between the king and the rook.
* The king is not currently in check.
* The king does not pass through or land on a square attacked by an opponent's piece.

Kingside castling moves the king from E1 to G1 (or E8 to G8 for black), with the rook going from H1 to F1 (or H8 to F8). Queenside castling moves the king from E1 to C1 (or E8 to C8), with the rook going from A1 to D1 (or A8 to D8).

**En passant:** If a pawn advances two squares from its starting position and lands beside an opponent's pawn, the opponent may capture it as if it had only moved one square. This capture must be made immediately on the very next move or the right is lost.

**Pawn promotion:** When a pawn reaches the opposite end of the board (rank 8 for white, rank 1 for black), it must be promoted to another piece. You choose from queen, rook, bishop, or knight. You can use the keyboard shortcuts Q, R, Shift+B, or K to promote quickly.

### Check, Checkmate, and Draws

**Check:** When a king is under direct attack, the player is in check. You must get out of check on your next move, either by moving the king, blocking the attack, or capturing the attacking piece. The game announces check with a sound and a spoken alert.

**Checkmate:** If a player is in check and has no legal move to escape, that player is checkmated and loses the game. A checkmate sound plays and the winner is announced.

**Stalemate:** If a player is not in check but has no legal moves, the game is a draw by stalemate.

**Other draws:**
* **Fifty-move rule:** If 50 consecutive moves pass with no pawn move and no capture, the game is automatically drawn (when auto-draw is enabled).
* **Threefold repetition:** If the same board position occurs three times, the game is automatically drawn (when auto-draw is enabled).
* **Insufficient material:** If neither player has enough pieces to deliver checkmate (for example, king versus king, or king and bishop versus king), the game is automatically drawn.
* **Draw by agreement:** Either player may offer a draw. If the opponent accepts, the game ends in a draw.

### Resigning and Undo
You may resign at any time, conceding the game to your opponent. You can also request to undo the last move; your opponent must accept the request for the undo to take effect.

### FEN Import
You can import a board position using FEN (Forsyth-Edwards Notation). Press I to open the FEN editor, paste a FEN string, and submit. This is useful for studying specific positions or resuming games from a known state.

### Turn Timer
When a turn timer is active, you have a set number of seconds to make your move. A warning sound plays when 5 seconds remain. If time runs out, the game automatically makes a move for you using the bot engine.

### Customizable Options
The host can configure the following settings before the game starts:

* **Turn Timer:** Sets a time limit per move. Options are 15 seconds, 30 seconds, 45 seconds, 1 minute, 1.5 minutes, 2 minutes, 3 minutes, 5 minutes, or unlimited. Defaults to unlimited.
* **Auto-draw on repetition/50 moves:** When enabled, the game automatically declares a draw for threefold repetition and the fifty-move rule. When disabled, these conditions are ignored and play continues. Defaults to enabled.
* **Show coordinates in moves:** When enabled, move announcements include square coordinates (for example, "E2 to E4"). Defaults to enabled.

## Keyboard Shortcuts
The board is presented as an 8-by-8 grid. You navigate it using arrow keys:

* **Arrow keys:** Move between squares on the board. Left and right move along the file (A through H). Up and down move along the rank (1 through 8).
* **Enter or Space:** Select the focused square. Use this to pick up a piece (first click) and then to place it (second click).
* **B:** View the full board state. Reads out every rank from 8 to 1, listing what is on each square.
* **S:** Check game status. Announces who is white, who is black, whose turn it is, and the move count.
* **Shift+F:** Flip the board orientation. By default, if you are playing as white, rank 1 is at the bottom (white's perspective). Flipping puts rank 8 at the bottom (black's perspective). This is the default view if you are playing as black. This only affects your view, not the game itself.
* **Shift+D:** Offer a draw to your opponent.
* **Y:** Accept a pending draw offer or undo request.
* **N:** Decline a pending draw offer or undo request.
* **Shift+U:** Request to undo the last move.
* **Shift+R:** Resign the game.
* **Shift+T:** Check how much time remains on the turn timer.
* **I:** Import a FEN position.
* **Q:** Promote pawn to queen (when a promotion is pending).
* **R:** Promote pawn to rook (when a promotion is pending).
* **Shift+B:** Promote pawn to bishop (when a promotion is pending).
* **K:** Promote pawn to knight (when a promotion is pending).
* **M:** Type a move. Opens an edit box allowing you to type your move. You can type a move in the most common universally accepted Chess notations:
    * ***e2e4***.
    * ***pe2e4***.
    * ***o-o or o-o-o*** King side and queen side castling.
    * ***e1g1/e1c1 or e8g8/e8c8*: another alternative way for king side and queen side castling.
    * In all cases, you can optionally enter a dash between the starting and the destination square to clearly separate them.



### How Grid Navigation Works
When it is your turn, the board is displayed as a grid of 64 squares. Your screen reader will announce the content of each square as you move to it. Squares containing pieces are announced with their color and piece type, such as "E2: white pawn." Empty squares are announced by their coordinate alone, such as "E4."

When you have selected a piece, its square label changes to include brackets, for example "[E2: white pawn]," so you can confirm your selection as you navigate.

The grid is 8 columns wide. Pressing right from H moves to A of the next rank; pressing left from A moves to H of the previous rank. This lets you traverse the entire board fluidly.

By default the board is oriented from white's perspective: rank 8 (black's back rank) is at the top and rank 1 (white's back rank) is at the bottom. Use Shift+F to flip this if you prefer to navigate from black's perspective.

## Game Theory / Tips
* **Control the center.** Pieces in the center of the board (especially E4, D4, E5, D5) have more mobility and influence. Open with moves like E4 or D4 to stake out central territory.
* **Develop your pieces early.** Get your knights and bishops off the back rank in the opening. Each move spent on something other than development gives your opponent more room to breathe.
* **Castle early.** Castling tucks your king behind a wall of pawns and connects your rooks. Delaying castling leaves your king exposed.
* **Do not bring your queen out too early.** The queen is powerful but vulnerable to being chased by less valuable pieces, wasting your tempo.
* **Think about pawn structure.** Pawns cannot move backward. Doubled pawns (two pawns on the same file), isolated pawns (no friendly pawns on adjacent files), and backward pawns (stuck behind enemy pawns) are all weaknesses.
* **Piece value as a rough guide:** Pawn = 1, knight = 3, bishop = 3, rook = 5, queen = 9. Trading a bishop for a rook (gaining 2 points of material) is usually favorable. Sacrificing material is only worth it if you get a concrete tactical advantage.
* **Look for tactics.** Forks (one piece attacking two targets), pins (a piece cannot move because it would expose a more valuable piece), and skewers (attacking a valuable piece that must move, exposing a less valuable piece behind it) win material.
* **In the endgame, activate your king.** Once most pieces are off the board, the king becomes a strong piece. March it toward the center to support your pawns.
* **Use the board view (B key) when you lose track of the position.** It reads every rank top to bottom, giving you a full picture of the board at any time.
* **With a turn timer active, premove in your head.** While your opponent is thinking, plan your response so you can execute it quickly when your turn comes.
