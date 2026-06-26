from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from server.cli import bootstrap_owner
from server.persistence.database import Database
from server.core.users.base import TrustLevel
from server.auth.auth import AuthManager
from server.core.server import Server, BOOTSTRAP_WARNING_ENV

LOCALES_DIR = Path(__file__).resolve().parents[1] / "locales"


@pytest.fixture
def mock_db():
    db = AsyncMock(spec=Database)
    db.get_user_count = AsyncMock(return_value=0)
    db.user_exists = AsyncMock(return_value=False)
    db.create_user = AsyncMock()
    db.update_user_password = AsyncMock()
    db.update_user_trust_level = AsyncMock()
    db.approve_user = AsyncMock()
    db.get_user = AsyncMock(return_value=None)
    db.close = AsyncMock()
    return db


async def test_bootstrap_owner_creates_new_owner(mock_db):
    action = await bootstrap_owner(
        username="admin",
        password="secret-pass",
        locale="en",
        force=False,
        quiet=True,
        database=mock_db,
    )

    assert action == "Created"
    mock_db.create_user.assert_awaited_once()


async def test_bootstrap_owner_requires_force_when_users_exist(mock_db):
    mock_db.get_user_count = AsyncMock(return_value=1)

    with pytest.raises(RuntimeError):
        await bootstrap_owner(
            username="admin",
            password="secret",
            force=False,
            quiet=True,
            database=mock_db,
        )


async def test_bootstrap_owner_force_updates_existing_user(mock_db):
    mock_db.get_user_count = AsyncMock(return_value=1)
    mock_db.user_exists = AsyncMock(return_value=True)

    action = await bootstrap_owner(
        username="admin",
        password="new-secret",
        force=True,
        quiet=True,
        database=mock_db,
    )

    assert action == "Updated"
    mock_db.update_user_password.assert_awaited_once()
    mock_db.update_user_trust_level.assert_awaited_once()
    mock_db.approve_user.assert_awaited_once()


async def test_warn_if_no_users_prints_message(capsys, tmp_path):
    server = Server(db_path=str(tmp_path / "db.sqlite"), locales_dir=LOCALES_DIR)
    server._db = AsyncMock(get_user_count=AsyncMock(return_value=0))
    await server._warn_if_no_users()
    out = capsys.readouterr().out
    assert "bootstrap-owner" in out


async def test_warn_if_no_users_respects_env(monkeypatch, capsys, tmp_path):
    server = Server(db_path=str(tmp_path / "db.sqlite"), locales_dir=LOCALES_DIR)
    server._db = AsyncMock(get_user_count=AsyncMock(return_value=0))
    monkeypatch.setenv(BOOTSTRAP_WARNING_ENV, "1")
    await server._warn_if_no_users()
    out = capsys.readouterr().out
    assert out == ""
