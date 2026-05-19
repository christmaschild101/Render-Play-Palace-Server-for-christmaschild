"""GNUBG subprocess integration for Backgammon bot AI.

Manages a persistent gnubg-cli --tty subprocess for move evaluation.
Falls back to random moves when GNUBG is unavailable.
"""

from __future__ import annotations

import base64
import logging
import queue
import re
import shutil
import subprocess
import threading
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from .state import BackgammonGameState

log = logging.getLogger(__name__)

_available: bool | None = None  # None = untested


def _find_gnubg() -> str | None:
    """Find gnubg-cli executable on PATH."""
    for name in ("gnubg-cli", "gnubg-cli.exe", "gnubg", "gnubg.exe"):
        path = shutil.which(name)
        if path:
            return path
    return None


def is_gnubg_available() -> bool:
    """Check if GNUBG binary is on PATH. Caches result after first check."""
    global _available
    if _available is not None:
        return _available
    _available = _find_gnubg() is not None
    if not _available:
        log.info("GNUBG not found on PATH; bot will use random fallback")
    return _available


# ---------------------------------------------------------------------------
# Position ID encoding
# ---------------------------------------------------------------------------


def encode_position_id(state: BackgammonGameState) -> str:
    """Encode the board as a GNUBG Position ID (14-char base64 string).

    GNUBG position key is 80 bits built from unary-encoded checker counts:
      First half: NOT-on-roll player's points 1-24 (from their perspective) + bar
      Second half: on-roll player's points 1-24 (from their perspective) + bar
    Each point: N ones followed by a zero separator. 80 bits total.
    Packed little-endian into 10 bytes, then base64-encoded (no padding).

    We always encode from the on-roll player's perspective, with the
    opponent (not-on-roll) encoded first per the GNUBG spec.
    """
    board = state.board

    # Build checker arrays from each player's perspective
    # Red: point 1 = index 0, point 24 = index 23 (positive values)
    # White: point 1 (their perspective) = index 23 (negative values)
    red_counts = []
    for i in range(24):
        red_counts.append(max(0, board.points[i]))
    red_bar = board.bar_red

    white_counts = []
    for i in range(23, -1, -1):  # White's point 1 = index 23
        white_counts.append(max(0, -board.points[i]))
    white_bar = board.bar_white

    # GNUBG format: opponent (not-on-roll) first, then on-roll player
    if state.current_color == "red":
        first_counts, first_bar = white_counts, white_bar  # opponent
        second_counts, second_bar = red_counts, red_bar  # on-roll
    else:
        first_counts, first_bar = red_counts, red_bar  # opponent
        second_counts, second_bar = white_counts, white_bar  # on-roll

    # Build bit string: for each player, 24 points + bar, unary encoded
    bits: list[int] = []
    for count in first_counts:
        bits.extend([1] * count)
        bits.append(0)
    bits.extend([1] * first_bar)
    bits.append(0)

    for count in second_counts:
        bits.extend([1] * count)
        bits.append(0)
    bits.extend([1] * second_bar)
    bits.append(0)

    # Pad to exactly 80 bits
    while len(bits) < 80:
        bits.append(0)

    # Pack into 10 bytes, little-endian bit order
    key_bytes = bytearray(10)
    for i, bit in enumerate(bits[:80]):
        if bit:
            key_bytes[i // 8] |= 1 << (i % 8)

    return base64.b64encode(bytes(key_bytes)).decode("ascii").rstrip("=")


# ---------------------------------------------------------------------------
# Hint parsing
# ---------------------------------------------------------------------------

# Matches lines like: "    1. Cubeful 0-ply    8/5 6/5                      Eq.: +0.201"
_HINT_RE = re.compile(
    r"^\s*(\d+)\.\s+Cubeful\s+\d+-ply\s+(.*?)\s+Eq\.",
)

# Individual sub-move patterns within the move string
# "8/5" or "24/18(2)" or "bar/22" or "3/off"
_SUBMOVE_RE = re.compile(r"(bar|\d+)/(off|\d+)(?:\((\d+)\))?")


def parse_hint_line(line: str) -> list[tuple[str, str, int]] | None:
    """Parse a single hint line into a list of (source, dest, count) tuples.

    Returns None if the line doesn't match.
    Source/dest are strings: "bar", "off", or point number strings.
    Count is how many checkers make that sub-move (default 1).
    """
    m = _HINT_RE.match(line)
    if not m:
        return None
    move_str = m.group(2).strip()
    submoves = []
    for sm in _SUBMOVE_RE.finditer(move_str):
        src = sm.group(1)
        dst = sm.group(2)
        count = int(sm.group(3)) if sm.group(3) else 1
        submoves.append((src, dst, count))
    return submoves if submoves else None


def hint_to_goals(
    hint_submoves: list[tuple[str, str, int]],
    color: str,
) -> list[tuple[int, int]]:
    """Convert parsed GNUBG hint sub-moves to checker goals.

    Returns a list of (source_idx, dest_idx) pairs representing where
    each checker should START and where it should END UP. These are NOT
    individual die moves — compound moves like "24/14" become a single
    goal (24, 14). The bot resolves each goal into individual die steps
    at execution time using the game's legal move generator, which
    correctly handles bar-first rules, forced dice, and overshoot.
    """
    goals: list[tuple[int, int]] = []
    for src_str, dst_str, count in hint_submoves:
        src_idx = _linear_to_index(_parse_linear(src_str), color)
        dst_idx = _linear_to_index(_parse_linear(dst_str), color)
        for _ in range(count):
            goals.append((src_idx, dst_idx))
    return goals


def resolve_next_action(
    goals: list[tuple[int, int]],
    state: "BackgammonGameState",
    color: str,
    forced_dice: list[int] | None = None,
) -> str | None:
    """Pick the next legal move that progresses toward a GNUBG goal.

    Examines the goal list and finds a legal move that advances a checker
    toward its target. Modifies `goals` in place (removes completed goals,
    updates source of in-progress goals). Returns an action string like
    "point_{src}_{dst}", or None if no goal can be progressed.
    """
    from .moves import generate_legal_moves
    from .state import bar_count, remaining_dice_unique

    usable_dice = remaining_dice_unique(state)
    if forced_dice is not None:
        usable_dice = [d for d in usable_dice if d in forced_dice]
    if not usable_dice:
        goals.clear()
        return None

    # Build all legal moves for quick lookup
    legal_by_source: dict[int, list[tuple[int, int, int]]] = {}
    for die_val in usable_dice:
        for m in generate_legal_moves(state, color, die_val):
            legal_by_source.setdefault(m.source, []).append((m.source, m.destination, die_val))

    # If on bar, we must enter first — find a bar goal or any bar entry
    on_bar = bar_count(state, color) > 0
    if on_bar:
        bar_moves = legal_by_source.get(-1, [])
        if not bar_moves:
            goals.clear()
            return None
        # Find a goal that starts from bar
        for i, (gsrc, gdst) in enumerate(goals):
            if gsrc == -1:
                # Find best bar entry for this goal
                for src, dst, dv in bar_moves:
                    # If entering directly at the goal destination, perfect
                    if dst == gdst:
                        goals[i] = (gdst, gdst)  # Mark complete
                        return f"point_{src}_{dst}"
                # Enter anywhere legal and update goal source
                src, dst, dv = bar_moves[0]
                goals[i] = (dst, gdst)
                return f"point_{src}_{dst}"
        # No bar goal found but we're on bar — just enter
        src, dst, dv = bar_moves[0]
        return f"point_{src}_{dst}"

    # Not on bar — try each goal in order
    for i, (gsrc, gdst) in enumerate(goals):
        if gsrc == gdst:
            # Goal already complete (e.g. checker reached destination)
            continue

        moves_from_src = legal_by_source.get(gsrc, [])
        if not moves_from_src:
            continue

        # Exact match: a legal move reaches the goal destination directly
        for src, dst, dv in moves_from_src:
            if dst == gdst:
                goals[i] = (gdst, gdst)  # Mark complete
                return f"point_{src}_{dst}"

        # Partial: pick the move that gets closest to the destination
        # For a goal that needs multiple dice (compound move), we want
        # to advance toward the destination. "Closest" depends on color
        # direction, but since all moves from this source go in the
        # right direction, pick the one nearest to gdst.
        best = None
        best_dist = 999
        for src, dst, dv in moves_from_src:
            if dst == 24:
                # Bear off — if the goal is also bear-off, great
                if gdst == 24:
                    goals[i] = (24, 24)
                    return f"point_{src}_{dst}"
                continue  # Don't bear off if the goal isn't bear-off
            dist = abs(dst - gdst)
            if dist < best_dist:
                best_dist = dist
                best = (src, dst)

        if best is not None:
            goals[i] = (best[1], gdst)  # Update source to new position
            return f"point_{best[0]}_{best[1]}"

    # No goal could be progressed — clear stale goals
    goals.clear()
    return None


def _parse_linear(point_str: str) -> int:
    """Parse a GNUBG point string to linear position (bar=25, off=0)."""
    if point_str == "bar":
        return 25
    if point_str == "off":
        return 0
    return int(point_str)


def _linear_to_index(pos: int, color: str) -> int:
    """Convert a linear position to a board index.

    Linear space: bar=25, points 24→1, off=0
    Board indices: bar=-1, points 0-23, off=24

    Red:   point N → index N-1  (point 1 = index 0)
    White: point N → index 24-N (point 1 = index 23)
    """
    if pos == 25:  # bar
        return -1
    if pos <= 0:  # off (0 or negative from overshoot bear-off)
        return 24
    if color == "red":
        return pos - 1
    else:
        return 24 - pos


# ---------------------------------------------------------------------------
# Subprocess manager
# ---------------------------------------------------------------------------


class GnubgProcess:
    """Manages a persistent gnubg-cli subprocess for move evaluation.

    Uses a persistent reader thread to consume stdout lines into a queue,
    since select() doesn't work with subprocess pipes on Windows.

    Commands are batched and sent together; only a single short idle wait
    is needed after the final command to collect all output.
    """

    # Idle wait after the last line of output before we consider GNUBG done.
    # GNUBG responds in <1ms locally, so 50ms is generous.
    _IDLE_WAIT = 0.05
    # Longer idle wait for startup (banner can be slow).
    _STARTUP_IDLE_WAIT = 0.5

    def __init__(self, ply: int = 0):
        self._proc: subprocess.Popen | None = None
        self._lock = threading.Lock()
        self._ply = ply
        self._started = False
        self._output_queue: queue.Queue[str | None] = queue.Queue()

    def start(self) -> bool:
        """Start the GNUBG subprocess. Returns True on success."""
        exe = _find_gnubg()
        if not exe:
            return False
        try:
            self._proc = subprocess.Popen(
                [exe, "-t", "-r", "-q"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                bufsize=1,
            )
            # Start persistent reader thread
            self._output_queue = queue.Queue()
            reader = threading.Thread(target=self._reader_loop, daemon=True)
            reader.start()

            # Read startup banner (may be slow)
            self._read_until_idle(idle_wait=self._STARTUP_IDLE_WAIT)
            # Set ply depth and start a game — batch these setup commands
            self._send_batch(
                [
                    f"set evaluation chequerplay evaluation plies {self._ply}",
                    "new game",
                ]
            )
            self._read_until_idle(idle_wait=self._STARTUP_IDLE_WAIT)
            self._started = True
            log.info("GNUBG subprocess started (ply=%d)", self._ply)
            return True
        except (OSError, FileNotFoundError) as e:
            log.warning("Failed to start GNUBG: %s", e)
            self._proc = None
            return False

    def _reader_loop(self) -> None:
        """Persistent thread that reads stdout lines into the queue."""
        try:
            while self._proc and self._proc.stdout:
                line = self._proc.stdout.readline()
                if not line:
                    self._output_queue.put(None)
                    return
                self._output_queue.put(line.rstrip("\n\r"))
        except (ValueError, OSError):
            self._output_queue.put(None)

    def stop(self) -> None:
        """Terminate the subprocess."""
        with self._lock:
            if self._proc:
                try:
                    self._proc.stdin.write("quit\n")
                    self._proc.stdin.flush()
                    self._proc.wait(timeout=3)
                except Exception:
                    try:
                        self._proc.kill()
                    except Exception:
                        pass
                self._proc = None
                self._started = False

    # ------------------------------------------------------------------
    # Public query API
    # ------------------------------------------------------------------

    def get_best_move(
        self, state: BackgammonGameState, color: str, timeout: float = 5.0
    ) -> list[tuple[int, int]] | None:
        """Get the best move for the current position.

        Returns a list of (source_idx, dest_idx) pairs, or None on failure.
        """
        with self._lock:
            if not self._proc or not self._started:
                return None
            try:
                return self._query_hint(state, color, timeout, pick_worst=False)
            except Exception as e:
                log.warning("GNUBG query failed: %s", e)
                self._restart()
                return None

    def get_worst_move(
        self, state: BackgammonGameState, color: str, timeout: float = 5.0
    ) -> list[tuple[int, int]] | None:
        """Get the worst move (Whackgammon). Asks for many hints, picks last."""
        with self._lock:
            if not self._proc or not self._started:
                return None
            try:
                return self._query_hint(state, color, timeout, pick_worst=True)
            except Exception as e:
                log.warning("GNUBG query failed: %s", e)
                self._restart()
                return None

    def get_cube_decision(
        self, state: BackgammonGameState, color: str, timeout: float = 5.0
    ) -> str | None:
        """Get GNUBG's cube decision for the current position.

        Always queries from the on-roll player's perspective. Returns one of:
            "no-double"    — should not double
            "too-good"     — too good to double (would lose gammon value)
            "double-take"  — should double, opponent should take
            "double-pass"  — should double, opponent should drop
            None — on failure
        """
        with self._lock:
            if not self._proc or not self._started:
                return None
            try:
                return self._query_cube(state, color, timeout)
            except Exception as e:
                log.warning("GNUBG cube query failed: %s", e)
                self._restart()
                return None

    def get_cube_hint_text(
        self, state: BackgammonGameState, color: str, timeout: float = 5.0
    ) -> str | None:
        """Get a human-readable cube hint string from GNUBG.

        Returns the "Proper cube action" line, or None on failure.
        """
        with self._lock:
            if not self._proc or not self._started:
                return None
            try:
                output = self._setup_and_query_cube(state, color, timeout)
                for line in output:
                    if "Proper cube action" in line:
                        return line.strip()
                return None
            except Exception as e:
                log.warning("GNUBG cube hint failed: %s", e)
                self._restart()
                return None

    def get_move_hint_text(
        self,
        state: BackgammonGameState,
        color: str,
        hint_count: int = 3,
        timeout: float = 5.0,
    ) -> list[str] | None:
        """Get ranked move hints as human-readable strings.

        Returns a list like ["1. 8/5 6/5", "2. 13/7"] or None on failure.
        """
        with self._lock:
            if not self._proc or not self._started:
                return None
            try:
                unused_dice = [d for d, u in zip(state.dice, state.dice_used) if not u]
                if len(unused_dice) < 2:
                    return None

                self._send_batch(
                    [
                        *self._position_commands(state),
                        f"set dice {unused_dice[0]} {unused_dice[1]}",
                        f"hint {hint_count}",
                    ]
                )
                output = self._read_until_match(
                    lambda line: _HINT_RE.match(line) is not None,
                    timeout=timeout,
                )

                hints = []
                for line in output:
                    m = _HINT_RE.match(line)
                    if m:
                        hints.append(f"{m.group(1)}. {m.group(2).strip()}")
                return hints or None
            except Exception as e:
                log.warning("GNUBG move hint failed: %s", e)
                self._restart()
                return None

    # ------------------------------------------------------------------
    # Internal query implementations
    # ------------------------------------------------------------------

    @staticmethod
    def _position_commands(state: BackgammonGameState) -> list[str]:
        """Build the commands to set up a board position."""
        return [
            f"set board {encode_position_id(state)}",
            "set turn 1",
        ]

    @staticmethod
    def _cube_commands(state: BackgammonGameState, color: str) -> list[str]:
        """Build the commands to set up cube state."""
        cmds = [f"set cube value {state.cube_value}"]
        if not state.cube_owner:
            cmds.append("set cube centre")
        elif state.cube_owner == color:
            cmds.append("set cube owner 1")  # on-roll player
        else:
            cmds.append("set cube owner 0")  # opponent
        return cmds

    def _setup_and_query_cube(
        self,
        state: BackgammonGameState,
        color: str,
        timeout: float,
    ) -> list[str]:
        """Set position + cube, send hint 0, return raw output lines."""
        self._send_batch(
            [
                *self._position_commands(state),
                *self._cube_commands(state, color),
                "hint 0",
            ]
        )
        return self._read_until_match(
            lambda line: "proper cube action" in line.lower()
            or (line.strip().startswith("1.") and "No double" in line),
            timeout=timeout,
        )

    def _query_cube(
        self,
        state: BackgammonGameState,
        color: str,
        timeout: float,
    ) -> str | None:
        """Send position to GNUBG and parse the cube evaluation.

        Returns one of:
            "no-double"    — should not double
            "too-good"     — too good to double (would lose gammon value)
            "double-take"  — should double, opponent should take
            "double-pass"  — should double, opponent should drop
            None           — on failure
        """
        output = self._setup_and_query_cube(state, color, timeout)

        # Parse "Proper cube action:" line
        for line in output:
            low = line.lower()
            if "proper cube action" not in low:
                continue
            if "no double" in low or "no redouble" in low:
                if "too good" in low:
                    return "too-good"
                return "no-double"
            if "double" in low or "redouble" in low:
                if "pass" in low or "drop" in low:
                    return "double-pass"
                return "double-take"  # "take" or unqualified double
            if "take" in low:
                return "double-take"  # opponent asked, should take
            if "pass" in low or "drop" in low:
                return "double-pass"  # opponent asked, should drop

        # Fallback: parse the cubeful equities to decide
        # Line format: "1. No double           +0.098"
        equities: dict[str, float] = {}
        for line in output:
            line_s = line.strip()
            if line_s.startswith("1.") and "No double" in line_s:
                try:
                    equities["no-double"] = float(line_s.split()[-1])
                except ValueError:
                    pass
            elif "pass" in line_s.lower() and "Double" in line_s:
                try:
                    equities["double-pass"] = float(line_s.split()[-2])
                except (ValueError, IndexError):
                    pass
            elif "take" in line_s.lower() and "Double" in line_s:
                try:
                    equities["double-take"] = float(line_s.split()[-2])
                except (ValueError, IndexError):
                    pass

        if equities:
            nd = equities.get("no-double", -999)
            dt = equities.get("double-take", -999)
            dp = equities.get("double-pass", -999)
            best = max(nd, dt, dp)
            if best == nd:
                return "no-double"
            if best == dp:
                return "double-pass"
            return "double-take"

        return None

    def _query_hint(
        self,
        state: BackgammonGameState,
        color: str,
        timeout: float,
        pick_worst: bool = False,
    ) -> list[tuple[int, int]] | None:
        """Send position to GNUBG and parse the hint response.

        Returns a list of checker goals as (source_idx, dest_idx) pairs.
        These are final destinations, not individual die steps.
        """
        unused_dice = [d for d, u in zip(state.dice, state.dice_used) if not u]
        if len(unused_dice) < 2:
            if unused_dice:
                d = unused_dice[0]
                unused_dice = [d, d]
            else:
                log.debug("GNUBG query skipped: no unused dice")
                return None

        hint_count = 999 if pick_worst else 1
        self._send_batch(
            [
                *self._position_commands(state),
                f"set dice {unused_dice[0]} {unused_dice[1]}",
                f"hint {hint_count}",
            ]
        )
        output = self._read_until_match(
            lambda line: _HINT_RE.match(line) is not None,
            timeout=timeout,
        )
        log.debug("GNUBG hint response: %d lines", len(output))

        # Parse all hint lines
        last_submoves = None
        first_submoves = None
        for line in output:
            submoves = parse_hint_line(line)
            if submoves:
                if first_submoves is None:
                    first_submoves = submoves
                last_submoves = submoves

        chosen = last_submoves if pick_worst else first_submoves
        if chosen:
            goals = hint_to_goals(chosen, color)
            log.debug("GNUBG goals: %s", goals)
            return goals
        log.debug("GNUBG: no hint parsed from output")
        return None

    # ------------------------------------------------------------------
    # Low-level I/O
    # ------------------------------------------------------------------

    def _send(self, command: str) -> None:
        """Send a single command to GNUBG."""
        if self._proc and self._proc.stdin:
            self._proc.stdin.write(command + "\n")
            self._proc.stdin.flush()

    def _send_batch(self, commands: list[str]) -> None:
        """Send multiple commands to GNUBG at once.

        All commands are written before flushing, so GNUBG processes them
        back-to-back with no idle gaps between them.
        """
        if self._proc and self._proc.stdin:
            self._proc.stdin.write("".join(cmd + "\n" for cmd in commands))
            self._proc.stdin.flush()

    def _read_until_idle(
        self,
        timeout: float = 5.0,
        idle_wait: float | None = None,
    ) -> list[str]:
        """Read GNUBG output from the queue until idle.

        GNUBG is considered idle when no new output arrives for `idle_wait`
        seconds after receiving at least one line. Use only for startup/setup
        where there's no specific pattern to wait for.
        """
        import time

        if idle_wait is None:
            idle_wait = self._IDLE_WAIT

        lines: list[str] = []
        deadline = time.monotonic() + timeout

        while time.monotonic() < deadline:
            remaining = deadline - time.monotonic()
            wait_time = min(idle_wait, remaining)
            try:
                item = self._output_queue.get(timeout=max(0.01, wait_time))
                if item is None:  # EOF
                    break
                lines.append(item)
            except queue.Empty:
                if lines:
                    break

        return lines

    def _read_until_match(
        self,
        predicate: Callable[[str], bool],
        timeout: float = 5.0,
    ) -> list[str]:
        """Read GNUBG output until a line matches the predicate.

        Returns all lines read (including the match). This is the correct
        way to wait for query results — it doesn't depend on idle timing,
        so it works regardless of how long GNUBG takes to compute.
        """
        import time

        lines: list[str] = []
        deadline = time.monotonic() + timeout

        while time.monotonic() < deadline:
            remaining = deadline - time.monotonic()
            try:
                item = self._output_queue.get(timeout=max(0.01, remaining))
                if item is None:  # EOF
                    break
                lines.append(item)
                if predicate(item):
                    # Drain any remaining quick output (e.g. multi-hint)
                    self._drain_quick(lines)
                    break
            except queue.Empty:
                pass

        return lines

    def _drain_quick(self, lines: list[str]) -> None:
        """Drain any output that arrives quickly after a match.

        After seeing the first hint line, there may be more (equity details,
        additional hints for pick_worst). Grab them without a long wait.
        """
        import time

        deadline = time.monotonic() + self._IDLE_WAIT
        while time.monotonic() < deadline:
            remaining = deadline - time.monotonic()
            try:
                item = self._output_queue.get(timeout=max(0.001, remaining))
                if item is None:
                    break
                lines.append(item)
            except queue.Empty:
                break

    def _restart(self) -> None:
        """Kill and restart the subprocess."""
        log.info("Restarting GNUBG subprocess")
        if self._proc:
            try:
                self._proc.kill()
            except Exception:
                pass
            self._proc = None
        self._started = False
        self.start()
