from configparser import ConfigParser
from glob import glob


def launchermap(dir: str):
    launchers = glob(f"{dir}/*.ini")
    prefix = f"{dir}/"
    postfix = ".ini"
    return {launcher[len(prefix) : -len(postfix)]: launcher for launcher in launchers}


def makelaunchstring(cwd: str, configfile: ConfigParser):

    default_addons = configfile["defaults"]["addons"]
    default_zdoom_configfile = configfile["defaults"]["config"]

    game_name = configfile["zdoom"]["name"]
    game_iwad = configfile["zdoom"]["iwad"]
    game_pwad = configfile["zdoom"].get("pwad")  # pwad(s) are optional
    addons = configfile["zdoom"].get("addons")  # addons are optional
    zdoom_configfile = configfile["zdoom"].get("config")

    addons = default_addons if addons == "default" else addons
    zdoom_configfile = default_zdoom_configfile if not zdoom_configfile else zdoom_configfile

    iwad_path = f"{cwd}/{configfile['dirnames']['iwads']}/{game_iwad}"
    save_path = f"{cwd}/{configfile['dirnames']['savefiles']}/{game_name}"
    config_path = f"{cwd}/{configfile['dirnames']['configfiles']}/{zdoom_configfile}"
    pwad_path = [f"{cwd}/{configfile['dirnames']['pwads']}/{pwad}" for pwad in game_pwad.split()] if game_pwad else None
    addon_paths = [f"{cwd}/{configfile['dirnames']['addons']}/{addon}" for addon in addons.split()] if addons else None

    launch_string = "gzdoom"
    launch_string += f" -iwad {iwad_path}"
    launch_string += f" -savedir {save_path}"
    launch_string += f" -config {config_path}"

    if pwad_path:
        pwad_paths_concat = " ".join(pwad_path)
        launch_string += f" -file {pwad_paths_concat}"

    if addon_paths:
        addon_paths_concat = " ".join(addon_paths)
        launch_string += f" -file {addon_paths_concat}"

    return launch_string
