#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from .context import roulette


@pytest.fixture
def playermartingale_regular():
    return roulette.player.PlayerMartingale(
        stake=100,
        rounds=350,
        base_bet_amount=10
    )


def test__determine_bets(playermartingale_regular):
    player_bet = playermartingale_regular._determine_bets()[0]
    assert player_bet.amount_bet == 10
    assert player_bet.outcome == roulette.wheel_builder.get_outcome('Black')


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
    # Lose
    playermartingale_regular.lose()
    table = roulette.model.Table(300)
    playermartingale_regular.place_bets(table)
    # Win and reset the loss count.
    playermartingale_regular.win(playermartingale_regular._determine_bets()[0])
    assert playermartingale_regular.loss_count == 0


def test_lose(playermartingale_regular):
    playermartingale_regular.lose()
    assert playermartingale_regular.loss_count == 1
