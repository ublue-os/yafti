# Copyright 2023 Marco Ceppi
# SPDX-License-Identifier: Apache-2.0

from enum import Enum
from pathlib import Path
from typing import Optional, Any

import yaml
from pydantic import BaseModel, BaseSettings
from pydantic.env_settings import SettingsSourceCallable


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


class YaftSaveState(str, Enum):
    always = "always"
    end = "last-screen"


class YaftiProperties(BaseModel):
    path: Optional[Path] = Path("~/.config/yafti/last-run")
    mode: YaftiRunModes = YaftiRunModes.changed
    save_state: YaftSaveState = YaftSaveState.always


class Config(BaseSettings):
    title: str
    properties: YaftiProperties = YaftiProperties()
    actions: Optional[ActionConfig]
    screens: Optional[dict[str, ScreenConfig]]  # Screens are parsed per plugin

    class Config:
        env_prefix = "yafti_"
        env_nested_delimiter = "__"
        env_file = "/etc/yafti.yml"

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ):
            return (
                init_settings,
                yaml_config_settings_source,
                env_settings,
                file_secret_settings,
            )


def yaml_config_settings_source(settings: BaseSettings) -> dict[str, Any]:
    """
    A simple settings source that loads variables from a JSON file
    at the project's root.

    Here we happen to choose to use the `env_file_encoding` from Config
    when reading `config.json`
    """
    encoding = settings.__config__.env_file_encoding
    return yaml.safe_load(Path(settings.__config__.env_file).read_text(encoding))
