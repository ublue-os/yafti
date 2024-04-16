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
import hashlib
from pathlib import Path
import os
import yaml

import gbulb
from gi.repository import Adw, Gdk, Gio, Gtk

from yafti.parser import Config, YaftiRunModes
from yafti.views.content import Content
from yafti.views.sidebar import Sidebar
from yafti.windows.window import ApplicationWindow
from yafti.settings import Config


class Yafti(Adw.Application):
    """
    Yafti main application
    https://developer.gnome.org/documentation/tutorials/menus.html
    """
    def __init__(self, cfg: str = None, loop=None):
        self.config = Config(cfg)
        super().__init__(application_id=self.config.APP_ID)

        resource = Gio.Resource.load(
            os.path.join(self.config.APP_ROOT, "gresource.gresource")
        )
        resource._register()

        self.loop = loop or gbulb.get_event_loop()

    @property
    def temp_config(self) -> Config:
        return self.config.system_config

    def run(self, *args, force_run: bool = False, **kwargs):
        configured_mode = self.config.system_config.properties.mode
        _p: Path = self.config.system_config.properties.path.expanduser()

        # TODO we need to maintain state of all installed applications and this hash should be moved to dconf/GSettings.
        # TODO(GH-#103): Remove this prior to 1.0 release. Start.
        _old_p = Path("~/.config/yafti-last-run").expanduser()

        if _old_p.exists() and _old_p.resolve() != _p.resolve():
            if not _p.parent.is_dir():
                _p.parent.mkdir(mode=0o755, parents=True, exist_ok=True)
            if _p.is_file():
                _p.unlink()

            _old_p.rename(_p)
        # TODO(GH-#103): End.

        if not force_run:
            if configured_mode == YaftiRunModes.disable:
                return

            if configured_mode == YaftiRunModes.changed:
                if _p.exists() and _p.read_text() == self.config_sha:
                    return

            if configured_mode == YaftiRunModes.ignore and _p.exists():
                return

        super().run(*args, **kwargs)

    def do_activate(self):
        # self._win = Window(application=self)
        # this needs to be set in the constructor
        print("@@@@@@@@@@@@@@@ Application Entrypoint @@@@@@@@@@@@@@@@@@@@@")
        self.window = ApplicationWindow(application=self, width_request=280, height_request=200)

        ## GTK UI CSS Provider
        self.css = Gtk.CssProvider()

        # pull from resources
        self.css.load_from_path("yafti/assets/css/application.css")
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), self.css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        ## Establish the navigation split view object & properties
        self.split_view = Adw.NavigationSplitView()
        self.split_view.set_vexpand(True)

        # The breakpoint is used to hide the sidebar when the window is resized
        self.breakpoint = Adw.Breakpoint.new(
            condition=Adw.BreakpointCondition.parse("max-width: 450px")
        )
        self.breakpoint.add_setter(self.split_view, property="collapsed", value=True)
        self.window.add_breakpoint(self.breakpoint)

        # In order to ge the split headerbar view in the navigation split view,
        # an invisible headerbar is added to the window
        # TODO: Check if there is a way to avoid this
        self.dummy_header_bar = Adw.HeaderBar()
        self.dummy_header_bar.set_visible(False)

        # The main window box is the container for the navigation split view
        self.main_window_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.main_window_box.set_vexpand(True)
        self.main_window_box.append(self.dummy_header_bar)
        self.main_window_box.append(self.split_view)
        self.window.set_content(self.main_window_box)

        self.window.__setattr__("bundle_list", self.config.bundles)
        # Set the sidebar and content panes
        self.split_view.set_sidebar(Sidebar(self.window))
        self.split_view.set_content(Content())

        on_deactivate = Gio.SimpleAction(name="quit")
        on_deactivate.connect("activate", self.quit)
        self.add_action(on_deactivate)

        self.window.connect("destroy", self.quit)
        self.window.present()
        self.loop.run()

    @property
    def config_sha(self):
        return hashlib.sha256(yaml.dump(self.config.dict()).encode()).hexdigest()

    def sync_last_run(self):
        """ """
        p = self.config.properties.path.expanduser()
        if not p.parent.is_dir():
            p.parent.mkdir(mode=0o755, parents=True, exist_ok=True)

        p.write_text(self.config_sha)

    def quit(self, *args, **kwargs):
        """
        https://python-gtk-3-tutorial.readthedocs.io/en/latest/builder.html#gtk-template
        """
        self.loop.stop()
        super().quit()
        # This has been commented out during development
        # if self.config.properties.save_state == YaftiSaveState.always:
        #     self.sync_last_run()
        #
        # if (
        #         self.config.properties.save_state == YaftiSaveState.end
        #         and self._win
        #         and self._win.is_last_page
        # ):
        #     self.sync_last_run()
