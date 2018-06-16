#!/usr/bin/env python

import pytest
import random
from .context import roulette


def test_outcome_win_amount():
    outcome = roulette.model.Outcome('1', 35)
    assert outcome.win_amount(10) == 350

def test_outcome_eq():
    outcome1 = roulette.model.Outcome('Red', 1)
    outcome2 = roulette.model.Outcome('Red', 1)
    assert outcome1 == outcome2

def test_outcome_neq():
    outcome1 = roulette.model.Outcome('Red', 1)
    outcome3 = roulette.model.Outcome('1', 35)
    assert outcome1 != outcome3

def test_outcome_hash_eq():
    outcome1 = roulette.model.Outcome('Red', 1)
    outcome2 = roulette.model.Outcome('Red', 1)
    assert hash(outcome1) == hash(outcome2)
