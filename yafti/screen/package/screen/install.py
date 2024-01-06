import asyncio
import json

from gi.repository import Gtk
from typing import Optional

import yafti.share
from yafti import events
from yafti import log
from yafti.abc import YaftiScreen
from yafti.screen.console import ConsoleScreen
from yafti.screen.package.state import PackageScreenState

_xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <requires lib="gtk" version="4.0"/>
  <template class="YaftiPackageInstallScreen" parent="GtkBox">
    <property name="orientation">vertical</property>
    <child>
      <object class="AdwStatusPage" id="status_page">
        <property name="halign">fill</property>
        <property name="valign">fill</property>
        <property name="hexpand">true</property>
        <property name="title" translatable="yes">Package Installation</property>
      </object>
    </child>
    <child>
        <object class="GtkBox">
            <property name="orientation">vertical</property>
            <property name="halign">fill</property>
            <property name="hexpand">True</property>
            <property name="valign">fill</property>
            <child>
                <object class="GtkProgressBar" id="pkg_progress">
                <property name="margin-start">40</property>
                <property name="margin-end">40</property>
                </object>
            </child>
            <child>
                <object class="GtkBox">
                    <property name="orientation">horizontal</property>
                    <child>
                        <object class="GtkBox">
                            <property name="halign">fill</property>
                            <property name="hexpand">true</property>
                        </object>
                    </child>
                    <child>
                        <object class="GtkButton" id="btn_console">
                            <property name="visible">True</property>
                            <property name="margin-end">40</property>
                            <property name="margin-top">20</property>
                            <property name="margin-bottom">20</property>
                            <property name="label">Show Console</property>
                        </object>
                    </child>
                </object>
            </child>
        </object>
    </child>
  </template>
</interface>
"""


@Gtk.Template(string=_xml)
class PackageInstallScreen(YaftiScreen, Gtk.Box):
    __gtype_name__ = "YaftiPackageInstallScreen"

    status_page = Gtk.Template.Child()
    pkg_progress = Gtk.Template.Child()
    btn_console = Gtk.Template.Child()
    started = False
    already_run = False
    pulse = True

    def __init__(
        self,
        state: PackageScreenState,
        title: str = "Package Installation",
        package_manager: str = "yafti.plugin.flatpak",
        package_manager_defaults: Optional[dict] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        from yafti.registry import PLUGINS

        self.status_page.set_title(title)
        self.package_manager = PLUGINS.get(package_manager)
        self.package_manager_defaults = package_manager_defaults or {}
        self.btn_console.connect("clicked", self.toggle_console)
        self.state = state

    async def on_activate(self):
        if self.started or self.already_run:
            return
        self.console = ConsoleScreen()
        self.started = True
        events.on("btn_next", self.next)
        await self.draw()

    async def next(self, _):
        return self.started

    def toggle_console(self, btn):
        btn.set_label("Show Console" if self.console.get_visible() else "Hide Console")
        self.console.toggle_visible()

    async def do_pulse(self):
        self.pkg_progress.set_pulse_step(1.0)
        while self.pulse:
            self.pkg_progress.pulse()
            await asyncio.sleep(0.5)

    def draw(self):
        self.console.hide()
        self.append(self.console)
        packages = [item.replace("pkg:", "") for item in self.state.get_on("pkg:")]
        asyncio.create_task(self.do_pulse())
        return self.install(packages)

    def run_package_manager(self, packge_config):
        try:
            config = json.loads(packge_config)
        except json.decoder.JSONDecodeError as e:
            log.debug("could not parse", config=packge_config, e=e)
            config = {"package": packge_config}

        log.debug("parsed packages config", config=config)
        opts = self.package_manager_defaults.copy()
        opts.update(config)
        return self.package_manager.install(**opts)

    async def install(self, packages: list):
        total = len(packages)
        yafti.share.BTN_NEXT.set_label("Installing...")
        yafti.share.BTN_BACK.set_visible(False)
        for idx, pkg in enumerate(packages):
            results = await self.run_package_manager(pkg)
            self.console.stdout(results.stdout)
            self.console.stderr(results.stderr)
            self.pulse = False
            self.pkg_progress.set_fraction((idx + 1) / total)

        self.console.stdout(b"Installation Complete!")

        self.started = False
        self.already_run = True
        yafti.share.BTN_NEXT.set_label("Next")
        yafti.share.BTN_BACK.set_visible(True)
