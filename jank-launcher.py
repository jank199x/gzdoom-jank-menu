#!/usr/bin/env python3

import configparser
import os

import click

from gzjank_utils import makelaunchstring

DEFAULTS_CONFIG = "jank-launcher.ini"


@click.command()
@click.argument("configfile", type=click.Path(exists=True, dir_okay=False))
def launch(configfile):
    """
    \b
    Runs a WAD specified in CONFIGFILE via gzdoom
    """
    config = configparser.ConfigParser()
    config.read(DEFAULTS_CONFIG)
    config.read(configfile)

    launch_string = makelaunchstring(
        cwd=os.getcwd(),
        configfile=config,
    )

    os.system(launch_string)


if __name__ == "__main__":
    launch()
