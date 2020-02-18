#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import random
from unittest.mock import Mock
from .context import roulette


@pytest.fixture
def wheel1():
    return roulette.model._Wheel()


def test_wheel_add_outcome(wheel1):
    """Test if outcomes can be added to the wheel."""
    outcome = roulette.model.Outcome("Red", 1)
    wheel1.add_outcome(0, outcome)
    assert outcome in wheel1[0].outcomes


def test_wheel_random_bin(wheel1):
    """Tests the wheel's random bin selection."""
    assert wheel1.spin() in wheel1.bins
