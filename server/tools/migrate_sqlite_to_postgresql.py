"""One-time migration: copy the committed SQLite DB into PostgreSQL.

Reads `var/server/playpalace.db` (SQLite) and inserts all rows into the
PostgreSQL database specified by DATABASE_URL (or the --db-url flag).

Usage:
    cd server
    uv run python tools/migrate_sqlite_to_postgresql.py

Environment:
    DATABASE_URL  — PostgreSQL connection string (required).
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path

import asyncpg


REPO_ROOT = Path(__file__).resolve().parents[2]
SERVER_DIR = REPO_ROOT / "server"
SQLITE_PATH = REPO_ROOT / "var" / "server" / "playpalace.db"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Migrate committed SQLite data to PostgreSQL.",
    )
    parser.add_argument(
        "--sqlite-path",
        type=Path,
        default=SQLITE_PATH,
        help="Path to the SQLite database file.",
    )
    parser.add_argument(
        "--db-url",
        default=None,
        help="PostgreSQL DSN (default: $DATABASE_URL).",
    )
    return parser.parse_args()


def _read_sqlite(path: Path) -> dict[str, list[dict]]:
    """Read all tables from SQLite into dict-of-lists."""
    conn = sqlite3.connect(str(path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    result: dict[str, list[dict]] = {}
    for name in tables:
        cursor.execute(f'SELECT * FROM "{name}"')
        rows = [dict(row) for row in cursor.fetchall()]
        result[name] = rows
        print(f"  SQLite [{name}]: {len(rows)} rows")
    conn.close()
    return result


def _coerce_row(table: str, row: dict) -> dict:
    """Coerce types for PostgreSQL compatibility."""
    coerced = dict(row)
    for key, value in coerced.items():
        if value is None:
            continue
        # booleans: SQLite uses 0/1; asyncpg expects Python bools for BOOLEAN
        # but our schema uses INTEGER for approved/is_bot, so keep as int
        # Timestamps/integers should be int
        if key in ("id", "trust_level", "approved", "duration_ticks", "online_ticks",
                     "target_online_ticks", "game_join_tick", "expires_at", "created_at",
                     "revoked_at"):
            coerced[key] = int(value)
    return coerced


_SQLITE_TO_PG_TABLES: dict[str, str] = {
    "users": """
        INSERT INTO users (id, username, password_hash, uuid, locale,
                           preferences_json, trust_level, approved, fluent_languages)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        ON CONFLICT (username) DO NOTHING
    """,
    "transcriber_assignments": """
        INSERT INTO transcriber_assignments (user_id, lang_code)
        VALUES ($1, $2)
        ON CONFLICT DO NOTHING
    """,
    "tables": """
        INSERT INTO tables (table_id, game_type, host, members_json,
                            game_json, status)
        VALUES ($1, $2, $3, $4, $5, $6)
        ON CONFLICT (table_id) DO NOTHING
    """,
    "saved_tables": """
        INSERT INTO saved_tables (username, save_name, game_type,
                                  game_json, members_json, saved_at)
        VALUES ($1, $2, $3, $4, $5, $6)
    """,
    "game_results": """
        INSERT INTO game_results (game_type, timestamp, duration_ticks, custom_data)
        VALUES ($1, $2, $3, $4)
    """,
    "game_result_players": """
        INSERT INTO game_result_players (result_id, player_id, player_name,
                                         is_bot, is_virtual_bot)
        VALUES ($1, $2, $3, $4, $5)
    """,
    "player_ratings": """
        INSERT INTO player_ratings (player_id, game_type, mu, sigma)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (player_id, game_type) DO NOTHING
    """,
    "refresh_tokens": """
        INSERT INTO refresh_tokens (username, token, expires_at,
                                    created_at, revoked_at, replaced_by)
        VALUES ($1, $2, $3, $4, $5, $6)
        ON CONFLICT (token) DO NOTHING
    """,
    "virtual_bots": """
        INSERT INTO virtual_bots (name, state, online_ticks,
                                  target_online_ticks, table_id, game_join_tick)
        VALUES ($1, $2, $3, $4, $5, $6)
        ON CONFLICT (name) DO NOTHING
    """,
}

# Column order for each table (matching the INSERT statements above).
_TABLE_COLUMNS: dict[str, list[str]] = {
    "users": ["id", "username", "password_hash", "uuid", "locale",
              "preferences_json", "trust_level", "approved", "fluent_languages"],
    "transcriber_assignments": ["user_id", "lang_code"],
    "tables": ["table_id", "game_type", "host", "members_json",
               "game_json", "status"],
    "saved_tables": ["username", "save_name", "game_type",
                     "game_json", "members_json", "saved_at"],
    "game_results": ["game_type", "timestamp", "duration_ticks", "custom_data"],
    "game_result_players": ["result_id", "player_id", "player_name",
                            "is_bot", "is_virtual_bot"],
    "player_ratings": ["player_id", "game_type", "mu", "sigma"],
    "refresh_tokens": ["username", "token", "expires_at",
                       "created_at", "revoked_at", "replaced_by"],
    "virtual_bots": ["name", "state", "online_ticks",
                     "target_online_ticks", "table_id", "game_join_tick"],
}


async def _migrate(sqlite_data: dict[str, list[dict]], dsn: str) -> int:
    conn = await asyncpg.connect(dsn)
    total = 0
    try:
        for table_name, sql in _SQLITE_TO_PG_TABLES.items():
            rows = sqlite_data.get(table_name, [])
            if not rows:
                continue
            for row in rows:
                coerced = _coerce_row(table_name, row)
                values = [coerced.get(col) for col in _TABLE_COLUMNS[table_name]]
                await conn.execute(sql, *values)
                total += 1
            print(f"  PG [{table_name}]: migrated {len(rows)} rows")
    finally:
        await conn.close()
    return total


async def main() -> None:
    args = _parse_args()

    dsn = args.db_url or os.environ.get("DATABASE_URL")
    if not dsn:
        print("ERROR: DATABASE_URL not set and --db-url not provided.", file=sys.stderr)
        sys.exit(1)

    sqlite_path = args.sqlite_path
    if not sqlite_path.exists():
        print(f"ERROR: SQLite database not found at {sqlite_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Reading SQLite: {sqlite_path}")
    sqlite_data = _read_sqlite(sqlite_path)

    total_rows = sum(len(rows) for rows in sqlite_data.values())
    if total_rows == 0:
        print("No data to migrate.")
        return

    print(f"\nMigrating {total_rows} rows to PostgreSQL ...")
    migrated = await _migrate(sqlite_data, dsn)
    print(f"Done — {migrated} rows inserted into PostgreSQL.")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
