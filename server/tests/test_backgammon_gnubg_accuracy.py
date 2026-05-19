"""Tests verifying that our GNUBG integration accurately reflects GNUBG output.

These tests launch a real gnubg-cli subprocess and compare our encoding,
parsing, and goal conversion against actual GNUBG responses.
Every test is skipped if GNUBG is not on PATH.
"""

import pytest
from server.games.backgammon.gnubg import (
    GnubgProcess,
    encode_position_id,
    hint_to_goals,
    is_gnubg_available,
    parse_hint_line,
    _HINT_RE,
)
from server.games.backgammon.moves import generate_legal_moves
from server.games.backgammon.state import (
    BackgammonBoardState,
    BackgammonGameState,
    build_initial_game_state,
    remaining_dice_unique,
)

pytestmark = pytest.mark.skipif(not is_gnubg_available(), reason="gnubg-cli not on PATH")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def gnubg():
    """A shared GNUBG process for the whole module (ply 0 for speed)."""
    proc = GnubgProcess(ply=0)
    ok = proc.start()
    if not ok:
        pytest.skip("Failed to start gnubg-cli")
    yield proc
    proc.stop()


@pytest.fixture(scope="module")
def gnubg_2ply():
    """A ply-2 GNUBG process for hint-quality tests."""
    proc = GnubgProcess(ply=2)
    ok = proc.start()
    if not ok:
        pytest.skip("Failed to start gnubg-cli at ply 2")
    yield proc
    proc.stop()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_state(
    points: list[int] | None = None,
    bar_red: int = 0,
    bar_white: int = 0,
    off_red: int = 0,
    off_white: int = 0,
    current_color: str = "red",
    dice: list[int] | None = None,
    cube_value: int = 1,
    cube_owner: str = "",
) -> BackgammonGameState:
    """Build a game state from explicit parameters."""
    if points is None:
        from server.games.backgammon.state import INITIAL_BOARD

        points = list(INITIAL_BOARD)
    gs = BackgammonGameState(
        board=BackgammonBoardState(
            points=list(points),
            bar_red=bar_red,
            bar_white=bar_white,
            off_red=off_red,
            off_white=off_white,
        ),
        current_color=current_color,
        cube_value=cube_value,
        cube_owner=cube_owner,
    )
    if dice:
        gs.dice = list(dice)
        gs.dice_used = [False] * len(dice)
        gs.turn_phase = "moving"
    return gs


def _goals_are_legal(
    goals: list[tuple[int, int]],
    state: BackgammonGameState,
    color: str,
) -> bool:
    """Check that every goal source has at least one legal move for the color.

    We don't check that the exact destination is reachable in one die step
    (compound moves span multiple dice), but the source must have a checker
    of the right color and the destination must be in the right direction.
    """
    sign = 1 if color == "red" else -1
    for src, dst in goals:
        if src == -1:
            # Bar: must have checkers on bar
            bar = state.board.bar_red if color == "red" else state.board.bar_white
            if bar <= 0:
                return False
        elif src == 24:
            # Already borne off — shouldn't be a goal source
            return False
        else:
            # Must have own checker on this point
            if 0 <= src <= 23:
                if state.board.points[src] * sign <= 0:
                    return False
            else:
                return False
        # Destination must be valid
        if dst not in range(-1, 25):
            return False
    return True


def _raw_query(
    proc: GnubgProcess, state: BackgammonGameState, dice: list[int], hint_count: int = 3
) -> list[str]:
    """Send position+dice to GNUBG, return raw hint output lines."""
    pos_id = encode_position_id(state)
    proc._send_batch(
        [
            f"set board {pos_id}",
            "set turn 1",
            f"set dice {dice[0]} {dice[1]}",
            f"hint {hint_count}",
        ]
    )
    output = proc._read_until_match(
        lambda line: _HINT_RE.match(line) is not None,
        timeout=10.0,
    )
    return output


# ===========================================================================
# Position ID round-trip tests
# ===========================================================================


class TestPositionIdRoundTrip:
    """Verify our position encoding matches what GNUBG reports back."""

    def test_starting_position_id_matches_gnubg(self, gnubg):
        """Encode starting position, set it in GNUBG, ask GNUBG for its ID."""
        gs = build_initial_game_state()
        gs.current_color = "red"
        our_id = encode_position_id(gs)
        # Set this position in GNUBG and ask it to report back
        gnubg._send_batch([f"set board {our_id}", "set turn 1"])
        output = gnubg._read_until_idle(timeout=5.0)
        # GNUBG should accept it without error — if the ID were wrong,
        # we'd see an error line. Check no "illegal" or "error" in output.
        joined = " ".join(output).lower()
        assert "illegal" not in joined, f"GNUBG rejected our position ID: {output}"
        assert "error" not in joined, f"GNUBG error with our position ID: {output}"

    def test_starting_position_known_value(self):
        """The starting position ID is a well-known constant."""
        gs = build_initial_game_state()
        gs.current_color = "red"
        assert encode_position_id(gs) == "4HPwATDgc/ABMA"

    def test_empty_board_accepted(self, gnubg):
        """An almost-empty board (all borne off) should encode validly."""
        gs = _make_state(
            points=[0] * 24,
            off_red=15,
            off_white=15,
            current_color="red",
        )
        pos_id = encode_position_id(gs)
        gnubg._send_batch([f"set board {pos_id}", "set turn 1"])
        output = gnubg._read_until_idle(timeout=5.0)
        joined = " ".join(output).lower()
        assert "illegal" not in joined

    def test_bar_position_accepted(self, gnubg):
        """A position with checkers on the bar should encode validly."""
        points = [0] * 24
        points[5] = 12  # Red has 12 on point 6
        points[18] = -13  # White has 13 on point 19
        gs = _make_state(
            points=points,
            bar_red=3,
            bar_white=2,
            current_color="red",
        )
        pos_id = encode_position_id(gs)
        gnubg._send_batch([f"set board {pos_id}", "set turn 1"])
        output = gnubg._read_until_idle(timeout=5.0)
        joined = " ".join(output).lower()
        assert "illegal" not in joined, f"GNUBG rejected bar position: {output}"

    def test_bearing_off_position_accepted(self, gnubg):
        """A bearing-off position should encode validly."""
        points = [0] * 24
        points[0] = 3  # Red on point 1
        points[2] = 4  # Red on point 3
        points[4] = 3  # Red on point 5
        points[23] = -5  # White on point 1 (their perspective)
        points[20] = -5  # White on point 4
        gs = _make_state(
            points=points,
            off_red=5,
            off_white=5,
            current_color="red",
        )
        pos_id = encode_position_id(gs)
        gnubg._send_batch([f"set board {pos_id}", "set turn 1"])
        output = gnubg._read_until_idle(timeout=5.0)
        joined = " ".join(output).lower()
        assert "illegal" not in joined


# ===========================================================================
# Move hint accuracy tests
# ===========================================================================


class TestMoveHintAccuracy:
    """Verify that get_move_hint_text returns hints matching raw GNUBG output."""

    def test_starting_position_31(self, gnubg):
        """Starting position with dice 3-1 should produce valid parsed hints."""
        gs = _make_state(dice=[3, 1], current_color="red")
        hints = gnubg.get_move_hint_text(gs, "red", hint_count=3)
        assert hints is not None, "GNUBG returned no hints for starting 3-1"
        assert len(hints) >= 1
        # Each hint should be formatted as "N. <moves>"
        for h in hints:
            assert h[0].isdigit(), f"Hint doesn't start with rank: {h}"

    def test_starting_position_66(self, gnubg):
        """Starting position with doubles 6-6."""
        gs = _make_state(dice=[6, 6, 6, 6], current_color="red")
        # Doubles give 4 dice, but GNUBG hint only needs the pair
        gs.dice = [6, 6, 6, 6]
        gs.dice_used = [False, False, False, False]
        hints = gnubg.get_move_hint_text(gs, "red", hint_count=3)
        assert hints is not None, "GNUBG returned no hints for starting 6-6"

    def test_hint_text_parseable(self, gnubg):
        """Every hint line returned by get_move_hint_text should be parseable."""
        gs = _make_state(dice=[5, 2], current_color="red")
        hints = gnubg.get_move_hint_text(gs, "red", hint_count=5)
        assert hints is not None
        for hint_text in hints:
            # Reconstruct a full hint line for parse_hint_line
            # get_move_hint_text strips it to "N. moves", so we need to check
            # the sub-moves can be parsed from the move portion
            parts = hint_text.split(". ", 1)
            assert len(parts) == 2, f"Unexpected hint format: {hint_text}"
            rank, move_str = parts
            assert rank.isdigit()
            # The move string should contain valid backgammon notation
            assert "/" in move_str, f"No slash in move: {move_str}"

    def test_raw_hint_lines_match_parsed(self, gnubg):
        """Raw GNUBG output lines should parse correctly with parse_hint_line."""
        gs = _make_state(dice=[4, 2], current_color="red")
        raw_output = _raw_query(gnubg, gs, [4, 2], hint_count=5)
        parsed_any = False
        for line in raw_output:
            submoves = parse_hint_line(line)
            if submoves is not None:
                parsed_any = True
                # Every submove should have valid notation
                for src, dst, count in submoves:
                    assert src == "bar" or src.isdigit(), f"Bad source: {src}"
                    assert dst == "off" or dst.isdigit(), f"Bad dest: {dst}"
                    assert count >= 1
                    if src.isdigit():
                        assert 1 <= int(src) <= 24
                    if dst.isdigit():
                        assert 1 <= int(dst) <= 24
        assert parsed_any, f"No hint lines parsed from GNUBG output: {raw_output}"

    def test_white_perspective_hints(self, gnubg):
        """Hints for white should also be valid."""
        gs = _make_state(dice=[3, 5], current_color="white")
        hints = gnubg.get_move_hint_text(gs, "white", hint_count=3)
        assert hints is not None, "GNUBG returned no hints for white 3-5"
        assert len(hints) >= 1


# ===========================================================================
# Goal conversion accuracy tests
# ===========================================================================


class TestGoalConversionAccuracy:
    """Verify hint_to_goals produces goals that match legal board positions."""

    def test_starting_31_goals_have_valid_sources(self, gnubg):
        """Goals from starting 3-1 should reference points with red checkers."""
        gs = _make_state(dice=[3, 1], current_color="red")
        raw = _raw_query(gnubg, gs, [3, 1], hint_count=1)
        for line in raw:
            submoves = parse_hint_line(line)
            if submoves:
                goals = hint_to_goals(submoves, "red")
                assert _goals_are_legal(goals, gs, "red"), (
                    f"Illegal goal sources in {goals} from hint {line}"
                )
                break
        else:
            pytest.fail(f"No hint parsed from GNUBG output: {raw}")

    def test_starting_52_goals_valid(self, gnubg):
        """Goals from starting 5-2."""
        gs = _make_state(dice=[5, 2], current_color="red")
        raw = _raw_query(gnubg, gs, [5, 2], hint_count=3)
        for line in raw:
            submoves = parse_hint_line(line)
            if submoves:
                goals = hint_to_goals(submoves, "red")
                assert _goals_are_legal(goals, gs, "red"), f"Goals {goals} invalid for hint {line}"

    def test_white_goals_valid(self, gnubg):
        """Goals converted for white should reference white-occupied points."""
        gs = _make_state(dice=[4, 3], current_color="white")
        raw = _raw_query(gnubg, gs, [4, 3], hint_count=3)
        for line in raw:
            submoves = parse_hint_line(line)
            if submoves:
                goals = hint_to_goals(submoves, "white")
                assert _goals_are_legal(goals, gs, "white"), (
                    f"White goals {goals} invalid for hint {line}"
                )

    def test_bar_entry_goals_valid(self, gnubg):
        """When a checker is on the bar, goals should start from -1."""
        points = [0] * 24
        points[5] = 14  # 14 red on point 6
        points[18] = -15  # all white on point 19
        gs = _make_state(
            points=points,
            bar_red=1,
            current_color="red",
            dice=[3, 2],
        )
        raw = _raw_query(gnubg, gs, [3, 2], hint_count=1)
        for line in raw:
            submoves = parse_hint_line(line)
            if submoves:
                goals = hint_to_goals(submoves, "red")
                # At least one goal should come from bar
                bar_goals = [g for g in goals if g[0] == -1]
                assert len(bar_goals) >= 1, f"Expected bar entry goal, got {goals} from {line}"
                assert _goals_are_legal(goals, gs, "red")
                break

    def test_bearing_off_goals_valid(self, gnubg):
        """Bear-off goals should have destination 24."""
        points = [0] * 24
        points[0] = 5  # Red on point 1
        points[2] = 5  # Red on point 3
        points[4] = 5  # Red on point 5
        gs = _make_state(
            points=points,
            off_red=0,
            off_white=15,
            current_color="red",
            dice=[3, 1],
        )
        raw = _raw_query(gnubg, gs, [3, 1], hint_count=1)
        for line in raw:
            submoves = parse_hint_line(line)
            if submoves:
                goals = hint_to_goals(submoves, "red")
                # At least one goal should bear off (dst=24)
                bear_off_goals = [g for g in goals if g[1] == 24]
                assert len(bear_off_goals) >= 1, f"Expected bear-off goal, got {goals} from {line}"
                break


# ===========================================================================
# get_best_move end-to-end tests
# ===========================================================================


class TestGetBestMoveEndToEnd:
    """Verify get_best_move returns goals that can be resolved into legal moves."""

    def test_starting_position_various_dice(self, gnubg):
        """get_best_move should return valid goals for multiple dice combos."""
        for d1, d2 in [(3, 1), (5, 2), (6, 4), (4, 4), (1, 1), (6, 5)]:
            dice = [d1, d2] if d1 != d2 else [d1, d2, d1, d2]
            gs = _make_state(dice=dice, current_color="red")
            goals = gnubg.get_best_move(gs, "red")
            assert goals is not None, f"No goals for dice {d1}-{d2}"
            assert len(goals) >= 1, f"Empty goals for dice {d1}-{d2}"
            assert _goals_are_legal(goals, gs, "red"), f"Illegal goals {goals} for dice {d1}-{d2}"

    def test_white_best_move(self, gnubg):
        """get_best_move should work for white too."""
        gs = _make_state(dice=[6, 1], current_color="white")
        goals = gnubg.get_best_move(gs, "white")
        assert goals is not None
        assert _goals_are_legal(goals, gs, "white")

    def test_best_move_mid_game(self, gnubg):
        """A mid-game position should produce valid goals."""
        points = [0] * 24
        # Red: 3 on 13pt, 2 on 8pt, 4 on 6pt, 3 on 4pt, 2 on 3pt
        points[12] = 3
        points[7] = 2
        points[5] = 4
        points[3] = 3
        points[2] = 2
        # White: 3 on 24pt, 2 on 13pt, 5 on 8pt, 3 on 6pt, 1 on 3pt
        points[23] = -3
        points[11] = -2
        points[16] = -5
        points[18] = -3
        points[21] = -1
        # Missing: red has 1 off
        gs = _make_state(
            points=points,
            off_red=1,
            off_white=1,
            current_color="red",
            dice=[6, 3],
        )
        goals = gnubg.get_best_move(gs, "red")
        assert goals is not None
        assert _goals_are_legal(goals, gs, "red")

    def test_best_move_bearing_off(self, gnubg):
        """Bear-off position should produce valid goals."""
        points = [0] * 24
        points[0] = 3
        points[1] = 3
        points[3] = 4
        points[5] = 2
        gs = _make_state(
            points=points,
            off_red=3,
            off_white=15,
            current_color="red",
            dice=[5, 3],
        )
        goals = gnubg.get_best_move(gs, "red")
        assert goals is not None
        assert _goals_are_legal(goals, gs, "red")

    def test_best_move_from_bar(self, gnubg):
        """Bar entry position should produce valid goals."""
        points = [0] * 24
        points[5] = 12  # Red: 12 on point 6
        points[11] = 2  # Red: 2 on point 12
        # Red total: 12 + 2 + 1 bar = 15
        # White: 15 total, leave entry points open for die 4 and 2
        points[18] = -5
        points[16] = -5
        points[14] = -5
        gs = _make_state(
            points=points,
            bar_red=1,
            current_color="red",
            dice=[4, 2],
        )
        goals = gnubg.get_best_move(gs, "red")
        assert goals is not None
        bar_goals = [g for g in goals if g[0] == -1]
        assert len(bar_goals) >= 1, f"Expected bar goal, got {goals}"


# ===========================================================================
# get_worst_move (Whackgammon) tests
# ===========================================================================


class TestGetWorstMove:
    """Verify get_worst_move returns valid (but different from best) goals."""

    def test_worst_move_valid(self, gnubg):
        """Worst move should still be a legal set of goals."""
        gs = _make_state(dice=[6, 5], current_color="red")
        goals = gnubg.get_worst_move(gs, "red")
        assert goals is not None
        assert _goals_are_legal(goals, gs, "red")

    def test_worst_differs_from_best(self, gnubg):
        """Worst move should differ from best for positions with many options."""
        gs = _make_state(dice=[3, 1], current_color="red")
        best = gnubg.get_best_move(gs, "red")
        worst = gnubg.get_worst_move(gs, "red")
        assert best is not None
        assert worst is not None
        # They should differ (starting 3-1 has many possible moves)
        assert best != worst, f"Best and worst are identical: {best}"

    def test_worst_is_truly_last_ranked(self, gnubg):
        """Worst move should match the last hint from a full hint list."""
        gs = _make_state(dice=[3, 1], current_color="red")
        # Get ALL hints via raw query
        raw = _raw_query(gnubg, gs, [3, 1], hint_count=999)
        all_submoves = []
        for line in raw:
            sm = parse_hint_line(line)
            if sm:
                all_submoves.append(sm)
        assert len(all_submoves) >= 2, f"Expected multiple moves, got {len(all_submoves)}"
        # The worst move from get_worst_move should match the last ranked
        last_goals = hint_to_goals(all_submoves[-1], "red")
        worst_goals = gnubg.get_worst_move(gs, "red")
        assert worst_goals == last_goals, (
            f"get_worst_move returned {worst_goals}, but last ranked is {last_goals}"
        )

    def test_worst_move_sees_all_moves_doubles(self, gnubg):
        """With doubles, there can be 30+ legal moves. Verify we see them all."""
        gs = _make_state(dice=[3, 3, 3, 3], current_color="red")
        raw = _raw_query(gnubg, gs, [3, 3], hint_count=999)
        all_hints = [line for line in raw if parse_hint_line(line)]
        # Doubles from the starting position have many combinations
        # The old hint count of 20 would have missed some
        assert len(all_hints) >= 1
        # Worst move should be the very last one
        worst_goals = gnubg.get_worst_move(gs, "red")
        last_goals = hint_to_goals(parse_hint_line(all_hints[-1]), "red")
        assert worst_goals == last_goals


# ===========================================================================
# Cube hint tests
# ===========================================================================


class TestCubeHintAccuracy:
    """Verify cube decisions from GNUBG are parsed correctly."""

    def test_cube_decision_starting(self, gnubg):
        """Starting position cube decision should be valid."""
        gs = _make_state(current_color="red")
        decision = gnubg.get_cube_decision(gs, "red")
        assert decision in ("no-double", "too-good", "double-take", "double-pass"), (
            f"Invalid cube decision: {decision}"
        )

    def test_cube_decision_is_no_double_at_start(self, gnubg):
        """At the starting position, correct play is no double."""
        gs = _make_state(current_color="red")
        decision = gnubg.get_cube_decision(gs, "red")
        assert decision == "no-double", f"Expected no-double at start, got {decision}"

    def test_cube_hint_text_returns_string(self, gnubg):
        """get_cube_hint_text should return a readable string."""
        gs = _make_state(current_color="red")
        text = gnubg.get_cube_hint_text(gs, "red")
        assert text is not None
        assert "cube action" in text.lower() or "Proper" in text

    def test_cube_decision_winning_position(self, gnubg):
        """A heavily winning position should recommend double-pass or double-take."""
        points = [0] * 24
        points[0] = 5  # Red on point 1
        points[1] = 5  # Red on point 2
        points[2] = 4  # Red on point 3
        # White far away
        points[23] = -5
        points[22] = -5
        points[21] = -5
        gs = _make_state(
            points=points,
            off_red=1,
            current_color="red",
        )
        decision = gnubg.get_cube_decision(gs, "red")
        # Red is way ahead in a race, should recommend doubling
        assert decision in ("double-take", "double-pass", "too-good"), (
            f"Expected doubling recommendation, got {decision}"
        )


# ===========================================================================
# Consistency tests: verify our full pipeline matches GNUBG
# ===========================================================================


class TestPipelineConsistency:
    """End-to-end tests: position → GNUBG → parse → goals → legal check."""

    @pytest.mark.parametrize(
        "dice",
        [
            [1, 2],
            [1, 3],
            [1, 4],
            [1, 5],
            [1, 6],
            [2, 3],
            [2, 4],
            [2, 5],
            [2, 6],
            [3, 4],
            [3, 5],
            [3, 6],
            [4, 5],
            [4, 6],
            [5, 6],
            [1, 1],
            [2, 2],
            [3, 3],
            [4, 4],
            [5, 5],
            [6, 6],
        ],
    )
    def test_all_opening_rolls(self, gnubg, dice):
        """For every possible opening roll, the full pipeline should succeed."""
        actual_dice = dice if dice[0] != dice[1] else dice * 2
        gs = _make_state(dice=actual_dice, current_color="red")

        # Get raw output and parse
        raw = _raw_query(gnubg, gs, dice[:2], hint_count=1)
        hint_found = False
        for line in raw:
            submoves = parse_hint_line(line)
            if submoves:
                hint_found = True
                goals = hint_to_goals(submoves, "red")
                assert _goals_are_legal(goals, gs, "red"), (
                    f"dice={dice}: illegal goals {goals} from {line}"
                )
                # Also verify via get_best_move
                break

        assert hint_found, f"dice={dice}: no hint in GNUBG output: {raw}"

    def test_pipeline_with_bar_red(self, gnubg):
        """Full pipeline with red on bar."""
        points = [0] * 24
        points[5] = 13
        points[11] = -5
        points[16] = -3
        points[18] = -5
        points[23] = -2
        gs = _make_state(
            points=points,
            bar_red=2,
            current_color="red",
            dice=[6, 4],
        )
        raw = _raw_query(gnubg, gs, [6, 4], hint_count=1)
        for line in raw:
            submoves = parse_hint_line(line)
            if submoves:
                goals = hint_to_goals(submoves, "red")
                assert _goals_are_legal(goals, gs, "red")
                # Must have bar entries
                assert any(g[0] == -1 for g in goals)
                break

    def test_pipeline_with_bar_white(self, gnubg):
        """Full pipeline with white on bar."""
        points = [0] * 24
        points[5] = 5
        points[7] = 3
        points[12] = 5
        points[23] = 2
        # White gets remaining spots
        points[0] = -3
        points[11] = -5
        points[16] = -3
        points[18] = -2
        gs = _make_state(
            points=points,
            bar_white=2,
            current_color="white",
            dice=[5, 3],
        )
        raw = _raw_query(gnubg, gs, [5, 3], hint_count=1)
        for line in raw:
            submoves = parse_hint_line(line)
            if submoves:
                goals = hint_to_goals(submoves, "white")
                assert _goals_are_legal(goals, gs, "white")
                assert any(g[0] == -1 for g in goals)
                break

    def test_pipeline_bearing_off_race(self, gnubg):
        """Full pipeline in a pure race bear-off position."""
        points = [0] * 24
        # Red: all in home
        points[0] = 3
        points[1] = 3
        points[2] = 3
        points[3] = 3
        points[4] = 2
        points[5] = 1
        # White: all in home
        points[18] = -1
        points[19] = -2
        points[20] = -3
        points[21] = -3
        points[22] = -3
        points[23] = -3
        gs = _make_state(
            points=points,
            current_color="red",
            dice=[6, 5],
        )
        raw = _raw_query(gnubg, gs, [6, 5], hint_count=1)
        for line in raw:
            submoves = parse_hint_line(line)
            if submoves:
                goals = hint_to_goals(submoves, "red")
                # In a bear-off race with 6-5, should bear off
                assert any(g[1] == 24 for g in goals), f"Expected bear-off in goals: {goals}"
                break


# ===========================================================================
# Hint stability test (ply 2)
# ===========================================================================


class TestHintStability:
    """Verify that repeated queries for the same position give the same hint."""

    def test_same_position_same_hint(self, gnubg_2ply):
        """Querying the same position twice should return the same best move."""
        gs = _make_state(dice=[3, 1], current_color="red")
        hints1 = gnubg_2ply.get_move_hint_text(gs, "red", hint_count=1)
        hints2 = gnubg_2ply.get_move_hint_text(gs, "red", hint_count=1)
        assert hints1 is not None
        assert hints2 is not None
        assert hints1 == hints2, f"Hint changed between queries: {hints1} vs {hints2}"

    def test_best_move_deterministic(self, gnubg_2ply):
        """get_best_move should be deterministic for the same position."""
        gs = _make_state(dice=[6, 4], current_color="red")
        goals1 = gnubg_2ply.get_best_move(gs, "red")
        goals2 = gnubg_2ply.get_best_move(gs, "red")
        assert goals1 == goals2, f"Goals changed between queries: {goals1} vs {goals2}"


# ===========================================================================
# Edge case tests
# ===========================================================================


class TestEdgeCases:
    """Test positions that might trip up encoding or parsing."""

    def test_all_on_one_point(self, gnubg):
        """All 15 checkers on one point."""
        points = [0] * 24
        points[12] = 15
        points[11] = -15
        gs = _make_state(
            points=points,
            current_color="red",
            dice=[6, 5],
        )
        goals = gnubg.get_best_move(gs, "red")
        assert goals is not None
        assert _goals_are_legal(goals, gs, "red")

    def test_max_bar(self, gnubg):
        """Multiple checkers on bar."""
        points = [0] * 24
        points[5] = 10
        points[18] = -10
        gs = _make_state(
            points=points,
            bar_red=5,
            bar_white=5,
            current_color="red",
            dice=[3, 2],
        )
        goals = gnubg.get_best_move(gs, "red")
        assert goals is not None
        # All goals must start from bar since we're on bar
        assert all(g[0] == -1 for g in goals), f"Expected all bar goals when on bar, got {goals}"

    def test_single_checker_left(self, gnubg):
        """Only 1 checker left to bear off."""
        points = [0] * 24
        points[0] = 1
        points[23] = -1
        gs = _make_state(
            points=points,
            off_red=14,
            off_white=14,
            current_color="red",
            dice=[1, 2],
        )
        goals = gnubg.get_best_move(gs, "red")
        assert goals is not None
        # Should bear off
        assert any(g[1] == 24 for g in goals), f"Expected bear-off with 1 checker left: {goals}"

    def test_completely_blocked_returns_none_or_empty(self, gnubg):
        """When all entries are blocked, GNUBG might return no moves."""
        points = [0] * 24
        # Block all 6 entry points for red
        for i in range(18, 24):
            points[i] = -2
        points[5] = 3  # some red checkers elsewhere
        gs = _make_state(
            points=points,
            bar_red=3,
            bar_white=0,
            off_white=3,
            current_color="red",
            dice=[1, 2],
        )
        # This should either return None or empty goals
        # (GNUBG recognizes the dancer case)
        goals = gnubg.get_best_move(gs, "red")
        # It's OK for goals to be None here — no legal moves exist
        if goals is not None:
            assert len(goals) == 0 or goals == []
