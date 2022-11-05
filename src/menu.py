#!/usr/bin/env python3

import configparser
import os
import sys
from datetime import datetime
from collections import namedtuple

import questionary

import jank

DEFAULTS_CONFIG = "defaults.ini"
PATHS_CONFIG = "paths.ini"
STATS_FILE = "stats.ini"

Choice = namedtuple("Choice", ["name", "last_played", "play_count"])


def launch():
    cwd = os.getcwd()

    config = configparser.ConfigParser()

    config.read(f"{cwd}/{PATHS_CONFIG}")
    config.read(f"{cwd}/{DEFAULTS_CONFIG}")

    stats = configparser.ConfigParser()
    if os.path.exists(STATS_FILE):
        stats.read(STATS_FILE)

    rootdir = config["paths"]["root"]
    launcherdir = f"{rootdir}/{config['dirnames']['launchers']}"

    launchermap = jank.launchermap(launcherdir)
    choices_names = sorted(launchermap.keys())

    choices_raw = []
    for name in choices_names:
        if name in stats:
            last_played = stats[name]["last_played"]
            play_count = stats[name]["play_count"]
            choices_raw.append(
                Choice(
                    name=name,
                    play_count=play_count,
                    last_played=last_played,
                )
            )
        else:
            choices_raw.append(
                Choice(
                    name=name,
                    play_count="0",
                    last_played="not played",
                )
            )

    choices_raw.sort(key=lambda x: (x.play_count, x.last_played), reverse=True)

    choices = []
    for choice in choices_raw:
        choices.append(f"{choice.name}: {choice.last_played}, {choice.play_count}")

    selection = questionary.select(
        "Which Doom WAD?",
        choices=choices,
    ).ask()

    if not selection:
        sys.exit()

    wad_name = selection.split(":")[0]

    config.read(launchermap[wad_name])
    launch_string = jank.makelaunchstring(
        cwd=rootdir,
        configfile=config,
    )

    if wad_name not in stats:
        stats[wad_name] = {
            "last_played": datetime.now().date().isoformat(),
            "play_count": 1,
        }
    else:
        play_count = stats[wad_name]["play_count"]
        stats[wad_name] = {
            "last_played": datetime.now().date().isoformat(),
            "play_count": int(play_count) + 1,
        }
    with open(STATS_FILE, "w+") as stats_file:
        stats.write(stats_file)

    os.system(launch_string)


if __name__ == "__main__":
    launch()
