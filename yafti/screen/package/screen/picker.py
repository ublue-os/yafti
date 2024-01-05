from functools import partial
import json

from gi.repository import Adw, Gtk
from pydantic import BaseModel

from yafti import log
from yafti.abc import YaftiScreen
from yafti.screen.dialog import DialogBox
from yafti.screen.package.state import PackageScreenState
from yafti.screen.utils import find_parent

_xml = """\
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


@Gtk.Template(string=_xml)
class PackagePickerScreen(YaftiScreen, Adw.Bin):
    __gtype_name__ = "YaftiPackagePickerScreen"

    status_page = Gtk.Template.Child()
    package_list = Gtk.Template.Child()

    class Config(BaseModel):
        title: str = "Package Installation"
        packages: list | dict

    def __init__(
        self,
        state: PackageScreenState,
        title: str,
        packages: list | dict,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.status_page.set_title(title)
        self.packages = packages
        self.state = state
        self.draw()

    def draw(self):
        if isinstance(self.packages, list):
            for item in self._build_apps(self.packages):
                self.package_list.add(item)
            return

        for name, details in self.packages.items():
            action_row = Adw.ActionRow(title=name, subtitle=details.get("description"))

            def state_set(group, _, value):
                self.state.set(f"group:{group}", value)
                d = self.packages.get(group)
                for pkg in d.get("packages", []):
                    for pkg_name in pkg.values():
                        if isinstance(pkg_name, dict):
                            pkg_name = json.dumps(pkg_name)
                        self.state.set(f"pkg:{pkg_name}", value)

            state_set(name, None, details.get("default", True))
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
            "The following list includes only applications available in your preferred "
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
                if isinstance(pkg, dict):
                    pkg = json.dumps(pkg)
                _app_switcher.set_active(self.state.get(f"pkg:{pkg}"))
                _app_switcher.set_valign(Gtk.Align.CENTER)

                def set_state(pkg, btn, value):
                    log.debug("state-set", pkg=pkg, value=value)
                    self.state.set(f"pkg:{pkg}", value)

                set_state_func = partial(set_state, pkg)
                _app_switcher.connect("state-set", set_state_func)
                _apps_action_row.add_suffix(_app_switcher)
                yield _apps_action_row
