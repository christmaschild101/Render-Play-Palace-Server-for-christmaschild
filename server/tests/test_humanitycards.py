"""Tests for Humanity Cards (Cards Against Humanity) game."""

import pytest

from server.core.users.bot import Bot
from server.core.users.test_user import MockUser
from server.games.humanitycards.game import HumanityCardsGame, HumanityCardsOptions


# ==========================================================================
# Helpers
# ==========================================================================


def _make_white(count: int, start: int = 0) -> list[dict]:
    return [{"text": f"White card {i}", "pack": "Test", "id": i} for i in range(start, start + count)]


def _make_black(text: str = "Why is _ so funny?", pick: int = 1) -> dict:
    return {"text": text, "pick": pick, "pack": "Test"}


def _inject_decks(game: HumanityCardsGame, white_count: int = 200, black_count: int = 50) -> None:
    """Replace decks with deterministic test cards."""
    game.white_deck = _make_white(white_count)
    game.black_deck = [_make_black(f"Question {i} _") for i in range(black_count)]
    game.white_discard = []
    game.black_discard = []


def _setup_game(
    num_players: int = 3,
    options: HumanityCardsOptions | None = None,
    use_bots: bool = False,
) -> tuple[HumanityCardsGame, list[MockUser]]:
    opts = options or HumanityCardsOptions()
    game = HumanityCardsGame(options=opts)
    game._build_decks = lambda: _inject_decks(game)  # type: ignore[method-assign]
    users = []
    for i in range(num_players):
        name = f"Player{i}"
        if use_bots:
            user: MockUser | Bot = Bot(name)
        else:
            user = MockUser(name)
        game.add_player(name, user)
        if not use_bots:
            users.append(user)  # type: ignore[arg-type]
    game.on_start()
    return game, users


def _get_player(game: HumanityCardsGame, index: int):
    return game.get_active_players()[index]


# ==========================================================================
# Metadata & options
# ==========================================================================


def test_game_metadata():
    game = HumanityCardsGame()
    assert game.get_name() == "Cards Against Humanity"
    assert game.get_type() == "humanitycards"
    assert game.get_min_players() == 3
    assert game.get_max_players() >= 6


def test_options_defaults():
    opts = HumanityCardsOptions()
    assert opts.winning_score == 7
    assert opts.hand_size == 10
    assert opts.czar_selection == "Rotating"
    assert opts.num_judges == 1


# ==========================================================================
# Game startup
# ==========================================================================


def test_game_starts_in_submitting_phase():
    game, _ = _setup_game()
    assert game.phase == "submitting"
    assert game.status == "playing"
    assert game.round == 1


def test_players_dealt_hands_on_start():
    game, _ = _setup_game(num_players=3)
    for p in game.get_active_players():
        assert len(p.hand) == game.options.hand_size  # type: ignore[union-attr]


def test_player_scores_zero_on_start():
    game, _ = _setup_game()
    for p in game.get_active_players():
        assert p.score == 0  # type: ignore[union-attr]


def test_black_card_dealt_on_start():
    game, _ = _setup_game()
    assert game.current_black_card is not None
    assert "text" in game.current_black_card
    assert "pick" in game.current_black_card


# ==========================================================================
# Judge selection
# ==========================================================================


def test_one_judge_on_start():
    game, _ = _setup_game()
    judges = game._get_judges()
    assert len(judges) == 1


def test_rotating_judge_advances_each_round():
    game, _ = _setup_game(num_players=4)
    first_judge_id = game._get_judges()[0].id
    # Simulate completing a round by triggering next round
    game._start_round()
    second_judge_id = game._get_judges()[0].id
    assert first_judge_id != second_judge_id


def test_judge_count_never_exceeds_active_minus_one():
    game, _ = _setup_game(num_players=3, options=HumanityCardsOptions(num_judges=3))
    # 3 players, max judges = active - 1 = 2
    judges = game._get_judges()
    assert len(judges) <= len(game.get_active_players()) - 1


def test_random_judge_selection_picks_valid_player():
    game, _ = _setup_game(options=HumanityCardsOptions(czar_selection="Random"))
    judges = game._get_judges()
    active_ids = {p.id for p in game.get_active_players()}
    for j in judges:
        assert j.id in active_ids


def test_winner_judge_selection_uses_last_winner():
    game, _ = _setup_game(
        num_players=4, options=HumanityCardsOptions(czar_selection="Most Recent Winner")
    )
    active = game.get_active_players()
    game.last_winner_index = 2
    game._start_round()
    judges = game._get_judges()
    assert judges[0].id == active[2].id


def test_judge_personal_announcement_spoken():
    game, users = _setup_game(num_players=3)
    judge = game._get_judges()[0]
    judge_user = next(u for u in users if u.username == judge.name)
    spoken = judge_user.get_spoken_messages()
    assert any("Card Czar" in m for m in spoken)


# ==========================================================================
# Utility methods
# ==========================================================================


def test_fill_in_blanks_single():
    game, _ = _setup_game()
    result = game._fill_in_blanks("I love _.", ["cats"])
    assert result == "I love cats."


def test_fill_in_blanks_multiple():
    game, _ = _setup_game()
    result = game._fill_in_blanks("_ meets _.", ["Alice", "Bob"])
    assert result == "Alice meets Bob."


def test_fill_in_blanks_no_blank_appends():
    game, _ = _setup_game()
    result = game._fill_in_blanks("Why?", ["Because reasons"])
    assert result == "Why? Because reasons"


def test_speech_friendly_black_replaces_underscore():
    game, _ = _setup_game()
    assert game._speech_friendly_black("I love _.") == "I love blank."


def test_speech_friendly_black_multiple():
    game, _ = _setup_game()
    assert game._speech_friendly_black("_ and _.") == "blank and blank."


# ==========================================================================
# Deck reshuffle
# ==========================================================================


def test_white_deck_reshuffles_from_discard():
    game, _ = _setup_game()
    # Drain white deck
    game.white_deck = []
    game.white_discard = _make_white(5, start=100)
    drawn = game._draw_white(3)
    assert len(drawn) == 3
    # Remaining discard minus drawn cards
    assert len(game.white_deck) + len(drawn) == 5


def test_white_deck_reshuffle_broadcasts():
    game, users = _setup_game()
    game.white_deck = []
    game.white_discard = _make_white(5, start=100)
    for u in users:
        u.clear_messages()
    game._draw_white(1)
    all_spoken = [m for u in users for m in u.get_spoken_messages()]
    assert any("reshuffled" in m.lower() for m in all_spoken)


def test_black_deck_reshuffles_from_discard():
    game, _ = _setup_game()
    game.black_deck = []
    game.black_discard = [_make_black("Test _ card") for _ in range(3)]
    card = game._draw_black()
    assert card is not None


def test_draw_white_returns_empty_list_when_no_cards():
    game, _ = _setup_game()
    game.white_deck = []
    game.white_discard = []
    drawn = game._draw_white(5)
    assert drawn == []


# ==========================================================================
# Card toggling
# ==========================================================================


def test_toggle_card_selects_card():
    game, users = _setup_game()
    non_judge = game._get_non_judges()[0]
    assert len(non_judge.selected_indices) == 0
    game.execute_action(non_judge, "toggle_card_0")
    assert 0 in non_judge.selected_indices


def test_toggle_card_deselects_card():
    game, _ = _setup_game()
    non_judge = game._get_non_judges()[0]
    game.execute_action(non_judge, "toggle_card_0")
    assert 0 in non_judge.selected_indices
    game.execute_action(non_judge, "toggle_card_0")
    assert 0 not in non_judge.selected_indices


def test_judge_cannot_toggle_cards():
    game, _ = _setup_game()
    judge = game._get_judges()[0]
    game.execute_action(judge, "toggle_card_0")
    assert 0 not in judge.selected_indices  # type: ignore[union-attr]


def test_card_toggle_plays_select_sound():
    game, users = _setup_game()
    non_judge = game._get_non_judges()[0]
    non_judge_user = next(u for u in users if u.username == non_judge.name)
    non_judge_user.clear_messages()
    game.execute_action(non_judge, "toggle_card_0")
    sounds = non_judge_user.get_sounds_played()
    assert any("cardselect" in s for s in sounds)


def test_card_toggle_plays_unselect_sound():
    game, users = _setup_game()
    non_judge = game._get_non_judges()[0]
    non_judge_user = next(u for u in users if u.username == non_judge.name)
    game.execute_action(non_judge, "toggle_card_0")
    non_judge_user.clear_messages()
    game.execute_action(non_judge, "toggle_card_0")
    sounds = non_judge_user.get_sounds_played()
    assert any("cardunselect" in s for s in sounds)


# ==========================================================================
# Submission
# ==========================================================================


def test_submit_cards_removes_from_hand():
    game, _ = _setup_game()
    non_judge = game._get_non_judges()[0]
    hand_size_before = len(non_judge.hand)
    game.execute_action(non_judge, "toggle_card_0")
    game.execute_action(non_judge, "submit_cards")
    assert non_judge.submitted_cards is not None
    assert len(non_judge.hand) == hand_size_before - 1


def test_submit_cards_records_submission():
    game, _ = _setup_game()
    non_judge = game._get_non_judges()[0]
    expected_text = non_judge.hand[0]["text"]
    game.execute_action(non_judge, "toggle_card_0")
    game.execute_action(non_judge, "submit_cards")
    assert non_judge.submitted_cards == [expected_text]


def test_submit_wrong_count_rejected():
    game, users = _setup_game()
    # Force a pick-2 black card
    game.current_black_card = _make_black("_ loves _ forever.", pick=2)
    non_judge = game._get_non_judges()[0]
    non_judge_user = next(u for u in users if u.username == non_judge.name)
    # Select only 1 card, need 2
    game.execute_action(non_judge, "toggle_card_0")
    non_judge_user.clear_messages()
    game.execute_action(non_judge, "submit_cards")
    assert non_judge.submitted_cards is None
    spoken = non_judge_user.get_spoken_messages()
    assert any("2" in m for m in spoken)


def test_submit_already_submitted_rejected():
    game, users = _setup_game()
    non_judge = game._get_non_judges()[0]
    non_judge_user = next(u for u in users if u.username == non_judge.name)
    game.execute_action(non_judge, "toggle_card_0")
    game.execute_action(non_judge, "submit_cards")
    submission_after_first = list(non_judge.submitted_cards)  # type: ignore[arg-type]
    non_judge_user.clear_messages()
    # Try to submit again (no selected cards, already submitted)
    game.execute_action(non_judge, "submit_cards")
    assert non_judge.submitted_cards == submission_after_first


def test_judge_cannot_submit():
    game, _ = _setup_game()
    judge = game._get_judges()[0]
    game.execute_action(judge, "toggle_card_0")
    game.execute_action(judge, "submit_cards")
    assert judge.submitted_cards is None  # type: ignore[union-attr]


def test_all_submit_triggers_judging_phase():
    game, _ = _setup_game(num_players=3)
    for non_judge in game._get_non_judges():
        game.execute_action(non_judge, "toggle_card_0")
        game.execute_action(non_judge, "submit_cards")
    assert game.phase == "judging"


def test_submission_no_progress_broadcast():
    # Progress broadcast was removed — sound only, no speech
    game, users = _setup_game(num_players=3)
    for u in users:
        u.clear_messages()
    non_judge = game._get_non_judges()[0]
    game.execute_action(non_judge, "toggle_card_0")
    game.execute_action(non_judge, "submit_cards")
    all_spoken = [m for u in users for m in u.get_spoken_messages()]
    # Only the submitter hears "You submitted your cards." — no "N of M" broadcast
    assert not any("of" in m and "player" in m.lower() for m in all_spoken)


def test_pick_two_black_card_requires_two_submissions():
    game, _ = _setup_game()
    game.current_black_card = _make_black("_ with _ always.", pick=2)
    non_judge = game._get_non_judges()[0]
    game.execute_action(non_judge, "toggle_card_0")
    game.execute_action(non_judge, "toggle_card_1")
    game.execute_action(non_judge, "submit_cards")
    assert non_judge.submitted_cards is not None
    assert len(non_judge.submitted_cards) == 2


# ==========================================================================
# Judging
# ==========================================================================


def _get_to_judging(num_players: int = 3):
    game, users = _setup_game(num_players=num_players)
    for non_judge in game._get_non_judges():
        game.execute_action(non_judge, "toggle_card_0")
        game.execute_action(non_judge, "submit_cards")
    assert game.phase == "judging"
    return game, users


def test_judge_pick_awards_point():
    game, _ = _get_to_judging()
    judge = game._get_judges()[0]
    winner_before = {p.id: p.score for p in game.get_active_players()}  # type: ignore[union-attr]
    game.execute_action(judge, "judge_pick_0")
    winner_id = game.submissions[game.submission_order[0]]["player_id"]
    winner = game.get_player_by_id(winner_id)
    assert winner.score == winner_before[winner_id] + 1  # type: ignore[union-attr]


def test_judge_pick_transitions_to_round_end():
    game, _ = _get_to_judging()
    judge = game._get_judges()[0]
    game.execute_action(judge, "judge_pick_0")
    assert game.phase == "round_end"


def test_winner_announcement_broadcast():
    game, users = _get_to_judging()
    for u in users:
        u.clear_messages()
    judge = game._get_judges()[0]
    game.execute_action(judge, "judge_pick_0")
    all_spoken = [m for u in users for m in u.get_spoken_messages()]
    assert any("wins" in m.lower() for m in all_spoken)


def test_non_judge_cannot_pick():
    game, _ = _get_to_judging()
    non_judge = game._get_non_judges()[0]
    # Non-judges have no valid submissions to pick at this point, action is hidden
    submissions_before = list(game.submissions)
    game.execute_action(non_judge, "judge_pick_0")
    # State unchanged
    assert game.submissions == submissions_before
    assert game.phase == "judging"


def test_submissions_shuffled_before_judging():
    # Run many times; at least some ordering should differ from insertion order
    game, _ = _setup_game(num_players=4)
    for non_judge in game._get_non_judges():
        game.execute_action(non_judge, "toggle_card_0")
        game.execute_action(non_judge, "submit_cards")
    # submission_order exists and covers all submissions
    assert len(game.submission_order) == len(game.submissions)
    assert sorted(game.submission_order) == list(range(len(game.submissions)))


# ==========================================================================
# Win condition
# ==========================================================================


def test_game_ends_when_winning_score_reached():
    game, _ = _setup_game(options=HumanityCardsOptions(winning_score=1))
    for non_judge in game._get_non_judges():
        game.execute_action(non_judge, "toggle_card_0")
        game.execute_action(non_judge, "submit_cards")
    judge = game._get_judges()[0]
    game.execute_action(judge, "judge_pick_0")
    assert game.status == "finished"


def test_round_continues_when_score_below_winning():
    game, _ = _setup_game(options=HumanityCardsOptions(winning_score=5))
    for non_judge in game._get_non_judges():
        game.execute_action(non_judge, "toggle_card_0")
        game.execute_action(non_judge, "submit_cards")
    judge = game._get_judges()[0]
    game.execute_action(judge, "judge_pick_0")
    assert game.status == "playing"
    assert game.phase == "round_end"


def test_game_winner_broadcast():
    game, users = _setup_game(options=HumanityCardsOptions(winning_score=1))
    for non_judge in game._get_non_judges():
        game.execute_action(non_judge, "toggle_card_0")
        game.execute_action(non_judge, "submit_cards")
    for u in users:
        u.clear_messages()
    judge = game._get_judges()[0]
    game.execute_action(judge, "judge_pick_0")
    all_spoken = [m for u in users for m in u.get_spoken_messages()]
    assert any("wins" in m.lower() for m in all_spoken)


# ==========================================================================
# Score display (fix 3: speak_l not raw speak)
# ==========================================================================


def test_check_scores_speaks_all_players_v2():
    game, users = _setup_game(num_players=3)
    player0 = _get_player(game, 0)
    player0.score = 3  # type: ignore[union-attr]
    user0 = next(u for u in users if u.username == player0.name)
    user0.clear_messages()
    game.execute_action(player0, "check_scores")
    spoken = user0.get_spoken_messages()
    assert any(player0.name in m for m in spoken)


def test_check_scores_includes_score_values():
    game, users = _setup_game(num_players=3)
    player0 = _get_player(game, 0)
    player0.score = 5  # type: ignore[union-attr]
    user0 = next(u for u in users if u.username == player0.name)
    user0.clear_messages()
    game.execute_action(player0, "check_scores")
    spoken = user0.get_spoken_messages()
    # Score "5" or "5 points" should appear
    assert any("5" in m for m in spoken)


def test_check_scores_ordered_descending():
    game, users = _setup_game(num_players=3)
    active = game.get_active_players()
    active[0].score = 5  # type: ignore[union-attr]
    active[1].score = 3  # type: ignore[union-attr]
    active[2].score = 1  # type: ignore[union-attr]
    user0 = next(u for u in users if u.username == active[0].name)
    user0.clear_messages()
    game.execute_action(active[0], "check_scores")
    spoken = user0.get_spoken_messages()
    # First spoken message should mention the highest scorer
    assert active[0].name in spoken[0]


def test_check_scores_speaks_all_players():
    game, users = _setup_game(num_players=3)
    player0 = _get_player(game, 0)
    user0 = next(u for u in users if u.username == player0.name)
    user0.clear_messages()
    game.execute_action(player0, "check_scores")
    spoken = user0.get_spoken_messages()
    assert len(spoken) == 3  # One line per player


# ==========================================================================
# Judge personal announcement (fix 4: hc-you-are-judge)
# ==========================================================================


def test_judge_hears_you_are_judge_message():
    game, users = _setup_game(num_players=3)
    judge = game._get_judges()[0]
    judge_user = next(u for u in users if u.username == judge.name)
    spoken = judge_user.get_spoken_messages()
    assert any("Card Czar" in m for m in spoken)


def test_non_judge_does_not_hear_you_are_judge():
    game, users = _setup_game(num_players=3)
    judge_ids = {j.id for j in game._get_judges()}
    non_judge_users = [
        u for u in users
        if game.get_player_by_id(
            next((p.id for p in game.get_active_players() if p.name == u.username), "")
        ) is not None
        and next(
            (p for p in game.get_active_players() if p.name == u.username), None
        ) is not None
        and next(p for p in game.get_active_players() if p.name == u.username).id not in judge_ids
    ]
    for u in non_judge_users:
        spoken = u.get_spoken_messages()
        # Non-judges hear "X is the Card Czar" (broadcast) but NOT "You are the Card Czar"
        assert not any(m.startswith("You are the Card Czar") for m in spoken)


def test_judge_announcement_fires_each_new_round():
    game, users = _setup_game(num_players=3)
    # Complete submissions to advance round
    for non_judge in game._get_non_judges():
        game.execute_action(non_judge, "toggle_card_0")
        game.execute_action(non_judge, "submit_cards")
    first_judge = game._get_judges()[0]
    old_judge_user = next(u for u in users if u.username == first_judge.name)
    old_judge_user.clear_messages()
    # Pick winner → round_end → next round
    game.execute_action(first_judge, "judge_pick_0")
    # Advance tick countdown to trigger next round
    game.round_end_ticks = 1
    game.on_tick()
    # New judge should have received announcement
    new_judge = game._get_judges()[0]
    new_judge_user = next(u for u in users if u.username == new_judge.name)
    spoken = new_judge_user.get_spoken_messages()
    assert any("Card Czar" in m for m in spoken)


# ==========================================================================
# ==========================================================================
# Multi-judge voting
# ==========================================================================


def _setup_multi_judge(num_judges: int = 2, num_players: int = 4):
    game, users = _setup_game(
        num_players=num_players,
        options=HumanityCardsOptions(num_judges=num_judges),
    )
    for non_judge in game._get_non_judges():
        game.execute_action(non_judge, "toggle_card_0")
        game.execute_action(non_judge, "submit_cards")
    assert game.phase == "judging"
    return game, users


def test_multi_judge_waits_for_all_judges():
    game, _ = _setup_multi_judge(num_judges=2, num_players=4)
    judges = game._get_judges()
    assert len(judges) == 2
    # First judge picks — should NOT end round yet
    game.execute_action(judges[0], "judge_pick_0")
    assert game.phase == "judging"
    assert len(game.judge_picks) == 1


def test_multi_judge_resolves_after_all_pick():
    game, _ = _setup_multi_judge(num_judges=2, num_players=4)
    judges = game._get_judges()
    game.execute_action(judges[0], "judge_pick_0")
    game.execute_action(judges[1], "judge_pick_0")
    assert game.phase in ("round_end", "finished")


def test_multi_judge_cannot_vote_twice():
    game, _ = _setup_multi_judge(num_judges=2, num_players=4)
    judges = game._get_judges()
    game.execute_action(judges[0], "judge_pick_0")
    first_picks = dict(game.judge_picks)
    game.execute_action(judges[0], "judge_pick_1")  # attempt second vote
    assert game.judge_picks == first_picks


def test_multi_judge_majority_wins():
    game, _ = _setup_multi_judge(num_judges=2, num_players=4)
    judges = game._get_judges()
    # Both judges pick submission 0 → that player wins
    sub0_player_id = game.submissions[game.submission_order[0]]["player_id"]
    game.execute_action(judges[0], "judge_pick_0")
    game.execute_action(judges[1], "judge_pick_0")
    winner = game.get_player_by_id(sub0_player_id)
    assert winner.score == 1  # type: ignore[union-attr]


def test_multi_judge_split_vote_tiebreak_by_order():
    game, _ = _setup_multi_judge(num_judges=2, num_players=4)
    judges = game._get_judges()
    assert len(game.submissions) >= 2
    # Judges split — submission_order[0] should win tiebreak
    sub0_player_id = game.submissions[game.submission_order[0]]["player_id"]
    game.execute_action(judges[0], "judge_pick_0")
    game.execute_action(judges[1], "judge_pick_1")
    winner = game.get_player_by_id(sub0_player_id)
    assert winner.score == 1  # type: ignore[union-attr]


def test_multi_judge_voted_broadcast():
    game, users = _setup_multi_judge(num_judges=2, num_players=4)
    for u in users:
        u.clear_messages()
    judges = game._get_judges()
    game.execute_action(judges[0], "judge_pick_0")
    all_spoken = [m for u in users for m in u.get_spoken_messages()]
    assert any("made their choice" in m for m in all_spoken)


def test_single_judge_no_waiting_broadcast():
    game, users = _get_to_judging(num_players=3)
    for u in users:
        u.clear_messages()
    judge = game._get_judges()[0]
    game.execute_action(judge, "judge_pick_0")
    all_spoken = [m for u in users for m in u.get_spoken_messages()]
    # No "made their choice" intermediate broadcast — single judge goes straight to result
    assert not any("made their choice" in m for m in all_spoken)


def test_wrong_card_count_speaks_error_not_raw_tuple():
    game, users = _setup_game(num_players=3)
    game.current_black_card = _make_black("_ with _ always.", pick=2)
    non_judge = game._get_non_judges()[0]
    non_judge_user = next(u for u in users if u.username == non_judge.name)
    # Select only 1 card, need 2
    game.execute_action(non_judge, "toggle_card_0")
    non_judge_user.clear_messages()
    game.execute_action(non_judge, "submit_cards")
    spoken = non_judge_user.get_spoken_messages()
    assert spoken, "should have spoken an error"
    assert not any("hc-wrong-card-count" in m for m in spoken), "raw key leaked into speech"
    assert any("2" in m for m in spoken)


# Round transition via ticks
# ==========================================================================


def test_round_end_ticks_advance_to_next_round():
    game, _ = _setup_game()
    for non_judge in game._get_non_judges():
        game.execute_action(non_judge, "toggle_card_0")
        game.execute_action(non_judge, "submit_cards")
    game.execute_action(game._get_judges()[0], "judge_pick_0")
    assert game.phase == "round_end"
    game.round_end_ticks = 1
    game.on_tick()
    assert game.phase == "submitting"
    assert game.round == 2


# ==========================================================================
# Full bot game
# ==========================================================================


def test_bot_game_completes():
    opts = HumanityCardsOptions(winning_score=3)
    game = HumanityCardsGame(options=opts)
    game._build_decks = lambda: _inject_decks(game, white_count=500, black_count=100)  # type: ignore[method-assign]
    for i in range(4):
        game.add_player(f"Bot{i}", Bot(f"Bot{i}"))
    game.on_start()

    for _ in range(100_000):
        if game.status == "finished":
            break
        game.on_tick()

    assert game.status == "finished"


def test_bot_game_all_players_score_tracked():
    opts = HumanityCardsOptions(winning_score=2)
    game = HumanityCardsGame(options=opts)
    game._build_decks = lambda: _inject_decks(game, white_count=500, black_count=100)  # type: ignore[method-assign]
    for i in range(3):
        game.add_player(f"Bot{i}", Bot(f"Bot{i}"))
    game.on_start()
    for _ in range(100_000):
        if game.status == "finished":
            break
        game.on_tick()
    total_score = sum(p.score for p in game.get_active_players())  # type: ignore[union-attr]
    assert total_score >= opts.winning_score
