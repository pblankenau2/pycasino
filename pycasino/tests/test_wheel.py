#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import random
from unittest import mock
from .context import roulette


@pytest.fixture
def wheel1():
    return roulette.model.Wheel()


def test_wheel_add_outcome(wheel1):
    """Test if outcomes can be added to the wheel."""
    outcome = roulette.model.Outcome('Red', 1)
    wheel1.add_outcome(0, outcome)
    assert outcome in wheel1[0].outcomes


def test_wheel_random_bin(wheel1):
    """Tests the wheel's random bin selection."""
    wheel1.random_num_gen = mock.Mock()
    wheel1.random_num_gen.choice = mock.Mock(return_value="bin1")
    assert wheel1.spin() == "bin1"