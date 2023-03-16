from functools import partial
from typing import Optional

from gi.repository import Adw, Gtk
from pydantic import BaseModel

import yafti.share
from yafti import events
from yafti.abc import YaftiScreen
from yafti.registry import PLUGINS
from yafti.screen.console import ConsoleScreen
from yafti.screen.dialog import DialogBox
from yafti.screen.utils import find_parent

_mainxml = """\
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <requires lib="gtk" version="4.0"/>
  <template class="YaftiPackageScreen" parent="AdwBin">
    <property name="halign">fill</property>
    <property name="valign">fill</property>
    <property name="hexpand">true</property>
    <child>
      <object class="AdwCarousel" id="pkg_carousel">
        <property name="vexpand">True</property>
        <property name="hexpand">True</property>
        <property name="allow_scroll_wheel">False</property>
        <property name="allow_mouse_drag">False</property>
        <property name="allow_long_swipes">False</property>
      </object>
    </child>
  </template>
</interface>
"""

_package_screen_xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <requires lib="gtk" version="4.0"/>
  <template class="YaftiPackagePickerScreen" parent="AdwBin">
    <property name="halign">fill</property>
    <property name="valign">fill</property>
    <property name="hexpand">true</property>
    <child>
      <object class="AdwStatusPage" id="status_page">
        <property name="halign">fill</property>
        <property name="valign">fill</property>
        <property name="hexpand">true</property>
        <child>
          <object class="GtkBox">
            <property name="orientation">vertical</property>
            <property name="vexpand">true</property>
            <property name="hexpand">true</property>
            <property name="valign">center</property>
            <child>
              <object class="AdwPreferencesPage">
                <child>
                  <object class="AdwPreferencesGroup" id="package_list"></object>
                </child>
              </object>
            </child>
          </object>
        </child>
      </object>
    </child>
  </template>
</interface>
"""

_installer_xml = """\
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

STATE = None


class PackageConfig(BaseModel):
    __root__: dict[str, str]


class PackageGroupConfigDetails(BaseModel):
    description: str
    packages: list[PackageConfig]


class PackageGroupConfig(BaseModel):
    __root__: dict[str, PackageGroupConfigDetails]


class PackageScreenState:
    __slots__ = ["state"]

    @classmethod
    def from_dict(cls, data: dict) -> "PackageScreenState":
        state = cls()
        for k, v in data.items():
            state.set(k, v)
        return state

    def __init__(self):
        self.state = {}

    def remove(self, item: str) -> None:
        del self.state[item]

    def on(self, item: str) -> None:
        self.set(item, True)

    def off(self, item: str) -> None:
        self.set(item, False)

    def toggle(self, item: str) -> bool:
        self.state[item] = not self.state[item]
        return self.get(item)

    def set(self, item: str, state: bool):
        self.state[item] = state

    def get_on(self, prefix: str = ""):
        return [
            item
            for item, value in self.state.items()
            if item.startswith(prefix) and value is True
        ]

    def keys(self):
        return self.state.keys()

    def get(self, item: str) -> bool:
        return self.state.get(item)


def parse_packages(packages: dict | list) -> dict:
    output = {}

    if isinstance(packages, dict):
        for group, value in packages.items():
            output[f"group:{group}"] = True
            output.update(parse_packages(value["packages"]))
        return output

    for pkgcfg in packages:
        output.update({f"pkg:{package}": True for package in pkgcfg.values()})
    return output


@Gtk.Template(string=_mainxml)
class PackageScreen(YaftiScreen, Adw.Bin):
    __gtype_name__ = "YaftiPackageScreen"

    pkg_carousel = Gtk.Template.Child()

    class Config(BaseModel):
        show_terminal: bool = True
        package_manager: str
        groups: Optional[PackageGroupConfig] = None
        packages: Optional[list[PackageConfig]] = None

    def __init__(
        self,
        title: str = "Package Installation",
        package_manager: str = "yafti.plugin.flatpak",
        packages: list[PackageConfig] = None,
        groups: PackageGroupConfig = None,
        show_terminal: bool = True,
        **kwargs,
    ):
        global STATE
        super().__init__(**kwargs)
        self.title = title
        self.packages = groups or packages
        self.show_terminal = show_terminal
        self.package_manager = package_manager
        if not STATE:
            STATE = PackageScreenState.from_dict(parse_packages(self.packages))
        self.pkg_carousel.connect("page-changed", self.changed)
        self.draw()

    def draw(self):
        self.pkg_carousel.append(
            PackagePickerScreen(title=self.title, packages=self.packages)
        )
        self.pkg_carousel.append(
            PackageInstallScreen(title=self.title, package_manager=self.package_manager)
        )

    def on_activate(self):
        events.on("btn_next", self.next)
        events.on("btn_back", self.back)
        yafti.share.BTN_NEXT.set_label("Install")

    def on_deactivate(self):
        events.detach("btn_next", self.next)
        events.detach("btn_back", self.back)

    @property
    def idx(self):
        return self.pkg_carousel.get_position()

    @property
    def total(self):
        return self.pkg_carousel.get_n_pages()

    def goto(self, page: int, animate: bool = True):
        if page < 0:
            page = 0

        if page >= self.pkg_carousel.get_n_pages():
            page = self.pkg_carousel.get_n_pages()

        current_screen = self.pkg_carousel.get_nth_page(self.idx)
        next_screen = self.pkg_carousel.get_nth_page(page)

        current_screen.deactivate()
        self.pkg_carousel.scroll_to(next_screen, animate)

    def changed(self, *args):
        current_screen = self.pkg_carousel.get_nth_page(self.idx)
        current_screen.activate()

    async def next(self, _):
        if not self.active:
            return False
        if self.idx + 1 == self.total:
            return False
        self.goto(self.idx + 1)

    async def back(self, _):
        if not self.active:
            return False
        print(self.idx)
        if self.idx - 1 < 0:
            return False
        self.goto(self.idx - 1)


@Gtk.Template(string=_installer_xml)
class PackageInstallScreen(YaftiScreen, Gtk.Box):
    __gtype_name__ = "YaftiPackageInstallScreen"

    pkg_progress = Gtk.Template.Child()
    btn_console = Gtk.Template.Child()
    started = False
    already_run = False

    class Config(BaseModel):
        package_manager: str = "yafti.plugin.flatpak"

    def __init__(
        self,
        title: str = "Package Installation",
        package_manager: str = "yafti.plugin.flatpak",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.package_manager = PLUGINS.get(package_manager)
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

    async def draw(self):
        self.console.hide()
        self.append(self.console)
        packages = [item.replace("pkg:", "") for item in STATE.get_on("pkg:")]
        await self.install(packages)

    async def install(self, packages: list):
        total = len(packages)
        self.pkg_progress.set_fraction(0.01)
        yafti.share.BTN_NEXT.set_label("Installing...")
        yafti.share.BTN_BACK.set_visible(False)

        for idx, pkg in enumerate(packages):
            r = await self.package_manager.install(pkg)
            self.console.stdout(r.stdout)
            self.console.stderr(r.stderr)
            self.pkg_progress.set_fraction((idx + 1) / total)

        self.console.stdout(b"Installation Complete!")

        self.started = False
        self.already_run = True
        yafti.share.BTN_NEXT.set_label("Next")
        yafti.share.BTN_BACK.set_visible(True)


@Gtk.Template(string=_package_screen_xml)
class PackagePickerScreen(YaftiScreen, Adw.Bin):
    __gtype_name__ = "YaftiPackagePickerScreen"

    status_page = Gtk.Template.Child()
    package_list = Gtk.Template.Child()

    class Config(BaseModel):
        title: str = "Package Installation"
        packages: list | dict

    def __init__(
        self,
        title: str,
        packages: list | dict,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.status_page.set_title(title)
        self.packages = packages
        self.draw()

    def draw(self):
        if isinstance(self.packages, list):
            # TODO: Implement a list of packages and not package groups
            return

        for name, details in self.packages.items():
            action_row = Adw.ActionRow(title=name, subtitle=details.get("description"))

            def state_set(group, _, value):
                STATE.set(f"group:{group}", value)
                d = self.packages.get(group)
                for pkg in d.get("packages", []):
                    for pkg_name in pkg.values():
                        STATE.set(f"pkg:{pkg_name}", value)

            _switcher = Gtk.Switch()
            _switcher.set_active(STATE.get(f"group:{name}"))
            _switcher.set_valign(Gtk.Align.CENTER)

            state_set_fn = partial(state_set, name)
            _switcher.connect("state-set", state_set_fn)
            action_row.add_suffix(_switcher)

            _customize = Gtk.Button()
            _customize.set_icon_name("go-next-symbolic")
            _customize.set_valign(Gtk.Align.CENTER)
            _customize.add_css_class("flat")
            action_row.add_suffix(_customize)
            picker_fn = partial(self._build_picker, details.get("packages", []))
            _customize.connect("clicked", picker_fn)
            self.package_list.add(action_row)

    def _build_picker(self, packages: list, *args):
        dialog = DialogBox(find_parent(self, Gtk.Window))

        btn_cancel = Gtk.Button()
        btn_save = Gtk.Button()
        btn_cancel.set_label("Cancel")
        btn_save.set_label("Save")
        btn_save.add_css_class("suggested-action")

        header = Adw.HeaderBar()
        header.pack_start(btn_cancel)
        header.pack_end(btn_save)
        header.set_show_end_title_buttons(False)
        header.set_show_start_title_buttons(False)

        item_list = Adw.PreferencesGroup()
        item_list.set_description(
            "The following list includes only applications available in your preferred"
            "package manager."
        )
        page = Adw.PreferencesPage()
        page.add(item_list)

        box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        box.append(header)
        box.append(page)

        dialog.set_content(box)
        dialog.set_default_size(500, 600)

        for item in self._build_apps(packages):
            item_list.add(item)

        btn_cancel.connect("clicked", lambda x: dialog.close())
        btn_save.connect("clicked", lambda x: dialog.close())
        dialog.show()

    def _build_apps(self, packages: list):
        for item in packages:
            for name, pkg in item.items():
                _apps_action_row = Adw.ActionRow(
                    title=name,
                )
                _app_switcher = Gtk.Switch()
                _app_switcher.set_active(STATE.get(f"pkg:{pkg}"))
                _app_switcher.set_valign(Gtk.Align.CENTER)

                def set_state(pkg, btn, value):
                    print(pkg, value)
                    STATE.set(f"pkg:{pkg}", value)

                set_state_func = partial(set_state, pkg)
                _app_switcher.connect("state-set", set_state_func)
                _apps_action_row.add_suffix(_app_switcher)
                yield _apps_action_row
