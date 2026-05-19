"""Pusoy Dos hand evaluator — combo detection, comparison, and instant wins."""

from __future__ import annotations

from dataclasses import dataclass, field
from collections import Counter

from mashumaro.mixins.json import DataClassJSONMixin

from ...game_utils.cards import Card


# ---------------------------------------------------------------------------
# Card value helpers
# ---------------------------------------------------------------------------


def get_rank_value(rank: int) -> int:
    """Big Two rank value. 3 is lowest (3), 2 is highest (15)."""
    if rank == 2:
        return 15
    if rank == 1:  # Ace
        return 14
    return rank


def get_suit_value(suit: int) -> int:
    """Big Two suit value. Diamonds(1) > Hearts(3) > Spades(4) > Clubs(2)."""
    return {1: 4, 3: 3, 4: 2, 2: 1}.get(suit, 0)


def card_value(card: Card) -> int:
    """Combined value for sorting: rank * 10 + suit."""
    return get_rank_value(card.rank) * 10 + get_suit_value(card.suit)


def sort_cards(cards: list[Card]) -> list[Card]:
    """Sort cards by Big Two rank then suit (ascending)."""
    return sorted(cards, key=card_value)


# ---------------------------------------------------------------------------
# Combo dataclass
# ---------------------------------------------------------------------------

TIER_MAP = {
    "single": 0,
    "pair": 0,
    "three_of_a_kind": 0,
    "straight": 1,
    "flush": 2,
    "full_house": 3,
    "four_of_a_kind": 4,
    "straight_flush": 5,
}


@dataclass
class Combo(DataClassJSONMixin):
    type_name: str
    cards: list[Card]
    rank_value: int
    suit_value: int
    tier: int = 0

    def __post_init__(self):
        self.cards = sort_cards(self.cards)
        self.tier = TIER_MAP.get(self.type_name, 0)

    def beats(self, other: Combo) -> bool:
        """Return True if this combo beats *other*."""
        if len(self.cards) != len(other.cards):
            return False

        if len(self.cards) == 5:
            if self.tier != other.tier:
                return self.tier > other.tier
            # Same tier — compare by type-specific rules
            if self.type_name in ("straight", "straight_flush"):
                if self.rank_value != other.rank_value:
                    return self.rank_value > other.rank_value
                return self.suit_value > other.suit_value
            elif self.type_name == "flush":
                if self.suit_value != other.suit_value:
                    return self.suit_value > other.suit_value
                return self.rank_value > other.rank_value
            else:  # full_house, four_of_a_kind
                return self.rank_value > other.rank_value

        # 1, 2, or 3 cards
        if self.rank_value != other.rank_value:
            return self.rank_value > other.rank_value
        return self.suit_value > other.suit_value


# ---------------------------------------------------------------------------
# Straight detection
# ---------------------------------------------------------------------------


def _detect_straight(
    ranks: list[int], sorted_cards: list[Card], allow_2: bool
) -> tuple[bool, int, int]:
    """Return (is_straight, high_rank, high_suit) for a 5-card hand.

    *ranks* must be the rank_values of *sorted_cards* in ascending order.
    When allow_2 is False, the 2 (rank_value 15) cannot appear in any straight.
    """
    if not allow_2 and 15 in ranks:
        return False, 0, 0

    # Standard consecutive check (covers most cases including A-high straights)
    if ranks == list(range(ranks[0], ranks[0] + 5)):
        return True, ranks[4], get_suit_value(sorted_cards[4].suit)

    # Wrap-around: A-2-3-4-5 (only valid when allow_2 is True)
    # Sorted rank values would be [3, 4, 5, 14, 15]
    if allow_2 and ranks == [3, 4, 5, 14, 15]:
        # 5 is the high card in this wrap-around straight
        for c in sorted_cards:
            if get_rank_value(c.rank) == 5:
                return True, 5, get_suit_value(c.suit)

    # Wrap-around: 2-3-4-5-6 (only valid when allow_2 is True)
    # Sorted rank values would be [3, 4, 5, 6, 15]
    if allow_2 and ranks == [3, 4, 5, 6, 15]:
        for c in sorted_cards:
            if get_rank_value(c.rank) == 6:
                return True, 6, get_suit_value(c.suit)

    # Wrap-around: J-Q-K-A-2 (only valid when allow_2 is True)
    # Sorted rank values would be [11, 12, 13, 14, 15]
    if allow_2 and ranks == [11, 12, 13, 14, 15]:
        for c in sorted_cards:
            if get_rank_value(c.rank) == 15:
                return True, 15, get_suit_value(c.suit)

    return False, 0, 0


# ---------------------------------------------------------------------------
# Combo evaluation
# ---------------------------------------------------------------------------


def evaluate_combo(cards: list[Card], *, allow_2_in_straights: bool = True) -> Combo | None:
    """Evaluate a list of cards and return a Combo if valid, else None."""
    n = len(cards)
    if n not in (1, 2, 3, 5):
        return None

    sc = sort_cards(cards)

    if n == 1:
        return Combo("single", cards, get_rank_value(sc[0].rank), get_suit_value(sc[0].suit))

    if n == 2:
        if sc[0].rank == sc[1].rank:
            return Combo(
                "pair",
                cards,
                get_rank_value(sc[0].rank),
                max(get_suit_value(sc[0].suit), get_suit_value(sc[1].suit)),
            )
        return None

    if n == 3:
        if sc[0].rank == sc[1].rank == sc[2].rank:
            return Combo("three_of_a_kind", cards, get_rank_value(sc[0].rank), 0)
        return None

    # --- 5-card hands ---
    ranks = [get_rank_value(c.rank) for c in sc]
    is_flush = len({c.suit for c in cards}) == 1
    is_straight, straight_high, straight_suit = _detect_straight(ranks, sc, allow_2_in_straights)

    rank_counts = Counter(c.rank for c in cards)
    counts = sorted(rank_counts.values())

    # Four of a kind (4 + 1 kicker) — check before straight/flush
    if counts == [1, 4]:
        four_rank = next(r for r, cnt in rank_counts.items() if cnt == 4)
        return Combo("four_of_a_kind", cards, get_rank_value(four_rank), 0)

    # Full house (3 + 2)
    if counts == [2, 3]:
        three_rank = next(r for r, cnt in rank_counts.items() if cnt == 3)
        return Combo("full_house", cards, get_rank_value(three_rank), 0)

    # Straight flush
    if is_straight and is_flush:
        return Combo("straight_flush", cards, straight_high, straight_suit)

    # Flush
    if is_flush:
        return Combo("flush", cards, get_rank_value(sc[4].rank), get_suit_value(sc[4].suit))

    # Straight
    if is_straight:
        return Combo("straight", cards, straight_high, straight_suit)

    return None


# ---------------------------------------------------------------------------
# Instant win detection
# ---------------------------------------------------------------------------


def detect_instant_win(hand: list[Card], *, allow_2_in_straights: bool = True) -> str | None:
    """Check if a 13-card hand qualifies for an instant win.

    Returns the instant win type name or None:
      - "dragon": 13-card straight (3 through 2, all 13 ranks)
      - "four_twos": all four 2s in hand
      - "six_pairs": exactly six pairs + one single
    """
    if len(hand) != 13:
        return None

    # Dragon: one card of every rank (3,4,5,6,7,8,9,10,J,Q,K,A,2)
    ranks = {c.rank for c in hand}
    if len(ranks) == 13:
        return "dragon"

    # Four 2s
    twos = [c for c in hand if c.rank == 2]
    if len(twos) == 4:
        return "four_twos"

    # Six pairs: exactly 6 distinct ranks appear twice, 1 rank appears once
    rank_counts = Counter(c.rank for c in hand)
    count_dist = Counter(rank_counts.values())
    if count_dist.get(2, 0) == 6 and count_dist.get(1, 0) == 1 and len(rank_counts) == 7:
        return "six_pairs"

    return None
