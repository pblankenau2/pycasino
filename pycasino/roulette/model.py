# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A collection of classes to represent the game of roulette.

This code was inspired by the book Building Skills in Object-Oriented Design
by Steven Lott.

"""
import random
import copy


# TODO: consider using a dataclass instead (python 3.7 only)
class Outcome:
    """Represents an outcome of a spin of a wheel in roulette.

    :param name: The name of the outcome, e.g. "Red", "1".
    :param odds: The odds of the outcome.

    """

    def __init__(self, name, odds):
        self.name = name
        self.odds = odds

    def win_amount(self, amount):
        """Calculate the amount of money won.

        :param amount: The amount of money bet.
        :type amount: float
        :return: The amount of money won.
        :rtype: float
        """
        return amount * self.odds

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __hash__(self):
        """Make hash of name default for placing object in sets and dicts."""
        # TODO: Hashable objects are supposed to be immutable!
        return hash(self.name)

    def __str__(self):
        return f"{self.name} ({self.odds}:1)"

    def __repr__(self):
        return self.__class__.__qualname__ + f"({self.name!r}, {self.odds!r})"


class Bin:
    """Represents a bin on a roulette wheel. A collection of :class:`Outcome`."""

    def __init__(self):
        self.outcomes = frozenset()

    def add(self, outcome):
        """Add an outcome to the outcomes."""
        self.outcomes = self.outcomes.union({outcome})
        return self

    def __repr__(self):
        return self.__class__.__qualname__ + f"({self.outcomes!r})"


class _Wheel:
    """Represents a roulette wheel.  Contains :class:`Bin`s."""

    def __init__(self):
        self.bins = tuple(Bin() for i in range(38))
        self.random_num_gen = random.Random()
        # TODO: The books says this is where all_outcomes should be.
        # But we need a populated instance of Wheel to use the attribute
        # Which is clumsy.
        self.all_outcomes = dict()

    def __getitem__(self, index):
        return self.bins[index]

    def add_outcome(self, bin_number, outcome):
        """Add an outcome to the bin with the bin_number index."""
        self.bins[bin_number].add(outcome)
        self.all_outcomes[outcome.name] = outcome

    def spin(self):
        """Return a randomly selected Bin."""
        # Note: Steven Lott named this 'next' but that is for another purpose.
        return self.random_num_gen.choice(self.bins)

    def __repr__(self):
        return self.__class__.__qualname__ + "()"


class Bet:
    """Contains an amount bet and the :class:`Outcome` bet upon.

    :param amount: The amount of money to bet.
    :type amount: Float.
    :param outcome: The outcome to bet upon.
    :type outcome: Outcome.

    """

    def __init__(self, amount, outcome):
        self.amount_bet = float(amount)
        self.outcome = outcome

    @property
    def win_amount(self):
        """Amount player can win on the bet."""
        return self.amount_bet + self.outcome.win_amount(self.amount_bet)

    @property
    def lose_amount(self):
        """Amount player can lose on the bet."""
        return self.amount_bet

    def __str__(self):
        return "{:.2f} on {}".format(self.amount_bet, self.outcome)

    def __repr__(self):
        return (
            self.__class__.__qualname__ + f"({self.amount_bet:.2f}, {self.outcome!r})"
        )


class Table:
    """Contains all the bets created by the player.

    :param limit: The maximum permitted total bet on the table.
    :type limit: float
    :param bets: Bets to place on the table.
    :type bets: list

    """

    def __init__(self, limit, bets=None):
        self.limit = limit
        if bets:
            self.bets = bets
        else:
            self.bets = list()

    def place_bet(self, bet):
        """Add this bet to the list of working bets.

        :param bet: A bet to place.
        :type bet: Bet

        """
        self.bets.append(bet)

    def is_valid(self):
        """Check the bets on the table.

        Individual bets must be larger than the table minimum.
        The total off all bets on the table must not surpass the table limit.

        """
        if sum([bet.amount_bet for bet in self.bets]) > self.limit:
            raise InvalidBet("The sum of the bets is above the table maximum.")

    def clear_bets(self):
        """Clear bets off of the table."""
        self.bets = list()

    def __iter__(self):
        """Provide iterator functionality."""
        for bet in self.bets[:]:
            yield bet

    def __str__(self):
        return str(self.bets)

    def __repr__(self):
        return self.__class__.__qualname__ + f"({self.limit:.2f}, {self.bets!r})"


class Game:
    """Run the game of roulette.

    :param table: The :class:`Table` you want to play on.
    :type table: Table
    :param wheel: The :class:`Wheel` you want to play on.

    """

    def __init__(self, table, wheel):
        self.table = table
        self.wheel = wheel

    def cycle(self, player):
        """Execute a single cycle of play with a given :class:`Player`."""
        if player.playing:
            player.place_bets(self.table)
            self.table.is_valid()  # TODO: Won't this raise an unhandled exception?
            winning_bin = self.wheel.spin()
            for bet in self.table:
                if bet.outcome in winning_bin.outcomes:
                    player.win(bet)
                else:
                    player.lose()
            self.table.clear_bets()
            player.track_last_winning_outcomes(
                winning_bin.outcomes
            )  # TODO: Is there a better way?
        self.table.clear_bets()

    def __repr__(self):
        return self.__class__.__qualname__ + f"({self.table!r}, {self.wheel!r})"


class Simulator:
    """Collects roulette simulation statistics.

    :param game: An instance of :class:`Game`.
    :type game: Game
    :param player: An instance of :class:`Player`.
    :type player: Player

    """

    # TODO: Maybe we need a player factory.  Then maybe we wouldn't need to pass in a fully initialized player.
    # We could instead pass in the class of the player or it's name and a configuration and the player would be created.
    def __init__(self, game, player):

        self.game = game
        # This player will be used to produce fresh players
        self._original_player = copy.deepcopy(player)
        self.player = player
        self.durations = list()
        self.maxima = list()

    def _recreate_player(self):
        """Create a duplicate of the original player."""
        plr_copy = copy.deepcopy(self._original_player)
        return plr_copy

    def _session(self):
        """Execute a single game session."""
        self.player = self._recreate_player()
        stake_vals = [self.player.stake]
        while self.player.playing:
            self.game.cycle(self.player)
            stake_vals.append(self.player.stake)
        return stake_vals

    def gather(self, samples):
        """Execute n samples of game sessions."""
        for _ in range(samples):
            stakes = self._session()
            self.maxima.append(max(stakes))
            self.durations.append(
                len(stakes) - 1
            )  # -1 because stakes includes starting stake

    def __repr__(self):
        return self.__class__.__qualname__ + f"({self.game!r}, {self.player!r})"


class InvalidBet(Exception):
    """Raises an exception when there is an invalid bet."""

    # TODO: Should we instead use a built in exception?


# TODO: Write a main application function that writes outputs to sys.stdout
