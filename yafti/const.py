import os
from pathlib import Path
from collections import namedtuple

yafti = namedtuple("yafti", "APPID PATHID ROOT_DIR")

Constants = yafti(
    APPID="it.ublue.Yafti",
    PATHID="/it/ublue/Yafti",
    ROOT_DIR=os.path.dirname(os.path.abspath(__file__)),  # This is your Project Root
)
