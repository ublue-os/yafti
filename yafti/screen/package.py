from gi.repository import Adw, Gtk
from yafti.abc import YaftiScreen
from yafti.screen.dialog import DialogBox
from yafti.screen.utils import find_parent
from yafti.registry import PLUGINS

from typing import Optional, Any
from pydantic import BaseModel
from functools import partial


_xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <requires lib="gtk" version="4.0"/>
  <template class="YaftiPackageScreen" parent="AdwBin">
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

    def keys(self):
        return self.state.keys()

    def get(self, item: str) -> bool:
        return self.state.get(item)


class PackageScreen(YaftiScreen, Adw.Bin):
    __gtype_name__ = "YaftiPackageScreen"

    status_page = Gtk.Template.Child()
    package_list = Gtk.Template.Child()
    state = None

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
        super().__init__(**kwargs)
        self.status_page.set_title(title)
        self.packages = groups or packages
        self.show_terminal = show_terminal
        self.package_manager = PLUGINS.get(package_manager)
        self.state = PackageScreenState.from_dict(self.parse_packages(self.packages))
        self.draw()

    def parse_packages(self, packages: dict | list) -> dict:
        output = {}

        if isinstance(packages, dict):
            for group, value in packages.items():
                output[f"group:{group}"] = True
                output.update(self.parse_packages(value["packages"]))
            return output

        for pkgcfg in packages:
            output.update({f"pkg:{package}": True for package in pkgcfg.values()})
        return output

    def draw(self):
        if isinstance(self.packages, list):
            # TODO: Implement a list of packages and not package groups
            return

        for name, details in self.packages.items():
            action_row = Adw.ActionRow(title=name, subtitle=details.get("description"))

            def state_set(group, _, value):
                self.state.set(f"group:{group}", value)
                d = self.packages.get(group)
                for pkg in d.get("packages", []):
                    for pkg_name in pkg.values():
                        self.state.set(f"pkg:{pkg_name}", value)

            _switcher = Gtk.Switch()
            _switcher.set_active(self.state.get(f"group:{name}"))
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
                _app_switcher.set_active(self.state.get(f"pkg:{pkg}"))
                _app_switcher.set_valign(Gtk.Align.CENTER)

                def set_state(pkg, btn, value):
                    print(pkg, value)
                    self.state.set(f"pkg:{pkg}", value)

                set_state_func = partial(set_state, pkg)
                _app_switcher.connect("state-set", set_state_func)
                _apps_action_row.add_suffix(_app_switcher)
                yield _apps_action_row
