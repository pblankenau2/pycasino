#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from .context import roulette


@pytest.fixture
def player1326_not_playing_because_rounds():
    return roulette.player.Player1326(stake=20, rounds=0, base_bet_amount=5)


@pytest.fixture
def player1326_not_playing_because_stake():
    return roulette.player.Player1326(stake=10, rounds=350, base_bet_amount=10)


@pytest.fixture
def player1326_regular():
    return roulette.player.Player1326(stake=100, rounds=350, base_bet_amount=10)


def test_playing_no_rounds_left(player1326_not_playing_because_rounds):
    assert not player1326_not_playing_because_rounds.playing


def test_playing_stake_too_small(player1326_not_playing_because_stake):
    assert not player1326_not_playing_because_stake.playing


def test_one_win_determine_bets(player1326_regular):
    player1326_regular.win(player1326_regular._determine_bets()[0])
    assert (
        player1326_regular._determine_bets()[0].amount_bet
        == player1326_regular.base_bet_amount * 3
    )


def test_two_wins_determine_bets(player1326_regular):
    player1326_regular.win(player1326_regular._determine_bets()[0])
    player1326_regular.win(player1326_regular._determine_bets()[0])
    assert (
        player1326_regular._determine_bets()[0].amount_bet
        == player1326_regular.base_bet_amount * 2
    )


def test_three_wins_determine_bets(player1326_regular):
    player1326_regular.win(player1326_regular._determine_bets()[0])
    player1326_regular.win(player1326_regular._determine_bets()[0])
    player1326_regular.win(player1326_regular._determine_bets()[0])
    assert (
        player1326_regular._determine_bets()[0].amount_bet
        == player1326_regular.base_bet_amount * 6
    )


def test_four_wins_determine_bets(player1326_regular):
    player1326_regular.win(player1326_regular._determine_bets()[0])
    player1326_regular.win(player1326_regular._determine_bets()[0])
    player1326_regular.win(player1326_regular._determine_bets()[0])
    player1326_regular.win(player1326_regular._determine_bets()[0])
    assert (
        player1326_regular._determine_bets()[0].amount_bet
        == player1326_regular.base_bet_amount
    )


def test_one_loss_determine_bets(player1326_regular):
    player1326_regular.lose()
    assert (
        player1326_regular._determine_bets()[0].amount_bet
        == player1326_regular.base_bet_amount
    )

