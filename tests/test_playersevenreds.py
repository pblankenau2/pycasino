#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from .context import roulette


# TODO: should we also run the martingale tests on this class?  How to make it DRY?

@pytest.fixture
def playersevenreds_regular():
    return roulette.player.PlayerSevenReds(
        stake=20,
        rounds=50,
        base_bet_amount=5
    )

# Note: this class inherits most of it's method from PlayerMartingale so they aren't tested.

def test__determine_bets_no_bet(playersevenreds_regular):
    # We are testing if the player makes a bet with zero dollars.
    player_bet = playersevenreds_regular._determine_bets()[0]
    assert player_bet.amount_bet == 0

def test__determine_bets_7reds(playersevenreds_regular):
    # We are testing if betting has begun after 7 reds being played in a row.
    playersevenreds_regular._winners = [playersevenreds_regular._red]
    # We determine bets 8 times with red being a winner each time
    playersevenreds_regular._determine_bets()
    playersevenreds_regular._determine_bets()
    playersevenreds_regular._determine_bets()
    playersevenreds_regular._determine_bets()
    playersevenreds_regular._determine_bets()
    playersevenreds_regular._determine_bets()
    playersevenreds_regular._determine_bets()
    player_bet = playersevenreds_regular._determine_bets()[0]
    assert player_bet.amount_bet == playersevenreds_regular.base_bet_amount
