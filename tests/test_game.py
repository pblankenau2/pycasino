#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from unittest.mock import Mock, MagicMock, PropertyMock
from .context import roulette


@pytest.fixture
def mock_player():
    return MagicMock()


@pytest.fixture
def mock_wheel():
    # TODO: This is really a stub not a mock?
    wheel = Mock(spec=roulette.model.Wheel)
    bin_ = Mock(spec=roulette.model.Bin)
    # TODO: could you patch outcomes?
    bin_.outcomes = frozenset([roulette.wheel_builder.get_outcome('Black')])
    wheel.spin.return_value = bin_
    return wheel


@pytest.fixture
def mock_table():
    table = MagicMock(spec=roulette.model.Table)
    bet = Mock(spec=roulette.model.Bet)
    bet.outcome = roulette.wheel_builder.get_outcome('Black')
    table.bets = [bet]
    table.__iter__.return_value = table.bets
    return table


def test_game_cycle(
        mock_player,
        mock_table,
        mock_wheel):
    """Tests that the game's cycle method works.

    The focus is testing any outgoing messages that
    change the game state.  It's important that messages
    changing game state are called.

    """

    game = roulette.model.Game(mock_table, mock_wheel)
    game.cycle(mock_player)

    mock_player.place_bets.assert_called_with(mock_table)
    mock_player.win.assert_called_with(mock_table.bets[0])
    mock_player.track_last_winning_outcomes.assert_called_with(mock_wheel.spin().outcomes)
    mock_table.clear_bets.assert_called()

