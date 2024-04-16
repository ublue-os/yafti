# Copyright 2024 abanna
# SPDX-License-Identifier: Apache-2.0

"""
Present the user with confirmation (consent) to proceed with modifications
on their system

Configuration usage example:

  screens:
    can-we-modify-your-flatpaks:
      source: yafti.screen.consent
      values:
        title: Welcome traveler
        condition:
          run: flatpak remotes --system | grep fedora
        description: |
          This tool modifies your flatpaks and flatpak sources.
          If you do not want to do this exit the installer.
          For new users just do it (tm)
        actions:
          - run: flatpak remote-delete fedora --force
          - run: flatpak remove --system --noninteractive --all

Configuration:

* title: Header of the screen
* description: long form text
* condition: dict of plugin: plugin config. Plugin must return a 0 code to display
             screen. Any other code will result in the screen being skipped
* actions: list of plugins to execute once screen is accepted
"""

import asyncio
from typing import Optional

from gi.repository import Adw, Gio, GLib, Gtk

from yafti import events
from yafti.abc import YaftiScreen, YaftiScreenConfig
from yafti.registry import PLUGINS

# TODO: refactor this asap


@Gtk.Template(filename="yafti/gtk/consent.ui")
class ConsentScreen(YaftiScreen, Adw.Bin):
    __gtype_name__ = "YaftiConsentScreen"

    status_page = Gtk.Template.Child()

    class Config(YaftiScreenConfig):
        title: str
        description: str
        actions: Optional[list[dict[str, str | dict]]] = None

    def __init__(
        self,
        title: str = None,
        description: str = None,
        actions: list = None,
        condition: dict = None,
        **kwargs
    ):
        super().__init__(**kwargs)

        events.register("accept")
        events.on("accept", self.next)
        self.status_page.set_title("Consent")
        self.status_page.set_description("Allowing us add and modify flatpaks to this system.")
        self.actions = actions
        self.condition = condition
        self.already_run = False

    def set_content(self, button, content=None):
        if content is None:
            content = Gio.Application.get_default().split_view.get_content()
            content.set_title("Welcome Travelers")

        button.set_label("Accept")
        content.pane.set_content(self)
        content.pane.set_reveal_bottom_bars(True)
        button.connect("clicked", lambda x: asyncio.ensure_future(self.next(x)))

    async def on_activate(self):
        events.on("btn_next", self.next)
        # yafti.share.BTN_NEXT.set_label("Accept")

    async def on_deactivate(self):
        events.detach("btn_next", self.next)

    async def next(self, _):
        if self.already_run:
            return False

        # Connect to root application to get config object
        application = Gio.Application.get_default()
        application.config.settings.set_value(
            "consent-accepted", GLib.Variant.new_boolean(True)
        )

        to_run = []
        if self.actions is not None:

            for action in self.actions:
                plugin_name = list(action.keys())[0]
                plugin = PLUGINS.get(plugin_name)
                to_run.append(plugin(action[plugin_name]))

            await asyncio.gather(*to_run)

        self.already_run = True

        return False
