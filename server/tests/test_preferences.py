"""Tests for the declarative user preferences system."""

from __future__ import annotations

import json

import pytest

from server.core.users.preferences import (
    DiceKeepingStyle,
    PREF_CATEGORIES,
    PrefMeta,
    UserPreferences,
)


# ---------------------------------------------------------------------------
# Basic field access and defaults
# ---------------------------------------------------------------------------


class TestDefaults:
    def test_default_values(self):
        prefs = UserPreferences()
        assert prefs.play_turn_sound is True
        assert prefs.clear_kept_on_roll is False
        assert prefs.dice_keeping_style == DiceKeepingStyle.PLAYPALACE
        assert prefs.game_overrides == {}

    def test_field_metadata_present(self):
        for name, meta in UserPreferences.get_pref_fields():
            assert isinstance(meta, PrefMeta)
            assert meta.category in dict(PREF_CATEGORIES)
            assert meta.label
            assert meta.change_msg

    def test_categories_have_fields(self):
        for cat_key, _ in PREF_CATEGORIES:
            fields = UserPreferences.get_fields_for_category(cat_key)
            assert fields, f"Category {cat_key} has no fields"

    def test_display_category_fields(self):
        names = [n for n, _ in UserPreferences.get_fields_for_category("display")]
        assert "brief_announcements" in names

    def test_sounds_category_fields(self):
        names = [n for n, _ in UserPreferences.get_fields_for_category("sounds")]
        assert "play_turn_sound" in names

    def test_dice_category_fields(self):
        names = [n for n, _ in UserPreferences.get_fields_for_category("dice")]
        assert "clear_kept_on_roll" in names
        assert "dice_keeping_style" in names


# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------


class TestSerialization:
    def test_to_dict_defaults(self):
        prefs = UserPreferences()
        d = prefs.to_dict()
        assert d["play_turn_sound"] is True
        assert d["clear_kept_on_roll"] is False
        assert d["dice_keeping_style"] == "playpalace"
        assert "game_overrides" not in d  # empty overrides omitted

    def test_to_dict_with_changes(self):
        prefs = UserPreferences()
        prefs.play_turn_sound = False
        prefs.dice_keeping_style = DiceKeepingStyle.QUENTIN_C
        d = prefs.to_dict()
        assert d["play_turn_sound"] is False
        assert d["dice_keeping_style"] == "quentin_c"

    def test_to_dict_with_overrides(self):
        prefs = UserPreferences()
        prefs.set_game_override("play_turn_sound", "pig", False)
        d = prefs.to_dict()
        assert d["game_overrides"]["pig"]["play_turn_sound"] is False

    def test_from_dict_defaults(self):
        prefs = UserPreferences.from_dict({})
        assert prefs.play_turn_sound is True
        assert prefs.clear_kept_on_roll is False
        assert prefs.dice_keeping_style == DiceKeepingStyle.PLAYPALACE

    def test_from_dict_round_trip(self):
        prefs = UserPreferences()
        prefs.play_turn_sound = False
        prefs.dice_keeping_style = DiceKeepingStyle.QUENTIN_C
        prefs.set_game_override("clear_kept_on_roll", "farkle", True)

        d = prefs.to_dict()
        json_str = json.dumps(d)
        restored = UserPreferences.from_dict(json.loads(json_str))

        assert restored.play_turn_sound is False
        assert restored.dice_keeping_style == DiceKeepingStyle.QUENTIN_C
        assert restored.get_game_override("clear_kept_on_roll", "farkle") is True

    def test_from_dict_bad_enum_falls_back(self):
        prefs = UserPreferences.from_dict({"dice_keeping_style": "nonexistent"})
        assert prefs.dice_keeping_style == DiceKeepingStyle.PLAYPALACE

    def test_from_dict_ignores_unknown_keys(self):
        prefs = UserPreferences.from_dict({"unknown_field": 42})
        assert prefs.play_turn_sound is True  # defaults

    def test_json_round_trip(self):
        """Full JSON encode/decode cycle."""
        prefs = UserPreferences()
        prefs.clear_kept_on_roll = True
        prefs.set_game_override("dice_keeping_style", "yahtzee", "quentin_c")
        json_str = json.dumps(prefs.to_dict())
        restored = UserPreferences.from_dict(json.loads(json_str))
        assert restored.clear_kept_on_roll is True
        assert restored.get_game_override("dice_keeping_style", "yahtzee") == "quentin_c"


# ---------------------------------------------------------------------------
# Per-game overrides
# ---------------------------------------------------------------------------


class TestGameOverrides:
    def test_get_effective_no_override(self):
        prefs = UserPreferences()
        assert prefs.get_effective("play_turn_sound") is True
        assert prefs.get_effective("play_turn_sound", game_type="pig") is True

    def test_get_effective_with_override(self):
        prefs = UserPreferences()
        prefs.set_game_override("play_turn_sound", "pig", False)
        assert prefs.get_effective("play_turn_sound", game_type="pig") is False
        assert prefs.get_effective("play_turn_sound", game_type="farkle") is True
        assert prefs.get_effective("play_turn_sound") is True  # no game_type

    def test_set_and_clear_override(self):
        prefs = UserPreferences()
        prefs.set_game_override("clear_kept_on_roll", "farkle", True)
        assert prefs.has_game_override("clear_kept_on_roll", "farkle")
        assert prefs.get_game_override("clear_kept_on_roll", "farkle") is True

        prefs.clear_game_override("clear_kept_on_roll", "farkle")
        assert not prefs.has_game_override("clear_kept_on_roll", "farkle")
        assert prefs.get_game_override("clear_kept_on_roll", "farkle") is None

    def test_clear_last_override_removes_game_key(self):
        prefs = UserPreferences()
        prefs.set_game_override("play_turn_sound", "pig", False)
        prefs.clear_game_override("play_turn_sound", "pig")
        assert "pig" not in prefs.game_overrides

    def test_enum_override_stored_as_string(self):
        prefs = UserPreferences()
        prefs.set_game_override("dice_keeping_style", "farkle", DiceKeepingStyle.QUENTIN_C)
        # Stored as string
        assert prefs.game_overrides["farkle"]["dice_keeping_style"] == "quentin_c"
        # get_effective returns the enum
        result = prefs.get_effective("dice_keeping_style", game_type="farkle")
        assert result == DiceKeepingStyle.QUENTIN_C

    def test_has_override_false_for_missing(self):
        prefs = UserPreferences()
        assert not prefs.has_game_override("play_turn_sound", "pig")


# ---------------------------------------------------------------------------
# Reset
# ---------------------------------------------------------------------------


class TestReset:
    def test_reset_all(self):
        prefs = UserPreferences()
        prefs.play_turn_sound = False
        prefs.clear_kept_on_roll = True
        prefs.dice_keeping_style = DiceKeepingStyle.QUENTIN_C
        prefs.set_game_override("play_turn_sound", "pig", False)

        prefs.reset_all()

        assert prefs.play_turn_sound is True
        assert prefs.clear_kept_on_roll is False
        assert prefs.dice_keeping_style == DiceKeepingStyle.PLAYPALACE
        assert prefs.game_overrides == {}

    def test_reset_category(self):
        prefs = UserPreferences()
        prefs.play_turn_sound = False  # display category
        prefs.clear_kept_on_roll = True  # dice category
        prefs.set_game_override("clear_kept_on_roll", "farkle", True)

        prefs.reset_category("dice")

        # Dice category reset
        assert prefs.clear_kept_on_roll is False
        assert not prefs.has_game_override("clear_kept_on_roll", "farkle")
        # Display category untouched
        assert prefs.play_turn_sound is False

    def test_reset_category_preserves_other_overrides(self):
        prefs = UserPreferences()
        prefs.set_game_override("play_turn_sound", "pig", False)
        prefs.set_game_override("clear_kept_on_roll", "farkle", True)

        prefs.reset_category("dice")

        # Display override preserved
        assert prefs.has_game_override("play_turn_sound", "pig")
        # Dice override cleared
        assert not prefs.has_game_override("clear_kept_on_roll", "farkle")


# ---------------------------------------------------------------------------
# Introspection
# ---------------------------------------------------------------------------


class TestIntrospection:
    def test_get_pref_meta(self):
        meta = UserPreferences.get_pref_meta("play_turn_sound")
        assert meta is not None
        assert meta.kind == "bool"
        assert meta.category == "sounds"

    def test_get_pref_meta_missing(self):
        assert UserPreferences.get_pref_meta("nonexistent") is None

    def test_relevant_games_from_registry(self):
        from server.games.registry import GameRegistry

        games = GameRegistry.get_games_for_preference("clear_kept_on_roll")
        assert "yahtzee" in games

    def test_play_turn_sound_no_relevant_games(self):
        from server.games.registry import GameRegistry

        games = GameRegistry.get_games_for_preference("play_turn_sound")
        assert games == []  # global-only

    def test_brief_announcements_relevant_games(self):
        from server.games.registry import GameRegistry

        games = GameRegistry.get_games_for_preference("brief_announcements")
        assert "backgammon" in games

    def test_dice_keeping_style_is_menu(self):
        meta = UserPreferences.get_pref_meta("dice_keeping_style")
        assert meta is not None
        assert meta.kind == "menu"
        assert meta.choices is not None
        assert len(meta.choices) == 2


# ---------------------------------------------------------------------------
# DiceKeepingStyle enum
# ---------------------------------------------------------------------------


class TestDiceKeepingStyle:
    def test_from_str_valid(self):
        assert DiceKeepingStyle.from_str("playpalace") == DiceKeepingStyle.PLAYPALACE
        assert DiceKeepingStyle.from_str("quentin_c") == DiceKeepingStyle.QUENTIN_C

    def test_from_str_invalid(self):
        assert DiceKeepingStyle.from_str("bad") == DiceKeepingStyle.PLAYPALACE
