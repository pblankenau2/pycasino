#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from mock import Mock, MagicMock
from .context import roulette


@pytest.fixture
def mock_player():
    player = Mock(spec=roulette.player.PlayerPassenger57)
    player.rounds = 10
    return player


@pytest.fixture
def mock_wheel():
    wheel = Mock(spec=roulette.model.Wheel)
    bin_ = Mock(spec=roulette.model.Bin)
    bin_.outcomes = frozenset([roulette.bin_builder.get_outcome('Black')])
    wheel.spin.return_value = bin_
    return wheel


@pytest.fixture
def mock_table():
    table = MagicMock(spec=roulette.model.Table)
    bet = Mock(spec=roulette.model.Bet)
    bet.outcome = roulette.bin_builder.get_outcome('Black')
    table.bets = [bet]
    table.__iter__.return_value = table.bets
    return table


def test_game_cycle(
        mock_player,
        mock_table,
        mock_wheel):
    """Tests that the game's cycle method works.

    Using all the mocks is probably not the best way to test
    the Game class.  Integration tests would likely be best,
    but I wanted to play with mocking.

    """

    game = roulette.model.Game(mock_table, mock_wheel)
    game.cycle(mock_player)

    mock_player.place_bets.assert_called_with()
    mock_table.is_valid.assert_called_with()
    mock_wheel.spin.assert_called_with()
    mock_player.win.assert_called_with(mock_table.bets[0])
    mock_table.clear_bets.assert_called_with()
    assert mock_player.rounds == 9
