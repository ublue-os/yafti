import asyncio
from gi.repository import Gtk

import yafti.share
from yafti import events
from yafti.abc import YaftiScreen, YaftiScreenConfig
from yafti.screen.console import ConsoleScreen
from yafti.screen.package.state import STATE

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

    pkg_progress = Gtk.Template.Child()
    btn_console = Gtk.Template.Child()
    started = False
    already_run = False
    pulse = True

    class Config(YaftiScreenConfig):
        package_manager: str = "yafti.plugin.flatpak"
        package_manager_args: dict = {"user": True, "system": False}

    def __init__(
        self,
        title: str = "Package Installation",
        package_manager: str = "yafti.plugin.flatpak",
        package_manager_args: dict = {"user": True, "system": False},
        **kwargs,
    ):
        super().__init__(**kwargs)
        from yafti.registry import PLUGINS

        self.package_manager = PLUGINS.get(package_manager)
        self.package_manager_args = package_manager_args
        self.btn_console.connect("clicked", self.toggle_console)

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
        packages = [item.replace("pkg:", "") for item in STATE.get_on("pkg:")]
        asyncio.create_task(self.do_pulse())
        return self.install(packages)

    async def install(self, packages: list):
        total = len(packages)
        yafti.share.BTN_NEXT.set_label("Installing...")
        yafti.share.BTN_BACK.set_visible(False)
        for idx, pkg in enumerate(packages):
            r = await self.package_manager.install(pkg, **self.package_manager_args)
            self.console.stdout(r.stdout)
            self.console.stderr(r.stderr)
            self.pulse = False
            self.pkg_progress.set_fraction((idx + 1) / total)

        self.console.stdout(b"Installation Complete!")

        self.started = False
        self.already_run = True
        yafti.share.BTN_NEXT.set_label("Next")
        yafti.share.BTN_BACK.set_visible(True)
