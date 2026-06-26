"""Tests for persistence.database.Database."""

import json
import os

import pytest

from server.persistence.database import Database
from server.core.tables.table import Table, TableMember
from server.core.users.base import TrustLevel

pytestmark = pytest.mark.skipif(
    not os.environ.get("DATABASE_URL"),
    reason="DATABASE_URL environment variable is required for database tests",
)


@pytest.fixture
async def db():
    database = Database()
    await database.connect()
    try:
        yield database
    finally:
        await database.close()


class TestUserOperations:
    async def test_create_and_get_user(self, db):
        user = await db.create_user("testuser", "hash", "en", TrustLevel.USER, approved=True)
        assert user is not None
        assert user.username == "testuser"
        assert user.password_hash == "hash"
        assert user.trust_level == TrustLevel.USER
        assert user.approved

        retrieved = await db.get_user("testuser")
        assert retrieved is not None
        assert retrieved.username == "testuser"

    async def test_user_exists(self, db):
        await db.create_user("existsuser", "hash", "en")
        assert await db.user_exists("existsuser")
        assert not await db.user_exists("nobody")

    async def test_delete_user(self, db):
        await db.create_user("deleteuser", "hash", "en")
        assert await db.delete_user("deleteuser")
        assert not await db.user_exists("deleteuser")

    async def test_delete_nonexistent_user(self, db):
        assert not await db.delete_user("nobody")

    async def test_approve_user(self, db):
        await db.create_user("approveuser", "hash", "en")
        assert await db.approve_user("approveuser")

        user = await db.get_user("approveuser")
        assert user.approved

    async def test_approve_nonexistent_user(self, db):
        assert not await db.approve_user("nobody")

    async def test_get_user_count(self, db):
        await db.create_user("count1", "hash", "en")
        await db.create_user("count2", "hash", "en")
        count = await db.get_user_count()
        assert count == 2

    async def test_update_user_trust_level(self, db):
        await db.create_user("trustuser", "hash", "en")
        await db.update_user_trust_level("trustuser", TrustLevel.ADMIN)

        user = await db.get_user("trustuser")
        assert user.trust_level == TrustLevel.ADMIN

    async def test_get_pending_users(self, db):
        await db.create_user("pending", "hash", "en", approved=False)
        await db.create_user("approveduser", "hash", "en", approved=True)

        pending = await db.get_pending_users()
        assert any(u.username == "pending" for u in pending)
        assert all(not u.approved for u in pending)

    async def test_get_non_admin_users(self, db):
        await db.create_user("user1", "hash", "en", trust_level=TrustLevel.USER)
        await db.create_user("user2", "hash", "en", trust_level=TrustLevel.ADMIN)

        non_admins = await db.get_non_admin_users()
        assert any(u.username == "user1" for u in non_admins)
        assert all(u.trust_level != TrustLevel.ADMIN for u in non_admins)

    async def test_get_admin_users(self, db):
        await db.create_user("admin1", "hash", "en", trust_level=TrustLevel.ADMIN)
        await db.create_user("user1", "hash", "en", trust_level=TrustLevel.USER)

        admins = await db.get_admin_users()
        assert any(u.username == "admin1" for u in admins)
        assert all(u.trust_level == TrustLevel.ADMIN for u in admins)

    async def test_banned_users(self, db):
        await db.create_user("gooduser", "hash", "en", trust_level=TrustLevel.USER)
        await db.create_user("banneduser", "hash", "en", trust_level=TrustLevel.BANNED)

        banned = await db.get_banned_users()
        assert any(u.username == "banneduser" for u in banned)
        assert all(u.trust_level == TrustLevel.BANNED for u in banned)

    async def test_update_user_password(self, db):
        await db.create_user("passuser", "oldhash", "en")
        await db.update_user_password("passuser", "newhash")

        user = await db.get_user("passuser")
        assert user.password_hash == "newhash"

    async def test_update_user_locale(self, db):
        await db.create_user("localeuser", "hash", "fr")
        await db.update_user_locale("localeuser", "de")

        user = await db.get_user("localeuser")
        assert user.locale == "de"

    async def test_update_user_preferences(self, db):
        await db.create_user("prefuser", "hash", "en")
        prefs_json = json.dumps({"theme": "dark"})
        await db.update_user_preferences("prefuser", prefs_json)

        user = await db.get_user("prefuser")
        assert json.loads(user.preferences_json) == {"theme": "dark"}

    async def test_fluent_languages(self, db):
        await db.create_user("languser", "hash", "en")
        await db.set_user_fluent_languages("languser", ["en", "fr"])

        langs = await db.get_user_fluent_languages("languser")
        assert "en" in langs
        assert "fr" in langs


class TestVirtualBotOperations:
    async def test_save_and_load_virtual_bots(self, db):
        await db.save_virtual_bot(
            username="bot1",
            trust_level=TrustLevel.USER,
            preferred_games=["pig"],
        )
        await db.save_virtual_bot(
            username="bot2",
            trust_level=TrustLevel.USER,
            preferred_games=[],
        )

        bots = await db.load_all_virtual_bots()
        assert len(bots) == 2
        assert any(b["username"] == "bot1" for b in bots)

    async def test_delete_all_virtual_bots(self, db):
        await db.save_virtual_bot("bot1", TrustLevel.USER, ["pig"])
        await db.save_virtual_bot("bot2", TrustLevel.USER, [])

        await db.delete_all_virtual_bots()
        bots = await db.load_all_virtual_bots()
        assert len(bots) == 0


class TestGameResultOperations:
    async def test_save_and_query_game_stats(self, db):
        await db.save_game_result(
            game_type="pig",
            timestamp="2024-01-01T00:00:00",
            duration_ticks=100,
            players=[("player1", "Player One", False, False)],
            custom_data={"winner_name": "Player One"},
        )

        stats = await db.get_game_stats("pig", limit=10)
        assert len(stats) == 1
        assert stats[0][1] == "pig"

    async def test_game_result_players(self, db):
        await db.save_game_result(
            game_type="pig",
            timestamp="2024-01-01T00:00:00",
            duration_ticks=100,
            players=[
                ("p1", "Alice", False, False),
                ("p2", "Bob", False, False),
            ],
            custom_data={},
        )

        stats = await db.get_game_stats("pig", limit=1)
        result_id = stats[0][0]
        players = await db.get_game_result_players(result_id)
        assert len(players) == 2


class TestRatingOperations:
    async def test_player_rating(self, db):
        await db.set_player_rating("player1", "pig", 25.0, 8.33)
        rating = await db.get_player_rating("player1", "pig")
        assert rating is not None
        mu, sigma = rating
        assert mu == 25.0
        assert sigma == 8.33

    async def test_rating_leaderboard(self, db):
        await db.set_player_rating("alice", "pig", 30.0, 5.0)
        await db.set_player_rating("bob", "pig", 20.0, 6.0)

        board = await db.get_rating_leaderboard("pig", limit=10)
        assert len(board) >= 2
        assert board[0][0] in ("alice", "bob")


class TestTableStorage:
    async def test_save_and_load_tables(self, db):
        tables = await db.load_all_tables()
        assert isinstance(tables, list)

        await db.delete_all_tables()

    async def test_saved_table_operations(self, db):
        await db.save_user_table(
            username="host",
            save_name="My Game",
            game_type="pig",
            game_json='{"state": "test"}',
            members_json='[{"username": "host", "is_bot": false}]',
        )

        saved = await db.get_user_saved_tables("host")
        assert len(saved) == 1
        save_id = saved[0].id

        record = await db.get_saved_table(save_id)
        assert record is not None
        assert record.save_name == "My Game"

        await db.delete_saved_table(save_id)
        remaining = await db.get_user_saved_tables("host")
        assert len(remaining) == 0


class TestTranscriberOperations:
    async def test_transcriber_assignments(self, db):
        await db.add_transcriber_assignment("trans1", "en")
        await db.add_transcriber_assignment("trans1", "fr")

        languages = await db.get_transcriber_languages("trans1")
        assert "en" in languages
        assert "fr" in languages

        all_trans = await db.get_all_transcribers()
        assert "trans1" in all_trans

    async def test_transcriber_for_language(self, db):
        await db.add_transcriber_assignment("trans1", "en")
        await db.add_transcriber_assignment("trans2", "en")

        transcribers = await db.get_transcribers_for_language("en")
        assert len(transcribers) >= 2

    async def test_remove_transcriber_assignment(self, db):
        await db.add_transcriber_assignment("trans1", "en")
        await db.remove_transcriber_assignment("trans1", "en")

        languages = await db.get_transcriber_languages("trans1")
        assert "en" not in languages

    async def test_nonexistent_transcriber(self, db):
        languages = await db.get_transcriber_languages("nobody")
        assert len(languages) == 0
