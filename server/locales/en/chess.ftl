# Chess

game-name-chess = Chess

# Options
chess-set-turn-timer = Turn timer: { $mode }
chess-select-turn-timer = Select turn timer
chess-option-changed-turn-timer = Turn timer set to { $mode }.

chess-toggle-auto-draw = Auto-draw on repetition/50 moves: { $enabled }
chess-option-changed-auto-draw = Auto-draw { $enabled }.

chess-toggle-show-coordinates = Show coordinates in moves: { $enabled }
chess-option-changed-show-coordinates = Show coordinates { $enabled }.

# Game start
chess-game-started = { $white } is white, { $black } is black. White moves first.

# Turn / move messages
chess-you-select = Selected { $piece } at { $square }. Click destination.
chess-no-piece = No piece to select there.
chess-move-cancelled = Move cancelled.
chess-illegal-move = Illegal move.

chess-you-move = You move { $piece } from { $from } to { $to }.
chess-player-moves = { $player } moves { $piece } from { $from } to { $to }.
chess-you-capture = You capture { $captured } on { $to } with { $piece } from { $from }.
chess-player-captures = { $player } captures { $captured } on { $to } with { $piece } from { $from }.

chess-you-en-passant = You capture en passant on { $to } with pawn from { $from }.
chess-player-en-passant = { $player } captures en passant on { $to } with pawn from { $from }.

chess-you-castle-kingside = You castle kingside.
chess-player-castles-kingside = { $player } castles kingside.
chess-you-castle-queenside = You castle queenside.
chess-player-castles-queenside = { $player } castles queenside.

chess-you-promote = You promote pawn to { $piece } on { $square }.
chess-player-promotes = { $player } promotes pawn to { $piece } on { $square }.

# Check / checkmate / draw
chess-check = Check!
chess-checkmate = Checkmate! { $winner } wins.
chess-you-win-checkmate = Checkmate! You win.
chess-stalemate = Stalemate. The game is a draw.
chess-draw-fifty = Draw by fifty-move rule.
chess-draw-repetition = Draw by threefold repetition.
chess-draw-material = Draw by insufficient material.
chess-draw-agreement = Draw by agreement.

# Resign
chess-resign = Resign
chess-resign-confirm = Are you sure you want to resign?
chess-resign-yes = Yes, resign
chess-resign-no = No, keep playing
chess-you-resign = You resign. { $opponent } wins.
chess-player-resigns = { $player } resigns. { $opponent } wins.

# Draw offer
chess-offer-draw = Offer draw
chess-you-offer-draw = You offer a draw.
chess-player-offers-draw = { $player } offers a draw.
chess-you-accept-draw = You accept the draw.
chess-player-accepts-draw = { $player } accepts the draw.
chess-you-decline-draw = You decline the draw.
chess-player-declines-draw = { $player } declines the draw.
chess-no-draw-offer = There is no draw offer to respond to.
chess-already-offered = You have already offered a draw.

# Undo
chess-undo-request = Undo last move
chess-you-request-undo = You request to undo the last move.
chess-player-requests-undo = { $player } requests to undo the last move.
chess-you-accept-undo = You accept the undo.
chess-player-accepts-undo = { $player } accepts the undo. Move undone.
chess-you-decline-undo = You decline the undo.
chess-player-declines-undo = { $player } declines the undo request.
chess-no-undo-request = There is no undo request to respond to.
chess-no-moves-to-undo = There are no moves to undo.
chess-already-requested-undo = You have already requested an undo.
chess-undo-applied = Last move undone. It is now { $player }'s turn.

# Promotion
chess-select-promotion = Select promotion piece

# View board
chess-view-board = View board
chess-flip-board = Flip board
chess-viewer-own = your
chess-viewer-opponent = opponent's
chess-board-flipped = Flipped board to view { $viewer } perspective ({ $color }).
chess-board-rank = Rank { $rank }: { $pieces }
chess-empty = empty
chess-board-header = Board state:

# Status / scores
chess-status-white = White: { $player }
chess-status-black = Black: { $player }
chess-status-turn = Turn: { $color }
chess-status-move-count = Moves: { $count }
chess-check-status = Check game status

# Type move
chess-type-move = Type a move
chess-enter-move = Enter move (e.g. e2-e4, o-o, o-o-o)
chess-move-parse-error = Could not understand that move. Try e2-e4, pe2-e4, o-o, or o-o-o.

# FEN
chess-import-fen = Import FEN
chess-enter-fen = Paste FEN string
chess-fen-loaded = FEN loaded successfully.
chess-fen-error = Error loading FEN.

# Piece names
chess-piece-pawn = pawn
chess-piece-knight = knight
chess-piece-bishop = bishop
chess-piece-rook = rook
chess-piece-queen = queen
chess-piece-king = king

# Piece grammatical gender (m = masculine, f = feminine)
# Translators: change these to match the grammatical gender in your language.
chess-piece-pawn-gender = m
chess-piece-knight-gender = m
chess-piece-bishop-gender = m
chess-piece-rook-gender = m
chess-piece-queen-gender = f
chess-piece-king-gender = m

# Timer
chess-check-turn-timer = Turn timer
chess-turn-timeout = Time's up!

# Timer choice labels (game-specific durations)
chess-timer-120 = 2 minutes
chess-timer-180 = 3 minutes
chess-timer-300 = 5 minutes
