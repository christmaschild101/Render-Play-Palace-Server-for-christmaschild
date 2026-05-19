"""Tests for the Chess game."""

import random

import pytest
import json

from server.games.chess.game import (
    ChessGame,
    ChessPlayer,
    ChessOptions,
    index_to_notation,
    notation_to_index,
)
from server.core.users.test_user import MockUser
from server.core.users.bot import Bot


class TestChessMetadata:
    """Test game metadata."""

    def test_game_creation(self):
        game = ChessGame()
        assert game.get_name() == "Chess"
        assert game.get_type() == "chess"
        assert game.get_category() == "category-board-games"
        assert game.get_min_players() == 2
        assert game.get_max_players() == 2

    def test_player_creation(self):
        game = ChessGame()
        user = MockUser("Alice")
        player = game.add_player("Alice", user)
        assert player.name == "Alice"
        assert player.color == ""
        assert player.is_bot is False

    def test_options_defaults(self):
        game = ChessGame()
        assert game.options.turn_timer == "0"
        assert game.options.auto_draw is True
        assert game.options.show_coordinates is True


class TestNotation:
    """Test notation conversion functions."""

    def test_index_to_notation(self):
        assert index_to_notation(0) == "a1"
        assert index_to_notation(7) == "h1"
        assert index_to_notation(8) == "a2"
        assert index_to_notation(63) == "h8"
        assert index_to_notation(4) == "e1"
        assert index_to_notation(60) == "e8"

    def test_notation_to_index(self):
        assert notation_to_index("a1") == 0
        assert notation_to_index("h1") == 7
        assert notation_to_index("a2") == 8
        assert notation_to_index("h8") == 63
        assert notation_to_index("e1") == 4
        assert notation_to_index("e8") == 60

    def test_roundtrip(self):
        for i in range(64):
            assert notation_to_index(index_to_notation(i)) == i

    def test_invalid_notation(self):
        assert notation_to_index("z1") is None
        assert notation_to_index("a9") is None
        assert notation_to_index("") is None
        assert notation_to_index("abc") is None


class TestBoardSetup:
    """Test board initialization."""

    def setup_method(self):
        self.game = ChessGame()
        self.game._init_board()

    def test_initial_board_has_32_pieces(self):
        count = sum(1 for sq in self.game.board if sq is not None)
        assert count == 32

    def test_white_back_rank(self):
        expected = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
        for i, piece in enumerate(expected):
            assert self.game.board[i]["piece"] == piece
            assert self.game.board[i]["color"] == "white"

    def test_black_back_rank(self):
        expected = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
        for i, piece in enumerate(expected):
            assert self.game.board[56 + i]["piece"] == piece
            assert self.game.board[56 + i]["color"] == "black"

    def test_white_pawns(self):
        for i in range(8, 16):
            assert self.game.board[i]["piece"] == "pawn"
            assert self.game.board[i]["color"] == "white"

    def test_black_pawns(self):
        for i in range(48, 56):
            assert self.game.board[i]["piece"] == "pawn"
            assert self.game.board[i]["color"] == "black"

    def test_empty_squares(self):
        for i in range(16, 48):
            assert self.game.board[i] is None

    def test_castling_rights(self):
        assert self.game.castle_white_kingside is True
        assert self.game.castle_white_queenside is True
        assert self.game.castle_black_kingside is True
        assert self.game.castle_black_queenside is True


class TestPieceMovement:
    """Test piece movement validation."""

    def setup_method(self):
        self.game = ChessGame()
        self.game._init_board()

    def test_pawn_forward_one(self):
        # e2 to e3
        legal, _ = self.game._is_legal_move(12, 20, "white")
        assert legal

    def test_pawn_forward_two_from_start(self):
        # e2 to e4
        legal, _ = self.game._is_legal_move(12, 28, "white")
        assert legal

    def test_pawn_cannot_move_two_after_first(self):
        # Move e2 to e3 first
        self.game.execute_move_silent(12, 20)
        # e3 to e5 should be illegal
        legal, _ = self.game._is_legal_move(20, 36, "white")
        assert not legal

    def test_pawn_capture_diagonal(self):
        # Place a black piece at d3 for white pawn on e2 to capture
        self.game.board[19] = {"piece": "pawn", "color": "black", "has_moved": True}
        legal, _ = self.game._is_legal_move(12, 19, "white")
        assert legal

    def test_pawn_cannot_capture_forward(self):
        # Place black piece directly ahead
        self.game.board[20] = {"piece": "pawn", "color": "black", "has_moved": True}
        legal, _ = self.game._is_legal_move(12, 20, "white")
        assert not legal

    def test_knight_l_shape(self):
        # b1 knight to c3
        legal, _ = self.game._is_legal_move(1, 18, "white")
        assert legal

    def test_knight_jumps_over_pieces(self):
        # g1 knight to f3 (jumping over pawns)
        legal, _ = self.game._is_legal_move(6, 21, "white")
        assert legal

    def test_bishop_blocked_at_start(self):
        # c1 bishop can't move (blocked by pawns)
        legal, _ = self.game._is_legal_move(2, 11, "white")
        assert not legal

    def test_cannot_capture_own_piece(self):
        # white rook can't capture white pawn
        legal, _ = self.game._is_legal_move(0, 8, "white")
        assert not legal

    def test_king_one_square(self):
        # Clear path for king
        self.game.board = [None] * 64
        self.game.board[4] = {"piece": "king", "color": "white", "has_moved": False}
        legal, _ = self.game._is_legal_move(4, 5, "white")
        assert legal

    def test_king_cannot_move_two(self):
        self.game.board = [None] * 64
        self.game.board[4] = {"piece": "king", "color": "white", "has_moved": True}
        # Non-castling 2-square move (king already moved)
        self.game.castle_white_kingside = False
        legal, _ = self.game._is_legal_move(4, 6, "white")
        assert not legal


class TestCheckDetection:
    """Test check and checkmate detection."""

    def setup_method(self):
        self.game = ChessGame()

    def test_king_in_check(self):
        self.game.board = [None] * 64
        self.game.board[4] = {"piece": "king", "color": "white", "has_moved": True}
        self.game.board[60] = {"piece": "king", "color": "black", "has_moved": True}
        self.game.board[28] = {"piece": "rook", "color": "black", "has_moved": True}
        # Black rook at e4 attacks white king at e1 along the e-file
        assert self.game.is_in_check("white")

    def test_king_not_in_check(self):
        self.game._init_board()
        assert not self.game.is_in_check("white")
        assert not self.game.is_in_check("black")

    def test_checkmate_scholars_mate(self):
        """Test a basic checkmate position (back rank mate)."""
        self.game.board = [None] * 64
        self.game.board[0] = {"piece": "king", "color": "white", "has_moved": True}
        self.game.board[8] = {"piece": "pawn", "color": "white", "has_moved": False}
        self.game.board[9] = {"piece": "pawn", "color": "white", "has_moved": False}
        self.game.board[63] = {"piece": "king", "color": "black", "has_moved": True}
        self.game.board[7] = {"piece": "rook", "color": "black", "has_moved": True}
        # Back rank mate: black rook on h1, white king on a1, pawns blocking a2/b2
        self.game.current_color = "white"
        assert self.game.is_checkmate("white")

    def test_stalemate(self):
        """Test a stalemate position."""
        self.game.board = [None] * 64
        self.game.board[0] = {"piece": "king", "color": "white", "has_moved": True}
        self.game.board[17] = {"piece": "queen", "color": "black", "has_moved": True}
        self.game.board[63] = {"piece": "king", "color": "black", "has_moved": True}
        # White king on a1, black queen on b3 - white has no legal moves but isn't in check
        self.game.current_color = "white"
        self.game.castle_white_kingside = False
        self.game.castle_white_queenside = False
        assert self.game.is_stalemate("white")


class TestCastling:
    """Test castling mechanics."""

    def setup_method(self):
        self.game = ChessGame()
        self.game.board = [None] * 64
        # Set up minimal position for castling
        self.game.board[4] = {"piece": "king", "color": "white", "has_moved": False}
        self.game.board[7] = {"piece": "rook", "color": "white", "has_moved": False}
        self.game.board[0] = {"piece": "rook", "color": "white", "has_moved": False}
        self.game.board[60] = {"piece": "king", "color": "black", "has_moved": False}
        self.game.castle_white_kingside = True
        self.game.castle_white_queenside = True

    def test_kingside_castling_legal(self):
        legal, _ = self.game._is_legal_move(4, 6, "white")
        assert legal

    def test_queenside_castling_legal(self):
        legal, _ = self.game._is_legal_move(4, 2, "white")
        assert legal

    def test_castling_blocked(self):
        # Put a piece between king and rook
        self.game.board[5] = {"piece": "bishop", "color": "white", "has_moved": True}
        legal, _ = self.game._is_legal_move(4, 6, "white")
        assert not legal

    def test_castling_through_check(self):
        # Put a black rook attacking f1
        self.game.board[53] = {"piece": "rook", "color": "black", "has_moved": True}
        legal, _ = self.game._is_legal_move(4, 6, "white")
        assert not legal

    def test_castling_from_check(self):
        # Put a black rook attacking e1
        self.game.board[52] = {"piece": "rook", "color": "black", "has_moved": True}
        legal, _ = self.game._is_legal_move(4, 6, "white")
        assert not legal

    def test_castling_execution(self):
        self.game._execute_castling("white", "kingside")
        assert self.game.board[6] is not None
        assert self.game.board[6]["piece"] == "king"
        assert self.game.board[5] is not None
        assert self.game.board[5]["piece"] == "rook"
        assert self.game.board[4] is None
        assert self.game.board[7] is None


class TestEnPassant:
    """Test en passant mechanics."""

    def setup_method(self):
        self.game = ChessGame()
        self.game.board = [None] * 64
        self.game.board[4] = {"piece": "king", "color": "white", "has_moved": True}
        self.game.board[60] = {"piece": "king", "color": "black", "has_moved": True}

    def test_en_passant_capture(self):
        # White pawn on e5 (rank 4, file 4 = index 36), black pawn just moved d7-d5
        self.game.board[36] = {"piece": "pawn", "color": "white", "has_moved": True}
        self.game.board[35] = {"piece": "pawn", "color": "black", "has_moved": True}
        self.game.en_passant_target = 43  # d6

        legal, _ = self.game._is_legal_move(36, 43, "white")
        assert legal


class TestFEN:
    """Test FEN import/export."""

    def setup_method(self):
        self.game = ChessGame()
        self.game._init_board()

    def test_starting_position_fen(self):
        fen = self.game._get_fen()
        assert fen.startswith("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
        assert "w KQkq" in fen

    def test_load_starting_fen(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        success, _ = self.game._load_fen(fen)
        assert success
        assert self.game.board[0]["piece"] == "rook"
        assert self.game.board[4]["piece"] == "king"
        assert self.game.current_color == "white"

    def test_fen_roundtrip(self):
        original_fen = self.game._get_fen()
        success, _ = self.game._load_fen(original_fen)
        assert success
        new_fen = self.game._get_fen()
        # Compare board part (move counts may differ)
        assert original_fen.split()[0] == new_fen.split()[0]


class TestDrawConditions:
    """Test draw detection."""

    def setup_method(self):
        self.game = ChessGame()

    def test_insufficient_material_kk(self):
        """King vs King is insufficient."""
        self.game.board = [None] * 64
        self.game.board[4] = {"piece": "king", "color": "white", "has_moved": True}
        self.game.board[60] = {"piece": "king", "color": "black", "has_moved": True}
        assert self.game._is_insufficient_material()

    def test_insufficient_material_kbk(self):
        """King+Bishop vs King is insufficient."""
        self.game.board = [None] * 64
        self.game.board[4] = {"piece": "king", "color": "white", "has_moved": True}
        self.game.board[20] = {"piece": "bishop", "color": "white", "has_moved": True}
        self.game.board[60] = {"piece": "king", "color": "black", "has_moved": True}
        assert self.game._is_insufficient_material()

    def test_sufficient_material_krk(self):
        """King+Rook vs King is sufficient."""
        self.game.board = [None] * 64
        self.game.board[4] = {"piece": "king", "color": "white", "has_moved": True}
        self.game.board[20] = {"piece": "rook", "color": "white", "has_moved": True}
        self.game.board[60] = {"piece": "king", "color": "black", "has_moved": True}
        assert not self.game._is_insufficient_material()

    def test_fifty_move_clock(self):
        self.game._init_board()
        self.game.halfmove_clock = 100
        self.game.options.auto_draw = True
        result = self.game._check_draw_conditions()
        assert result
        assert self.game.draw_reason == "fifty_move_rule"


class TestBotPlay:
    """Test that bots can complete a game."""

    def test_bot_game_completes(self):
        """Run a full bot game and verify it completes."""
        game = ChessGame()
        game.host = "Alice"
        p1 = game.add_player("Alice", Bot("Alice"))
        p2 = game.add_player("Bob", Bot("Bob"))
        game.on_start()

        for _ in range(30000):
            game.on_tick()
            if not game.game_active:
                break

        assert not game.game_active
        assert game.status == "finished"

    def test_serialization_during_play(self):
        """Test that the game can be serialized and restored mid-game."""
        rng_state = random.getstate()
        random.seed(42)
        try:
            game = ChessGame()
            game.host = "Alice"
            p1 = game.add_player("Alice", Bot("Alice"))
            p2 = game.add_player("Bob", Bot("Bob"))
            game.on_start()

            for i in range(15000):
                game.on_tick()
                if not game.game_active:
                    break
                if i == 200:
                    # Serialize mid-game
                    data = game.to_dict()
                    game2 = ChessGame.from_dict(data)
                    game2.__post_init__()
                    for p in game2.players:
                        game2.attach_user(p.id, Bot(p.name, uuid=p.id))
                    game = game2

            assert not game.game_active
        finally:
            random.setstate(rng_state)


class TestPromotion:
    """Test pawn promotion."""

    def setup_method(self):
        self.game = ChessGame()
        self.game.board = [None] * 64
        self.game.board[4] = {"piece": "king", "color": "white", "has_moved": True}
        self.game.board[60] = {"piece": "king", "color": "black", "has_moved": True}

    def test_promotion_pending(self):
        """Test that moving a pawn to the 8th rank triggers promotion."""
        # White pawn on e7 (index 52)
        self.game.board[52] = {"piece": "pawn", "color": "white", "has_moved": True}

        # Set up game with players
        user1 = MockUser("Alice")
        user2 = MockUser("Bob")
        p1 = self.game.add_player("Alice", user1)
        p2 = self.game.add_player("Bob", user2)
        p1.color = "white"
        p2.color = "black"
        self.game.status = "playing"
        self.game.game_active = True
        self.game.current_color = "white"
        self.game.set_turn_players([p1, p2])

        # Execute move e7 to e8
        self.game._execute_move_full(p1, 52, 60)

        # Promotion should be pending (but king is on e8, so let's use f7->f8)
        # Actually let me adjust: put pawn on f7, clear f8
        self.game.board = [None] * 64
        self.game.board[4] = {"piece": "king", "color": "white", "has_moved": True}
        self.game.board[60] = {"piece": "king", "color": "black", "has_moved": True}
        self.game.board[53] = {"piece": "pawn", "color": "white", "has_moved": True}
        self.game.promotion_pending = False
        self.game.current_color = "white"
        self.game._execute_move_full(p1, 53, 61)

        assert self.game.promotion_pending
        assert self.game.promotion_square == 61
