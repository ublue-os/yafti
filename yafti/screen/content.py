import asyncio
from typing import Optional

import gi.repository.GObject
from gi.repository import Adw, Gio, GLib, Gtk

from yafti import log
from yafti.abc import YaftiScreen, YaftiScreenConfig
from yafti.registry import PLUGINS, SCREENS
from yafti.screen.consent import ConsentScreen
from yafti.screen.dialog import DialogBox
from yafti.screen.package.models import PackageConfig, PackageGroupConfig

# The content pane is a shell to swap panes in and out of the content area of the navigation split view
# The content pane must be a subclass of Adw.NavigationPage
# The content pane consists of a top_bar, content area, and bottom_bar
# For specific content panes, common bottom toolbar is used to control
# the state of the data factory updating for linked panes class
# In other content panes, the common bottom toolbar can be hidden

# When a button is clicked in the sidebar, it should update the toolbar content and the bottom toolbar visibility
# It should be able to remove the bottom toolbar from the content pane using an empty widget


class Content(Adw.NavigationPage):
    """
    Content class creates the content pane structure

    Other pane classes update the content pane with their content
    """

    def __init__(self):
        super().__init__()

        self.set_visible(True)

        self.pane = Adw.ToolbarView(top_bar_style=Adw.ToolbarStyle.FLAT)
        self.header = Adw.HeaderBar()
        self.header.set_decoration_layout("menu:close")

        self.menu = Gio.Menu()
        self.menu.append("Dark Mode", "app.dark_mode")
        self.menu_button = Gtk.MenuButton(
            icon_name="open-menu-symbolic", menu_model=self.menu
        )
        self.header.pack_start(self.menu_button)

        # self.pane.replace_data
        self.pane.add_top_bar(self.header)
        self.set_child(self.pane)

        start_button = Gtk.Button()
        start_button.set_label("Start")
        start_button.set_halign(Gtk.Align.CENTER)

        start_button.set_css_classes(["suggested-action"])

        bottom_bar = Gtk.Box()
        bottom_bar.set_margin_top(12)
        bottom_bar.set_margin_bottom(12)
        bottom_bar.set_margin_end(12)
        bottom_bar.set_halign(Gtk.Align.END)
        bottom_bar.append(start_button)
        bottom_bar.set_css_classes([".toolbar"])

        self.pane.add_bottom_bar(bottom_bar)
        self.pane.set_reveal_bottom_bars(True)

        # Packages is unable to resolve the Application object before the content pane is first created
        # So the content pane is passed as an argument to the set_content method
        # Connect to root application to get config object
        application = Gio.Application.get_default()
        consent_accepted = application.config.settings.get_value(
            "consent-accepted"
        ).get_boolean()
        log.info(f"consent has been set to: {consent_accepted}")
        if consent_accepted is False:
            pkg = Packages(self, [])
            pkg.set_content(None, self)
        else:
            self.set_title("Welcome Travelers")
            welcome = ConsentScreen()
            welcome.set_content(start_button, self)

    def next(self):
        """
        Next screen this currently doesn't work
        """
        log.debug("Next screen")
        application = Gio.Application.get_default()
        # application.


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
          <object class="GtkButton" id="btn_next">
            <property name="margin-end">12</property>
            <property name="margin-start">12</property>
            <property name="icon-name">go-next-symbolic</property>
            <property name="halign">end</property>
            <property name="valign">center</property>
            <property name="tooltip-text" translatable="yes">Next</property>
            <style>
              <class name="circular" />
              <class name="suggested-action" />
            </style>
          </object>
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
    btn_next = Gtk.Template.Child()

    class Config(YaftiScreenConfig):
        title: str
        show_terminal: bool = True
        package_manager: str
        groups: Optional[PackageGroupConfig] = None
        packages: Optional[list[PackageConfig]] = None
        package_manager_defaults: Optional[dict] = None

    def __init__(self, window, package_list, **kwargs):
        super().__init__(**kwargs)

        log.debug(package_list)

        self.__window = window
        self.btn_next.connect("clicked", self.__next_step)
        # self.__window.connect("changed", self.__on_page_changed)
        self.set_property("visible", True)
        self.package_list = package_list or []
        self._all_packages = []
        # self.scrolled_window = Gtk.ScrolledWindow()
        self.set_vexpand(True)
        self.__register_widgets = []

        asyncio.ensure_future(self.build_screens(package_list))

    def __next_step(self, *args):
        """
        This still does not work
        """
        self.__window.next()

        # if self.packages_overview is None:
        #     print(self.packages_overview)
        #     self.content_box = Gtk.Box()
        # else:
        #     self.content_box = self.packages_overview
        #
        #
        # self.packages_overview.set_halign(Gtk.Align.CENTER)
        # self.packages_overview.set_valign(Gtk.Align.CENTER)
        # self.packages_overview.append(Gtk.Label(label='Packages'))

        # self.connect("")
        # self.bind_template_child_full(self.packages_overview)
        # self.set_child(self.content_box)

        # textview = Gtk.TextView(vexpand=True)
        # self.textbuffer = textview.get_buffer()
        # self.set_child(textview)
        # self.progress = Gtk.ProgressBar(show_text=True)
        # self.set_child(self.progress)

        # if self.package_list is not None:
        #     print(self.package_list)
        #     for package in self.package_list:
        #         self.package_list.connect()

    def language_filter_func(self, model, iter, data):
        """
        Not working
        """
        if self.current_filter is None or self.current_filter == "None":
            return True
        else:
            return model[iter][2] == self.current_filter

    # @Gtk.Template.Callback()
    def on_selection_button_clicked(self, widget):
        """
        not working
        """
        # we set the current language filter to the button's label
        self.current_filter_language = widget.get_label()
        # print("%s language selected!" % self.current_filter_language)
        # we update the filter, which updates in turn the view
        self.language_filter.refilter()

    def set_content(self, button, content=None):
        """
        set_content sets the Packages pane content in the navigation split view
        """
        if content is None:
            content = Gio.Application.get_default().split_view.get_content()
            content.set_title("Packages")

        # if button is None:
        #     button = Gtk.Button(label='testing')

        # button.connect('clicked', lambda event: self.content_box.append(Gtk.Label()))
        # self.scrolled_window.set_child(button)
        self._all_packages = []
        log.debug(self.package_list)
        asyncio.ensure_future(self.build_screens(self._all_packages))
        content.pane.set_content(self)
        content.pane.set_reveal_bottom_bars(True)

        # flatpaks only support for bluefin for mvp
        # bluefin portal
        # next or install the bottom right over side scroller
        # currently installed and update or remove
        # add icon for network connectivity - they need to be on the network
        # installer
        # progress bar
        # terminal console
        # do not let computer sleep during install
        # strech goal for about page will have links to video

        # mvp v2
        # ujust
        # brew
        # ostree

        # self.show()
        # self.scrolled_window.set_data(re)

    async def build_screens(self, package_list=None):
        """
        This entire function needs to be refactored
        """
        package_manager: str = "yafti.plugin.flatpak"

        results = await PLUGINS.get(package_manager).ls()
        decoded_current = results.stdout.decode("utf-8").replace(
            "current packages: ", ""
        )

        # move to config
        headers = ["application", "ref", "name", "runtime", "installation", "options"]
        # view = Gtk.ListView.new(self.task_selection, tasks_signals)
        # view.set_show_separators(True)
        # view.add_css_class('task-list')
        # self.init_template()

        for p in decoded_current.splitlines():
            turds = p.split("\t")

            with_headers = {headers[i]: t for i, t in enumerate(turds)}
            self._all_packages.append(with_headers.copy())

        # self.test_list_store = Gtk.ListStore(str, str, bool, list)
        if isinstance(package_list, dict):
            for k, v in package_list.items():
                log.debug(f"Building {k} ======== {v}")

        self.status_page.set_icon_name("package")
        self.status_page.set_title("Flatpaks")
        __packages = {}
        if package_list is None or isinstance(package_list, list):
            self.status_page.set_description("Generic message")
        else:
            self.status_page.set_description(
                package_list.get("description", "something went wrong")
            )
            __packages = package_list.get("packages", {})

        self.list_store = Gtk.ListStore(str, str)
        new_headers = ["ref", "application"]
        self._all_packages = []

        for p in __packages:
            for k, v in p.items():
                self.list_store.append([k, v])
                self._all_packages.append({new_headers[0]: k, new_headers[1]: v})

        self.current_filter = None
        # Creating the filter, feeding it with the liststore model
        self.language_filter = self.list_store.filter_new()
        # setting the filter function, note that we're not using the
        self.language_filter.set_visible_func(self.language_filter_func)

        # creating the treeview, making it use the filter as a model, and adding the columns
        self.treeview = Gtk.TreeView(model=self.language_filter)
        for i, column_title in enumerate(headers):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeview.append_column(column)

        selection_dialogs = []
        _index = 0

        def close_customize(widget, dialog):
            dialog.hide()

        def apply_preferences(widget, dialog, apps_list, item):
            for app in item["applications"]:
                app["active"] = app["switch"].get_active()
            dialog.hide()

        for item in self._all_packages:
            _selection_dialog = DialogBox(Gtk.Window())

            _cancel_button = Gtk.Button()
            _apply_button = Gtk.Button()
            _cancel_button.set_label("Cancel")
            _apply_button.set_label("Apply")
            _apply_button.add_css_class("suggested-action")

            _header_bar = Adw.HeaderBar()
            _header_bar.pack_start(_cancel_button)
            _header_bar.pack_end(_apply_button)
            _header_bar.set_show_end_title_buttons(False)
            _header_bar.set_show_start_title_buttons(False)

            _apps_list = Adw.PreferencesGroup()
            _apps_list.set_description(
                "The following list includes only applications available in your preferred package manager."
            )
            _apps_page = Adw.PreferencesPage()
            _apps_page.add(_apps_list)

            _box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
            _box.append(_header_bar)
            _box.append(_apps_page)

            _selection_dialog.set_content(_box)
            _selection_dialog.set_default_size(500, 600)
            selection_dialogs.append(_selection_dialog)

            _action_row = Adw.ActionRow(
                # title=item["title"], subtitle=item.get("subtitle", "")
                title=item["ref"]
            )
            _switcher = Gtk.Switch()
            _switcher.set_active(item.get("default", False))
            _switcher.set_valign(Gtk.Align.CENTER)
            _action_row.add_suffix(_switcher)

            # _customize = Gtk.Button()
            # _customize.set_icon_name("go-next-symbolic")
            # _customize.set_valign(Gtk.Align.CENTER)
            # _customize.add_css_class("flat")
            # _action_row.add_suffix(_customize)
            #
            # _customize.connect(
            #     "clicked", present_customize, selection_dialogs[-1], _apps_list, item
            # )
            _cancel_button.connect("clicked", close_customize, selection_dialogs[-1])
            _apply_button.connect(
                "clicked", apply_preferences, selection_dialogs[-1], _apps_list, item
            )

            self.bundle_list.add(_action_row)
            self.__register_widgets.append((item["application"], _switcher, _index))
            _index += 1

    def __on_page_changed(self, widget, page):
        log.debug("on_page_changed")
        if page == self.__key:
            tmp_finals = self.__window.builder.get_temp_finals("packages")

            # if no package manager is selected, use Flatpak as default
            if tmp_finals is None:
                self.bundle_list.set_sensitive(True)
                return

            packages_vars = tmp_finals["vars"]
            has_flatpak = packages_vars.get("flatpak", False)
            self.bundle_list.set_sensitive(has_flatpak)
