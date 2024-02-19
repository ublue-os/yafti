"""
Copyright 2024 uBlue

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

import hashlib
from pathlib import Path

import gbulb
import yaml
from gi.repository import Adw

from yafti.const import Constants
from yafti.core.config import Config, YaftiRunModes, YaftSaveState
from yafti.screen.window import Window


class Yafti(Adw.Application):
    def __init__(self, cfg: Config = None, loop=None):
        super().__init__(application_id=Constants.APPID)
        self.config = cfg
        self.loop = loop or gbulb.get_event_loop()

    def run(self, *args, force_run: bool = False, **kwargs):
        configured_mode = self.config.properties.mode
        path: Path = self.config.properties.path.expanduser()
        if not force_run:
            if configured_mode == YaftiRunModes.disable:
                return

            if configured_mode == YaftiRunModes.changed:
                if path.exists() and path.read_text() == self.config_sha:
                    return

            if configured_mode == YaftiRunModes.ignore and path.exists():
                return

        super().run(*args, **kwargs)

    def do_activate(self):
        self._win = Window(application=self)
        self._win.present()
        self.loop.run()

    @property
    def config_sha(self):
        return hashlib.sha256(yaml.dump(self.config.dict()).encode()).hexdigest()

    def sync_last_run(self):
        p = self.config.properties.path.expanduser()
        if not p.parent.is_dir():
            p.parent.mkdir(mode=0o755, parents=True, exist_ok=True)
        p.write_text(self.config_sha)

    def quit(self, *args, **kwargs):
        self.loop.stop()
        if self.config.properties.save_state == YaftSaveState.always:
            self.sync_last_run()

        if (
            self.config.properties.save_state == YaftSaveState.end
            and self._win
            and self._win.is_lastpathage
        ):
            self.sync_last_run()

        super().quit()
