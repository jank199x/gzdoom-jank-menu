import configparser
import os

import questionary

import gzjank_utils as util

DEFAULTS_CONFIG = "jank-launcher.ini"


def launch():
    cwd = os.getcwd()

    config = configparser.ConfigParser()
    config.read(f"{cwd}/{DEFAULTS_CONFIG}")

    launcherdir = f"{cwd}/{config['dirnames']['launchers']}"
    launchermap = util.launchermap(launcherdir)
    choices = sorted(launchermap.keys())

    selection = questionary.select(
        "Which Doom WAD?",
        choices=choices,
    ).ask()

    config.read(launchermap[selection])
    launch_string = util.makelaunchstring(
        cwd=os.getcwd(),
        configfile=config,
    )

    os.system(launch_string)


if __name__ == "__main__":
    launch()
