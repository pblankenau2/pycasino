#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from .context import roulette


@pytest.fixture
def table():
    return roulette.model.Table(300)


@pytest.fixture
def table_with_bets():
    return roulette.model.Table(
        300, roulette.model.Bet(200, roulette.model.Outcome("Red", 1))
    )


# TODO: Does this test really add any info?
def test_table_no_bets(table):
    """Check that the table has no bets by default."""
    assert table.bets == list()


# TODO: Does this test really add any info?
def test_table_with_bets(table_with_bets):
    """Check if using the bet argument adds a bet."""
    assert table_with_bets.bets != list()


def test_table_place_bet(table):
    """Check if place bet adds a bet to the table."""
    table.place_bet(roulette.model.Bet(200, roulette.model.Outcome("Red", 1)))

    assert table.bets != list()


def test_table_bets_is_valid_valid(table):
    """Check to see if a valid bet is valid."""
    table.place_bet(roulette.model.Bet(300, roulette.model.Outcome("Red", 1)))
    table.is_valid()


def test_table_bets_is_valid_invalid_over_limit(table):
    """Check if an 'over the limit' bet throws the right error."""
    with pytest.raises(roulette.model.InvalidBet):
        table.place_bet(roulette.model.Bet(400, roulette.model.Outcome("Red", 1)))
        table.is_valid()
