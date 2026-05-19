"""Tests for the scoresheet picker flow added in PR #243.

PR #243 added the ability to view any active player's Yahtzee scoresheet.

Keybind layout (active players):
- ``c``      -> immediately show the viewer's own scoresheet (status_box).
- ``shift+c`` -> open a transient picker (scoresheet_player_select) listing all
  active players + a Back item; selecting a player shows their scoresheet.

For spectators (no own scoresheet), ``c`` falls back to the picker so the
experience is seamless.
"""

from __future__ import annotations

from server.core.users.base import MenuItem
from server.core.users.test_user import MockUser
from server.games.yahtzee.game import YahtzeeGame


def _last_show_menu_for(user: MockUser, menu_id: str) -> dict | None:
    for m in reversed(user.messages):
        if m.type == "show_menu" and m.data.get("menu_id") == menu_id:
            return m.data
    return None


def _item_id(item) -> str:
    return item.id if isinstance(item, MenuItem) else item["id"]


def _item_text(item) -> str:
    return item.text if isinstance(item, MenuItem) else item["text"]


def _spoken_texts(user: MockUser) -> list[str]:
    return [m.data["text"] for m in user.messages if m.type == "speak"]


def _make_game(player_specs: list[tuple[str, str]], spectators: list[str] | None = None):
    """Build a started YahtzeeGame.

    player_specs: list of (name, locale) for active players.
    spectators: list of names for spectators.
    Returns (game, players_by_name, users_by_name).
    """
    game = YahtzeeGame()
    users: dict[str, MockUser] = {}
    players: dict = {}
    for name, locale in player_specs:
        user = MockUser(name, locale=locale)
        users[name] = user
        players[name] = game.add_player(name, user)
    for name in spectators or []:
        user = MockUser(name)
        users[name] = user
        players[name] = game.add_spectator(name, user)
    game.on_start()
    # Clear startup chatter so menu-finders don't trip on stale messages.
    for u in users.values():
        u.clear_messages()
    return game, players, users


# ---------------------------------------------------------------------------
# `c` (own sheet) path
# ---------------------------------------------------------------------------


def test_view_scoresheet_active_player_shows_own_sheet_immediately():
    """Active player pressing `c` should see their own scoresheet directly,
    not the picker."""
    game, players, users = _make_game([("Alice", "en"), ("Bob", "en")])
    alice = players["Alice"]

    game._action_view_scoresheet(alice, "view_scoresheet")

    state = game._get_transient_display_state(alice)
    assert state is not None
    assert state.kind == "status_box", f"expected status_box, got {state.kind!r}"

    menu = _last_show_menu_for(users["Alice"], "transient_display")
    assert menu is not None
    text_blob = " ".join(_item_text(it) for it in menu["items"])
    assert "Alice" in text_blob, "viewer's own name should be in the header"
    assert "Bob" not in text_blob


# ---------------------------------------------------------------------------
# `shift+c` (picker) path
# ---------------------------------------------------------------------------


def test_view_all_scoresheets_opens_player_picker():
    game, players, users = _make_game([("Alice", "en"), ("Bob", "en")])
    alice = players["Alice"]

    game._action_view_all_scoresheets(alice, "view_all_scoresheets")

    state = game._get_transient_display_state(alice)
    assert state is not None
    assert state.kind == "scoresheet_player_select"

    menu = _last_show_menu_for(users["Alice"], "transient_display")
    assert menu is not None
    item_ids = [_item_id(it) for it in menu["items"]]
    assert players["Alice"].id in item_ids
    assert players["Bob"].id in item_ids
    assert "transient_display_back" in item_ids, "Back item should be last entry"


def test_view_all_scoresheets_excludes_spectators_from_picker():
    game, players, users = _make_game(
        [("Alice", "en"), ("Bob", "en")],
        spectators=["Spec"],
    )
    alice = players["Alice"]

    game._action_view_all_scoresheets(alice, "view_all_scoresheets")

    menu = _last_show_menu_for(users["Alice"], "transient_display")
    assert menu is not None
    item_ids = [_item_id(it) for it in menu["items"]]
    assert players["Spec"].id not in item_ids, "spectators should not appear as targets"
    assert players["Alice"].id in item_ids
    assert players["Bob"].id in item_ids


def test_selecting_player_in_picker_renders_their_scoresheet():
    game, players, users = _make_game([("Alice", "en"), ("Bob", "en")])
    alice = players["Alice"]
    bob = players["Bob"]
    bob.scores["ones"] = 3
    bob.scores["yahtzee"] = 50

    game._action_view_all_scoresheets(alice, "view_all_scoresheets")
    game._handle_transient_display_selection(alice, bob.id)

    state = game._get_transient_display_state(alice)
    assert state is not None
    assert state.kind == "status_box"

    box_menu = _last_show_menu_for(users["Alice"], "transient_display")
    assert box_menu is not None
    text_blob = " ".join(_item_text(it) for it in box_menu["items"])
    assert "Bob" in text_blob, "scoresheet should be for Bob (the selected target)"


def test_selecting_back_in_picker_closes_it_without_opening_sheet():
    game, players, users = _make_game([("Alice", "en"), ("Bob", "en")])
    alice = players["Alice"]

    game._action_view_all_scoresheets(alice, "view_all_scoresheets")
    assert game._get_transient_display_state(alice).kind == "scoresheet_player_select"

    game._handle_transient_display_selection(alice, "transient_display_back")

    assert game._get_transient_display_state(alice) is None


# ---------------------------------------------------------------------------
# Spectator fallback: `c` opens picker because spectators have no own sheet.
# ---------------------------------------------------------------------------


def test_spectator_pressing_view_scoresheet_falls_back_to_picker():
    game, players, users = _make_game(
        [("Alice", "en")],
        spectators=["Spec"],
    )
    spec = players["Spec"]

    game._action_view_scoresheet(spec, "view_scoresheet")

    state = game._get_transient_display_state(spec)
    assert state is not None
    assert state.kind == "scoresheet_player_select", (
        "spectator with no own sheet should be routed to the picker"
    )

    menu = _last_show_menu_for(users["Spec"], "transient_display")
    assert menu is not None
    item_ids = [_item_id(it) for it in menu["items"]]
    assert players["Alice"].id in item_ids
    assert spec.id not in item_ids, "spectator should not appear as a target"


# ---------------------------------------------------------------------------
# Edge cases: silence-is-a-bug feedback.
# ---------------------------------------------------------------------------


def test_picker_with_no_active_players_speaks_not_found():
    """If the picker is somehow triggered with no active players, the action
    must produce speech (per CLAUDE.md "silence is a bug")."""
    game = YahtzeeGame()
    user = MockUser("Spec")
    spec = game.add_spectator("Spec", user)
    user.clear_messages()

    game._action_view_all_scoresheets(spec, "view_all_scoresheets")

    assert game._get_transient_display_state(spec) is None
    assert "Player not found." in _spoken_texts(user)


def test_picker_with_stale_selection_id_speaks_not_found():
    """If a player is selected from the picker but has since disconnected /
    been removed, the action must produce speech rather than silently dropping."""
    game, players, users = _make_game([("Alice", "en"), ("Bob", "en")])
    alice = players["Alice"]

    game._action_view_all_scoresheets(alice, "view_all_scoresheets")
    users["Alice"].clear_messages()

    game._handle_transient_display_selection(alice, "nonexistent-player-id")

    assert game._get_transient_display_state(alice) is None
    assert "Player not found." in _spoken_texts(users["Alice"])


# ---------------------------------------------------------------------------
# Re-pressing shift+c while a sheet is open should reopen the picker.
# ---------------------------------------------------------------------------


def test_pressing_view_all_scoresheets_again_replaces_open_sheet_with_picker():
    game, players, users = _make_game([("Alice", "en"), ("Bob", "en")])
    alice = players["Alice"]
    bob = players["Bob"]

    game._action_view_all_scoresheets(alice, "view_all_scoresheets")
    game._handle_transient_display_selection(alice, bob.id)
    assert game._get_transient_display_state(alice).kind == "status_box"

    game._action_view_all_scoresheets(alice, "view_all_scoresheets")

    state = game._get_transient_display_state(alice)
    assert state is not None
    assert state.kind == "scoresheet_player_select"
