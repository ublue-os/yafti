from pathlib import Path

from yafti.const import Constants


def get_root_dir():
    return Path(Constants.ROOT_DIR)
