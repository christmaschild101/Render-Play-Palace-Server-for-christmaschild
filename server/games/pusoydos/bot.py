"""Pusoy Dos bot AI — strategic card play and card passing."""

from __future__ import annotations

from itertools import combinations
from typing import TYPE_CHECKING
import random

from ...game_utils.cards import Card
from .evaluator import Combo, evaluate_combo, sort_cards, card_value, get_rank_value

if TYPE_CHECKING:
    from .game import PusoyDosGame, PusoyDosPlayer


# ---------------------------------------------------------------------------
# Combo generation
# ---------------------------------------------------------------------------


def get_all_valid_combos(hand: list[Card], *, allow_2: bool = True) -> list[Combo]:
    """Generate all valid combos from a hand."""
    combos: list[Combo] = []

    for c in hand:
        combo = evaluate_combo([c], allow_2_in_straights=allow_2)
        if combo:
            combos.append(combo)

    for cards in combinations(hand, 2):
        combo = evaluate_combo(list(cards), allow_2_in_straights=allow_2)
        if combo:
            combos.append(combo)

    for cards in combinations(hand, 3):
        combo = evaluate_combo(list(cards), allow_2_in_straights=allow_2)
        if combo:
            combos.append(combo)

    if len(hand) >= 5:
        for cards in combinations(hand, 5):
            combo = evaluate_combo(list(cards), allow_2_in_straights=allow_2)
            if combo:
                combos.append(combo)

    return combos


def _combo_strength(combo: Combo) -> tuple[int, int, int]:
    """Sort key: (tier, rank_value, suit_value) — higher is stronger."""
    return (combo.tier, combo.rank_value, combo.suit_value)


# ---------------------------------------------------------------------------
# Strategic helpers
# ---------------------------------------------------------------------------


def _is_two(card: Card) -> bool:
    return card.rank == 2


def _count_twos(cards: list[Card]) -> int:
    return sum(1 for c in cards if _is_two(c))


def _hand_strength(hand: list[Card]) -> float:
    """Rough hand strength heuristic: sum of card values."""
    return sum(card_value(c) for c in hand)


# ---------------------------------------------------------------------------
# Bot play logic
# ---------------------------------------------------------------------------


def bot_think(game: "PusoyDosGame", player: "PusoyDosPlayer") -> list[int]:
    """Return card IDs to play, or empty list to pass."""
    hand = sort_cards(player.hand)
    current_combo = game.current_combo
    is_first_turn = game.is_first_turn
    allow_2 = game.options.allow_2_in_straights

    # Must include 3 of Clubs on first turn
    has_3c = any(c.rank == 3 and c.suit == 2 for c in hand)
    if is_first_turn and has_3c:
        all_combos = get_all_valid_combos(hand, allow_2=allow_2)
        valid_starts = [
            c for c in all_combos if any(card.rank == 3 and card.suit == 2 for card in c.cards)
        ]
        if valid_starts:
            # Prefer larger combos to clear more cards, but avoid using 2s
            valid_starts.sort(
                key=lambda c: (
                    -len(c.cards),
                    _count_twos(c.cards),  # fewer 2s is better
                    _combo_strength(c),
                )
            )
            return [c.id for c in valid_starts[0].cards]

    all_combos = get_all_valid_combos(hand, allow_2=allow_2)

    if current_combo is None:
        # Free play — lead strategically
        return _bot_free_play(hand, all_combos)

    # Must beat the current combo
    valid_plays = [
        c for c in all_combos if len(c.cards) == len(current_combo.cards) and c.beats(current_combo)
    ]

    if not valid_plays:
        return []  # Pass

    return _bot_choose_play(hand, valid_plays)


def _bot_free_play(hand: list[Card], all_combos: list[Combo]) -> list[int]:
    """Choose what to lead with when starting a new trick."""
    if not all_combos:
        return []

    cards_left = len(hand)

    # Endgame: if 5 or fewer cards, try to dump everything
    if cards_left <= 5:
        # Check if we can play all remaining cards as one combo
        full_combo = evaluate_combo(hand)
        if full_combo:
            return [c.id for c in hand]

    # Prefer 5-card combos to clear more cards at once
    five_card = [c for c in all_combos if len(c.cards) == 5]
    if five_card and cards_left > 5:
        # Play the weakest 5-card combo (save strong ones)
        five_card.sort(key=_combo_strength)
        # Avoid leading with combos containing 2s unless we must
        non_two_fives = [c for c in five_card if _count_twos(c.cards) == 0]
        if non_two_fives:
            return [c.id for c in non_two_fives[0].cards]
        return [c.id for c in five_card[0].cards]

    # Otherwise play weakest singles/pairs/triples
    small_combos = [c for c in all_combos if len(c.cards) < 5]
    if small_combos:
        # Sort: prefer combos without 2s, then weakest first
        small_combos.sort(
            key=lambda c: (
                _count_twos(c.cards),
                _combo_strength(c),
            )
        )
        return [c.id for c in small_combos[0].cards]

    return []


def _bot_choose_play(hand: list[Card], valid_plays: list[Combo]) -> list[int]:
    """Choose the best play from valid options that beat the current trick."""
    cards_left = len(hand)

    # If we can win and empty our hand, always do it
    for combo in valid_plays:
        if len(combo.cards) == cards_left:
            return [c.id for c in combo.cards]

    # Play the weakest valid combo to conserve strong cards
    # But avoid wasting 2s unless necessary
    non_two_plays = [c for c in valid_plays if _count_twos(c.cards) == 0]
    if non_two_plays:
        non_two_plays.sort(key=_combo_strength)
        return [c.id for c in non_two_plays[0].cards]

    # Must use 2s — play the weakest option
    valid_plays.sort(key=_combo_strength)
    return [c.id for c in valid_plays[0].cards]


# ---------------------------------------------------------------------------
# Card passing (tribute) logic
# ---------------------------------------------------------------------------


def bot_choose_give_cards(hand: list[Card], count: int) -> list[int]:
    """Choose cards to give back during card passing (winner gives worst cards)."""
    sorted_hand = sort_cards(hand)
    # Give the lowest-value cards
    give = sorted_hand[:count]
    return [c.id for c in give]
