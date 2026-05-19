"""Tests for Senet."""

import json
import pytest

from server.games.senet.state import (
    SenetGameState,
    NUM_SQUARES,
    PIECES_PER_PLAYER,
    HOUSE_REBIRTH,
    HOUSE_HAPPINESS,
    HOUSE_WATER,
    HOUSE_THREE_TRUTHS,
    HOUSE_RE_ATUM,
    EXACT_BEAROFF,
    SAFE_SQUARES,
    build_initial_state,
    find_rebirth_square,
    has_blocking_line,
    is_protected,
    opponent_num,
    pieces_remaining,
    throw_sticks,
)
from server.games.senet.moves import (
    SenetMove,
    apply_move,
    generate_legal_moves,
    has_any_legal_move,
)
from server.games.senet.bot import _score_move
from server.games.senet.game import SenetGame, SenetOptions
from server.core.users.bot import Bot


# ==========================================================================
# State tests
# ==========================================================================


class TestInitialState:
    def test_alternating_pieces(self):
        gs = build_initial_state()
        for i in range(10):
            expected = 1 if i % 2 == 0 else 2
            assert gs.board[i] == expected, f"Square {i+1} should be player {expected}"
        for i in range(10, 30):
            assert gs.board[i] == 0, f"Square {i+1} should be empty"

    def test_no_pieces_off(self):
        gs = build_initial_state()
        assert gs.off == [0, 0, 0]

    def test_initial_phase(self):
        gs = build_initial_state()
        assert gs.turn_phase == "throwing"
        assert gs.current_player_num == 1
        assert gs.current_roll == 0

    def test_five_pieces_per_player(self):
        gs = build_initial_state()
        assert pieces_remaining(gs, 1) == 5
        assert pieces_remaining(gs, 2) == 5


class TestHelpers:
    def test_opponent_num(self):
        assert opponent_num(1) == 2
        assert opponent_num(2) == 1

    def test_throw_sticks_range(self):
        import random
        rng = random.Random(42)
        values = set()
        for _ in range(500):
            val, bonus = throw_sticks(rng)
            assert 1 <= val <= 5
            values.add(val)
            if val in (1, 4, 5):
                assert bonus is True
            else:
                assert bonus is False
        assert values == {1, 2, 3, 4, 5}

    def test_is_protected_pair(self):
        board = [0] * 30
        board[5] = 1
        board[6] = 1
        assert is_protected(board, 5) is True
        assert is_protected(board, 6) is True

    def test_is_protected_gap(self):
        board = [0] * 30
        board[5] = 1
        board[7] = 1
        assert is_protected(board, 5) is False
        assert is_protected(board, 7) is False

    def test_is_protected_empty(self):
        board = [0] * 30
        assert is_protected(board, 5) is False

    def test_blocking_line_three(self):
        board = [0] * 30
        board[10] = 2
        board[11] = 2
        board[12] = 2
        assert has_blocking_line(board, 8, 14, 1) is True

    def test_no_blocking_line_two(self):
        board = [0] * 30
        board[10] = 2
        board[11] = 2
        assert has_blocking_line(board, 8, 14, 1) is False

    def test_blocking_line_own_pieces_dont_block(self):
        board = [0] * 30
        board[10] = 1
        board[11] = 1
        board[12] = 1
        assert has_blocking_line(board, 8, 14, 1) is False

    def test_find_rebirth_square_empty(self):
        board = [0] * 30
        assert find_rebirth_square(board) == HOUSE_REBIRTH

    def test_find_rebirth_square_occupied(self):
        board = [0] * 30
        board[HOUSE_REBIRTH] = 1
        result = find_rebirth_square(board)
        assert result < HOUSE_REBIRTH
        assert board[result] == 0

    def test_find_rebirth_square_chain_occupied(self):
        board = [0] * 30
        board[HOUSE_REBIRTH] = 1
        board[HOUSE_REBIRTH - 1] = 2
        board[HOUSE_REBIRTH - 2] = 1
        result = find_rebirth_square(board)
        assert result == HOUSE_REBIRTH - 3
        assert board[result] == 0


# ==========================================================================
# Move generation tests
# ==========================================================================


class TestMoveGeneration:
    def _empty_state(self) -> SenetGameState:
        gs = SenetGameState()
        gs.board = [0] * 30
        return gs

    def test_normal_forward_move(self):
        gs = self._empty_state()
        gs.board[5] = 1
        moves = generate_legal_moves(gs, 1, 3)
        assert len(moves) == 1
        assert moves[0].source == 5
        assert moves[0].destination == 8
        assert not moves[0].is_swap
        assert not moves[0].is_bear_off

    def test_cannot_land_on_own_piece(self):
        gs = self._empty_state()
        gs.board[5] = 1
        gs.board[8] = 1
        moves = generate_legal_moves(gs, 1, 3)
        # Piece at 5 cannot go to 8 (own piece), but piece at 8 can go to 11
        assert not any(m.source == 5 for m in moves)
        assert any(m.source == 8 and m.destination == 11 for m in moves)

    def test_swap_unprotected_opponent(self):
        gs = self._empty_state()
        gs.board[5] = 1
        gs.board[8] = 2
        moves = generate_legal_moves(gs, 1, 3)
        assert len(moves) == 1
        assert moves[0].is_swap is True

    def test_cannot_swap_protected_opponent(self):
        gs = self._empty_state()
        gs.board[5] = 1
        gs.board[8] = 2
        gs.board[9] = 2  # Adjacent pair = protected
        moves = generate_legal_moves(gs, 1, 3)
        assert len(moves) == 0

    def test_cannot_jump_blocking_line(self):
        gs = self._empty_state()
        gs.board[5] = 1
        gs.board[7] = 2
        gs.board[8] = 2
        gs.board[9] = 2  # 3 consecutive opponents between 5 and 11
        moves = generate_legal_moves(gs, 1, 5)
        # Target would be 10, but path crosses 3 opponents at 7,8,9
        # Wait: from 5, target 10, path checks indices 6..9
        # board[7]=2, board[8]=2, board[9]=2 => 3 consecutive at 7,8,9
        assert len(moves) == 0

    def test_happiness_mandatory_stop(self):
        gs = self._empty_state()
        gs.board[23] = 1  # Square 24, before happiness (26)
        moves = generate_legal_moves(gs, 1, 4)
        # Target = 27 (past happiness at 25), should be blocked
        assert len(moves) == 0

    def test_happiness_exact_landing(self):
        gs = self._empty_state()
        gs.board[23] = 1  # Square 24
        moves = generate_legal_moves(gs, 1, 2)
        # Target = 25 = HOUSE_HAPPINESS, landing exactly on it
        assert len(moves) == 1
        assert moves[0].destination == HOUSE_HAPPINESS

    def test_move_from_happiness_forward(self):
        gs = self._empty_state()
        gs.board[HOUSE_HAPPINESS] = 1  # Already on happiness
        moves = generate_legal_moves(gs, 1, 2)
        # Target = 27, past happiness but piece is on/past it
        assert len(moves) == 1
        assert moves[0].destination == HOUSE_HAPPINESS + 2

    def test_water_sends_to_rebirth(self):
        gs = self._empty_state()
        gs.board[HOUSE_HAPPINESS] = 1
        moves = generate_legal_moves(gs, 1, 1)
        # Target = 26 = HOUSE_WATER
        assert len(moves) == 1
        assert moves[0].destination == HOUSE_WATER
        assert moves[0].water_dest == HOUSE_REBIRTH

    def test_water_rebirth_occupied(self):
        gs = self._empty_state()
        gs.board[HOUSE_HAPPINESS] = 1
        gs.board[HOUSE_REBIRTH] = 2  # Rebirth occupied
        moves = generate_legal_moves(gs, 1, 1)
        assert len(moves) == 1
        assert moves[0].water_dest is not None
        assert moves[0].water_dest < HOUSE_REBIRTH

    def test_bearoff_exact_three_truths(self):
        gs = self._empty_state()
        gs.board[HOUSE_THREE_TRUTHS] = 1
        # Exact roll of 3 required
        moves_3 = generate_legal_moves(gs, 1, 3)
        assert len(moves_3) == 1
        assert moves_3[0].is_bear_off is True

        moves_2 = generate_legal_moves(gs, 1, 2)
        assert len(moves_2) == 0

        moves_1 = generate_legal_moves(gs, 1, 1)
        assert len(moves_1) == 0

    def test_bearoff_exact_re_atum(self):
        gs = self._empty_state()
        gs.board[HOUSE_RE_ATUM] = 1
        moves_2 = generate_legal_moves(gs, 1, 2)
        assert len(moves_2) == 1
        assert moves_2[0].is_bear_off is True

        moves_1 = generate_legal_moves(gs, 1, 1)
        assert len(moves_1) == 0

    def test_bearoff_exact_square_30(self):
        gs = self._empty_state()
        gs.board[29] = 1  # Square 30
        moves_1 = generate_legal_moves(gs, 1, 1)
        assert len(moves_1) == 1
        assert moves_1[0].is_bear_off is True

        moves_2 = generate_legal_moves(gs, 1, 2)
        assert len(moves_2) == 0

    def test_cannot_bearoff_from_normal_square(self):
        gs = self._empty_state()
        gs.board[26] = 1  # Square 27 (water), not a bearoff square via overshoot
        moves = generate_legal_moves(gs, 1, 5)
        # Target = 31, off the board, but square 27 isn't in EXACT_BEAROFF
        # Actually square 27 is index 26 = HOUSE_WATER which IS NOT in EXACT_BEAROFF
        # EXACT_BEAROFF = {27: 3, 28: 2, 29: 1} so index 26 is not locked
        # target = 31 >= 30, so it's illegal
        assert len(moves) == 0

    def test_safe_squares_prevent_capture(self):
        gs = self._empty_state()
        gs.board[25] = 1  # Before Three Truths
        gs.board[HOUSE_THREE_TRUTHS] = 2  # Opponent on safe square
        moves = generate_legal_moves(gs, 1, 2)
        # Target = 27 = HOUSE_THREE_TRUTHS, which is safe
        assert len(moves) == 0

    def test_no_legal_moves(self):
        gs = self._empty_state()
        gs.board[5] = 1
        gs.board[8] = 1
        gs.board[11] = 1  # All destinations blocked by own pieces
        moves = [m for m in generate_legal_moves(gs, 1, 3) if m.source == 5]
        assert len(moves) == 0  # Piece at 5 has no legal move (blocked by 8)

    def test_has_no_legal_move(self):
        gs = self._empty_state()
        # One piece right before happiness, own piece already on happiness
        # and no other pieces on the board
        gs.board[24] = 1
        gs.board[HOUSE_HAPPINESS] = 1
        # Piece at 24 can't go to 25 (own), can't jump past happiness
        # But piece at 25 CAN move, so check just piece at 24 specifically
        moves_from_24 = [
            m for m in generate_legal_moves(gs, 1, 1) if m.source == 24
        ]
        assert len(moves_from_24) == 0

        # True "no moves at all" scenario: single piece, target is own piece
        gs2 = self._empty_state()
        gs2.board[HOUSE_THREE_TRUTHS] = 1  # Locked: needs exact 3
        assert has_any_legal_move(gs2, 1, 1) is False  # Wrong roll
        assert has_any_legal_move(gs2, 1, 2) is False  # Wrong roll
        assert has_any_legal_move(gs2, 1, 3) is True  # Correct roll


# ==========================================================================
# Apply move tests
# ==========================================================================


class TestApplyMove:
    def _empty_state(self) -> SenetGameState:
        gs = SenetGameState()
        gs.board = [0] * 30
        return gs

    def test_normal_move(self):
        gs = self._empty_state()
        gs.board[5] = 1
        move = SenetMove(source=5, destination=8)
        apply_move(gs, move, 1)
        assert gs.board[5] == 0
        assert gs.board[8] == 1

    def test_swap_move(self):
        gs = self._empty_state()
        gs.board[5] = 1
        gs.board[8] = 2
        move = SenetMove(source=5, destination=8, is_swap=True)
        apply_move(gs, move, 1)
        assert gs.board[5] == 2  # Opponent goes to source
        assert gs.board[8] == 1  # Our piece at destination

    def test_water_move(self):
        gs = self._empty_state()
        gs.board[HOUSE_HAPPINESS] = 1
        move = SenetMove(source=HOUSE_HAPPINESS, destination=HOUSE_WATER, water_dest=HOUSE_REBIRTH)
        apply_move(gs, move, 1)
        assert gs.board[HOUSE_HAPPINESS] == 0
        assert gs.board[HOUSE_WATER] == 0  # Not placed on water
        assert gs.board[HOUSE_REBIRTH] == 1  # Placed at rebirth

    def test_bearoff_move(self):
        gs = self._empty_state()
        gs.board[29] = 1
        move = SenetMove(source=29, destination=30, is_bear_off=True)
        apply_move(gs, move, 1)
        assert gs.board[29] == 0
        assert gs.off[1] == 1

    def test_swap_with_water(self):
        gs = self._empty_state()
        gs.board[HOUSE_HAPPINESS] = 1
        gs.board[HOUSE_WATER] = 2
        move = SenetMove(
            source=HOUSE_HAPPINESS, destination=HOUSE_WATER,
            is_swap=True, water_dest=HOUSE_REBIRTH,
        )
        apply_move(gs, move, 1)
        assert gs.board[HOUSE_HAPPINESS] == 2  # Opponent goes to source
        assert gs.board[HOUSE_WATER] == 0
        assert gs.board[HOUSE_REBIRTH] == 1  # Our piece at rebirth


# ==========================================================================
# Bot tests
# ==========================================================================


class TestBotScoring:
    def _empty_state(self) -> SenetGameState:
        gs = SenetGameState()
        gs.board = [0] * 30
        return gs

    def test_prefers_bearoff(self):
        gs = self._empty_state()
        gs.board[HOUSE_THREE_TRUTHS] = 1
        gs.board[10] = 1
        bearoff_move = SenetMove(source=HOUSE_THREE_TRUTHS, destination=30, is_bear_off=True)
        normal_move = SenetMove(source=10, destination=13)
        assert _score_move(gs, bearoff_move, 1) > _score_move(gs, normal_move, 1)

    def test_prefers_capture(self):
        gs = self._empty_state()
        gs.board[5] = 1
        gs.board[10] = 1
        gs.board[8] = 2
        swap_move = SenetMove(source=5, destination=8, is_swap=True)
        normal_move = SenetMove(source=10, destination=13)
        assert _score_move(gs, swap_move, 1) > _score_move(gs, normal_move, 1)


# ==========================================================================
# Game registration
# ==========================================================================


class TestGameRegistration:
    def test_metadata(self):
        game = SenetGame()
        assert game.get_name() == "Senet"
        assert game.get_type() == "senet"
        assert game.get_category() == "category-board-games"
        assert game.get_min_players() == 2
        assert game.get_max_players() == 2


# ==========================================================================
# Serialization
# ==========================================================================


class TestSerialization:
    def test_round_trip(self):
        game = SenetGame(options=SenetOptions())
        user1 = Bot("Alice")
        user2 = Bot("Bob")
        game.add_player("Alice", user1)
        game.add_player("Bob", user2)
        game.on_start()

        json_str = game.to_json()
        data = json.loads(json_str)
        assert "game_state" in data

        loaded = SenetGame.from_json(json_str)
        assert loaded.game_state.board == game.game_state.board
        assert loaded.game_state.off == game.game_state.off
        assert loaded.status == "playing"


# ==========================================================================
# Bot game completion
# ==========================================================================


class TestBotGame:
    def test_bot_game_completes(self):
        game = SenetGame()
        for i in range(2):
            bot = Bot(f"Bot{i}")
            game.add_player(f"Bot{i}", bot)
        game.on_start()

        for _ in range(50000):
            if game.status == "finished":
                break
            game.on_tick()

        assert game.status == "finished", "Game should complete within 50000 ticks"
        gs = game.game_state
        assert gs.off[1] == PIECES_PER_PLAYER or gs.off[2] == PIECES_PER_PLAYER
