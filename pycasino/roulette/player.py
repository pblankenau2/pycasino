#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import abc
import random
import inspect
from . import model
from . import wheel_builder


def delegates(to=None, keep=False):
    """Decorator: replace `**kwargs` in signature with params from `to`
    
    Taken from the fast.ai blog post by Jeremy Howard dated 06 Aug 2019.
    
    """
    def _f(f):
        if to is None: to_f,from_f = f.__base__.__init__,f.__init__
        else:          to_f,from_f = to,f
        sig = inspect.signature(from_f)
        sigd = dict(sig.parameters)
        k = sigd.pop('kwargs')
        s2 = {k:v for k,v in inspect.signature(to_f).parameters.items()
              if v.default != inspect.Parameter.empty and k not in sigd}
        sigd.update(s2)
        if keep: sigd['kwargs'] = k
        from_f.__signature__ = sig.replace(parameters=sigd.values())
        return f
    return _f


class Player(abc.ABC):
    """Abstract base class for players.

    :param table: A table to play on.
    :type table: Table
    :param stake: An intial pool of money to bet with.
    :type stake: float
    :param rounds: Number of spins of the wheel to stay at the table.
    :type rounds: int

    """

    def __init__(self, stake=100.0, base_bet_amount=10.0, rounds=250):
        self.stake = float(stake)
        self.base_bet_amount = float(base_bet_amount)
        self.rounds = rounds
        self._winners = list()

    def _post_init(self, **kwargs):
        """This is a hook into the superclass init method.
        
        This is a technique to avoid undue coupling between
        a parent and child class.  It lets you subclass without
        worrying about overriding __init__, and calling super
        with the correct args. It only works with a single
        level of inheritence.
        """
        pass

    @property
    def bet_amount(self):
        return self.base_bet_amount

    @property
    def playing(self):
        """Returns True while player is still playing."""
        if self.stake <= self.bet_amount:
            return False
        elif self.rounds <= 0:
            return False
        else:
            return True

    @abc.abstractmethod
    def _determine_bets(self):
        """Return the next bets.

        :returns: List of bets.
        :rtype: list
        """
        pass

    def place_bets(self, table):
        """Update the table with bets."""
        bets = list(self._determine_bets())
        for bet in bets:
            table.place_bet(bet)
            self.stake -= bet.lose_amount

    def track_last_winning_outcomes(self, outcomes):
        [self._winners.append(outcome) for outcome in outcomes]

    def win_hook(self):
        pass

    def win(self, bet):
        """Performs tasks when a bet is won."""
        self.rounds -= 1
        self.stake += bet.win_amount
        self.win_hook()

    def lose_hook(self):
        pass

    def lose(self):
        """Performs tasks when a bet is lost."""
        self.rounds -= 1
        self.lose_hook()

# TODO: should this be a fixture in a testing module?
@delegates()
class PlayerDouble(Player):
    """This is a simple subclass of Player.
    
    A player that only bets on black. This
    class allows for the testing of the
    baseclass methods.

    :param table: A table to play on.
    :type table: Table
    :param stake: An intial pool of money to bet with.
    :type stake: float

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.black = wheel_builder.get_outcome('Black')

    def _determine_bets(self):
        return [model.Bet(self.base_bet_amount, self.black)]


@delegates()
class PlayerMartingale(Player):
    """A player class using the Martingale betting strategy.

    The player doubles their bet on every loss
    and resets their bet to a base amount on each win.

    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loss_count = 0

    # TODO: should we bet the remaining stake if the stake is under the strategy bet amount?
    @property
    def bet_amount(self):
        return self.base_bet_amount * (2.0 ** self.loss_count) # TODO: make sure bet_amount is less than table maximum?

    def _determine_bets(self):
        outcome = wheel_builder.get_outcome('Black')
        bet = [model.Bet(self.bet_amount, outcome)]
        return bet

    def win_hook(self):
        self.loss_count = 0

    def lose_hook(self):
        self.loss_count += 1


@delegates()
class PlayerSevenReds(PlayerMartingale):
    """SevenReds is a Martingale player who places bets in Roulette.

    This player waits until the wheel has spun red seven
    times in a row before betting black.  The behavior thereafter is
    the same as the Martingale stategy.  I am not sure if, after a loss,
    the betting should be suspended until seven reds appear again.  Currently
    after the first time seven reds in a row occur the player essentially
    becomes a PlayerMartingale player.

    :param table: A table to play on.
    :type table: Table
    :param stake: An intial pool of money to bet with.
    :type stake: float
    :param base_bet_amount: An intial amount to bet.
    :type base_bet_amount: float

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._red_count = 7
        self._red = wheel_builder.get_outcome('Red')
        self._black = wheel_builder.get_outcome('Black')

    @property
    def _waiting(self):
        return self._red_count != 0

    def _determine_bets(self):
        if self._waiting:
            if self._red in self._winners:
                self._red_count -= 1
            else:
                self._red_count = 7
            return [model.Bet(0.0, self._black)]  # TODO: It would be nice if the player didn't have to bet every time.
        else:
            bet = [model.Bet(self.bet_amount, self._black)]
            return bet

    def lose_hook(self):
        if self._waiting:
            self.loss_count = 0 # Keeps bets from inflating during wait.
        else:
            self.loss_count += 1


@delegates()
class PlayerRandom(Player):
    """A player who bets on random outcomes.

    :param stake: An intial pool of money to bet with.
    :type stake: float
    :param bet_amount: An amount to bet on each bet.
    :type bet_amount: float

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._random_number_generator = random.Random()
        self._outcomes = list(wheel_builder.create_wheel().all_outcomes.values())

    def _determine_bets(self):
        outcome_index = self._random_number_generator.randrange(0, len(self._outcomes))
        bet = [model.Bet(self.base_bet_amount, self._outcomes[outcome_index])]
        return bet


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


@delegates()
class Player1326(Player):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.outcome = wheel_builder.get_outcome('Black')
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

    def win_hook(self):
        self.state = self.state.next_won()

    def lose_hook(self):
        self.state = self.state.next_lost()


class PlayerCancellation(Player):
    """Player that uses the cancellation betting strategy."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sequence = list(range(1, 7))
        self.outcome = wheel_builder.get_outcome('Black')

    @property
    def playing(self):
        if len(self.sequence) <= 1:
            # This is the first conditional because
            # bet_amount will error if the sequence list
            # is empty.
            return False
        elif self.stake <= self.bet_amount:
            return False
        elif self.rounds <= 0:
            return False
        else:
            return True

    def _determine_bets(self):
        return [model.Bet(self.bet_amount, self.outcome)]

    def win_hook(self):
        self.sequence.pop(0)
        self.sequence.pop(-1)

    def lose_hook(self):
        self.sequence.append(self.bet_amount)

    @property
    def bet_amount(self):
        return self.sequence[-1] + self.sequence[0]


@delegates()
class PlayerFibonacci(PlayerMartingale):
    """Player that uses the Fibonacci betting system.

    After a loss, the player adds the current bet multiplier
    to the previous bet multiplier to get the next bet multiplier.
    After a win the current bet multiplier returns to 1.
    Base bets are multiplied by this multiplier to get the bet
    amount.

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current = 1
        self.previous = 0

    @property
    def bet_amount(self):
        return self.current * self.base_bet_amount

    def win_hook(self):
        self.current = 1
        self.previous = 0

    def lose_hook(self):
        self.current, self.previous = (self.current + self.previous), self.current
