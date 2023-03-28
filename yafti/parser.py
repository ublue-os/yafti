# Copyright 2023 Marco Ceppi
# SPDX-License-Identifier: Apache-2.0

from enum import Enum
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel


class ActionConfig(BaseModel):
    pre: Optional[list[dict[str, str | dict]]]
    post: Optional[list[dict[str, str | dict]]]


class ScreenConfig(BaseModel):
    source: str
    values: Optional[dict]


class YaftiRunModes(str, Enum):
    changed = "run-on-change"
    ignore = "run-once"
    disable = "disabled"


class YaftiProperties(BaseModel):
    path: Optional[Path] = Path("~/.config/yafti-last-run")
    mode: YaftiRunModes = YaftiRunModes.changed


class Config(BaseModel):
    title: str
    properties: YaftiProperties = YaftiProperties()
    actions: Optional[ActionConfig]
    screens: Optional[dict[str, ScreenConfig]]  # Screens are parsed per plugin


def parse(config_file: str) -> Config:
    """Parse the YAML or JSON file passed and return a rendered Config object"""
    with open(config_file) as f:
        cfg = yaml.safe_load(f)
    return Config.parse_obj(cfg)
