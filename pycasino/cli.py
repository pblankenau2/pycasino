#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import click
import yaml
import click_config_file
from .roulette import model
from .roulette import player
from .roulette import wheel_builder


def player_factory(player_name, **kwargs):
    """
    kwargs will contain all the params necessary to initialize the player
    """
    return player.REGISTERED_PLAYERS[player_name](**kwargs)


def read_config(filepath, cmd_name):
    with open(filepath) as config_data:
        return yaml.safe_load(config_data)[cmd_name]


@click.group()
def main():
    """Collects statistics about the outcomes of using particular betting
    strategies in different games.  This is not a simulation where you play
    the game yourself.  Instead, you select your game, a player that
    will play with a certain betting strategy and the number of game sessions
    that player should play.  A players session is limited by his/her stake
    and a maximum number of rounds to play.  These can be modified in a 
    configuration file.
    
    """
    pass


@main.command()
@click.option(
    "--num-games",
    "-n",
    default=50,
    show_default=True,
    help="The number of games to play.",
)
@click.option(
    "--stake", "-s", default=100.0, show_default=True, help="The players initial funds."
)
@click.option(
    "--max-rounds",
    default=20,
    show_default=True,
    help="The maximum # of rounds per game.",
)
@click.option(
    "--base-bet-amount",
    default=20.0,
    show_default=True,
    help="The initial bet amount (strategies modify following bets amounts).",
)
@click.option(
    "--table-limit",
    default=350.0,
    show_default=True,
    help="The maximum amount a bet can be.",
)
@click_config_file.configuration_option(provider=read_config, implicit=False)
@click.argument(
    "player",
    type=click.Choice(player.REGISTERED_PLAYERS.keys(), case_sensitive=False),
    nargs=1,
)
def roulette(player, stake, base_bet_amount, max_rounds, table_limit, num_games):

    player_args = {
        "stake": stake,
        "base_bet_amount": base_bet_amount,
        "rounds": max_rounds,
    }

    game = model.Game(
        table=model.Table(table_limit), wheel=wheel_builder.create_wheel()
    )
    sim = model.Simulator(
        game=game, player=player_factory(player_name=player, **player_args)
    )
    sim.gather(num_games)

    click.echo("maximum_stake, rounds_played")
    for i in zip(sim.maxima, sim.durations):
        click.echo(f"{i[0]}, {i[1]}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

