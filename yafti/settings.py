# -*- coding: utf-8 -*-
import asyncio
import hashlib
import io
import itertools
import os
import time
from enum import Enum
from functools import lru_cache

import yaml
from gi.repository import Gio, GLib
from sphinx.errors import ExtensionError

import yafti.parser
from yafti import __name__ as app_name
from yafti import __version__ as app_version
from yafti import log
from yafti.registry import PLUGINS

# from dotenv import load_dotenv
# from pydantic import BaseSettings
# from pydantic.fields import Field


class BaseConfig:
    """
    Base configuration

    TODO:
        get user arch version kind
    """

    APP_NAME: str = app_name
    PROJECT_ROOT: str = os.path.realpath(
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
            os.pardir,
            APP_NAME,
        )
    )

    APP_ROOT: str = os.path.realpath(os.path.join(PROJECT_ROOT, APP_NAME))
    VERSION: str = app_version
    # not local all the time...
    ENVIRONMENT: str = "local"

    # load_dotenv()
    APP_ID: str = "org.ublue-os.yafti"

    # pydantic configuration
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @classmethod
    @lru_cache()
    def get_settings(cls, **overrides):
        """
        Get a settings object from YAML file.
        This is not working as intended.
        """
        # TODO: override settings that are passed and look up env vars to override values.
        return cls(**overrides)

    # TODO: The Config class presents persistent application settings stored in dconf/GSettings
    #  and exposes them in the Application class The schema for this application contains
    #  nested elements to be addressed independently. org.ublue-os.yafti.


class YaftiRunMode(str, Enum):
    ENABLED = 0
    NONCE = 1
    ON_BOOT = 2
    DAEMON = 3


class Config(BaseConfig):
    """
    Configuration class for the application.
    """

    # TODO: support more than just flatpak please
    package_manager: str = "yafti.plugins.flatpak"

    def __init__(self, config_path: str = "/etc/yafti.yml") -> None:
        schema_dir = f"{self.APP_ROOT}"
        schema_source = Gio.SettingsSchemaSource.new_from_directory(
            schema_dir,
            Gio.SettingsSchemaSource.get_default(),
            True,
        )
        # TODO: add filter and other currently non imported schemas
        schema = schema_source.lookup("org.ublue-os.yafti", True)
        self.filter = Gio.Settings.new_full(schema, None)

        # Load Window config schema
        schema = schema_source.lookup("org.ublue-os.yafti.windows", True)
        self.window = Gio.Settings.new_full(schema, None, None)
        # Load Settings config schema
        schema = schema_source.lookup("org.ublue-os.yafti.settings", True)
        self.settings = Gio.Settings.new_full(schema, None, None)
        self.__yafti_config_path: str = os.environ.get("YAFTI_CONFIG", config_path)
        self.__yafti_config = None

        _config_sum = self.settings.get_value("config-sum")
        _decoded_config_sum = _config_sum.get_data_as_bytes().get_data().decode("utf-8")
        self.__yafti_config_sum = _decoded_config_sum
        self.__system_state = None
        self.__screens = None
        self.__bundles: list = []
        self.__title: str = "yafti"
        self.__mode: YaftiRunMode = YaftiRunMode.NONCE
        self.__enabled: bool = True
        self.__for_justice: list = []

        asyncio.ensure_future(
            self.__async_callback(PLUGINS.get(self.package_manager).list())
        )

        self.yafti_config_path = self.__yafti_config_path

    ###
    # private methods
    ###
    async def __async_callback(self, callback):
        # TODO: check for is awaitable
        # self._all_packages = task.result()
        # if inspect.isawaitable(callback):
        #     results = await callback()
        #     self._all_packages = results
        # else:
        #     results = callback()
        #
        #     self._all_packages = results

        retry_count = itertools.count()
        while True:
            try:
                loop = asyncio.get_running_loop()
                if loop.is_running():
                    async with asyncio.TaskGroup() as tg:
                        task = tg.create_task(callback)

                    self.__for_justice = task.result()
            except RuntimeError as e:
                if next(retry_count) >= 10:
                    time.sleep(30)
                    continue
                else:
                    print("failed on max retries.")
                    raise e
            except Exception as e:
                print("unrecoverable error")
                raise e
            break

    def __parse_yafti_config(self):
        """
        Parse the yafti config file and return a dictionary of the parsed data.

        example config:
            screens:
              first-screen:
                source: yafti.screen.title
                values:
                  title: "Welcome to Bluefin (Beta)"
                  icon: "/path/to/icon"
                  description: |
                    Applications are also installing in the background, the system will notify you when it is finished.
              applications:
                source: yafti.screen.package
                values:
                  title: Application Installation
                  show_terminal: true
                  package_manager: yafti.plugin.flatpak
                  groups:
                    Communication:
                      default: false
                      description: Tools to communicate and collaborate
                      packages:
                      - Discord: com.discordapp.Discord
                      - Slack: com.slack.Slack
                    Cloud Native Development Tools:
                      description: Start your cloud-native journey here!
                      default: false
                      packages:
                      - Podman Desktop: io.podman_desktop.PodmanDesktop
                      - Headlamp: io.kinvolk.Headlamp
                      - Cockpit Client: org.cockpit_project.CockpitClient
                    Gaming:
                      description: "Rock and Stone!"
                      default: false
                      packages:
                      - Bottles: com.usebottles.bottles
                      - Heroic Games Launcher: com.heroicgameslauncher.hgl
                      - Lutris: net.lutris.Lutris
                      - MangoHUD: org.freedesktop.Platform.VulkanLayer.MangoHud//22.08
                      - Steam: com.valvesoftware.Steam
                      - Proton Plus for Steam: com.vysp3r.ProtonPlus
                    Office:
                      description: Work apps, Bow to Capitalism
                      default: false
                      packages:
                      - OnlyOffice: org.onlyoffice.desktopeditors
                      - LibreOffice: org.libreoffice.LibreOffice
                      - LogSeq: com.logseq.Logseq
                      - Obsidian: md.obsidian.Obsidian
                      - Standard Notes: org.standardnotes.standardnotes
                      - Todoist: com.todoist.Todoist
                    Other Web Browsers:
                      description: Additional browsers to complement Firefox
                      default: false
                      packages:
                      - Brave: com.brave.Browser
                      - Google Chrome: com.google.Chrome
                      - Microsoft Edge: com.microsoft.Edge
                      - Opera: com.opera.Opera
                      - Vivaldi: com.vivaldi.Vivaldi
                    Streaming:
                      description: Stream to the Internet
                      default: false
                      packages:
                      - OBS Studio: com.obsproject.Studio
                      - VkCapture for OBS: com.obsproject.Studio.OBSVkCapture
                      - Gstreamer for OBS: com.obsproject.Studio.Plugin.Gstreamer
                      - Gstreamer VAAPI for OBS: com.obsproject.Studio.Plugin.GStreamerVaapi
                      - Boatswain for Streamdeck: com.feaneron.Boatswain
                    Utilities:
                      description: Useful Utilities
                      default: true
                      packages:
                      - Font Downloader: org.gustavoperedo.FontDownloader
                      - PinApp Menu Editor: io.github.fabrialberio.pinapp
                      - Backup: org.gnome.DejaDup
                      - LocalSend (Easily send files across your network): org.localsend.localsend_app
                      - Peek (Simple Screen Recorder): com.uploadedlobster.peek
                      - Syncthing: com.github.zocker_160.SyncThingy
              final-screen:
                source: yafti.screen.title
                values:
                  title: "All done!"
                  icon: "/path/to/icon"
                  links:
                    - "Install More Applications":
                        run: /usr/bin/gnome-software
                    - "Documentation":
                        run: /usr/bin/xdg-open https://universal-blue.discourse.group/t/introduction-to-bluefin/41
                    - "Discussions and Announcements":
                        run: /usr/bin/xdg-open https://universal-blue.discourse.group/c/bluefin/6
                    - "Join the Discord Community":
                        run: /usr/bin/xdg-open https://discord.gg/XjG48C7VHx
                  description: |
                    Thanks for trying Bluefin, we hope you enjoy it!
        """
        try:
            with open(self.__yafti_config_path, "r") as f:
                _cfg = yaml.safe_load(f)
        except FileNotFoundError as e:
            log.debug(e)
            raise FileNotFoundError(e)

    def __verify_file_extension(self, path: str) -> bool:
        __valid_extensions = [".yml", ".yaml"]
        path, f = os.path.split(path)
        _, ext = os.path.splitext(f)

        return ext.lower() in __valid_extensions

    ###
    # public methods
    ###
    def apps_by_screen(self, name: str):
        log.debug(f"APPS BY SCREEN {name}")
        # return all apps based on bundle

        return NotImplementedError

    @property
    @lru_cache(None)
    def for_justice(self):
        return self.__for_justice

    @property
    def installed(self):
        return self.__for_justice

    def is_installed(self, application_id: str) -> bool:
        """
        Check if an application is installed
        """
        for i in self.__for_justice:
            if i.application == application_id:
                # log.debug(f"Is Installed ==> {application_id} : {i.application}")
                return True

        # log.debug(f"Is Not Installed ==> {application_id}")
        return False

    @property
    @lru_cache(None)
    def yafti_config_path(self):
        return self.__yafti_config_path

    @yafti_config_path.setter
    def yafti_config_path(self, value: str):
        """
        Sets the path to the yafti configuration file.
        """
        _path = None
        if isinstance(value, io.TextIOWrapper):
            _path = value.name
        else:
            _path = value

        full_path = os.path.realpath(_path)
        if not os.path.isfile(full_path):
            raise FileNotFoundError()
        elif not self.__verify_file_extension(full_path):
            raise ExtensionError
        else:
            with open(full_path, "r") as f:
                try:
                    cfg = yaml.safe_load(f)
                    self.__yafti_config = yafti.parser.Config.parse_obj(cfg)

                    config_sum = hashlib.sha256(f.buffer.read()).hexdigest()
                    if config_sum != self.__yafti_config_sum:
                        # when config is updated should likely ask user stuff.
                        self.__yafti_config_sum = config_sum
                        self.settings.set_value(
                            "included-packages", GLib.Variant.new_string("")
                        )
                        self.settings.set_value(
                            "config-sum", GLib.Variant.new_string(config_sum)
                        )
                except yaml.YAMLError as e:
                    log.error(e)
                    raise e

    @property
    @lru_cache(None)
    def bundles(self):
        # fix me
        test = self.screens.get("applications", None).values
        for k, v in test.items():
            log.debug(f"@@@@@ bundles @@@@@\n" f"Name:  {k} \n" f"Value: {v} \n")
            if k == "groups":
                self.__bundles.append(v)

        return self.__bundles

    @property
    @lru_cache(None)
    def screens(self):
        return self.system_config.screens

    @property
    def system_state(self):
        return self.__system_state

    @property
    @lru_cache(None)
    def system_config(self):
        return self.__yafti_config

    @system_config.setter
    def system_config(self, value: str):
        raise NotImplementedError

    @classmethod
    @lru_cache()
    def system_settings(cls):
        return cls.system_config


class Screens:
    pass


class Bundles:
    pass


class Packages:
    pass


class ExcludedPackages:
    pass


class IncludedPackages:
    pass
