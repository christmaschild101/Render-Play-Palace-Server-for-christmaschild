"""Chess bot AI with material and positional evaluation."""

from __future__ import annotations

from typing import TYPE_CHECKING
import random

if TYPE_CHECKING:
    from .game import ChessGame, ChessPlayer

# Piece values for evaluation
PIECE_VALUES = {
    "pawn": 100,
    "knight": 320,
    "bishop": 330,
    "rook": 500,
    "queen": 900,
    "king": 20000,
}

# Piece-square tables (encourage good positioning)
# Indexed [rank*8 + file] from white's perspective
PAWN_TABLE = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    50,
    10,
    10,
    20,
    30,
    30,
    20,
    10,
    10,
    5,
    5,
    10,
    25,
    25,
    10,
    5,
    5,
    0,
    0,
    0,
    20,
    20,
    0,
    0,
    0,
    5,
    -5,
    -10,
    0,
    0,
    -10,
    -5,
    5,
    5,
    10,
    10,
    -20,
    -20,
    10,
    10,
    5,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]

KNIGHT_TABLE = [
    -50,
    -40,
    -30,
    -30,
    -30,
    -30,
    -40,
    -50,
    -40,
    -20,
    0,
    0,
    0,
    0,
    -20,
    -40,
    -30,
    0,
    10,
    15,
    15,
    10,
    0,
    -30,
    -30,
    5,
    15,
    20,
    20,
    15,
    5,
    -30,
    -30,
    0,
    15,
    20,
    20,
    15,
    0,
    -30,
    -30,
    5,
    10,
    15,
    15,
    10,
    5,
    -30,
    -40,
    -20,
    0,
    5,
    5,
    0,
    -20,
    -40,
    -50,
    -40,
    -30,
    -30,
    -30,
    -30,
    -40,
    -50,
]

BISHOP_TABLE = [
    -20,
    -10,
    -10,
    -10,
    -10,
    -10,
    -10,
    -20,
    -10,
    0,
    0,
    0,
    0,
    0,
    0,
    -10,
    -10,
    0,
    10,
    10,
    10,
    10,
    0,
    -10,
    -10,
    5,
    5,
    10,
    10,
    5,
    5,
    -10,
    -10,
    0,
    10,
    10,
    10,
    10,
    0,
    -10,
    -10,
    10,
    10,
    10,
    10,
    10,
    10,
    -10,
    -10,
    5,
    0,
    0,
    0,
    0,
    5,
    -10,
    -20,
    -10,
    -10,
    -10,
    -10,
    -10,
    -10,
    -20,
]

ROOK_TABLE = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    5,
    10,
    10,
    10,
    10,
    10,
    10,
    5,
    -5,
    0,
    0,
    0,
    0,
    0,
    0,
    -5,
    -5,
    0,
    0,
    0,
    0,
    0,
    0,
    -5,
    -5,
    0,
    0,
    0,
    0,
    0,
    0,
    -5,
    -5,
    0,
    0,
    0,
    0,
    0,
    0,
    -5,
    -5,
    0,
    0,
    0,
    0,
    0,
    0,
    -5,
    0,
    0,
    0,
    5,
    5,
    0,
    0,
    0,
]

QUEEN_TABLE = [
    -20,
    -10,
    -10,
    -5,
    -5,
    -10,
    -10,
    -20,
    -10,
    0,
    0,
    0,
    0,
    0,
    0,
    -10,
    -10,
    0,
    5,
    5,
    5,
    5,
    0,
    -10,
    -5,
    0,
    5,
    5,
    5,
    5,
    0,
    -5,
    0,
    0,
    5,
    5,
    5,
    5,
    0,
    -5,
    -10,
    5,
    5,
    5,
    5,
    5,
    0,
    -10,
    -10,
    0,
    5,
    0,
    0,
    0,
    0,
    -10,
    -20,
    -10,
    -10,
    -5,
    -5,
    -10,
    -10,
    -20,
]

KING_TABLE_MIDGAME = [
    -30,
    -40,
    -40,
    -50,
    -50,
    -40,
    -40,
    -30,
    -30,
    -40,
    -40,
    -50,
    -50,
    -40,
    -40,
    -30,
    -30,
    -40,
    -40,
    -50,
    -50,
    -40,
    -40,
    -30,
    -30,
    -40,
    -40,
    -50,
    -50,
    -40,
    -40,
    -30,
    -20,
    -30,
    -30,
    -40,
    -40,
    -30,
    -30,
    -20,
    -10,
    -20,
    -20,
    -20,
    -20,
    -20,
    -20,
    -10,
    20,
    20,
    0,
    0,
    0,
    0,
    20,
    20,
    20,
    30,
    10,
    0,
    0,
    10,
    30,
    20,
]

PST = {
    "pawn": PAWN_TABLE,
    "knight": KNIGHT_TABLE,
    "bishop": BISHOP_TABLE,
    "rook": ROOK_TABLE,
    "queen": QUEEN_TABLE,
    "king": KING_TABLE_MIDGAME,
}


def _pst_index(sq_index: int, color: str) -> int:
    """Convert board index to piece-square table index."""
    rank = sq_index // 8
    file = sq_index % 8
    if color == "white":
        return (7 - rank) * 8 + file
    else:
        return rank * 8 + file


def _score_move(game: "ChessGame", move: dict, color: str) -> int:
    """Score a single move for the bot without deep search.

    Considers:
    - Material gain from captures (MVV-LVA)
    - Positional improvement (piece-square table delta)
    - Check bonus
    - Castling bonus
    - Pawn promotion bonus
    """
    from_sq = move["from"]
    to_sq = move["to"]
    piece = game.board[from_sq]
    target = game.board[to_sq]
    score = 0

    if not piece:
        return 0

    piece_type = piece["piece"]

    # Capture value (MVV-LVA: prioritize capturing high-value pieces with low-value pieces)
    if target:
        score += PIECE_VALUES.get(target["piece"], 0) * 10 - PIECE_VALUES.get(piece_type, 0)

    # En passant capture
    if piece_type == "pawn" and to_sq == game.en_passant_target:
        score += PIECE_VALUES["pawn"] * 10

    # Positional improvement from piece-square tables
    pst = PST.get(piece_type)
    if pst:
        old_pst = pst[_pst_index(from_sq, color)]
        new_pst = pst[_pst_index(to_sq, color)]
        score += (new_pst - old_pst) * 2

    # Castling bonus
    if piece_type == "king":
        file_diff = abs((to_sq % 8) - (from_sq % 8))
        if file_diff == 2:
            score += 60  # Encourage castling

    # Pawn promotion bonus
    if piece_type == "pawn":
        to_rank = to_sq // 8
        if (color == "white" and to_rank == 7) or (color == "black" and to_rank == 0):
            score += PIECE_VALUES["queen"]

    # Check bonus: simulate and see if move gives check
    saved = game.save_position()
    game.execute_move_silent(from_sq, to_sq)
    opponent = "black" if color == "white" else "white"
    if game.is_in_check(opponent):
        score += 50
    game.restore_position(saved)

    # Small random factor to vary play
    score += random.randint(-5, 5)  # nosec B311

    return score


def find_best_move(game: "ChessGame", player: "ChessPlayer") -> dict | None:
    """Find the best move using single-ply evaluation."""
    moves = game.get_legal_moves(player.color)
    if not moves:
        return None

    scored_moves = []
    for move in moves:
        score = _score_move(game, move, player.color)
        scored_moves.append((score, move))

    scored_moves.sort(key=lambda x: x[0], reverse=True)

    # Pick from top moves with some randomness for variety
    top_score = scored_moves[0][0]
    top_moves = [m for s, m in scored_moves if s >= top_score - 20]

    return random.choice(top_moves)  # nosec B311


def bot_think(game: "ChessGame", player: "ChessPlayer") -> str | None:
    """Decide what action the bot should take."""
    if game.promotion_pending:
        return "promote_queen"

    if game.draw_offer_from and game.draw_offer_from != player.id:
        # Accept draw if losing material
        my_material = sum(
            PIECE_VALUES.get(game.board[i]["piece"], 0)
            for i in range(64)
            if game.board[i] and game.board[i]["color"] == player.color
        )
        opp_material = sum(
            PIECE_VALUES.get(game.board[i]["piece"], 0)
            for i in range(64)
            if game.board[i] and game.board[i]["color"] != player.color
        )
        if my_material < opp_material - 200:
            return "accept_draw"
        return "decline_draw"

    if game.undo_request_from and game.undo_request_from != player.id:
        return "decline_undo"

    if game.current_player != player:
        return None

    move = find_best_move(game, player)
    if move is not None:
        return f"square_{move['from']}_{move['to']}"

    return None
