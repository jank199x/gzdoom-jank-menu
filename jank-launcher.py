#!/usr/bin/env python3

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

    launch_string = makelaunchstring(
        cwd=os.getcwd(),
        defaults=DEFAULTS_CONFIG,
        configfile=configfile,
    )

    os.system(launch_string)


if __name__ == "__main__":
    launch()
