#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import click
from .roulette import model
from .roulette import player
from .roulette import wheel_builder


def player_factory(player_name, **kwargs):
    """
    kwargs will contain all the params necessary to initialize the player
    """
    return player.REGISTERED_PLAYERS[player_name](**kwargs)


@click.command()
@click.option("--num-games", "-n", default=50, help="The number of games to play.")
@click.option(
    "--player",
    "-p",
    required=True,
    type=click.Choice(player.REGISTERED_PLAYERS.keys(), case_sensitive=False),
    help="A player will play a game with a particular betting strategy.",
)
@click.option(
    "--game",
    "-g",
    required=True,
    type=click.Choice(["roulette"], case_sensitive=False),
    help="The casino game you want to play.",
)  # TODO: See if you can make it not run if the args are missing.  Give help  instead?
def main(game, player, num_games):
    """Collects statistics about the outcomes of using particular betting
    strategies in different games.  This is not a simulation where you play
    the game yourself.  Instead, you select your game, a player that
    will play with a certain betting strategy and the number of game sessions
    that player should play.  A players session is limited by his/her stake
    and a maximum number of rounds to play.  These can be modified in a 
    configuration file.
    
    """
    # TODO: Make player etc. configurable in a config file.

    if game == "roulette":  # TODO: Make roulette a subcommand not an option
        game = model.Game(
            table=model.Table(limit=350), wheel=wheel_builder.create_wheel()
        )
        sim = model.Simulator(game=game, player=player_factory(player_name=player))
        sim.gather(samples=num_games)
        for i in sim.maxima:
            click.echo(i)

    return 0


if __name__ == "__main__":
    sys.exit(main())

