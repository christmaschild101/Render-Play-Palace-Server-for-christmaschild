"""Declarative user preferences for PlayPalace.

Preferences are defined using the same option types as game options
(BoolOption, MenuOption, etc.) with category grouping, per-game overrides,
and auto-serialization.

Usage:
    prefs = UserPreferences()
    prefs.play_turn_sound  # True (default)
    prefs.get_effective("play_turn_sound", game_type="pig")  # per-game or global
    prefs.set_game_override("play_turn_sound", "pig", False)
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from enum import Enum
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    pass


# ---------------------------------------------------------------------------
# Dice keeping style enum (kept for type safety in game code)
# ---------------------------------------------------------------------------


class DiceKeepingStyle(Enum):
    """Dice keeping style preference."""

    PLAYPALACE = "playpalace"  # Dice indexes (1-5 keys)
    QUENTIN_C = "quentin_c"  # Dice values (1-6 keys)

    @classmethod
    def from_str(cls, value: str) -> "DiceKeepingStyle":
        """Convert string to enum, defaulting to PLAYPALACE."""
        try:
            return cls(value)
        except ValueError:
            return cls.PLAYPALACE


# ---------------------------------------------------------------------------
# Preference field metadata
# ---------------------------------------------------------------------------


@dataclass
class PrefMeta:
    """Metadata for a single preference field.

    Attributes:
        category: Category key (e.g. "display", "dice").
        label: Fluent key for menu label (receives $status or $choice).
        change_msg: Fluent key for change announcement.
        description: Fluent key spoken on Space.
        prompt: Fluent key for input prompt (menu options only).
        kind: "bool" or "menu".
        default: Default value.
        choices: For menu prefs, list of (value, fluent_key) tuples.
        enum_class: Optional enum class for type conversion.
    """

    category: str
    label: str
    change_msg: str
    description: str = ""
    prompt: str = ""
    kind: str = "bool"  # "bool" or "menu"
    default: Any = None
    choices: list[tuple[str, str]] | None = None
    enum_class: type[Enum] | None = None


def pref_field(meta: PrefMeta) -> Any:
    """Create a dataclass field with preference metadata."""
    from dataclasses import field as dc_field

    return dc_field(default=meta.default, metadata={"pref_meta": meta})


# ---------------------------------------------------------------------------
# Category definitions (order matters — this is menu order)
# ---------------------------------------------------------------------------

PREF_CATEGORIES: list[tuple[str, str]] = [
    ("display", "pref-category-display"),
    ("sounds", "pref-category-sounds"),
    ("gameplay", "pref-category-gameplay"),
    ("dice", "pref-category-dice"),
]
"""(category_key, fluent_key) in display order."""


# ---------------------------------------------------------------------------
# UserPreferences dataclass
# ---------------------------------------------------------------------------


@dataclass
class UserPreferences:
    """User preferences that persist across sessions.

    Fields are defined in display order within each category.
    Metadata on each field drives menu generation and serialization.
    """

    # --- Display category ---
    brief_announcements: bool = pref_field(
        PrefMeta(
            category="display",
            label="pref-set-brief-announcements",
            change_msg="pref-changed-brief-announcements",
            description="pref-desc-brief-announcements",
            kind="bool",
            default=False,
        )
    )

    # --- Sounds category ---
    play_turn_sound: bool = pref_field(
        PrefMeta(
            category="sounds",
            label="pref-set-play-turn-sound",
            change_msg="pref-changed-play-turn-sound",
            description="pref-desc-play-turn-sound",
            kind="bool",
            default=True,
        )
    )

    # --- Gameplay category ---
    confirm_destructive_actions: bool = pref_field(
        PrefMeta(
            category="gameplay",
            label="pref-set-confirm-destructive-actions",
            change_msg="pref-changed-confirm-destructive-actions",
            description="pref-desc-confirm-destructive-actions",
            kind="bool",
            default=True,
        )
    )

    # --- Dice category ---
    clear_kept_on_roll: bool = pref_field(
        PrefMeta(
            category="dice",
            label="pref-set-clear-kept-on-roll",
            change_msg="pref-changed-clear-kept-on-roll",
            description="pref-desc-clear-kept-on-roll",
            kind="bool",
            default=False,
        )
    )

    dice_keeping_style: DiceKeepingStyle = pref_field(
        PrefMeta(
            category="dice",
            label="pref-set-dice-keeping-style",
            change_msg="pref-changed-dice-keeping-style",
            description="pref-desc-dice-keeping-style",
            prompt="pref-select-dice-keeping-style",
            kind="menu",
            default=DiceKeepingStyle.PLAYPALACE,
            choices=[
                ("playpalace", "pref-dice-keeping-style-playpalace"),
                ("quentin_c", "pref-dice-keeping-style-quentin_c"),
            ],
            enum_class=DiceKeepingStyle,
        )
    )

    # --- Per-game overrides ---
    game_overrides: dict[str, dict[str, Any]] = field(
        default_factory=dict,
        metadata={"skip_pref": True},  # not a preference itself
    )

    # ------------------------------------------------------------------
    # Introspection helpers
    # ------------------------------------------------------------------

    @classmethod
    def get_pref_fields(cls) -> list[tuple[str, PrefMeta]]:
        """Return (field_name, PrefMeta) for every preference field, in order."""
        result = []
        for f in fields(cls):
            meta = f.metadata.get("pref_meta")
            if meta is not None:
                result.append((f.name, meta))
        return result

    @classmethod
    def get_fields_for_category(cls, category: str) -> list[tuple[str, PrefMeta]]:
        """Return pref fields belonging to a category, in definition order."""
        return [(n, m) for n, m in cls.get_pref_fields() if m.category == category]

    @classmethod
    def get_pref_meta(cls, field_name: str) -> PrefMeta | None:
        """Get PrefMeta for a field by name."""
        for f in fields(cls):
            if f.name == field_name:
                return f.metadata.get("pref_meta")
        return None

    # ------------------------------------------------------------------
    # Per-game overrides
    # ------------------------------------------------------------------

    def get_effective(self, field_name: str, game_type: str | None = None) -> Any:
        """Get the effective value of a preference, considering per-game overrides.

        If game_type is provided and a per-game override exists, return that.
        Otherwise return the global value.
        """
        if game_type and game_type in self.game_overrides:
            overrides = self.game_overrides[game_type]
            if field_name in overrides:
                raw = overrides[field_name]
                # Convert enums
                meta = self.get_pref_meta(field_name)
                if meta and meta.enum_class:
                    return meta.enum_class(raw) if isinstance(raw, str) else raw
                return raw
        return getattr(self, field_name)

    def set_game_override(self, field_name: str, game_type: str, value: Any) -> None:
        """Set a per-game override."""
        if game_type not in self.game_overrides:
            self.game_overrides[game_type] = {}
        # Store enum values as strings
        if isinstance(value, Enum):
            value = value.value
        self.game_overrides[game_type][field_name] = value

    def clear_game_override(self, field_name: str, game_type: str) -> None:
        """Remove a per-game override (revert to global default)."""
        if game_type in self.game_overrides:
            self.game_overrides[game_type].pop(field_name, None)
            if not self.game_overrides[game_type]:
                del self.game_overrides[game_type]

    def get_game_override(self, field_name: str, game_type: str) -> Any | None:
        """Get a per-game override, or None if not set."""
        if game_type in self.game_overrides:
            return self.game_overrides[game_type].get(field_name)
        return None

    def has_game_override(self, field_name: str, game_type: str) -> bool:
        """Check if a per-game override is set."""
        return game_type in self.game_overrides and field_name in self.game_overrides[game_type]

    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------

    def reset_all(self) -> None:
        """Reset all preferences and overrides to defaults."""
        for name, meta in self.get_pref_fields():
            setattr(self, name, meta.default)
        self.game_overrides.clear()

    def reset_category(self, category: str) -> None:
        """Reset all preferences in a category to defaults."""
        for name, meta in self.get_fields_for_category(category):
            setattr(self, name, meta.default)
            # Also clear per-game overrides for these fields
            for game_type in list(self.game_overrides):
                self.game_overrides[game_type].pop(name, None)
                if not self.game_overrides[game_type]:
                    del self.game_overrides[game_type]

    # ------------------------------------------------------------------
    # Serialization (auto-generated from field metadata)
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Convert to dictionary for storage."""
        result: dict[str, Any] = {}
        for name, meta in self.get_pref_fields():
            value = getattr(self, name)
            if isinstance(value, Enum):
                result[name] = value.value
            else:
                result[name] = value
        if self.game_overrides:
            result["game_overrides"] = self.game_overrides
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "UserPreferences":
        """Create from dictionary."""
        kwargs: dict[str, Any] = {}
        for name, meta in cls.get_pref_fields():
            if name in data:
                raw = data[name]
                if meta.enum_class:
                    try:
                        kwargs[name] = meta.enum_class(raw)
                    except (ValueError, KeyError):
                        kwargs[name] = meta.default
                elif meta.kind == "bool":
                    kwargs[name] = bool(raw)
                else:
                    kwargs[name] = raw
            # If not in data, default is used automatically
        prefs = cls(**kwargs)
        if "game_overrides" in data and isinstance(data["game_overrides"], dict):
            prefs.game_overrides = data["game_overrides"]
        return prefs
