#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import pytest
from mock import Mock
from .context import roulette


@pytest.fixture
def playerrandom_not_playing_because_rounds():
    table = roulette.model.Table(300)
    return roulette.player.PlayerRandom(
        table=table,
        stake=20,
        rounds=0,
        bet_amount=5
    )


@pytest.fixture
def playerrandom_not_playing_because_stake():
    table = roulette.model.Table(300)
    return roulette.player.PlayerRandom(
        table=table,
        stake=10,
        rounds=350,
        bet_amount=10
    )


@pytest.fixture
def playerrandom_regular():
    table = roulette.model.Table(300)
    return roulette.player.PlayerRandom(
        table=table,
        stake=100,
        rounds=350,
        bet_amount=10
    )


def test_playing_no_rounds_left(playerrandom_not_playing_because_rounds):
    assert (not playerrandom_not_playing_because_rounds.playing)


def test_playing_stake_too_small(playerrandom_not_playing_because_stake):
    assert (not playerrandom_not_playing_because_stake.playing)


def test__determine_bets(playerrandom_regular):
    playerrandom_regular._random_number_generator = Mock(random.Random)
    playerrandom_regular._random_number_generator.randrange.return_value = 0
    player_bet = playerrandom_regular._determine_bets()[0]
    assert player_bet.amount_bet == 10
    assert player_bet.outcome == roulette.bin_builder.get_outcome('Straight 0')


def test_win(playerrandom_regular):
    playerrandom_regular._random_number_generator = Mock(random.Random)
    playerrandom_regular._random_number_generator.randrange.return_value = 0
    playerrandom_regular.place_bets()
    playerrandom_regular.win(playerrandom_regular._determine_bets()[0])
    assert playerrandom_regular.stake == (100 + 35 * 10)


def test_lose():
    # No lose method is implemented.
    pass