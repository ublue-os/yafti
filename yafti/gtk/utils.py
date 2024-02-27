from pathlib import Path

from yafti.const import Constants


def get_screen(name: str = "main"):
    return (
        Path(Constants.ROOT_DIR)
        .joinpath("gtk")
        .joinpath("screens")
        .joinpath(name + ".ui")
    )


def get_screen_string(name: str = "main"):
    return get_screen(name).read_text()
