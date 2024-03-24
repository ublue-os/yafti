# -*- coding: utf-8 -*-
import os
from functools import lru_cache

from gi.repository import Adw, Gio, Gtk

from yafti import __name__ as app_name
from yafti import __version__ as app_version

# from dotenv import load_dotenv
# from pydantic import BaseSettings
# from pydantic.fields import Field




class BaseConfig:
    APP_NAME: str = app_name
    APP_ROOT: str = os.path.realpath(
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))), os.pardir
        )
    )

    PROJECT_ROOT: str = os.path.realpath(os.path.join(APP_ROOT, os.pardir))
    VERSION: str = app_version
    ENVIRONMENT: str = "local"

    # load_dotenv()

    # TODO should be changed to somethng like org.gtk.yafti
    APP_ID: str = "it.ublue.Yafti"

    # pydantic configuration
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @classmethod
    @lru_cache()
    def get_settings(cls, **overrides):
        # TODO: override settings that are passed and look up env vars to override values
        return cls(**overrides)

    # TODO: The Config class presents persistent application settings stored in dconf/GSettings
    #  and exposes them in the Application class The schema for this application contains
    #  nested elements to be addressed independently. The schema is defined in the it.ublue.yafti.gschema.xml file.
    #  The schema file name should be changed to something like org.gtk.yafti.gschema.xml


class Config(BaseConfig):
    """ """

    def __init__(self) -> None:
        schema_dir = f"{self.APP_ROOT}/yafti/yafti/screen/assets"
        schema_source = Gio.SettingsSchemaSource.new_from_directory(
            schema_dir,
            Gio.SettingsSchemaSource.get_default(),
            False,
        )
        # Load Window config schema
        schema = schema_source.lookup("it.ublue.Yafti.window", False)
        self.window = Gio.Settings.new_full(schema, None, None)
        # Load Settings config schema
        schema = schema_source.lookup("it.ublue.Yafti.settings", False)
        self.settings = Gio.Settings.new_full(schema, None, None)
