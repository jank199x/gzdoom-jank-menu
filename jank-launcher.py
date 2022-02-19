#!/usr/bin/env python3

import configparser
import os

import click

import gzjank_utils as util

DEFAULTS_CONFIG = "jank-launcher.ini"


@click.command()
@click.argument("configfile", type=click.Path(exists=True, dir_okay=False))
def launch(configfile):
    """
    \b
    Runs a WAD specified in CONFIGFILE via gzdoom
    """
    cwd=os.getcwd()
    config = configparser.ConfigParser()
    config.read(f"{cwd}/{DEFAULTS_CONFIG}")
    config.read(configfile)

    launch_string = util.makelaunchstring(
        cwd=cwd,
        configfile=config,
    )

    os.system(launch_string)


if __name__ == "__main__":
    launch()
