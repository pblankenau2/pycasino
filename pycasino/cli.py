#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import click
from roulette import model
from roulette import player as player_module
from roulette import wheel_builder


def player_factory(player_name, **kwargs):
    """
    kwargs will contain all the params necessary to initialize the player
    """
    return player_module.REGISTERED_PLAYERS[player_name](**kwargs)


@click.command()
@click.option('--num-games', '-n', default=50, help='Greet as a cowboy.')
@click.option('--player','-p',required=True, type=click.Choice(player_module.REGISTERED_PLAYERS.keys() ,case_sensitive=False))
@click.option('--game', '-g', required=True, type=click.Choice(['roulette'], case_sensitive=False)) #TODO: See if you can make it not run if the args are missing.  Give help  instead?
def main(game, player, num_games):

    if game == 'roulette':
        plyr = player_factory(player_name=player)
        table = model.Table(limit=350)
        wheel = wheel_builder.create_wheel()
        game = model.Game(table=table, wheel=wheel)
        sim = model.Simulator(
            game=game,
            player=plyr
        )
        sim.gather(samples=num_games)
        click.echo(sim.maxima)

    return 0


if __name__ == '__main__':
    main()

