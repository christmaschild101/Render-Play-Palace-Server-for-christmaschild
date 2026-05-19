"""Heuristic bot logic for Humanity Cards."""

from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game import HumanityCardsGame, HumanityCardsPlayer


def bot_think(game: "HumanityCardsGame", player: "HumanityCardsPlayer") -> str | None:
    if game.phase == "submitting":
        return _think_submitting(game, player)
    if game.phase == "judging":
        return _think_judging(game, player)
    return None


def _think_submitting(game: "HumanityCardsGame", player: "HumanityCardsPlayer") -> str | None:
    if game._is_judge(player) and not game._all_players_are_judges():
        return None
    if player.submitted_cards is not None:
        return None

    required = game.current_black_card["pick"] if game.current_black_card else 1

    if len(player.selected_indices) < required:
        available = [i for i in range(len(player.hand)) if i not in player.selected_indices]
        if available:
            return f"toggle_card_{random.choice(available)}"  # nosec B311

    if len(player.selected_indices) == required:
        return "submit_cards"

    return None


def _think_judging(game: "HumanityCardsGame", player: "HumanityCardsPlayer") -> str | None:
    if not game._is_judge(player):
        return None
    if player.id in game.judge_picks:
        return None
    if not game.submission_order:
        return None

    valid_picks = list(range(len(game.submission_order)))
    if game._all_players_are_judges():
        valid_picks = [
            i for i in valid_picks
            if game.submission_order[i] < len(game.submissions)
            and game.submissions[game.submission_order[i]]["player_id"] != player.id
        ]

    if not valid_picks:
        return None

    return f"judge_pick_{random.choice(valid_picks)}"  # nosec B311
