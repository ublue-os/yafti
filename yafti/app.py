"""
Copyright 2023 Marco Ceppi

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import gbulb
from gi.repository import Adw
import hashlib
import yaml

from yafti.parser import Config, YaftiRunModes
from yafti.screen.window import Window


class Yafti(Adw.Application):
    def __init__(self, cfg: Config = None, loop=None):
        super().__init__(application_id="it.ublue.Yafti")
        self.config = cfg
        self.loop = loop or gbulb.get_event_loop()

    def run(self, *args, **kwargs):
        configured_mode = self.config.properties.mode
        _p = self.config.properties.path.expanduser()
        if configured_mode == YaftiRunModes.disable:
            return

        if configured_mode == YaftiRunModes.changed:
            if _p.exists() and _p.read_text() == self.config_sha:
                return

        if configured_mode == YaftiRunModes.ignore and _p.exists():
            return

        super().run(*args, **kwargs)

    def do_activate(self):
        win = Window(application=self)
        win.present()
        self.loop.run()

    @property
    def config_sha(self):
        return hashlib.sha256(yaml.dump(self.config.dict()).encode()).hexdigest()

    def sync_first_run(self):
        p = self.config.properties.path.expanduser()
        p.write_text(self.config_sha)

    def quit(self):
        self.loop.stop()
        self.sync_first_run()
        super().quit()
