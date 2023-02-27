from gi.repository import Adw, Gtk
from yafti.screen.dialog import DialogBox
from yafti.screen.utils import find_parent


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
                  <object class="AdwPreferencesGroup" id="packages"></object>
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
class PackageScreen(Adw.Bin):
    __gtype_name__ = "YaftiPackageScreen"

    status_page = Gtk.Template.Child()
    packages = Gtk.Template.Child()
    state = ()

    def __init__(
        self,
        title: str = None,
        description: str = None,
        packages: list = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.status_page.set_title("Hello COMPUTER")
        action_row = Adw.ActionRow(title="Core", subtitle="Essential applications")
        self.draw()

    def draw(self):
        for name in ("Core", "Gaming"):
            action_row = Adw.ActionRow(title=name, subtitle="Essential applications")

            _switcher = Gtk.Switch()
            _switcher.set_active(True)
            _switcher.set_valign(Gtk.Align.CENTER)
            action_row.add_suffix(_switcher)

            _customize = Gtk.Button()
            _customize.set_icon_name("go-next-symbolic")
            _customize.set_valign(Gtk.Align.CENTER)
            _customize.add_css_class("flat")
            action_row.add_suffix(_customize)

            _customize.connect("clicked", self._build_picker)
            self.packages.add(action_row)

    def _build_picker(self, *args):
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
            "The following list includes only applications available in your preferred package manager."
        )
        page = Adw.PreferencesPage()
        page.add(item_list)

        box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        box.append(header)
        box.append(page)

        dialog.set_content(box)
        dialog.set_default_size(500, 600)

        for item in self._build_apps():
            item_list.add(item)

        btn_cancel.connect("clicked", lambda x: dialog.close())
        btn_save.connect("clicked", lambda x: dialog.close())
        dialog.show()

    def _build_apps(self):
        for app in ["Calculator", "Calendar"]:
            _apps_action_row = Adw.ActionRow(
                title=app,
            )
            _app_switcher = Gtk.Switch()
            _app_switcher.set_active(True)
            _app_switcher.set_valign(Gtk.Align.CENTER)
            _apps_action_row.add_suffix(_app_switcher)
            yield _apps_action_row
