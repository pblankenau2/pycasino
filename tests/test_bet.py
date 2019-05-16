#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from .context import roulette


@pytest.fixture
def bet():
    return roulette.model.Bet(
        20,
        roulette.bin_builder.get_outcome('Red')
    )


def test_bet_win_amount(bet):
    assert bet.win_amount == 20 * 2


def test_bet_lose_amount(bet):
    assert bet.lose_amount == 20
