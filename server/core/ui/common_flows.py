"""Reusable menu flows shared across server features.

Usage examples::

    # Switching locale (options menu) — all languages, native names shown
    show_language_menu(
        user, include_native_names=True,
        on_select=self._apply_locale_change,
        on_back=lambda u: self._show_options_menu(u),
    )

    # Filtered subset with status labels
    counts = {code: f"({n} users)" for code, n in transcriber_counts.items()}
    show_language_menu(
        user, highlight_active_locale=False,
        status_labels=counts,
        on_select=self._show_transcribers_for_language,
    )

    # Multi-select with done/cancel — menu manages toggle state internally
    show_language_menu(
        user, highlight_active_locale=False, multi_select=True,
        selected=set(user.fluent_languages),
        on_done=lambda u, sel: apply_selection(u, sel),
        on_cancel=lambda u: go_back(u),
    )
"""

from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING

from ...messages.localization import Localization
from ..users.base import MenuItem, EscapeBehavior

if TYPE_CHECKING:
    from ..users.network_user import NetworkUser

# Per-user callback storage for single-select language menus.
_language_menu_callbacks: dict[
    str,
    tuple[
        Callable[[NetworkUser, str], Awaitable[None]] | None,
        Callable[[NetworkUser], Awaitable[None]] | None,
    ],
] = {}

# Per-user state for multi-select language menus.
_language_menu_multi: dict[str, dict] = {}


def show_yes_no_menu(
    user: NetworkUser,
    menu_id: str,
    question: str,
    *,
    include_cancel: bool = False,
    initial_focus: str | int = "yes",
    allow_escape: bool = True,
) -> None:
    """Show a yes/no confirmation menu.

    The first item is a static label displaying *question*.  Focus is placed
    on *initial_focus* (``"yes"`` by default) so the label is skipped.

    *initial_focus* accepts an item id string (``"yes"``, ``"no"``,
    ``"cancel"``, ``"question"``) **or** an integer shorthand:
    ``1`` = yes, ``2`` = no, ``3`` = cancel, anything else = question label.

    Callers are responsible for setting ``_user_states`` themselves, since they
    often need to store extra context (e.g. ``target_username``).
    """
    items = [
        MenuItem(text=question, id="question"),
        MenuItem(text=Localization.get(user.locale, "confirm-yes"), id="yes"),
        MenuItem(text=Localization.get(user.locale, "confirm-no"), id="no"),
    ]
    if include_cancel:
        items.append(MenuItem(text=Localization.get(user.locale, "cancel"), id="cancel"))

    # Resolve 1-based position from the requested focus target.
    if isinstance(initial_focus, int):
        int_to_id = {1: "yes", 2: "no", 3: "cancel"}
        initial_focus = int_to_id.get(initial_focus, "question")
    focus_positions = {item.id: i for i, item in enumerate(items, start=1)}
    position = focus_positions.get(initial_focus, 2)  # fallback to "yes"

    if position != 1:
        user.speak(question)

    escape = EscapeBehavior.SELECT_LAST if allow_escape else EscapeBehavior.KEYBIND
    user.show_menu(
        menu_id,
        items,
        multiletter=True,
        escape_behavior=escape,
        position=position,
    )


def show_language_menu(
    user: NetworkUser,
    highlight_active_locale: bool = True,
    include_native_names: bool = False,
    multi_select: bool = False,
    *,
    lang_codes: list[str] | None = None,
    selected: set[str] | None = None,
    status_labels: dict[str, str] | None = None,
    focus_lang: str | None = None,
    on_select: Callable[[NetworkUser, str], Awaitable[None]] | None = None,
    on_back: Callable[[NetworkUser], Awaitable[None]] | None = None,
    on_done: Callable[..., Awaitable[None]] | None = None,
    on_cancel: Callable[[NetworkUser], Awaitable[None]] | None = None,
) -> bool:
    """Show a language selection menu.

    *focus_lang* sets which language code receives initial focus.  When
    ``None`` (the default), the user's current locale is focused.

    When *multi_select* is ``True``, the menu shows Done and Cancel items
    instead of Back.  Escape selects Cancel (last item).  Pass *selected*
    to let the menu manage toggle state internally:

    - *selected* is a mutable ``set[str]`` of language codes that are
      currently "on".  The menu modifies it in-place on each toggle and
      auto-generates on/off status labels.  Pass ``set(original)`` if the
      original collection must remain untouched.
    - *on_done(user, selected)* is called when Done is pressed.
    - *on_cancel(user)* is called when Cancel is pressed.
    - *on_select* and *on_back* are ignored in this mode.

    Returns ``True`` if the menu was displayed, ``False`` if it could not be
    shown (e.g. localization warmup still running).
    """
    if Localization.is_warmup_active():
        user.speak_l("localization-in-progress-try-again", buffer="misc")
        return False

    focus_target = focus_lang or user.locale

    # Auto-generate on/off status labels when the menu manages toggle state.
    if multi_select and selected is not None:
        on_label = Localization.get(user.locale, "option-on")
        off_label = Localization.get(user.locale, "option-off")
        all_codes = Localization.get_available_locale_codes()
        status_labels = {code: on_label if code in selected else off_label for code in all_codes}

    # Native names (each language in its own script)
    native_names = Localization.get_available_languages(fallback=user.locale)
    # Localized names (all names in the user's locale)
    localized_names = Localization.get_available_languages(user.locale, fallback=user.locale)

    # Filter to requested codes, preserving the full-dict order.
    if lang_codes is not None:
        codes_set = set(lang_codes)
        native_names = {c: n for c, n in native_names.items() if c in codes_set}

    items: list[MenuItem] = []
    selected_position = 1
    for index, (lang_code, native) in enumerate(native_names.items(), start=1):
        is_active = highlight_active_locale and lang_code == user.locale
        prefix = "* " if is_active else ""
        localized = localized_names.get(lang_code, native)
        display = f"{prefix}{localized}"
        # Append native name when it differs and this isn't the highlighted item
        if include_native_names and native != localized and not is_active:
            display = f"{display} ({native})"
        # Append caller-supplied status label
        if status_labels and lang_code in status_labels:
            display = f"{display} {status_labels[lang_code]}"
        items.append(MenuItem(text=display, id=f"lang_{lang_code}"))
        if lang_code == focus_target:
            selected_position = index

    if multi_select:
        items.append(MenuItem(text=Localization.get(user.locale, "done"), id="done"))
        items.append(MenuItem(text=Localization.get(user.locale, "cancel"), id="cancel"))
    else:
        items.append(MenuItem(text=Localization.get(user.locale, "back"), id="back"))

    # Store callbacks / state for the handler.
    if multi_select and selected is not None:
        _language_menu_multi[user.username] = {
            "selected": selected,
            "on_done": on_done,
            "on_cancel": on_cancel,
            "highlight_active_locale": highlight_active_locale,
            "include_native_names": include_native_names,
            "lang_codes": lang_codes,
        }
        _language_menu_callbacks.pop(user.username, None)
    else:
        _language_menu_callbacks[user.username] = (on_select, on_back)
        _language_menu_multi.pop(user.username, None)

    user.show_menu(
        "language_menu",
        items,
        multiletter=True,
        escape_behavior=EscapeBehavior.SELECT_LAST,
        position=selected_position,
    )
    return True


async def _invoke(callback, *args):
    """Call *callback* with *args*, awaiting if the result is awaitable."""
    if callback is not None:
        result = callback(*args)
        if inspect.isawaitable(result):
            await result


async def handle_language_menu_selection(user: NetworkUser, selection_id: str) -> None:
    """Dispatch a language-menu selection to the stored callbacks."""
    multi = _language_menu_multi.pop(user.username, None)
    if multi is not None:
        selected: set[str] = multi["selected"]
        if selection_id.startswith("lang_"):
            lang_code = selection_id[5:]
            if lang_code in selected:
                selected.discard(lang_code)
                user.play_sound("checkbox_list_off.wav")
            else:
                selected.add(lang_code)
                user.play_sound("checkbox_list_on.wav")
            # Rebuild the menu, focusing the toggled item.
            show_language_menu(
                user,
                multi["highlight_active_locale"],
                multi["include_native_names"],
                True,
                lang_codes=multi["lang_codes"],
                selected=selected,
                focus_lang=lang_code,
                on_done=multi["on_done"],
                on_cancel=multi["on_cancel"],
            )
        elif selection_id == "done":
            await _invoke(multi["on_done"], user, selected)
        elif selection_id == "cancel":
            await _invoke(multi["on_cancel"], user)
        return

    on_select, on_back = _language_menu_callbacks.pop(user.username, (None, None))
    if selection_id.startswith("lang_"):
        lang_code = selection_id[5:]
        await _invoke(on_select, user, lang_code)
    else:
        await _invoke(on_back, user)
