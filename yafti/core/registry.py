# Copyright 2023 Marco Ceppi
# SPDX-License-Identifier: Apache-2.0

from importlib.metadata import entry_points

_plugins = entry_points(group="yafti.plugin")
PLUGINS = {s.name: s.load()() for s in _plugins}

_screens = entry_points(group="yafti.screen")
SCREENS = {s.name: s.load() for s in _screens}
