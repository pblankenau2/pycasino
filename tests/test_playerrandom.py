#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import pytest
from unittest.mock import Mock
from .context import roulette


@pytest.fixture
def playerrandom_regular():
    return roulette.player.PlayerRandom(
        stake=100,
        rounds=350,
        base_bet_amount=10
    )


def test__determine_bets(playerrandom_regular):
    playerrandom_regular._random_number_generator = Mock(random.Random)
    playerrandom_regular._random_number_generator.randrange.return_value = 0
    player_bet = playerrandom_regular._determine_bets()[0]
    assert player_bet.amount_bet == 10
    assert player_bet.outcome == roulette.wheel_builder.get_outcome('Straight 0')


def test_win(playerrandom_regular):
    table = roulette.model.Table(300)
    playerrandom_regular._random_number_generator = Mock(random.Random)
    playerrandom_regular._random_number_generator.randrange.return_value = 0
    playerrandom_regular.place_bets(table)
    playerrandom_regular.win(playerrandom_regular._determine_bets()[0])
    assert playerrandom_regular.stake == (100 + 35 * 10)
