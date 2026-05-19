"""Batch backgammon simulation — run many games in parallel and check win rates."""

import json
import subprocess
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

SERVER_DIR = Path(__file__).parent.parent
CLI = SERVER_DIR / "cli.py"
GAMES_PER_DIFFICULTY = 500
WORKERS = 4

DIFFICULTIES = ["random", "simple"]


def run_one_game(difficulty: str, game_id: int) -> dict:
    """Run a single backgammon simulation and return the result."""
    result = subprocess.run(
        [
            sys.executable,
            str(CLI),
            "simulate",
            "backgammon",
            "--bots",
            "2",
            "-o",
            f"bot_difficulty={difficulty}",
            "--json",
            "--quiet",
        ],
        capture_output=True,
        text=True,
        timeout=300,
        cwd=str(SERVER_DIR),
    )
    if result.returncode != 0:
        # Capture the last part of stderr for the traceback
        stderr = result.stderr.strip()
        # Get the last traceback if present
        if "Traceback" in stderr:
            stderr = stderr[stderr.rfind("Traceback") :]
        return {"difficulty": difficulty, "id": game_id, "error": stderr}

    data = json.loads(result.stdout)
    messages = data.get("messages", [])
    timed_out = data.get("timed_out", False)

    # Find winner from messages
    winner_color = None
    for msg in reversed(messages):
        if "wins the match" in msg or "wins" in msg:
            # "Alice wins X points." or "Alice wins the match!"
            # Alice is always Red (first bot), Bob is always White
            if msg.startswith("Alice"):
                winner_color = "red"
            elif msg.startswith("Bob"):
                winner_color = "white"
            break

    return {
        "difficulty": difficulty,
        "id": game_id,
        "winner": winner_color,
        "ticks": data.get("ticks", 0),
        "timed_out": timed_out,
        "error": None,
    }


def main():
    print(f"Running {GAMES_PER_DIFFICULTY} games per difficulty with {WORKERS} workers")
    print(f"Difficulties: {', '.join(DIFFICULTIES)}")
    print()

    all_tasks = []
    for diff in DIFFICULTIES:
        for i in range(GAMES_PER_DIFFICULTY):
            all_tasks.append((diff, i))

    results = []
    completed = 0
    total = len(all_tasks)

    with ProcessPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(run_one_game, diff, gid): (diff, gid) for diff, gid in all_tasks}
        for future in as_completed(futures):
            completed += 1
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                diff, gid = futures[future]
                results.append({"difficulty": diff, "id": gid, "error": str(e)})

            if completed % 50 == 0 or completed == total:
                print(f"  {completed}/{total} games complete")

    # Aggregate results per difficulty
    print()
    print("=" * 60)
    for diff in DIFFICULTIES:
        diff_results = [r for r in results if r["difficulty"] == diff]
        errors = [r for r in diff_results if r.get("error")]
        timeouts = [r for r in diff_results if r.get("timed_out")]
        wins = Counter(r.get("winner") for r in diff_results if r.get("winner"))
        total_games = len(diff_results) - len(errors)
        red_wins = wins.get("red", 0)
        white_wins = wins.get("white", 0)
        ticks = [r["ticks"] for r in diff_results if not r.get("error")]
        avg_ticks = sum(ticks) / len(ticks) if ticks else 0

        print(f"\n  Difficulty: {diff}")
        print(f"  Games: {total_games} (errors: {len(errors)}, timeouts: {len(timeouts)})")
        print(
            f"  Red wins:   {red_wins:4d}  ({red_wins / total_games * 100:5.1f}%)"
            if total_games
            else "  Red wins: 0"
        )
        print(
            f"  White wins: {white_wins:4d}  ({white_wins / total_games * 100:5.1f}%)"
            if total_games
            else "  White wins: 0"
        )
        print(f"  Avg ticks: {avg_ticks:.0f}")

        if total_games:
            # Simple chi-squared test against 50/50
            expected = total_games / 2
            chi2 = ((red_wins - expected) ** 2 + (white_wins - expected) ** 2) / expected
            fair = "FAIR" if chi2 < 3.84 else "BIASED"  # p=0.05 threshold
            print(f"  Chi-squared: {chi2:.2f} ({fair} at p=0.05)")

        if errors:
            # Deduplicate errors by last line (the actual exception)
            error_types = Counter()
            error_samples = {}
            for e in errors:
                err_text = e["error"]
                last_line = err_text.strip().split("\n")[-1] if err_text else "unknown"
                error_types[last_line] += 1
                if last_line not in error_samples:
                    error_samples[last_line] = err_text
            print(f"  Error breakdown:")
            for err_type, count in error_types.most_common():
                print(f"    [{count}x] {err_type}")
                print(f"         Full trace:")
                for line in error_samples[err_type].split("\n"):
                    print(f"           {line}")

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
