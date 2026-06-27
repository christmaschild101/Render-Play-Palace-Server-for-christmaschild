"""PostgreSQL database for persistence via asyncpg + Supabase."""

import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import asyncpg

from server.core.tables.table import Table
from server.core.users.base import TrustLevel


@dataclass
class UserRecord:
    """User record loaded from the database."""

    id: int
    username: str
    password_hash: str
    uuid: str
    locale: str = "en"
    preferences_json: str = "{}"
    trust_level: TrustLevel = TrustLevel.USER
    approved: bool = False
    fluent_languages: list[str] = field(default_factory=list)


@dataclass
class SavedTableRecord:
    """Saved table record from the database."""

    id: int
    username: str
    save_name: str
    game_type: str
    game_json: str
    members_json: str
    saved_at: str


@dataclass
class RefreshTokenRecord:
    """Refresh token record loaded from the database."""

    username: str
    token: str
    expires_at: int
    created_at: int
    revoked_at: int | None = None
    replaced_by: str | None = None


def _token_from_row(row: asyncpg.Record) -> RefreshTokenRecord:
    return RefreshTokenRecord(
        username=row["username"],
        token=row["token"],
        expires_at=row["expires_at"],
        created_at=row["created_at"],
        revoked_at=row["revoked_at"],
        replaced_by=row["replaced_by"],
    )


class Database:
    """PostgreSQL database for PlayPalace persistence via asyncpg.

    Stores users, tables, saved tables, game results, ratings, and virtual bots.
    Connects via the ``DATABASE_URL`` environment variable (set by Supabase or Render).
    """

    def __init__(self, db_path: str | Path = "playpalace.db"):
        self.db_path = Path(db_path)
        self._pool: asyncpg.Pool | None = None
        self._database_url: str | None = None

    @staticmethod
    def _load_dotenv() -> None:
        """Load DATABASE_URL from a .env file in the server directory, if present.

        Only sets the env var if it isn't already set — Render's env vars take
        precedence over the local .env file.
        """
        if os.environ.get("DATABASE_URL"):
            return
        dotenv_path = Path(__file__).resolve().parents[1] / ".env"
        if not dotenv_path.exists():
            dotenv_path = Path.cwd() / ".env"
        if not dotenv_path.exists():
            return
        try:
            for line in dotenv_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip("\"'")
                if key == "DATABASE_URL":
                    os.environ["DATABASE_URL"] = value
                    return
        except OSError:
            pass

    def _get_database_url(self) -> str:
        self._load_dotenv()
        url = self._database_url or os.environ.get("DATABASE_URL") or ""
        if not url:
            print(
                "ERROR: DATABASE_URL environment variable is not set. "
                "Please set it to your Supabase PostgreSQL connection string.",
                file=sys.stderr,
            )
            raise SystemExit(1)
        return url

    async def connect(self) -> None:
        dsn = self._get_database_url()
        try:
            self._pool = await asyncpg.create_pool(dsn=dsn, min_size=1, max_size=5)
        except Exception as exc:
            print(
                f"ERROR: Failed to connect to PostgreSQL: {exc}",
                file=sys.stderr,
            )
            raise SystemExit(1) from exc
        await self._create_tables()

    async def close(self) -> None:
        if self._pool:
            await self._pool.close()
            self._pool = None

    async def _execute(self, sql: str, *args: Any) -> str:
        if self._pool is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        async with self._pool.acquire() as conn:
            return await conn.execute(sql, *args)

    async def _fetch(self, sql: str, *args: Any) -> list[asyncpg.Record]:
        if self._pool is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        async with self._pool.acquire() as conn:
            return await conn.fetch(sql, *args)

    async def _fetchrow(self, sql: str, *args: Any) -> asyncpg.Record | None:
        if self._pool is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        async with self._pool.acquire() as conn:
            return await conn.fetchrow(sql, *args)

    async def _fetchval(self, sql: str, *args: Any) -> Any:
        if self._pool is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        async with self._pool.acquire() as conn:
            return await conn.fetchval(sql, *args)

    async def _create_tables(self) -> None:
        async with self._pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    uuid TEXT NOT NULL,
                    locale TEXT DEFAULT 'en',
                    preferences_json TEXT DEFAULT '{}',
                    trust_level INTEGER DEFAULT 1,
                    approved INTEGER DEFAULT 0,
                    fluent_languages TEXT DEFAULT '[]'
                )
            """)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS transcriber_assignments (
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    lang_code TEXT NOT NULL,
                    PRIMARY KEY (user_id, lang_code)
                )
            """)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS tables (
                    table_id TEXT PRIMARY KEY,
                    game_type TEXT NOT NULL,
                    host TEXT NOT NULL,
                    members_json TEXT NOT NULL,
                    game_json TEXT,
                    status TEXT DEFAULT 'waiting'
                )
            """)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS saved_tables (
                    id SERIAL PRIMARY KEY,
                    username TEXT NOT NULL,
                    save_name TEXT NOT NULL,
                    game_type TEXT NOT NULL,
                    game_json TEXT NOT NULL,
                    members_json TEXT NOT NULL,
                    saved_at TEXT NOT NULL
                )
            """)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS game_results (
                    id SERIAL PRIMARY KEY,
                    game_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    duration_ticks INTEGER,
                    custom_data TEXT
                )
            """)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS game_result_players (
                    id SERIAL PRIMARY KEY,
                    result_id INTEGER REFERENCES game_results(id) ON DELETE CASCADE,
                    player_id TEXT NOT NULL,
                    player_name TEXT NOT NULL,
                    is_bot INTEGER NOT NULL,
                    is_virtual_bot INTEGER NOT NULL DEFAULT 0
                )
            """)
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_game_results_type
                ON game_results(game_type)
            """)
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_game_results_timestamp
                ON game_results(timestamp)
            """)
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_result_players_player
                ON game_result_players(player_id)
            """)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS player_ratings (
                    player_id TEXT NOT NULL,
                    game_type TEXT NOT NULL,
                    mu REAL NOT NULL,
                    sigma REAL NOT NULL,
                    PRIMARY KEY (player_id, game_type)
                )
            """)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS refresh_tokens (
                    id SERIAL PRIMARY KEY,
                    username TEXT NOT NULL,
                    token TEXT UNIQUE NOT NULL,
                    expires_at INTEGER NOT NULL,
                    created_at INTEGER NOT NULL,
                    revoked_at INTEGER,
                    replaced_by TEXT
                )
            """)
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_refresh_tokens_username
                ON refresh_tokens(username)
            """)
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_refresh_tokens_expires
                ON refresh_tokens(expires_at)
            """)
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS virtual_bots (
                    name TEXT PRIMARY KEY,
                    state TEXT NOT NULL,
                    online_ticks INTEGER NOT NULL DEFAULT 0,
                    target_online_ticks INTEGER NOT NULL DEFAULT 0,
                    table_id TEXT,
                    game_join_tick INTEGER NOT NULL DEFAULT 0
                )
            """)
            # Case-insensitive unique index on username
            try:
                await conn.execute("""
                    CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username_lower
                    ON users(LOWER(username))
                """)
            except asyncpg.UniqueViolationError:
                print(
                    "ERROR: Duplicate usernames exist when compared case-insensitively. "
                    "Please resolve duplicates before restarting the server.",
                    file=sys.stderr,
                )
                raise SystemExit(1)

    # User operations

    _USER_COLUMNS = "id, username, password_hash, uuid, locale, preferences_json, trust_level, approved, fluent_languages"

    @staticmethod
    def _user_from_row(row: asyncpg.Record) -> UserRecord:
        trust_level_int = row["trust_level"] if row["trust_level"] is not None else 1
        return UserRecord(
            id=row["id"],
            username=row["username"],
            password_hash=row["password_hash"],
            uuid=row["uuid"],
            locale=row["locale"] or "en",
            preferences_json=row["preferences_json"] or "{}",
            trust_level=TrustLevel(trust_level_int),
            approved=bool(row["approved"]) if row["approved"] is not None else False,
            fluent_languages=json.loads(row["fluent_languages"] or "[]"),
        )

    async def get_user(self, username: str) -> UserRecord | None:
        row = await self._fetchrow(
            f"SELECT {self._USER_COLUMNS} FROM users WHERE LOWER(username) = LOWER($1)",
            username,
        )
        return self._user_from_row(row) if row else None

    async def create_user(
        self,
        username: str,
        password_hash: str,
        locale: str = "en",
        trust_level: TrustLevel = TrustLevel.USER,
        approved: bool = False,
    ) -> UserRecord:
        import uuid as uuid_module

        user_uuid = str(uuid_module.uuid4())
        row = await self._fetchrow(
            "INSERT INTO users (username, password_hash, uuid, locale, trust_level, approved) "
            "VALUES ($1, $2, $3, $4, $5, $6) RETURNING id",
            username, password_hash, user_uuid, locale, trust_level.value, 1 if approved else 0,
        )
        return UserRecord(
            id=row["id"],
            username=username,
            password_hash=password_hash,
            uuid=user_uuid,
            locale=locale,
            trust_level=trust_level,
            approved=approved,
        )

    async def user_exists(self, username: str) -> bool:
        val = await self._fetchval(
            "SELECT 1 FROM users WHERE LOWER(username) = LOWER($1)", username
        )
        return val is not None

    async def update_user_locale(self, username: str, locale: str) -> None:
        await self._execute(
            "UPDATE users SET locale = $1 WHERE LOWER(username) = LOWER($2)", locale, username
        )

    async def update_user_preferences(self, username: str, preferences_json: str) -> None:
        await self._execute(
            "UPDATE users SET preferences_json = $1 WHERE LOWER(username) = LOWER($2)",
            preferences_json, username,
        )

    async def update_user_password(self, username: str, password_hash: str) -> None:
        await self._execute(
            "UPDATE users SET password_hash = $1 WHERE LOWER(username) = LOWER($2)",
            password_hash, username,
        )

    # Refresh token operations

    async def store_refresh_token(
        self, username: str, token: str, expires_at: int, created_at: int
    ) -> None:
        await self._execute(
            "INSERT INTO refresh_tokens (username, token, expires_at, created_at) "
            "VALUES ($1, $2, $3, $4)",
            username, token, expires_at, created_at,
        )

    async def get_refresh_token(self, token: str) -> RefreshTokenRecord | None:
        row = await self._fetchrow(
            "SELECT username, token, expires_at, created_at, revoked_at, replaced_by "
            "FROM refresh_tokens WHERE token = $1",
            token,
        )
        return _token_from_row(row) if row else None

    async def revoke_refresh_token(
        self, token: str, revoked_at: int, replaced_by: str | None = None
    ) -> None:
        await self._execute(
            "UPDATE refresh_tokens SET revoked_at = $1, replaced_by = $2 WHERE token = $3",
            revoked_at, replaced_by, token,
        )

    async def revoke_user_refresh_tokens(self, username: str, revoked_at: int) -> None:
        await self._execute(
            "UPDATE refresh_tokens SET revoked_at = $1 "
            "WHERE LOWER(username) = LOWER($2) AND revoked_at IS NULL",
            revoked_at, username,
        )

    async def get_user_count(self) -> int:
        val = await self._fetchval("SELECT COUNT(*) FROM users")
        return val or 0

    async def initialize_trust_levels(self) -> str | None:
        rows = await self._fetch(
            "SELECT id, username FROM users WHERE trust_level IS NULL"
        )
        promoted_user = None

        if len(rows) == 1:
            total = await self._fetchval("SELECT COUNT(*) FROM users")
            if total == 1:
                username = rows[0]["username"]
                await self._execute(
                    "UPDATE users SET trust_level = $1 WHERE id = $2",
                    TrustLevel.SERVER_OWNER.value, rows[0]["id"],
                )
                promoted_user = username

        await self._execute(
            "UPDATE users SET trust_level = $1 WHERE trust_level IS NULL",
            TrustLevel.USER.value,
        )
        return promoted_user

    async def update_user_trust_level(self, username: str, trust_level: TrustLevel) -> None:
        await self._execute(
            "UPDATE users SET trust_level = $1 WHERE LOWER(username) = LOWER($2)",
            trust_level.value, username,
        )

    async def get_pending_users(self, exclude_banned: bool = True) -> list[UserRecord]:
        if exclude_banned:
            rows = await self._fetch(
                f"SELECT {self._USER_COLUMNS} FROM users "
                "WHERE approved = 0 AND trust_level > $1 ORDER BY username",
                TrustLevel.BANNED.value,
            )
        else:
            rows = await self._fetch(
                f"SELECT {self._USER_COLUMNS} FROM users WHERE approved = 0 ORDER BY username"
            )
        return [self._user_from_row(r) for r in rows]

    async def get_banned_users(self) -> list[UserRecord]:
        rows = await self._fetch(
            f"SELECT {self._USER_COLUMNS} FROM users WHERE trust_level = $1 ORDER BY username",
            TrustLevel.BANNED.value,
        )
        return [self._user_from_row(r) for r in rows]

    async def approve_user(self, username: str) -> bool:
        result = await self._execute(
            "UPDATE users SET approved = 1 WHERE LOWER(username) = LOWER($1)", username
        )
        return result.endswith(" 1")

    async def delete_user(self, username: str) -> bool:
        result = await self._execute(
            "DELETE FROM users WHERE LOWER(username) = LOWER($1)", username
        )
        return result.endswith(" 1")

    async def get_non_admin_users(self, exclude_banned: bool = True) -> list[UserRecord]:
        if exclude_banned:
            rows = await self._fetch(
                f"SELECT {self._USER_COLUMNS} FROM users "
                "WHERE approved = 1 AND trust_level > $1 AND trust_level < $2 "
                "ORDER BY username",
                TrustLevel.BANNED.value, TrustLevel.ADMIN.value,
            )
        else:
            rows = await self._fetch(
                f"SELECT {self._USER_COLUMNS} FROM users "
                "WHERE approved = 1 AND trust_level < $1 ORDER BY username",
                TrustLevel.ADMIN.value,
            )
        return [self._user_from_row(r) for r in rows]

    async def get_server_owner(self) -> UserRecord | None:
        row = await self._fetchrow(
            f"SELECT {self._USER_COLUMNS} FROM users WHERE trust_level = $1",
            TrustLevel.SERVER_OWNER.value,
        )
        return self._user_from_row(row) if row else None

    async def get_admin_users(self, include_server_owner: bool = True) -> list[UserRecord]:
        if include_server_owner:
            rows = await self._fetch(
                f"SELECT {self._USER_COLUMNS} FROM users "
                "WHERE trust_level >= $1 ORDER BY username",
                TrustLevel.ADMIN.value,
            )
        else:
            rows = await self._fetch(
                f"SELECT {self._USER_COLUMNS} FROM users "
                "WHERE trust_level = $1 ORDER BY username",
                TrustLevel.ADMIN.value,
            )
        return [self._user_from_row(r) for r in rows]

    # Fluent languages

    async def get_user_fluent_languages(self, username: str) -> list[str]:
        row = await self._fetchrow(
            "SELECT fluent_languages FROM users WHERE LOWER(username) = LOWER($1)", username
        )
        if row:
            return json.loads(row["fluent_languages"] or "[]")
        return []

    async def set_user_fluent_languages(self, username: str, languages: list[str]) -> None:
        await self._execute(
            "UPDATE users SET fluent_languages = $1 WHERE LOWER(username) = LOWER($2)",
            json.dumps(languages), username,
        )

    # Transcriber assignments

    async def get_transcriber_languages(self, username: str) -> list[str]:
        rows = await self._fetch(
            "SELECT ta.lang_code FROM transcriber_assignments ta "
            "JOIN users u ON ta.user_id = u.id "
            "WHERE LOWER(u.username) = LOWER($1) ORDER BY ta.lang_code",
            username,
        )
        return [r["lang_code"] for r in rows]

    async def add_transcriber_assignment(self, username: str, lang_code: str) -> bool:
        row = await self._fetchrow(
            "SELECT id FROM users WHERE LOWER(username) = LOWER($1)", username
        )
        if not row:
            return False
        user_id = row["id"]
        try:
            await self._execute(
                "INSERT INTO transcriber_assignments (user_id, lang_code) VALUES ($1, $2)",
                user_id, lang_code,
            )
            return True
        except asyncpg.UniqueViolationError:
            return False

    async def remove_transcriber_assignment(self, username: str, lang_code: str) -> bool:
        row = await self._fetchrow(
            "SELECT id FROM users WHERE LOWER(username) = LOWER($1)", username
        )
        if not row:
            return False
        user_id = row["id"]
        result = await self._execute(
            "DELETE FROM transcriber_assignments WHERE user_id = $1 AND lang_code = $2",
            user_id, lang_code,
        )
        return result.endswith(" 1")

    async def get_transcribers_for_language(self, lang_code: str) -> list[str]:
        rows = await self._fetch(
            "SELECT u.username FROM transcriber_assignments ta "
            "JOIN users u ON ta.user_id = u.id "
            "WHERE ta.lang_code = $1 ORDER BY u.username",
            lang_code,
        )
        return [r["username"] for r in rows]

    async def get_all_transcribers(self) -> dict[str, list[str]]:
        rows = await self._fetch(
            "SELECT u.username, ta.lang_code FROM transcriber_assignments ta "
            "JOIN users u ON ta.user_id = u.id "
            "ORDER BY u.username, ta.lang_code"
        )
        result: dict[str, list[str]] = {}
        for r in rows:
            result.setdefault(r["username"], []).append(r["lang_code"])
        return result

    # Table operations

    async def save_table(self, table: Table) -> None:
        members_json = json.dumps(
            [{"username": m.username, "is_spectator": m.is_spectator} for m in table.members]
        )
        await self._execute(
            "INSERT INTO tables (table_id, game_type, host, members_json, game_json, status) "
            "VALUES ($1, $2, $3, $4, $5, $6) "
            "ON CONFLICT (table_id) DO UPDATE SET "
            "game_type = $2, host = $3, members_json = $4, game_json = $5, status = $6",
            table.table_id, table.game_type, table.host,
            members_json, table.game_json, table.status,
        )

    async def load_table(self, table_id: str) -> Table | None:
        row = await self._fetchrow("SELECT * FROM tables WHERE table_id = $1", table_id)
        if not row:
            return None
        members_data = json.loads(row["members_json"])
        from server.core.tables.table import TableMember

        members = [
            TableMember(username=m["username"], is_spectator=m["is_spectator"])
            for m in members_data
        ]
        return Table(
            table_id=row["table_id"],
            game_type=row["game_type"],
            host=row["host"],
            members=members,
            game_json=row["game_json"],
            status=row["status"],
        )

    async def load_all_tables(self) -> list[Table]:
        rows = await self._fetch("SELECT table_id FROM tables")
        tables = []
        for r in rows:
            table = await self.load_table(r["table_id"])
            if table:
                tables.append(table)
        return tables

    async def delete_table(self, table_id: str) -> None:
        await self._execute("DELETE FROM tables WHERE table_id = $1", table_id)

    async def delete_all_tables(self) -> None:
        await self._execute("DELETE FROM tables")

    async def save_all_tables(self, tables: list[Table]) -> None:
        for table in tables:
            await self.save_table(table)

    # Saved table operations

    async def save_user_table(
        self,
        username: str,
        save_name: str,
        game_type: str,
        game_json: str,
        members_json: str,
    ) -> SavedTableRecord:
        from datetime import datetime

        saved_at = datetime.now().isoformat()
        row = await self._fetchrow(
            "INSERT INTO saved_tables (username, save_name, game_type, game_json, members_json, saved_at) "
            "VALUES ($1, $2, $3, $4, $5, $6) RETURNING id",
            username, save_name, game_type, game_json, members_json, saved_at,
        )
        return SavedTableRecord(
            id=row["id"],
            username=username,
            save_name=save_name,
            game_type=game_type,
            game_json=game_json,
            members_json=members_json,
            saved_at=saved_at,
        )

    async def get_user_saved_tables(self, username: str) -> list[SavedTableRecord]:
        rows = await self._fetch(
            "SELECT * FROM saved_tables WHERE LOWER(username) = LOWER($1) "
            "ORDER BY saved_at DESC",
            username,
        )
        return [
            SavedTableRecord(
                id=r["id"],
                username=r["username"],
                save_name=r["save_name"],
                game_type=r["game_type"],
                game_json=r["game_json"],
                members_json=r["members_json"],
                saved_at=r["saved_at"],
            )
            for r in rows
        ]

    async def get_saved_table(self, save_id: int) -> SavedTableRecord | None:
        row = await self._fetchrow("SELECT * FROM saved_tables WHERE id = $1", save_id)
        if not row:
            return None
        return SavedTableRecord(
            id=row["id"],
            username=row["username"],
            save_name=row["save_name"],
            game_type=row["game_type"],
            game_json=row["game_json"],
            members_json=row["members_json"],
            saved_at=row["saved_at"],
        )

    async def delete_saved_table(self, save_id: int) -> None:
        await self._execute("DELETE FROM saved_tables WHERE id = $1", save_id)

    # Game result operations

    async def save_game_result(
        self,
        game_type: str,
        timestamp: str,
        duration_ticks: int,
        players: list[tuple[str, str, bool, bool]],
        custom_data: dict | None = None,
    ) -> int:
        row = await self._fetchrow(
            "INSERT INTO game_results (game_type, timestamp, duration_ticks, custom_data) "
            "VALUES ($1, $2, $3, $4) RETURNING id",
            game_type, timestamp, duration_ticks,
            json.dumps(custom_data) if custom_data else None,
        )
        result_id = row["id"]

        for player_id, player_name, is_bot, is_virtual_bot in players:
            await self._execute(
                "INSERT INTO game_result_players "
                "(result_id, player_id, player_name, is_bot, is_virtual_bot) "
                "VALUES ($1, $2, $3, $4, $5)",
                result_id, player_id, player_name,
                1 if is_bot else 0, 1 if is_virtual_bot else 0,
            )
        return result_id

    async def get_player_game_history(
        self,
        player_id: str,
        game_type: str | None = None,
        limit: int = 50,
    ) -> list[dict]:
        if game_type:
            rows = await self._fetch(
                "SELECT gr.id, gr.game_type, gr.timestamp, gr.duration_ticks, gr.custom_data "
                "FROM game_results gr "
                "INNER JOIN game_result_players grp ON gr.id = grp.result_id "
                "WHERE grp.player_id = $1 AND gr.game_type = $2 "
                "ORDER BY gr.timestamp DESC LIMIT $3",
                player_id, game_type, limit,
            )
        else:
            rows = await self._fetch(
                "SELECT gr.id, gr.game_type, gr.timestamp, gr.duration_ticks, gr.custom_data "
                "FROM game_results gr "
                "INNER JOIN game_result_players grp ON gr.id = grp.result_id "
                "WHERE grp.player_id = $1 "
                "ORDER BY gr.timestamp DESC LIMIT $2",
                player_id, limit,
            )
        return [
            {
                "id": r["id"],
                "game_type": r["game_type"],
                "timestamp": r["timestamp"],
                "duration_ticks": r["duration_ticks"],
                "custom_data": json.loads(r["custom_data"]) if r["custom_data"] else {},
            }
            for r in rows
        ]

    async def get_game_result_players(self, result_id: int) -> list[dict]:
        rows = await self._fetch(
            "SELECT player_id, player_name, is_bot, is_virtual_bot "
            "FROM game_result_players WHERE result_id = $1",
            result_id,
        )
        return [
            {
                "player_id": r["player_id"],
                "player_name": r["player_name"],
                "is_bot": bool(r["is_bot"]),
                "is_virtual_bot": bool(r["is_virtual_bot"])
                if r["is_virtual_bot"] is not None else False,
            }
            for r in rows
        ]

    async def get_game_stats(self, game_type: str, limit: int | None = None) -> list[tuple]:
        if limit:
            rows = await self._fetch(
                "SELECT id, game_type, timestamp, duration_ticks, custom_data "
                "FROM game_results WHERE game_type = $1 "
                "ORDER BY timestamp DESC LIMIT $2",
                game_type, limit,
            )
        else:
            rows = await self._fetch(
                "SELECT id, game_type, timestamp, duration_ticks, custom_data "
                "FROM game_results WHERE game_type = $1 "
                "ORDER BY timestamp DESC",
                game_type,
            )
        return [(r["id"], r["game_type"], r["timestamp"], r["duration_ticks"], r["custom_data"]) for r in rows]

    async def get_game_stats_aggregate(self, game_type: str) -> dict:
        row = await self._fetchrow(
            "SELECT COUNT(*) as total_games, "
            "SUM(duration_ticks) as total_duration, "
            "AVG(duration_ticks) as avg_duration "
            "FROM game_results WHERE game_type = $1",
            game_type,
        )
        return {
            "total_games": row["total_games"] or 0,
            "total_duration_ticks": row["total_duration"] or 0,
            "avg_duration_ticks": row["avg_duration"] or 0,
        }

    async def get_player_stats(self, player_id: str, game_type: str | None = None) -> dict:
        if game_type:
            val = await self._fetchval(
                "SELECT COUNT(*) FROM game_result_players grp "
                "INNER JOIN game_results gr ON grp.result_id = gr.id "
                "WHERE grp.player_id = $1 AND gr.game_type = $2",
                player_id, game_type,
            )
        else:
            val = await self._fetchval(
                "SELECT COUNT(*) FROM game_result_players WHERE player_id = $1",
                player_id,
            )
        return {"games_played": val or 0}

    # Player rating operations

    async def get_player_rating(self, player_id: str, game_type: str) -> tuple[float, float] | None:
        row = await self._fetchrow(
            "SELECT mu, sigma FROM player_ratings "
            "WHERE player_id = $1 AND game_type = $2",
            player_id, game_type,
        )
        return (row["mu"], row["sigma"]) if row else None

    async def set_player_rating(self, player_id: str, game_type: str, mu: float, sigma: float) -> None:
        await self._execute(
            "INSERT INTO player_ratings (player_id, game_type, mu, sigma) "
            "VALUES ($1, $2, $3, $4) "
            "ON CONFLICT (player_id, game_type) DO UPDATE SET mu = $3, sigma = $4",
            player_id, game_type, mu, sigma,
        )

    async def get_rating_leaderboard(
        self, game_type: str, limit: int = 10
    ) -> list[tuple[str, float, float]]:
        rows = await self._fetch(
            "SELECT player_id, mu, sigma FROM player_ratings "
            "WHERE game_type = $1 ORDER BY mu DESC LIMIT $2",
            game_type, limit,
        )
        return [(r["player_id"], r["mu"], r["sigma"]) for r in rows]

    # Virtual bot persistence

    async def save_virtual_bot(
        self,
        name: str,
        state: str,
        online_ticks: int,
        target_online_ticks: int,
        table_id: str | None,
        game_join_tick: int,
    ) -> None:
        await self._execute(
            "INSERT INTO virtual_bots (name, state, online_ticks, target_online_ticks, table_id, game_join_tick) "
            "VALUES ($1, $2, $3, $4, $5, $6) "
            "ON CONFLICT (name) DO UPDATE SET "
            "state = $2, online_ticks = $3, target_online_ticks = $4, "
            "table_id = $5, game_join_tick = $6",
            name, state, online_ticks, target_online_ticks, table_id, game_join_tick,
        )

    async def load_all_virtual_bots(self) -> list[dict]:
        rows = await self._fetch(
            "SELECT name, state, online_ticks, target_online_ticks, table_id, game_join_tick "
            "FROM virtual_bots"
        )
        return [
            {
                "name": r["name"],
                "state": r["state"],
                "online_ticks": r["online_ticks"],
                "target_online_ticks": r["target_online_ticks"],
                "table_id": r["table_id"],
                "game_join_tick": r["game_join_tick"],
            }
            for r in rows
        ]

    async def delete_virtual_bot(self, name: str) -> None:
        await self._execute("DELETE FROM virtual_bots WHERE name = $1", name)

    async def delete_all_virtual_bots(self) -> None:
        await self._execute("DELETE FROM virtual_bots")
