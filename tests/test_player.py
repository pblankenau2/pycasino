#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from .context import roulette

# TODO: somehow we can use pytest.mark.parameterize to inject multiple classes into one test.


@pytest.fixture
def player_not_playing_because_rounds():
    return roulette.player.PlayerDouble(stake=20, rounds=0, base_bet_amount=5)


@pytest.fixture
def player_not_playing_because_stake():
    return roulette.player.PlayerDouble(stake=10, rounds=350, base_bet_amount=10)


@pytest.fixture
def player_regular():
    return roulette.player.PlayerDouble(stake=100.0, rounds=250, base_bet_amount=10.0)


@pytest.mark.parametrize("player", [roulette.player.PlayerDouble()])
def test_player(player):
    pass


def test_win(player_regular):
    player_regular.win(
        roulette.model.Bet(10.0, roulette.wheel_builder.get_outcome("Black"))
    )
    assert player_regular.stake == 120.0
    assert player_regular.rounds == 249


def test_lose(player_regular):
    player_regular.lose()
    assert player_regular.rounds == 249


def test_playing_no_rounds_left(player_not_playing_because_rounds):
    assert not player_not_playing_because_rounds.playing


def test_playing_stake_too_small(player_not_playing_because_stake):
    assert not player_not_playing_because_stake.playing


def test_place_bets(player_regular):
    table = roulette.model.Table(300)
    player_regular.place_bets(table)
    assert player_regular.stake == 90.0  # 100.0 - bet amount


def test_bet_amount(player_regular):
    assert player_regular.bet_amount == player_regular.base_bet_amount


def test_track_last_winning_outcomes(player_regular):
    player_regular.track_last_winning_outcomes(
        [
            roulette.wheel_builder.get_outcome("Black"),
            roulette.wheel_builder.get_outcome("Red"),
        ]
    )
    # Add more than one outcome.
    assert player_regular._winners[0] == roulette.wheel_builder.get_outcome("Black")
