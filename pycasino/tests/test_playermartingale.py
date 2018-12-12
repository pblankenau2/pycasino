#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from .context import roulette


@pytest.fixture
def playermartingale_not_playing_because_rounds():
    table = roulette.model.Table(300)
    return roulette.player.PlayerMartingale(
        table=table,
        stake=20,
        rounds=0,
        base_bet_amount=5
    )


@pytest.fixture
def playermartingale_not_playing_because_stake():
    table = roulette.model.Table(300)
    return roulette.player.PlayerMartingale(
        table=table,
        stake=10,
        rounds=350,
        base_bet_amount=10
    )


@pytest.fixture
def playermartingale_regular():
    table = roulette.model.Table(300)
    return roulette.player.PlayerMartingale(
        table=table,
        stake=100,
        rounds=350,
        base_bet_amount=10
    )


def test_playing_no_rounds_left(playermartingale_not_playing_because_rounds):
    assert (not playermartingale_not_playing_because_rounds.playing)


def test_playing_stake_too_small(playermartingale_not_playing_because_stake):
    assert (not playermartingale_not_playing_because_stake.playing)


def test__determine_bets(playermartingale_regular):
    player_bet = playermartingale_regular._determine_bets()[0]
    assert player_bet.amount_bet == 10
    assert player_bet.outcome == roulette.bin_builder.get_outcome('Black')


def test_bet_amount_on_win(playermartingale_regular):
    playermartingale_regular.win(playermartingale_regular._determine_bets()[0])
    assert playermartingale_regular.bet_amount == 10
    playermartingale_regular.win(playermartingale_regular._determine_bets()[0])
    assert playermartingale_regular.bet_amount == 10


def test_bet_amount_on_loss(playermartingale_regular):
    playermartingale_regular.lose()
    assert playermartingale_regular.bet_amount == 20
    playermartingale_regular.lose()
    assert playermartingale_regular.bet_amount == 40


def test_win(playermartingale_regular):
    playermartingale_regular.place_bets()
    playermartingale_regular.win(playermartingale_regular._determine_bets()[0])
    assert playermartingale_regular.stake == 110


def test_lose(playermartingale_regular):
    playermartingale_regular.lose()
    assert playermartingale_regular.loss_count == 1
