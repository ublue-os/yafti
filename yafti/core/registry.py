# SPDX-License-Identifier: Apache-2.0

from importlib.metadata import entry_points

_plugins = entry_points(group="yafti.plugin")
PLUGINS = {s.name: s.load()() for s in _plugins}

_screens = entry_points(group="yafti.screen")
SCREENS = {s.name: s.load() for s in _screens}


def register_plugin(name: str, plugin: callable):
    PLUGINS[name] = plugin


def register_screen(name: str, screen: callable):
    SCREENS[name] = screen
