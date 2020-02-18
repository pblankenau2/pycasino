#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from .context import roulette


@pytest.fixture
def playercancellation_not_playing_because_rounds():
    return roulette.player.PlayerCancellation(stake=20, rounds=0)


@pytest.fixture
def playercancellation_not_playing_because_stake():
    return roulette.player.PlayerCancellation(stake=5, rounds=350)


@pytest.fixture
def playercancellation_not_playing_because_sequence():
    player = roulette.player.PlayerCancellation(stake=10, rounds=350)
    player.sequence = [4]
    return player


@pytest.fixture
def playercancellation_regular():
    return roulette.player.PlayerCancellation(stake=100, rounds=350)


def test_playing_no_rounds_left(playercancellation_not_playing_because_rounds):
    assert not playercancellation_not_playing_because_rounds.playing


def test_playing_stake_too_small(playercancellation_not_playing_because_stake):
    assert not playercancellation_not_playing_because_stake.playing


def test_playing_not_enough_sequence(playercancellation_not_playing_because_sequence):
    assert not playercancellation_not_playing_because_sequence.playing


def test_bet_amount_win(playercancellation_regular):
    playercancellation_regular.win(playercancellation_regular._determine_bets()[0])
    assert playercancellation_regular.bet_amount == 7


def test_bet_amount_lose(playercancellation_regular):
    playercancellation_regular.lose()
    assert playercancellation_regular.bet_amount == 8
