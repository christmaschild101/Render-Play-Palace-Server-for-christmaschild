"""
Integration tests for PlayPalace v11.

Tests larger chunks of server code working together.
"""

import os
import pytest

from server.persistence.database import Database
from server.auth.auth import AuthManager, AuthResult
from server.core.tables.manager import TableManager
from server.core.tables.table import Table
from server.core.users.test_user import MockUser
from server.core.users.bot import Bot
from server.games.pig.game import PigGame, PigOptions
from server.games.registry import GameRegistry, get_game_class

pytestmark = pytest.mark.skipif(
    not os.environ.get("DATABASE_URL"),
    reason="DATABASE_URL environment variable is required for integration tests",
)


class TestDatabaseIntegration:
    """Test database operations."""

    async def test_user_creation_and_retrieval(self):
        """Test creating and retrieving users."""
        from server.persistence.database import Database

        db = Database()
        await db.connect()
        try:
            user = await db.create_user("testuser", "hashedpassword", "en")
            assert user.username == "testuser"

            retrieved = await db.get_user("testuser")
            assert retrieved is not None
            assert retrieved.username == "testuser"
            assert retrieved.password_hash == "hashedpassword"
            assert not retrieved.approved  # Default not approved

            exists = await db.user_exists("testuser")
            assert exists

            not_exists = await db.user_exists("nonexistent")
            assert not not_exists
        finally:
            await db.close()

    async def test_user_approval(self):
        """Test user approval workflow."""
        db = Database()
        await db.connect()
        try:
            await db.create_user("approveuser", "pw", "en")
            await db.approve_user("approveuser")

            user = await db.get_user("approveuser")
            assert user.approved
        finally:
            await db.close()

    async def test_get_pending_users(self):
        """Test getting pending (unapproved) users."""
        db = Database()
        await db.connect()
        try:
            await db.create_user("pending1", "pw1", "en")
            await db.create_user("pending2", "pw2", "en")
            await db.approve_user("pending1")

            pending = await db.get_pending_users()
            assert len(pending) == 1
            assert pending[0].username == "pending2"
        finally:
            await db.close()

    async def test_user_deletion(self):
        """Test deleting users."""
        db = Database()
        await db.connect()
        try:
            await db.create_user("deleteuser", "pw", "en")
            deleted = await db.delete_user("deleteuser")
            assert deleted

            user = await db.get_user("deleteuser")
            assert user is None
        finally:
            await db.close()

    async def test_user_count(self):
        """Test user count."""
        db = Database()
        await db.connect()
        try:
            await db.create_user("countuser1", "pw1", "en")
            await db.create_user("countuser2", "pw2", "en")
            count = await db.get_user_count()
            assert count == 2
        finally:
            await db.close()

    async def test_user_trust_level(self):
        """Test trust level updates."""
        db = Database()
        await db.connect()
        try:
            await db.create_user("trustuser", "pw", "en")
            from server.core.users.base import TrustLevel

            await db.update_user_trust_level("trustuser", TrustLevel.ADMIN)
            user = await db.get_user("trustuser")
            assert user.trust_level == TrustLevel.ADMIN
        finally:
            await db.close()


class TestAuthIntegration:
    """Test authentication flows."""

    async def test_register_and_authenticate(self):
        """Test user registration and authentication."""
        db = Database()
        await db.connect()
        try:
            auth = AuthManager(db)
            result = await auth.register("alice", "password123", approved=True, locale="en")
            assert result is True

            auth_result = await auth.authenticate("alice", "password123")
            assert auth_result.success
            assert auth_result.username == "alice"

            bad_auth = await auth.authenticate("alice", "wrongpassword")
            assert not bad_auth.success
        finally:
            await db.close()

    async def test_reset_password(self):
        """Test password reset."""
        db = Database()
        await db.connect()
        try:
            auth = AuthManager(db)
            await auth.register("bob", "oldpass", approved=True, locale="en")

            await auth.reset_password("bob", "newpass")
            auth_result = await auth.authenticate("bob", "newpass")
            assert auth_result.success

            old_auth = await auth.authenticate("bob", "oldpass")
            assert not old_auth.success
        finally:
            await db.close()

    async def test_refresh_token_flow(self):
        """Test refresh token creation and usage."""
        db = Database()
        await db.connect()
        try:
            auth = AuthManager(db)
            await auth.register("charlie", "pass", approved=True, locale="en")

            token, expires = await auth.create_refresh_token("charlie", 3600)
            assert token is not None
            assert expires > 0

            result = await auth.refresh_session(token)
            assert result.success
            assert result.username == "charlie"

            # Using same token again should fail (replaced)
            result2 = await auth.refresh_session(token)
            assert not result2.success
        finally:
            await db.close()


class TestTableIntegration:
    """Test table operations."""

    async def test_table_creation_and_retrieval(self):
        """Test creating and loading tables."""
        db = Database()
        await db.connect()
        try:
            await db.create_user("host", "pw", "en", approved=True)
            user = await db.get_user("host")

            game_cls = get_game_class("pig")
            manager = TableManager()
            table = manager.create_table("pig", "host", user, game_cls)

            game_json = table.game.to_json() if table.game else "{}"
            members_json = '[{"username": "host", "is_bot": false}]'

            await db.save_user_table(
                username="host",
                save_name="Test Save",
                game_type="pig",
                game_json=game_json,
                members_json=members_json,
            )

            saved = await db.get_user_saved_tables("host")
            assert len(saved) == 1
            assert saved[0].game_type == "pig"
            assert saved[0].save_name == "Test Save"

            loaded = await db.get_saved_table(saved[0].id)
            assert loaded is not None
            assert loaded.game_type == "pig"

            await db.delete_saved_table(saved[0].id)
            after_delete = await db.get_user_saved_tables("host")
            assert len(after_delete) == 0
        finally:
            await db.close()

    async def test_table_persistence_roundtrip(self):
        """Test full table persistence round-trip."""
        db = Database()
        await db.connect()
        try:
            await db.create_user("host2", "pw", "en", approved=True)
            user = await db.get_user("host2")

            game_cls = get_game_class("pig")
            manager = TableManager()
            table = manager.create_table("pig", "host2", user, game_cls)
            table.save_game_state()

            game_json = table.game_json

            await db.save_user_table(
                username="host2",
                save_name="Roundtrip",
                game_type="pig",
                game_json=game_json or "{}",
                members_json='[{"username": "host2", "is_bot": false}]',
            )

            saved = await db.get_user_saved_tables("host2")
            assert len(saved) == 1
            save_id = saved[0].id

            loaded_record = await db.get_saved_table(save_id)
            assert loaded_record is not None
            assert loaded_record.game_json == game_json
        finally:
            await db.close()
