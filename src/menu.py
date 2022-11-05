#!/usr/bin/env python3

import configparser
import os

import questionary

import jank

DEFAULTS_CONFIG = "defaults.ini"
PATHS_CONFIG="paths.ini"


def launch():
    cwd = os.getcwd()

    config = configparser.ConfigParser()

    config.read(f"{cwd}/{PATHS_CONFIG}")
    config.read(f"{cwd}/{DEFAULTS_CONFIG}")

    rootdir = config['paths']['root']
    launcherdir = f"{rootdir}/{config['dirnames']['launchers']}"
    
    launchermap = jank.launchermap(launcherdir)
    choices = sorted(launchermap.keys())

    selection = questionary.select(
        "Which Doom WAD?",
        choices=choices,
    ).ask()

    config.read(launchermap[selection])
    launch_string = jank.makelaunchstring(
        cwd=rootdir,
        configfile=config,
    )

    os.system(launch_string)


if __name__ == "__main__":
    launch()
