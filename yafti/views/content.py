import asyncio
import base64
import hashlib
import json
from pprint import pformat

from gi.repository import Adw, Gio, GLib, GObject, Gtk

from yafti import log
from yafti.views.consent import ConsentScreen
from yafti.views.dialog import DialogBox

# The content pane is a shell to swap panes in and out of the content area of the navigation split view
# The content pane must be a subclass of Adw.NavigationPage
# The content pane consists of a top_bar, content area, and bottom_bar
# For specific content panes, common bottom toolbar is used to control
# the state of the data factory updating for linked panes class
# In other content panes, the common bottom toolbar can be hidden

# When a button is clicked in the sidebar, it should update the toolbar content and the bottom toolbar visibility
# It should be able to remove the bottom toolbar from the content pane using an empty widget


# This would typically be its own file
MENU_XML = """
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="app-menu">
    <section>
      <attribute name="label" translatable="yes">Application Menu</attribute>
      <item>
        <attribute name="action">win.change_label</attribute>
        <attribute name="target"></attribute>
        <attribute name="label" translatable="yes">String 1</attribute>
      </item>
      <item>
        <attribute name="action">win.change_label</attribute>
        <attribute name="target"></attribute>
        <attribute name="label" translatable="yes">String 2</attribute>
      </item>
      <item>
        <attribute name="action">win.change_label</attribute>
        <attribute name="target"></attribute>
        <attribute name="label" translatable="yes">String 3</attribute>
      </item>
    </section>
    <section>
      <item>
        <attribute name="action">win.maximize</attribute>
        <attribute name="label" translatable="yes">Dark Mode</attribute>
      </item>
    </section>
    <section>
      <item>
        <attribute name="action">app.about</attribute>
        <attribute name="label" translatable="yes">_About</attribute>
      </item>
      <item>
        <attribute name="action">app.settings</attribute>
        <attribute name="label" translatable="yes">Settings</attribute>
      </item>
      <item>
        <attribute name="action">app.quit</attribute>
        <attribute name="label" translatable="yes">_Quit</attribute>
        <attribute name="accel">&lt;Primary&gt;q</attribute>
    </item>
    </section>
  </menu>
</interface>
"""


class Content(Adw.NavigationPage):
    """
    Content class creates the content pane structure
    https://gnome.pages.gitlab.gnome.org/libadwaita/doc/main/style-classes.html#toolbars
    Other pane classes update the content pane with their content
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_visible(True)
        self.pane = Adw.ToolbarView(top_bar_style=Adw.ToolbarStyle.FLAT)
        self.header = Adw.HeaderBar()

        # https://python-gtk-3-tutorial.readthedocs.io/en/latest/application.html
        self.header.set_decoration_layout("menu:false")
        self.menu = Gio.Menu()
        builder = Gtk.Builder.new_from_string(MENU_XML, -1)

        # self.menu.append("Dark Mode", "app.dark_mode")
        # self.menu_button = Gtk.MenuButton(
        #     icon_name="open-menu-symbolic", menu_model=self.menu
        # )

        self.end_menu_button = Gtk.MenuButton(
            icon_name="system-shutdown-symbolic",
            menu_model=builder.get_object("app-menu"),
        )

        # self.header.pack_start(self.menu_button)
        self.header.pack_end(self.end_menu_button)

        # self.pane.replace_data
        self.pane.add_top_bar(self.header)
        self.set_child(self.pane)

        # next button
        next_button = Gtk.Button()
        next_button.set_label("Next")
        next_button.set_halign(Gtk.Align.CENTER)
        next_button.set_css_classes(["suggested-action"])
        next_button.connect("clicked", lambda x: self.next())
        # bottom bar
        bottom_bar = Gtk.Box()
        bottom_bar.set_margin_top(12)
        bottom_bar.set_margin_bottom(12)
        bottom_bar.set_margin_end(12)
        bottom_bar.set_halign(Gtk.Align.END)
        bottom_bar.append(next_button)
        bottom_bar.set_css_classes([".toolbar"])
        # setting pane
        self.pane.add_bottom_bar(bottom_bar)
        self.pane.set_reveal_bottom_bars(True)

        # Packages is unable to resolve the Application object before the content pane is first created
        # So the content pane is passed as an argument to the set_content method
        # Connect to root application to get config object
        # need to properly send user to next page with content
        application = Gio.Application.get_default()
        consent_accepted = application.config.settings.get_value(
            "consent-accepted"
        ).get_boolean()
        log.info(f"consent has been set to: {consent_accepted}")

        if consent_accepted is True:
            first_screen = application.config.screens.get('first-screen')
            if first_screen is None:
                self.set_title("Welcome Travelers")
                pkg = Packages("Welcome", self, [])
            else:
                self.set_title("Welcome Travelers")
                self.set_description = first_screen.values['description']
                self.set_icon = first_screen.values['icon']
                pkg = Packages(first_screen.values['title'], self, [])

            pkg.set_content(None, self)

        else:
            # TODO: get from config file and load as view
            self.set_title("Welcome Travelers")
            welcome = ConsentScreen()
            welcome.set_content(next_button, self)

    def _closed(self, obj, pspec):
        log.debug(f"Closing {obj}")

    def next(self, **kwargs):
        """
        Next screen this currently doesn't work
        """
        log.debug("Next screen")
        application = Gio.Application.get_default()
        current = self.pane.set_content(application.split_view.get_content())
        pkg = Packages(
            self, package_list=[], window=application.get_default().split_view
        )
        pkg.set_content(current, self)


# TODO: move to .ui file.
_xml2 = """\
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <requires lib="gtk" version="4.0"/>
  <template class="YaftiPackages" parent="AdwBin">
    <property name="hexpand">1</property>
    <property name="vexpand">1</property>
    <child>
      <object class="GtkOverlay">
        <property name="valign">center</property>
        <child type="overlay">
          
        </child>
        
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
                      <object class="AdwPreferencesGroup" id="bundle_list"></object>
                    </child>
                  </object>
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


class Package(GObject.GObject):
    __gtype_name__ = "Package"

    def __init__(self, application, name, ref, installed):
        super().__init__()
        self.__app = Gtk.Application.get_default()
        self._application = application
        self._action = None
        self._checksum: str = ""
        self._name = name
        self._ref = ref
        self._installed = installed or False
        self._modified: bool = False
        self._install_button = Gtk.Button()
        self._window = Gtk.Window()
        self._dialog_box = DialogBox(self._window)
        self._apps_page = Adw.PreferencesPage()
        self._box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        self._box.append(self._apps_page)
        self._dialog_box.set_content(self._box)
        self._dialog_box.set_default_size(500, 600)
        self._action_row = Adw.ActionRow(title=self._ref)
        self._install_button.set_name("install")
        self._install_button.set_label("install")
        self._install_button.set_label("install")
        self._install_button.set_valign(Gtk.Align.CENTER)
        self._install_button.add_css_class("boxed_list")
        self._action_row.add_suffix(self._install_button)

        if self._installed is True and self._modified is False:
            log.debug(
                f"package was installed and not modified setting initial icon {self._name}"
            )
            self._install_button.set_icon_name("process-completed-symbolic")

    def to_dict(self):
        return {
            "action": self._action,
            "application": self._application,
            "name": self._name,
            "ref": self._ref,
            "installed": self._installed,
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    def __base64_encode(self):
        encoded_json = self.to_json().encode("utf-8")

        return base64.b64encode(encoded_json).decode("utf-8")

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value: str or None):
        if value not in ["install", "uninstall", None]:
            raise ValueError("Action must be either 'install' or 'uninstall'")

        self._action = value

    @property
    def checksum(self):
        sha256 = hashlib.sha256(self.to_json().encode("utf-8"))
        self._checksum = sha256.hexdigest()

        return self._checksum

    def __get_from_settings(self):
        pkg_settings = self.__app.config.settings.get_value("included-packages")
        encoded_pkgs = pkg_settings.get_data_as_bytes().get_data().decode("utf-8")

        all_pkgs = ""
        try:
            all_pkgs = json.loads(base64.b64decode(encoded_pkgs))
        except Exception:
            # attempt to rebuild full included package settings
            pass

        return all_pkgs

    def __get_installed(self):
        pass

    def __update_settings(self):
        included_packages = self.__app.config.settings.get_value("included-packages")
        pkg_data = included_packages.get_data_as_bytes().get_data().decode("utf-8")

        try:
            pkgs_loaded = json.loads(base64.b64decode(pkg_data))
        except json.JSONDecodeError as e:
            log.debug(
                f"failed to decode and json load package data updating settings: {pkg_data} -- {e}"
            )
            pkgs_loaded = {}
            pass

        exists = pkgs_loaded.get(self.application)
        if exists is None or exists.get("checksum") != self.checksum:
            self_dict = self.to_dict()
            self_dict["checksum"] = self.checksum
            pkgs_loaded[self.application] = self_dict
            pkgs_encoded = json.dumps(pkgs_loaded).encode("utf-8")
            b64 = base64.b64encode(pkgs_encoded).decode("utf-8")
            self.__app.config.settings.set_value(
                "included-packages", GLib.Variant.new_string(b64)
            )

    def update_state(self):
        self._modified = True
        self.__update_settings()

    @GObject.Property(type=str)
    def application(self):
        return self._application

    @GObject.Property(type=str)
    def name(self):
        return self._name

    @GObject.Property(type=str)
    def ref(self):
        return self._ref

    @GObject.Property(type=bool, default=False)
    def installed(self):
        if self._installed is True and self._modified is False:
            self._install_button.set_icon_name("process-completed-symbolic")

        return self._installed

    @installed.setter
    def installed(self, value: bool):
        if value is True and self._modified is False:
            self._install_button.set_icon_name("process-completed-symbolic")

        self._installed = value

    @property
    def install_button(self):
        return self._install_button

    @property
    def dialog_box(self):
        return self._dialog_box

    @property
    def action_row(self):
        return self._action_row

    def __repr__(self):
        return f"""
                Package(
                    action={self._action}
                    application={self._application},
                    name={self._name},
                    ref={self._ref},
                    installed{self._installed}
                )
            """  # noqa


# @Gtk.Template(filename="yafti/screen/assets/packages.ui")
# class Packages(Gtk.ScrolledWindow):
@Gtk.Template(string=_xml2)
class Packages(Adw.Bin):
    """
    Packages class defines the Packages content panes

    It generates the structure in memory to apply to the navigation split view
    """

    __gtype_name__ = "YaftiPackages"
    # scrolled_window = Gtk.ScrolledWindow()
    # package_list = Gtk.Template.Child()
    # packages_overview = Gtk.Template.Child()
    status_page = Gtk.Template.Child()
    bundle_list = Gtk.Template.Child()
    # bundle = Gtk.Template.Child()
    # btn_next = Gtk.Template.Child()

    def __init__(self, title, window, package_list, **kwargs):
        super().__init__(**kwargs)

        self.__window = window
        # self.btn_next.connect("clicked", self.__next_step)
        self.title: str = title
        self.set_property("visible", True)
        self.package_list = package_list or []
        self._all_packages = []
        # self.scrolled_window = Gtk.ScrolledWindow()
        self.set_vexpand(True)
        self.__register_widgets = []
        self.__app = Gtk.Application.get_default()
        # TODO get from config
        # self.bundle_list.activate_action("clicked", self.on_selection_button_clicked)
        self.list_store = Gio.ListStore.new(Package)
        self._currently_installed = []
        self.__loaded = []

        asyncio.ensure_future(self.build_screens(package_list))

    def currently_installed(self, force=False):
        if not self._currently_installed or force is True:
            self._currently_installed = []
            for pkg in self.__app.config.installed:
                self._currently_installed.append(pkg)

        return self._currently_installed

    def __next_step(self, *args):
        """
        This still does not work
        """
        log.debug(f"next_step: {args}")
        self.__window.next()

    def language_filter_func(self, model, iter, data):
        """
        Not working
        """
        if self.current_filter is None or self.current_filter == "None":
            return True
        else:
            return model[iter][2] == self.current_filter

    def on_ready_callback(self, source_object, result, user_data):
        """
        Not working
        """
        log.debug("on_ready_callback")

    # @Gtk.Template.Callback()
    def on_selection_button_clicked(self, widget, dialog, item):
        """ """
        log.debug("on_selection_button_clicked")
        dialog.set_visible(False)
        # dialog.connect()
        # we set the current language filter to the button's label

        state = widget.get_icon_name()
        log.debug(f"package action state: {state}")
        if state is None:
            widget.set_icon_name("selection-checked-symbolic")
            item.action = "install"
        if state == "process-completed-symbolic":
            widget.set_icon_name("process-error-symbolic")
            item.install_button.set_icon_name("process-error-symbolic")
            item.action = "uninstall"
        elif state == "selection-checked-symbolic":
            widget.set_label("install")
            item.action = None
        elif state == "process-error-symbolic":
            widget.set_icon_name("process-completed-symbolic")
            item.action = None

        item.update_state()

        # self.__app.config.setttings.set_active(item["application"])
        # self.__app.config.settings.preferences_group.get_value("")

        included_packages = self.__app.config.settings.get_value("included-packages")
        inc_bytes = included_packages.get_data_as_bytes().get_data().decode("utf-8")
        try:
            log.debug(pformat(json.loads(base64.b64decode(inc_bytes)), indent=4))
        except Exception as e:
            log.error(f"content button state error json loads: {e}", e)
            return

    def set_content(self, button, content=None):
        """
        set_content sets the Packages pane content in the navigation split view
        """
        # self.connect("noarg-signal", self.noarg_signal)
        if content is None:
            content = Gio.Application.get_default().split_view.get_content()
            content.set_title("Packages")

        content.pane.set_content(self)
        content.pane.set_reveal_bottom_bars(False)
        content.set_child(self)
        # self.show()
        # self.scrolled_window.set_data(self.__window)
        asyncio.ensure_future(self.build_screens())

    async def build_screens(self, package_list=None):
        """
        This entire function needs to be refactored
        """
        # TODO: get values from config file
        self.status_page.set_icon_name("package")
        if isinstance(self.title, Content):
            _content = self.title

            self.title = _content.get_title().title()
            self.status_page.set_title(self.title)
            self.set_content(None, _content)
        else:
            self.status_page.set_title(self.title)

        if self.package_list is None:
            self.status_page.set_description(
                "Install some Packages! If you're seeing this message update the yafti.yaml file."
            )
        elif isinstance(self.package_list, list):
            # for package in self.package_list:
            #     print(package)
            # TODO: make work
            log.debug(
                f"^^^^^^^^^^^^^^^^^^^^^^^ self.package_list is {self.package_list} ^^^^^^^^^^^^^^^^^^^^^^^"
            )

        else:
            self.status_page.set_description(
                self.package_list.get("description", "Should make a github issue...")
            )

        match self.title.lower():
            case "apply changes":
                log.debug(
                    f"-----------------------------------{self.title.lower()}-----------------------------------"
                )
                self.list_store = Gtk.ListStore(str, str, str, str, str)
                new_headers = [
                    "ref",
                    "name",
                    "runtime",
                    "installation",
                    "version",
                    "options",
                ]

                for p in self.package_list:
                    for k, v in p.items():
                        self.list_store.append([k, v])
                        self._all_packages.append(
                            {new_headers[0]: k, new_headers[1]: v}
                        )
            case "installed":
                log.debug(
                    f"-----------------------------------{self.title.lower()}-----------------------------------"
                )
                self.status_page.set_description("Currently installed on your system")
                self.list_store.remove_all()
                for p in self.currently_installed():
                    # self.list_store.append([p.ref, p.name])
                    pkg = Package(p.application, p.name, p.ref, True)
                    self.list_store.append(pkg)

                # not sure why installed is being called twice
                if self.title.lower() not in self.__loaded:
                    self.__loaded.append(self.title.lower())
                    self.__load_pages()
                elif "currently-installed" not in self.__loaded:
                    self.__loaded.append("currently-installed")
                    self.__load_pages()

            case _:
                log.debug(
                    f"-------------group package screen {self.title.lower()}--------------"
                )
                if isinstance(self.package_list, dict):
                    packages = self.package_list.get("packages", [])
                    if packages:
                        self.list_store.remove_all()
                        for p in packages:
                            for k, v in p.items():
                                is_installed = self.__app.config.is_installed(v)

                                pkg = Package(v, v, k, is_installed)
                                self.list_store.append(pkg)
                                self.list_store.connect(
                                    "notify", self.__on_page_changed, pkg
                                )

                        if self.title.lower() not in self.__loaded:
                            self.__loaded.append(self.title.lower())
                            self.__load_pages()

                else:
                    # TODO: this needs to be handled correctly
                    log.debug("something went wrong -- before loop started")

    def __load_pages(self):
        selection_dialogs = []
        _index = 0

        for item in self.list_store:
            selection_dialogs.append(item.dialog_box)
            # _customize.connect("clicked", self.on_selection_button_clicked, selection_dialogs[-1])  # selection_dialogs[-1], _apps_list, item
            item.install_button.connect(
                "clicked",
                self.on_selection_button_clicked,
                selection_dialogs[_index],
                item,
            )
            self.bundle_list.add(item.action_row)

            _index += 1

    def __on_page_changed(self, list_store, page, item):
        log.debug("on_page_changed")
        if item.installed is False:
            item.installed = self.__app.config.is_installed(item.application)
