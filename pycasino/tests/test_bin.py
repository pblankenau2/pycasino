#!/usr/bin/env python

import pytest
from .context import roulette

@pytest.fixture
def bin1():
    outcome1 = roulette.model.Outcome('Red', 1)
    outcome2 = roulette.model.Outcome('Red', 1)
    bin_ = roulette.model.Bin()
    bin_.add(outcome1)
    bin_.add(outcome2)
    return bin_

@pytest.fixture
def bin2():
    outcome1 = roulette.model.Outcome('Red', 1)
    bin_ = roulette.model.Bin()
    bin_.add(outcome1)
    return bin_

def test_bin_for_duplicates(bin1, bin2):
    assert bin1.outcomes == bin2.outcomes

def test_bin_add(bin2):
    bin3 = bin2.add(roulette.model.Outcome('Black', 1))
    bin_to_match = roulette.model.Bin()
    bin_to_match\
        .add(roulette.model.Outcome('Red', 1))\
        .add(roulette.model.Outcome('Black', 1))

    assert bin3.outcomes == bin_to_match.outcomes
