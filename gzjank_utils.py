import configparser


def makelaunchstring(cwd: str, defaults: str, configfile: str):
    config = configparser.ConfigParser()

    config.read(defaults)

    default_addons = config["default"]["addons"]
    default_zdoom_configfile = config["default"]["config"]

    config.read(configfile)

    game_name = config["zdoom"]["name"]
    game_iwad = config["zdoom"]["iwad"]
    game_pwad = config["zdoom"].get("pwad")  # pwad(s) are optional
    addons = config["zdoom"].get("addons")  # addons are optional
    zdoom_configfile = config["zdoom"].get("config")

    addons = default_addons if addons == "default" else addons
    zdoom_configfile = default_zdoom_configfile if not zdoom_configfile else zdoom_configfile

    iwad_path = f"{cwd}/{config['dirnames']['iwads']}/{game_iwad}"
    save_path = f"{cwd}/{config['dirnames']['savefiles']}/{game_name}"
    config_path = f"{cwd}/{config['dirnames']['configfiles']}/{zdoom_configfile}"
    pwad_path = [f"{cwd}/{config['dirnames']['pwads']}/{pwad}" for pwad in game_pwad.split()] if game_pwad else None
    addon_paths = [f"{cwd}/{config['dirnames']['addons']}/{addon}" for addon in addons.split()] if addons else None

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