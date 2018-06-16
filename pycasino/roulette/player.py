#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import abc
import random
from . import model
from . import bin_builder


class Player(abc.ABC):
    """Abstract base class for players.

    :param table: A table to play on.
    :type table: Table
    :param stake: An intial pool of money to bet with.
    :type stake: float
    :param rounds: Number of spins of the wheel to stay at the table.
    :type rounds: int

    """

    def __init__(self, table, stake=100, rounds=250):
        self.table = table
        self.stake = float(stake)
        self.rounds = rounds
        self._winners = list()

    @abc.abstractproperty
    def playing(self):
        """Returns True while player is still playing."""

    @abc.abstractmethod
    def _determine_bets(self):
        """Return the next bets.

        :returns: List of bets.
        :rtype: list
        """

    def place_bets(self):
        """Update the table with bets."""
        bets = list(self._determine_bets())
        for bet in bets:
            self.table.place_bet(bet)
            self.stake -= bet.lose_amount

    @abc.abstractmethod
    def win(self, bet):
        """Performs tasks when a bet is won."""

    @abc.abstractmethod
    def lose(self):
        """Performs tasks when a bet is lost."""


class PlayerPassenger57(Player):
    """A player that only bets on black.

    :param table: A table to play on.
    :type table: Table
    :param stake: An intial pool of money to bet with.
    :type stake: float
    :param bet_amount: An amount to place on each bet.
    :type bet_amount: float

    """
    def __init__(self, table, stake, rounds, bet_amount):
        super().__init__(table, stake, rounds)
        # TODO: We have to create a wheel to get our outcome mapping.  Very clumsy.
        self.wheel = bin_builder.create_wheel()
        self.black = self.wheel.get_outcome('Black')
        self.bet_amount = bet_amount

    @property
    def playing(self):
        if self.stake <= self.bet_amount:
            return False
        elif self.rounds <= 0:
            return False
        else:
            return True

    def _determine_bets(self):
        return model.Bet(self.bet_amount, self.black)

    def win(self, bet):
        self.stake += bet.win_amount

    def lose(self):
        pass


class PlayerMartingale(Player):
    """A player class using the Martingale betting strategy.

    The player doubles their bet on every loss
    and resets their bet to a base amount on each win.

    """

    def __init__(self, table, stake, rounds, base_bet_amount):
        super().__init__(table, stake, rounds)
        self.loss_count = 0
        self.wheel = bin_builder.create_wheel()
        self.base_bet_amount = base_bet_amount

    # TODO: should we bet the remaining stake if the stake is under the strategy bet amount?
    @property
    def bet_amount(self):
        return self.base_bet_amount * (2.0 ** self.loss_count)

    @property
    def playing(self):
        if self.stake <= self.bet_amount:
            return False
        elif self.rounds <= 0:
            return False
        else:
            return True

    def _determine_bets(self):
        outcome = self.wheel.get_outcome('Black')
        bet = [model.Bet(self.bet_amount, outcome)]
        return bet

    def win(self, bet):
        self.stake += bet.win_amount
        self.loss_count = 0

    def lose(self):
        self.loss_count += 1


class PlayerSevenReds(Martingale):
    """SevenReds is a Martingale player who places bets in Roulette.

    This player waits until the wheel has spun red seven
    times in a row before betting black.

    """

    def __init__(self, table, stake, rounds, base_bet_amount):
        super().__init__(table, stake, rounds, base_bet_amount)
        self._red_count = 7
        self._wheel = bin_builder.create_wheel()
        self._red = self.wheel.get_outcome('Red')
        self._black = self.wheel.get_outcome('Black')
        self._waiting = True

    def _determine_bets(self):
        if self._waiting:
            if self._red in self._winners:
                self._red_count -= 1
            elif self._black in self._winners:
                self._red_count = 7
            if self._red_count == 0:
                self._waiting = False
        else:
            bet = [model.Bet(self.bet_amount, self._black)]
        return bet


class PlayerRandom(Player):
    """A player who bets on random outcomes.

    :param table: A table to play on.
    :type table: Table
    :param stake: An intial pool of money to bet with.
    :type stake: float
    :param bet_amount: An amount to bet on each bet.
    :type bet_amount: float

    """

    def __init__(self, table, stake, rounds, bet_amount):
        super().__init__(table, stake, rounds)
        self.bet_amount = bet_amount
        self._random_number_generator = random.Random()
        self._outcomes = list(bin_builder.create_wheel().all_outcomes.values())

    @property
    def playing(self):
        if self.stake <= self.bet_amount:
            return False
        elif self.rounds <= 0:
            return False
        else:
            return True

    def _determine_bets(self):
        outcome_index = self._random_number_generator.randrange(0, len(self._outcomes))
        bet = [model.Bet(self.bet_amount, self._outcomes[outcome_index])]
        return bet

    def win(self, bet):
        self.stake += bet.win_amount

    def lose(self):
        pass # Though we often pass, this method is useful to have in the interface.


class Player1326StateAlternate:
    """Alternative player 1326 state class.

    This class provides alternative constructors for itself
    each representing a betting state.  The class
    instances keep track of which instance to
    instantiate next for the state change. This solution
    might be overly elaborate.

    """

    def __init__(self, player, bet_multiplier, next_win):
        self.player = player
        self.bet_multiplier = bet_multiplier
        self.next_win = next_win

    @property
    def current_bet(self):
        return model.Bet(
            self.player.base_bet_amount * self.bet_multiplier,
            self.player.outcome
            )

    def next_won(self):
        return self.next_win(self.player)

    def next_lost(self):
        return self._no_wins(self.player)

    @classmethod
    def _no_wins(cls, player):
        """Returns a class instance for the one win state."""
        return cls(player, 1, cls._one_wins)

    @classmethod
    def _one_wins(cls, player):
        """Returns a class instance for the two win state."""
        return cls(player, 3, cls._two_wins)

    @classmethod
    def _two_wins(cls, player):
        """Returns a class instance for the three win state."""
        return cls(player, 2, cls._three_wins)

    @classmethod
    def _three_wins(cls, player):
        """Returns a class instance for the no win state."""
        return cls(player, 6, cls._no_wins)


class Player1326State(abc.ABC):
    """Abstract base class for the player 1326 states.

    This is overengineered but demonstrates the state design pattern.

    """

    def __init__(self, player):
        self.player = player

    @abc.abstractproperty
    def current_bet(self):
        """Constructs a new Bet from the player’s preferred Outcome."""

    @abc.abstractmethod
    def next_won(self):
        """Constructs the new Player1326State instance when bet was a winner."""

    # This remains constant for all state subclasses.
    def next_lost(self):
        """Constructs the new Player1326State instance when bet was a loser."""
        return Player1326NoWins(self.player)


class Player1326NoWins(Player1326State):

    @property
    def current_bet(self):
        return model.Bet(self.player.base_bet_amount * 1, self.player.outcome)

    def next_won(self):
        return Player1326OneWins(self.player)


class Player1326OneWins(Player1326State):

    @property
    def current_bet(self):
        return model.Bet(self.player.base_bet_amount * 3, self.player.outcome)

    def next_won(self):
        return Player1326TwoWins(self.player)


class Player1326TwoWins(Player1326State):

    @property
    def current_bet(self):
        return model.Bet(self.player.base_bet_amount * 2, self.player.outcome)

    def next_won(self):
        return Player1326ThreeWins(self.player)


class Player1326ThreeWins(Player1326State):

    @property
    def current_bet(self):
        return model.Bet(self.player.base_bet_amount * 6, self.player.outcome)

    def next_won(self):
        return Player1326NoWins(self.player)


class Player1326(Player):

    def __init__(self, table, stake, rounds, base_bet_amount):
        super().__init__(table, stake, rounds)
        self.base_bet_amount = base_bet_amount
        self.outcome = bin_builder.create_wheel().get_outcome('Black')
        self.state = Player1326StateAlternate._no_wins(self)

    @property
    def playing(self):
        """Returns True while player is still playing."""
        if self.stake <= self.state.current_bet.amount_bet:
            return False
        elif self.rounds <= 0:
            return False
        else:
            return True

    def _determine_bets(self):
        return [self.state.current_bet]

    def win(self, bet):
        self.stake += bet.win_amount
        self.state = self.state.next_won()

    def lose(self):
        self.state = self.state.next_lost()


class PlayerCancellation(Player):

    def __init__(self, table, stake, rounds):
        super().__init__(table, stake, rounds)
        self.sequence = self.reset_sequence()
        self.outcome = bin_builder.create_wheel().get_outcome('Black')

    @property
    def playing(self):
        if self.stake <= self.bet_amount:
            return False
        elif self.rounds <= 0:
            return False
        else:
            return True

    def _determine_bets(self):
        return [model.Bet(self.bet_amount, self.outcome)]

    def win(self, bet):
        self.stake += bet.win_amount
        self.sequence.pop(0)
        self.sequence.pop(-1)

    def lose(self):
        self.sequence.append(self.bet_amount)

    def reset_sequence(self):
        self.sequence = range(1, 7)

    @property
    def bet_amount(self):
        return self.sequence[-1] + self.sequence[0]


class PlayerFibonacci(PlayerMartingale):
    """Player that uses the Fibonacci betting system.

    After a loss, the player adds the current bet multiplier
    to the previous bet multiplier to get the next bet multiplier.
    After a win the current bet multiplier returns to 1.
    Base bets are multiplied by this multiplier to get the bet
    amount.

    """

    def __init__(self, table, stake, rounds, base_bet_amount):
        super().__init__(table, stake, rounds, base_bet_amount)
        self.base_bet_amount
        self.current = 1
        self.previous = 0

    @property
    def bet_amount(self):
        return self.current * self.base_bet_amount

    def win(self, bet):
        self.stake += bet.win_amount
        self.current = 1
        self.previous = 0

    def lose(self, bet):
        self.current, self.previous = (self.current + self.previous), self.current
