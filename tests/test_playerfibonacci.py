#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from .context import roulette


@pytest.fixture
def playerfibonacci_regular():
    table = roulette.model.Table(300)
    return roulette.player.PlayerFibonacci(
        table=table,
        stake=100,
        rounds=350,
        base_bet_amount=10
    )

# Note: this class inherits most of it's method from PlayerMartingale so they aren't tested.

def test_bet_amount_win(playerfibonacci_regular):
    playerfibonacci_regular.win(playerfibonacci_regular._determine_bets()[0])
    assert (playerfibonacci_regular.bet_amount == 10)
    playerfibonacci_regular.win(playerfibonacci_regular._determine_bets()[0])
    assert (playerfibonacci_regular.bet_amount == 10)


def test_bet_amount_lose_several(playerfibonacci_regular):
    playerfibonacci_regular.lose()
    assert (playerfibonacci_regular.bet_amount == 10)
    playerfibonacci_regular.lose()
    assert (playerfibonacci_regular.bet_amount == 20)
    playerfibonacci_regular.lose()
    assert (playerfibonacci_regular.bet_amount == 30)
    playerfibonacci_regular.lose()
    assert (playerfibonacci_regular.bet_amount == 50)
