"""Tests for options and language/dice style menu handlers in core.server."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from server.core.server import Server
from server.core.users.preferences import UserPreferences, DiceKeepingStyle
from server.messages.localization import Localization


class DummyDB:
    def __init__(self):
        self.preferences_updates: list[tuple[str, str]] = []
        self.locale_updates: list[tuple[str, str]] = []
        self.fluent_languages_updates: list[tuple[str, list[str]]] = []

    def update_user_preferences(self, username: str, prefs_json: str) -> None:
        self.preferences_updates.append((username, prefs_json))

    def update_user_locale(self, username: str, locale: str) -> None:
        self.locale_updates.append((username, locale))

    def set_user_fluent_languages(self, username: str, languages: list[str]) -> None:
        self.fluent_languages_updates.append((username, list(languages)))


class DummyUser:
    def __init__(self, username: str, locale: str = "en"):
        self.username = username
        self.locale = locale
        self.preferences = UserPreferences()
        self.fluent_languages: list[str] = []
        self.spoken: list[tuple[str, dict]] = []
        self.menu_id: str | None = None
        self.music_played: list[str] = []
        self.sounds_played: list[str] = []

        async def _send(payload):
            return None

        self.connection = SimpleNamespace(send=_send)

    def speak_l(self, message_id: str, buffer: str = "misc", **kwargs) -> None:
        self.spoken.append((message_id, kwargs))

    def speak(self, text: str, buffer: str = "misc") -> None:
        self.spoken.append((text, {"buffer": buffer}))

    def show_menu(self, menu_id: str, *args, **kwargs) -> None:
        self.menu_id = menu_id

    def play_music(self, name: str, looping: bool = True) -> None:
        self.music_played.append(name)

    def play_sound(self, name: str, volume: int = 100, pan: int = 0, pitch: int = 100) -> None:
        self.sounds_played.append(name)

    def set_locale(self, locale: str) -> None:
        self.locale = locale


@pytest.fixture
def server(tmp_path, monkeypatch):
    srv = Server(host="127.0.0.1", port=0, db_path=tmp_path / "db.sqlite", preload_locales=True)
    srv._db = DummyDB()
    # simplify localization helpers
    monkeypatch.setattr(
        "server.messages.localization.Localization.get",
        lambda _locale, key, **kwargs: f"{key}:{kwargs}" if kwargs else key,
    )
    monkeypatch.setattr(
        "server.messages.localization.Localization.get_available_languages",
        lambda _locale="en", fallback="en": {"en": "English", "es": "Español"},
    )
    monkeypatch.setattr(
        "server.messages.localization.Localization.get_available_locale_codes",
        lambda: ["en", "es"],
    )
    return srv


@pytest.mark.asyncio
async def test_handle_pref_category_toggle_turn_sound(server, monkeypatch):
    user = DummyUser("alice")
    user.preferences.play_turn_sound = True
    shown = {}
    monkeypatch.setattr(
        server, "_show_pref_category_menu", lambda u, c, **kw: shown.setdefault("called", True)
    )
    server._user_states["alice"] = {"menu": "pref_category_menu", "pref_category": "sounds"}

    await server._handle_pref_category_selection(user, "pref_play_turn_sound")

    assert user.preferences.play_turn_sound is False
    assert user.sounds_played[-1] == "checkbox_list_off.wav"
    assert server._db.preferences_updates  # saved
    assert shown.get("called")


@pytest.mark.asyncio
async def test_handle_options_selection_language_opens_menu(server, monkeypatch):
    user = DummyUser("alice")
    opened = {}
    monkeypatch.setattr(
        "server.core.ui.common_flows.show_language_menu",
        lambda *a, **kw: opened.setdefault("lang", True),
    )

    await server._handle_options_selection(user, "language")

    assert opened.get("lang")


@pytest.mark.asyncio
async def test_handle_options_selection_language_warmup_in_progress(server, monkeypatch):
    user = DummyUser("alice")
    Localization.set_warmup_active(True)

    try:
        await server._handle_options_selection(user, "language")
    finally:
        Localization.set_warmup_active(False)

    # User stays on the options menu (no re-show), only hears the message
    assert user.spoken[-1][0] == "localization-in-progress-try-again"


@pytest.mark.asyncio
async def test_handle_dice_style_selection_changes_pref(server, monkeypatch):
    user = DummyUser("alice")
    user.preferences.dice_keeping_style = DiceKeepingStyle.PLAYPALACE
    shown = {}
    monkeypatch.setattr(server, "_show_options_menu", lambda u: shown.setdefault("options", True))
    monkeypatch.setattr(server, "_save_user_preferences", lambda u: shown.setdefault("saved", True))

    await server._handle_dice_keeping_style_selection(user, "style_quentin_c")

    assert user.preferences.dice_keeping_style == DiceKeepingStyle.QUENTIN_C
    assert shown.get("saved")
    assert shown.get("options")
    assert ("dice-keeping-style-changed", {"style": "dice-keeping-style-values"}) in user.spoken


@pytest.mark.asyncio
async def test_handle_language_selection_updates_locale(server, monkeypatch):
    user = DummyUser("alice")
    shown = {}
    monkeypatch.setattr(server, "_show_options_menu", lambda u: shown.setdefault("options", True))

    await server._apply_locale_change(user, "es")

    assert user.locale == "es"
    assert server._db.locale_updates == [("alice", "es")]
    assert ("language-changed", {"language": "Español"}) in user.spoken
    assert shown.get("options")


def test_show_language_menu_warmup_in_progress(server, monkeypatch):
    from server.core.ui.common_flows import show_language_menu

    user = DummyUser("alice")
    Localization.set_warmup_active(True)

    try:
        result = show_language_menu(user)
    finally:
        Localization.set_warmup_active(False)

    assert result is False
    assert user.spoken[-1][0] == "localization-in-progress-try-again"


@pytest.mark.asyncio
async def test_fluent_languages_warmup_in_progress(server, monkeypatch):
    user = DummyUser("alice")
    Localization.set_warmup_active(True)

    try:
        await server._handle_options_selection(user, "fluent_languages")
    finally:
        Localization.set_warmup_active(False)

    # User stays on the options menu (no re-show), only hears the message
    assert user.spoken[-1][0] == "localization-in-progress-try-again"


@pytest.mark.asyncio
async def test_fluent_languages_opens_language_menu(server, monkeypatch):
    user = DummyUser("alice")
    opened = {}
    monkeypatch.setattr(
        "server.core.ui.common_flows.show_language_menu",
        lambda *a, **kw: opened.setdefault("lang", True),
    )

    await server._handle_options_selection(user, "fluent_languages")

    assert opened.get("lang")
    assert server._user_states["alice"]["menu"] == "language_menu"


@pytest.mark.asyncio
async def test_fluent_language_toggle_deferred(server, monkeypatch):
    """Toggling a language plays a sound but does not touch user state or DB."""
    from server.core.ui.common_flows import handle_language_menu_selection

    user = DummyUser("alice")
    user.fluent_languages = ["en"]
    server._show_fluent_languages_menu(user)

    # Toggle es on — only the menu's internal selected set changes
    await handle_language_menu_selection(user, "lang_es")

    assert user.sounds_played[-1] == "checkbox_list_on.wav"
    assert user.fluent_languages == ["en"]  # unchanged
    assert server._db.fluent_languages_updates == []

    # Toggle es off again
    await handle_language_menu_selection(user, "lang_es")

    assert user.sounds_played[-1] == "checkbox_list_off.wav"
    assert server._db.fluent_languages_updates == []


@pytest.mark.asyncio
async def test_fluent_language_done_saves(server, monkeypatch):
    """Pressing Done applies the selected set and writes to the DB."""
    from server.core.ui.common_flows import handle_language_menu_selection

    user = DummyUser("alice")
    user.fluent_languages = ["en"]
    shown = {}
    monkeypatch.setattr(server, "_show_options_menu", lambda u: shown.setdefault("options", True))
    server._show_fluent_languages_menu(user)

    # Toggle es on, then press done
    await handle_language_menu_selection(user, "lang_es")
    await handle_language_menu_selection(user, "done")

    assert set(user.fluent_languages) == {"en", "es"}
    assert len(server._db.fluent_languages_updates) == 1
    assert shown.get("options")


@pytest.mark.asyncio
async def test_fluent_language_cancel_reverts(server, monkeypatch):
    """Pressing Cancel restores original fluent languages, nothing written."""
    from server.core.ui.common_flows import handle_language_menu_selection

    user = DummyUser("alice")
    user.fluent_languages = ["en"]
    shown = {}
    monkeypatch.setattr(server, "_show_options_menu", lambda u: shown.setdefault("options", True))
    server._show_fluent_languages_menu(user)

    # Toggle es on, then cancel
    await handle_language_menu_selection(user, "lang_es")
    await handle_language_menu_selection(user, "cancel")

    assert user.fluent_languages == ["en"]  # unchanged
    assert server._db.fluent_languages_updates == []  # nothing written
    assert shown.get("options")
