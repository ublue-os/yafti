# Copyright 2023 Marco Ceppi
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

from gi.repository import Adw, Gtk

import yafti.share
from yafti import events
from yafti.abc import YaftiScreen, YaftiScreenConfig
from yafti.registry import PLUGINS

_xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<interface>
    <requires lib="gtk" version="4.0"/>
    <requires lib="libadwaita" version="1.0" />
    <template class="YaftiConsentScreen" parent="AdwBin">
        <property name="halign">fill</property>
        <property name="valign">fill</property>
        <property name="hexpand">true</property>
        <child>
            <object class="AdwStatusPage" id="status_page">
                <property name="title" translatable="yes">Welcome!</property>
                <property name="description" translatable="yes">
                    Make your choices, this wizard will take care of everything.
                </property>
            </object>
        </child>
    </template>
</interface>
"""


@Gtk.Template(string=_xml)
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
        self.status_page.set_title(title)
        self.status_page.set_description(description)
        self.actions = actions
        self.condition = condition
        self.already_run = False

    async def on_activate(self):
        events.on("btn_next", self.next)
        yafti.share.BTN_NEXT.set_label("Accept")

    async def on_deactivate(self):
        events.detach("btn_next", self.next)

    async def next(self, _):
        if self.already_run:
            return False

        to_run = []
        for action in self.actions:
            plugin_name = list(action.keys())[0]
            plugin = PLUGINS.get(plugin_name)
            to_run.append(plugin(action[plugin_name]))
        await asyncio.gather(*to_run)
        self.already_run = True
        return False
