#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A set of functions used to add bins to the wheel."""
from . import model
from .model import Outcome


def create_wheel():
    """Populate the bins in wheel with outcomes."""
    wheel = model.Wheel()
    add_straight_bets(wheel)
    add_split_bets(wheel)
    add_column_bets(wheel)
    add_corner_bets(wheel)
    add_dozen_bets(wheel)
    add_line_bets(wheel)
    add_street_bets(wheel)
    add_even_money_bets(wheel)
    add_five_bets(wheel)
    return wheel


def add_five_bets(wheel):
    """Add five bet outcomes to the wheel."""
    wheel.add_outcome(0, Outcome('Five 00-0-1-2-3', 6))
    wheel.add_outcome(37, Outcome('Five 00-0-1-2-3', 6))


def add_straight_bets(wheel):
    """Generate straight bet outcomes and add them to the wheel."""
    for number in range(0, 36):
        outcome = Outcome('Straight {}'.format(number), 35)
        wheel.add_outcome(number, outcome)

    wheel.add_outcome(37, Outcome('Straight 00', 35))


def add_split_bets(wheel):
    """Add split bet outcomes to the wheel."""
    for row in range(0, 11):
        for col in range(1, 3):
            first_col_num = 3 * row + col
            outcome = Outcome('Split {}, {}'.format(first_col_num, first_col_num + 1), 17)
            wheel.add_outcome(first_col_num, outcome)
            wheel.add_outcome(first_col_num + 1, outcome)

    for col in range(1, 4):
        for row in range(0, 11):
            first_row_num = 3 * row + col
            outcome = Outcome('Split {}, {}'.format(first_row_num, first_row_num + 3), 17)
            wheel.add_outcome(first_row_num, outcome)
            wheel.add_outcome(first_row_num + 3, outcome)


def add_street_bets(wheel):
    """Add street bet outcomes to the wheel."""
    for row in range(0, 12):
        first_col_num = 3 * row + 1
        outcome = Outcome(
            'Street {}, {}, {}'.format(
                first_col_num,
                first_col_num + 1,
                first_col_num + 2
                ),
            11
            )
        wheel.add_outcome(first_col_num, outcome)
        wheel.add_outcome(first_col_num + 1, outcome)
        wheel.add_outcome(first_col_num + 2, outcome)


def add_corner_bets(wheel):
    """Add corner bet outcomes to the wheel."""
    for row in range(0, 11):
        for col in range(1, 3):
            first_col_num = 3 * row + col
            outcome = Outcome(
                'Corner {}, {}, {}, {}'.format(
                    first_col_num,
                    first_col_num + 1,
                    first_col_num + 3,
                    first_col_num + 4,
                    ),
                8
                )
            wheel.add_outcome(first_col_num, outcome)
            wheel.add_outcome(first_col_num + 1, outcome)
            wheel.add_outcome(first_col_num + 3, outcome)
            wheel.add_outcome(first_col_num + 4, outcome)


def add_line_bets(wheel):
    """Add line bet outcomes to the wheel."""
    for row in range(0, 11):
        first_col_num = 3 * row + 1
        outcome = Outcome(
            'Line {}, {}, {}, {}, {}, {}'.format(
                first_col_num,
                first_col_num + 1,
                first_col_num + 2,
                first_col_num + 3,
                first_col_num + 4,
                first_col_num + 5,
                ),
            5
            )
        wheel.add_outcome(first_col_num, outcome)
        wheel.add_outcome(first_col_num + 1, outcome)
        wheel.add_outcome(first_col_num + 2, outcome)
        wheel.add_outcome(first_col_num + 3, outcome)
        wheel.add_outcome(first_col_num + 4, outcome)
        wheel.add_outcome(first_col_num + 5, outcome)


def add_dozen_bets(wheel):
    """Add dozen bet outcomes to the wheel."""
    name_mapping = {0: 'First', 1: 'Second', 2: 'Third'}

    for dozen in range(0, 3):
        outcome = Outcome('{} 12'.format(name_mapping.get(dozen)), 2)
        for num in range(0, 12):
            wheel.add_outcome(12 * dozen + num + 1, outcome)


def add_column_bets(wheel):
    """Add column bet outcomes to the wheel."""
    for column in range(0, 3):
        outcome = Outcome('Column {}'.format(column + 1), 2)
        for row in range(0, 12):
            wheel.add_outcome(3 * row + column + 1, outcome)


def add_even_money_bets(wheel):
    """Add even-money bet outcomes to the wheel."""
    red_outcome = Outcome('Red', 1)
    black_outcome = Outcome('Black', 1)
    even_outcome = Outcome('Even', 1)
    odd_outcome = Outcome('Odd', 1)
    high_outcome = Outcome('High', 1)
    low_outcome = Outcome('Low', 1)

    for num in range(1, 37):
        if ((num >= 1) and (num < 19)):
            wheel.add_outcome(num, low_outcome)
        else:
            wheel.add_outcome(num, high_outcome)
        if num % 2 == 0:
            wheel.add_outcome(num, even_outcome)
        else:
            wheel.add_outcome(num, odd_outcome)
        if num in {1, 3, 5, 7, 9,
                   12, 14, 16, 18,
                   19, 21, 23, 25,
                   27, 30, 32, 34,
                   36}:
            wheel.add_outcome(num, red_outcome)
        else:
            wheel.add_outcome(num, black_outcome)
