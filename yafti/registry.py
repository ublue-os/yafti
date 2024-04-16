# Copyright 2023 Marco Ceppi
# SPDX-License-Identifier: Apache-2.0
import pprint
from importlib.metadata import entry_points

_plugins = entry_points(group="yafti.plugins")
pprint.pprint(_plugins, width=4)
PLUGINS = {s.name: s.load()() for s in _plugins}

_screens = entry_points(group="yafti.views")
pprint.pprint(_screens, width=4)
SCREENS = {s.name: s.load() for s in _screens}
