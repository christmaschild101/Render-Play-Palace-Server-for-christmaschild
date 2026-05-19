from dataclasses import dataclass

from server.game_utils.poker_pot import PokerPot
from server.game_utils.poker_payout import compute_ordered_payouts, resolve_pot
from server.game_utils.poker_payout import resolve_pots_with_payouts


@dataclass(frozen=True)
class DummyPlayer:
    id: str
    score: tuple[int, tuple[int, ...]]


def test_compute_ordered_payouts_distributes_odd_chips_one_at_a_time():
    winners = ["p1", "p2", "p3"]

    payouts = compute_ordered_payouts(5, winners)

    assert payouts == [("p1", 2), ("p2", 2), ("p3", 1)]


def test_resolve_pot_orders_winners_for_odd_chip_distribution():
    players = [
        DummyPlayer("button", (2, (10,))),
        DummyPlayer("left_1", (2, (10,))),
        DummyPlayer("left_2", (2, (10,))),
    ]

    winners, best_score, _share, _remainder = resolve_pot(
        5,
        players,
        active_ids=["button", "left_1", "left_2"],
        button_id="button",
        get_id=lambda player: player.id,
        score_fn=lambda player: player.score,
    )

    assert best_score == (2, (10,))
    assert [player.id for player in winners] == ["left_1", "left_2", "button"]
    assert [(player.id, payout) for player, payout in compute_ordered_payouts(5, winners)] == [
        ("left_1", 2),
        ("left_2", 2),
        ("button", 1),
    ]


def test_resolve_pots_with_payouts_applies_awards_in_order():
    players = {
        "button": DummyPlayer("button", (2, (10,))),
        "left_1": DummyPlayer("left_1", (2, (10,))),
        "left_2": DummyPlayer("left_2", (1, (9,))),
    }
    awarded: dict[str, int] = {}

    results = resolve_pots_with_payouts(
        [
            PokerPot(amount=5, eligible_player_ids={"button", "left_1", "left_2"}),
            PokerPot(amount=3, eligible_player_ids={"button", "left_1"}),
        ],
        get_player_by_id=lambda player_id: players.get(player_id),
        active_ids=["button", "left_1", "left_2"],
        button_id="button",
        get_id=lambda player: player.id,
        score_fn=lambda player: player.score,
        award_fn=lambda player, payout: awarded.__setitem__(
            player.id, awarded.get(player.id, 0) + payout
        ),
    )

    assert len(results) == 2
    assert [(player.id, payout) for player, payout in results[0].payouts] == [
        ("left_1", 3),
        ("button", 2),
    ]
    assert [(player.id, payout) for player, payout in results[1].payouts] == [
        ("left_1", 2),
        ("button", 1),
    ]
    assert awarded == {"left_1": 5, "button": 3}
