#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from .context import roulette

# TODO: make a player ABC test class?


@pytest.fixture
def player57_not_playing_because_rounds():
    table = roulette.model.Table(300)
    return roulette.player.PlayerPassenger57(
        table=table,
        stake=20,
        rounds=0,
        bet_amount=5
    )


@pytest.fixture
def player57_not_playing_because_stake():
    table = roulette.model.Table(300)
    return roulette.player.PlayerPassenger57(
        table=table,
        stake=10,
        rounds=350,
        bet_amount=10
    )


@pytest.fixture
def player57_regular():
    table = roulette.model.Table(300)
    return roulette.player.PlayerPassenger57(
        table=table,
        stake=100,
        rounds=350,
        bet_amount=10
    )


def test_playing_no_rounds_left(player57_not_playing_because_rounds):
    assert (not player57_not_playing_because_rounds.playing)


def test_playing_stake_too_small(player57_not_playing_because_stake):
    assert (not player57_not_playing_because_stake.playing)


def test__determine_bets(player57_regular):
    player_bet = player57_regular._determine_bets()[0]
    assert player_bet.amount_bet == 10
    assert player_bet.outcome == roulette.bin_builder.get_outcome('Black')


def test_win(player57_regular):
    player57_regular.place_bets()
    player57_regular.win(player57_regular._determine_bets()[0])
    assert player57_regular.stake == 110


def test_lose():
    # No lose method is implemented.
    pass
