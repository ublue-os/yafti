import asyncio
import itertools
import pprint
import time
from typing import Optional

from gi.repository import Adw, Gio, Gtk, GObject
from poetry.console.commands import self

from yafti import log
from yafti.abc import YaftiScreenConfig
from yafti.registry import PLUGINS
from yafti.views.consent import ConsentScreen
from yafti.views.dialog import DialogBox
from yafti.core.models import PackageConfig, PackageGroupConfig

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
      <attribute name="label" translatable="yes">Change label</attribute>
      <item>
        <attribute name="action">win.change_label</attribute>
        <attribute name="target">String 1</attribute>
        <attribute name="label" translatable="yes">String 1</attribute>
      </item>
      <item>
        <attribute name="action">win.change_label</attribute>
        <attribute name="target">String 2</attribute>
        <attribute name="label" translatable="yes">String 2</attribute>
      </item>
      <item>
        <attribute name="action">win.change_label</attribute>
        <attribute name="target">String 3</attribute>
        <attribute name="label" translatable="yes">String 3</attribute>
      </item>
    </section>
    <section>
      <item>
        <attribute name="action">win.maximize</attribute>
        <attribute name="label" translatable="yes">Maximize</attribute>
      </item>
    </section>
    <section>
      <item>
        <attribute name="action">app.about</attribute>
        <attribute name="label" translatable="yes">_About</attribute>
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

    def __init__(self):
        super().__init__()

        self.set_visible(True)
        self.pane = Adw.ToolbarView(top_bar_style=Adw.ToolbarStyle.FLAT)
        self.header = Adw.HeaderBar()

        # need to get this squared away
        # builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        # self.menu.append(builder.get_object('app-menu'))

        # https://python-gtk-3-tutorial.readthedocs.io/en/latest/application.html
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

        next_button = Gtk.Button()
        next_button.set_label("Next")
        next_button.set_halign(Gtk.Align.CENTER)
        next_button.set_css_classes(["suggested-action"])
        next_button.connect("clicked", lambda x: self.next())

        bottom_bar = Gtk.Box()
        bottom_bar.set_margin_top(12)
        bottom_bar.set_margin_bottom(12)
        bottom_bar.set_margin_end(12)
        bottom_bar.set_halign(Gtk.Align.END)
        bottom_bar.append(next_button)
        bottom_bar.set_css_classes([".toolbar"])

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
            pkg = Packages("Welcome", self, [])
            pkg.set_content(None, self)
        else:
            self.set_title("Welcome Travelers")
            welcome = ConsentScreen()
            welcome.set_content(next_button, self)

    def _closed(self, obj, pspec):
        print("######################################################################################")

    def next(self, **kwargs):
        """
        Next screen this currently doesn't work
        """
        log.debug("Next screen")
        application = Gio.Application.get_default()
        pprint.pprint(kwargs, indent=4)
        thing = self.pane.set_content(application.split_view.get_content())
        pkg = Packages(self, package_list=[], window=application.get_default().split_view)
        pkg.set_content(thing, self)
        # application.split_view.set_content()


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


class Stupid(GObject.GObject):
    __gtype_name__ = "Stupid"

    def __init__(self, application, name, ref, installed):
        super().__init__()
        self._application = application
        self._name = name
        self._ref = ref
        self._installed = installed or False

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

        return self._installed

    def __repr__(self):
        return f"Stupid(application={self.application}, name={self.name}, ref={self.ref}, installed{self.installed})"  # noqa


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

    class Config(YaftiScreenConfig):
        title: str
        show_terminal: bool = True
        package_manager: str
        groups: Optional[PackageGroupConfig] = None
        packages: Optional[list[PackageConfig]] = None
        package_manager_defaults: Optional[dict] = None

    def __init__(self, title, window, package_list, **kwargs):
        super().__init__(**kwargs)

        self.__window = window
        # self.btn_next.connect("clicked", self.__next_step)
        self.title: str = title
        # print(GObject.signal_list_names(self))
        self.set_property("visible", True)
        self.package_list = package_list or []
        self._all_packages = []
        # self.scrolled_window = Gtk.ScrolledWindow()
        self.set_vexpand(True)
        self.__register_widgets = []
        self.__app = Gtk.Application.get_default()
        # TODO get from config
        # self.bundle_list.activate_action("clicked", self.on_selection_button_clicked)
        self.list_store = Gio.ListStore.new(Stupid)

        asyncio.ensure_future(self.build_screens(package_list))

    # @GObject.Signal
    # def noarg_signal(self, *args):
    #
    #     package_manager: str = "yafti.plugins.flatpak"
    #     if len(self._all_packages) == 0:
    #         asyncio.ensure_future(self.__async_callback(PLUGINS.get(package_manager).list()))
    #
    #     loop = asyncio.new_event_loop()
    #     t = loop.run_until_complete(PLUGINS.get(package_manager).list())
    #     asyncio.ensure_future(PLUGINS.get(package_manager).list())
    #     package_manager: str = "yafti.plugins.flatpak"
    #     asyncio.ensure_future(self k.__async_callback(PLUGINS.get(package_manager).list()))

    def __next_step(self, *args):
        """
        This still does not work
        """
        print("next_step", args)
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

    def on_ready_callback(self, source_object, result, user_data):
        """
        Not working
        """
        print("on_ready_callback")

    # @Gtk.Template.Callback()
    def on_selection_button_clicked(self, widget, dialog):
        """
        not working
        """
        print("on_selection_button_clicked", widget)
        print("on_selection_button_clicked", dialog)
        dialog.set_visible(False)
        # dialog.connect()
        # we set the current language filter to the button's label

        state = widget.get_icon_name()
        print(state)
        if state is None:
            widget.set_icon_name("selection-checked-symbolic")
        if state == "process-completed-symbolic":
            widget.set_icon_name("process-error-symbolic")
        elif state == "selection-checked-symbolic":
            widget.set_label("install")
        elif state == "process-error-symbolic":
            widget.set_icon_name("process-completed-symbolic")

        # widget.set_icon_name("process-completed-symbolic")
        # self.current_filter_language = dialog.get_language()
        # print("%s language selected!" % self.current_filter_language)
        # we update the filter, which updates in turn the view
        # self.language_filter.refilter()

        return True

    def set_content(self, button, content=None):
        """
        set_content sets the Packages pane content in the navigation split view
        """
        # self.connect("noarg-signal", self.noarg_signal)
        if content is None:
            content = Gio.Application.get_default().split_view.get_content()
            content.set_title("Packages")



        # button.connect('clicked', lambda event: self.content_box.append(Gtk.Label()))
        # self.scrolled_window.set_child(button)
        # pprint.pprint(self.bundle_list)
        # asyncio.create_task(self.build_screens(self._all_packages))
        asyncio.ensure_future(self.build_screens())
        content.pane.set_content(self)
        content.pane.set_reveal_bottom_bars(False)
        content.set_child(self)
        # self.show()
        # self.scrolled_window.set_data(self.__window)

    async def build_screens(self, package_list=None):
        """
        This entire function needs to be refactored
        """
        # package_manager_defaults = Gtk.Template.Child()

        # results = await PLUGINS.get(package_manager).ls()
        # new_results = await PLUGINS.get(package_manager).list()

        # print(self.status_page.__dir__())
        # for r in new_results:
        #     print(r.name, r.version)
        #
        # decoded_current = results.stdout.decode("utf-8").replace(
        #     "current packages: ", ""
        # )

        # move to config
        headers = ["application", "ref", "name", "runtime", "installation", "options"]
        # view = Gtk.ListView.new(self.task_selection, tasks_signals)
        # view.set_show_separators(True)
        # view.add_css_class('task-list')
        # self.init_template()

        # for p in decoded_current.splitlines():
        #     turds = p.split("\t")
        #
        #     with_headers = {headers[i]: t for i, t in enumerate(turds)}
        #     self._all_packages.append(with_headers.copy())
        #
        # print(FOR_JUSTICE)
        # print(len(FOR_JUSTICE))
        # self.test_list_store = Gtk.ListStore(str, str, bool, list)

        # groups = {}
        # if isinstance(package_list, dict):
        #     for k, v in package_list.items():
        #         log.debug(f"Building {k} ======== {v}")
        #         pass
        #         # log.debug(f"Building {k} ======== {v}")


        # self.bundle.set_icon_name("package")
        # self.bundle.set_title("Flatpaks")
        # TODO: get values from config file
        self.status_page.set_icon_name("package")
        self.status_page.set_title(self.title)

        if self.package_list is None:
            self.status_page.set_description(
                "Install some Packages! If you're seeing this message update the yafti.yaml file."
            )
        elif isinstance(self.package_list, list):
            # for package in self.package_list:
            #     print(package)
            pass
        else:
            self.status_page.set_description(
                self.package_list.get("description", "Should make a github issue...")
            )

        match self.title.lower():
            case "apply changes":
                print(f"-----------------------------------{self.title.lower()}------------------------")
                self.list_store = Gtk.ListStore(str, str, str, str, str)
                new_headers = ["ref", "name", "runtime", "installation", "version", "options"]

                for p in self.package_list:
                    for k, v in p.items():
                        self.list_store.append([k, v])
                        self._all_packages.append({new_headers[0]: k, new_headers[1]: v})
            case "installed":
                print(f"-----------------------------------{self.title.lower()}------------------------")

                # self.list_store = Gtk.ListStore(str, str)
                # self.test_list_store = Gtk.ListStore(str, str, bool, list)
                self.status_page.set_description("Currently installed on your system")
                new_headers = ["ref", "application"]

                for p in self.__app.config.installed:
                    # self.list_store.append([p.ref, p.name])

                    self.list_store.append(Stupid(p.application, p.ref, p.name, True))
                    # self._all_packages.append({new_headers[0]: p.name, new_headers[1]: p.ref, "installed": True})
                        # self.list_store.append(p)
                        # self._all_packages.append({new_headers[0]: k, new_headers[1]: v})
            case _:
                print(f"-------------group package screen {self.title.lower()}--------------")
                # self.list_store = Gio.ListStore(item_type=Stupid)

                # screens = application.config.apps_by_screen(self.title.lower())
                new_headers = ["ref", "application"]
                # applications = screens.get('applications')

                # print(screens)
                # __test = []
                # print(applications)

                # for a in applications:
                #     # TODO: get from config
                #     if a == 'source' and b != 'yafti.screen.package':
                #         print(f"{a} @@@@@@@@@@@@@@@@@@@@@@@@@@@@ {b}")
                #         continue
                #
                #     elif a == 'values' and isinstance(b, dict):
                #         for k, v in b.items():
                #             match k:
                #                 case "title":
                #                     print(f"{k} @@@@@@@@@@@@@@@@@@@@@@@@@@@@ {v}")
                #
                #                 case "show_terminal":
                #                     # likely not needed
                #                     print(f"SHOW TERMINAL @@@@@@@@@@@@@@@@@@@@@@@@@@@@ {v}")
                #                     pass
                #                 case "package_manager":
                #                     # set package manager
                #                     print(f"PACKAGE MANAGER @@@@@@@@@@@@@@@@@@@@@@@@@@@@ {v}")
                #                     pass
                #                 case "groups":
                #                     print(f"~~~~~~~~~~~~~~~~~~~~~~~~~~{k}~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                #                     # {v}
                #                     for dn, te in v.items():
                #                         if dn.lower() == self.title.lower():
                #                             for n, z in te.items():
                #                                 print(f"@@@@@@@@@@@@@@@@@@@@ {n} @@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                #
                #                             break


                # for p in applications:
                #     # for k, v in p.items():
                #     #     self.list_store.append([k, v])
                #     #     print(f"{k} ---------------------------------------------{v}")
                #
                #         # installed = False
                #         # if application.config.installed:
                #         #
                #         #     print(f"{k} installed")
                #         #     for i in application.config.installed:
                #         #         print(f"{i.name}")
                #         #         if k in i.name:
                #         #             installed = True
                #
                #     fu = [{
                #         'name': 'Discord',
                #         'ref': 'com.discordapp.Discord',
                #         'installed': True},
                #         {'name':'Slack', 'ref': 'com.slack.Slack', 'installed': False}
                #     ]
                #
                #     self._all_packages.append({new_headers[0]: k, new_headers[1]: v, "installed": p.get("installed", False)})

                if isinstance(self.package_list, dict):
                    packages = self.package_list.get("packages", [])
                    if packages:
                        print(packages)

                        for p in packages:
                            print(p)

                            for k, v in p.items():
                                is_installed = self.__app.config.is_installed(v) or False
                                # print(f"{k} ------  {self.__app.config.is_installed(v)}  ------- {v}")
                                # update only
                                # self.list_store.append([k,v])
                                self.list_store.append(Stupid(k, v, k, is_installed))
                                # self._all_packages.append({new_headers[0]: k, new_headers[1]: v, "installed": is_installed})

                else:
                    print("broklen")

                # for p in __packages:
                #     for k, v in p.items():
                #         self.list_store.append([k, v])
                #         print(f"{k} --------------------  {application.config.is_installed(v)}  -------------------------{v}")
                #
                #
                #         # print(f"{k} -------------------------------------------- {v}")
                #
                #         # installed = False
                #         # if applications:
                #         #
                #         #     print(f"{k} installed")
                #         #     for i in applications:
                #         #         print(f"{i.name}")
                #         #         if k in i.name:
                #         #             installed = True
                #
                #         self._all_packages.append({new_headers[0]: k, new_headers[1]: v, "installed": True})

        # if self.title.lower() == "apply changes":
        #     self.list_store = Gtk.ListStore(str,str,str,str,str)
        #     new_headers = ["ref", "name", "runtime", "installation", "version", "options"]
        #     for p in __packages:
        #         for k, v in p.items():
        #             self.list_store.append([k, v])
        #             print(k)
        #             print(v)
        #             self._all_packages.append({new_headers[0]: k, new_headers[1]: v})

        # else:
        #     self.list_store = Gtk.ListStore(str, str)
        #     new_headers = ["ref", "application"]
        #     for p in __packages:
        #         for k, v in p.items():
        #             self.list_store.append([k, v])
        #             self._all_packages.append({new_headers[0]: k, new_headers[1]: v})

        # self.list_store = Gtk.ListStore(str, str)
        # new_headers = ["ref", "application"]
        # for p in __packages:
        #     for k, v in p.items():
        #         self.list_store.append([k, v])
        #         self._all_packages.append({new_headers[0]: k, new_headers[1]: v})

        # self.current_filter = None
        # Creating the filter, feeding it with the list store model
        # self.language_filter = self.list_store.filter_new()
        # setting the filter function, note that we're not using the
        # self.language_filter.set_visible_func(self.language_filter_func)

        # creating the treeview, making it use the filter as a model, and adding the columns
        # self.treeview = Gtk.TreeView(model=self.language_filter)
        # for i, column_title in enumerate(headers):
        #     renderer = Gtk.CellRendererText()

            # column = Gtk.TreeViewColumn(i, cell_area=self.language_filter, True, True, title=column_title)
            # self.treeview.append_column(column)

        selection_dialogs = []
        _index = 0

        def close_customize(widget, dialog):
            dialog.hide()

        def apply_preferences(widget, dialog, apps_list, item):
            # experimental

            for app in item["applications"]:
                app["active"] = app["switch"].get_active()

            dialog.hide()

        # for item in self._all_packages:
        for item in self.list_store:
            _selection_dialog = DialogBox(Gtk.Window())
            # TODO: get from config
            # _apps_list.set_description(
            #     "The following list includes a tailored list of applications for you're selection."
            # )

            _apps_page = Adw.PreferencesPage()
            # _apps_page.add(self.bundle_list)

            _box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
            _box.append(_apps_page)

            _selection_dialog.set_content(_box)
            _selection_dialog.set_default_size(500, 600)
            selection_dialogs.append(_selection_dialog)

            # TODO: expand on this
            _action_row = Adw.ActionRow(
                # title=item["title"], subtitle=item.get("subtitle", "")
                # title=item["ref"]
                title=item.ref
            )

            # _switcher = Adw.SwitchRow()
            # _switcher.set_active(item.get('install', True))
            # _switcher.set_active(item.installed)
            # _switcher.set_valign(Gtk.Align.CENTER)

            # _action_row.add_suffix(_switcher)
            # _action_row.set_name("yes")
            # _action_row.connect("activate",lambda x: print("yes"))
            # _switcher.connect("activate", lambda x: print("no"))

            _customize = Gtk.Button()
            _customize.set_name("install")
            _customize.set_label("install")
            # _customize.set_icon_name("selection-checked-symbolic")
            _customize.set_valign(Gtk.Align.CENTER)
            _customize.add_css_class("boxed_list")
            _action_row.add_suffix(_customize)

            if item.installed is True:
            # if item.get("installed", False):
                _customize.set_icon_name("process-completed-symbolic")

            _customize.connect("clicked", self.on_selection_button_clicked, selection_dialogs[-1]) # selection_dialogs[-1], _apps_list, item

            self.bundle_list.add(_action_row)
            self.list_store.connect("notify", self.__on_page_changed, selection_dialogs[-1])

            # self.__register_widgets.
            # print(_index)
            # self.__register_widgets.append(item)
            # self.__register_widgets.append(self.bundle_list)

            # application = Gio.Application.get_default()
            # application.config.setttings.set_active(item["application"])
            # application.config.settings.preferences_group.get_value("")
            # consent_accepted = application.config.settings.get_value(
            #     "consent-accepted"
            # ).get_boolean()
            #
            # log.info(f"consent has been set to: {consent_accepted}")

            # _index += 1

    def __on_page_changed(self, widget, page, selection_dialog):
        log.debug("on_page_changed")
        # self.__app.
        print(self.title)
        bundles = self.__app.config.bundles
        print(f"&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&\n{self.package_list}")
        counter = []

        if isinstance(self.package_list, dict):
            pkgs = self.package_list.get("packages", [])
        else:
            pkgs = self.package_list

        for bundle in bundles:
            print("@"*39)

            print(bundle.keys())
            print(self.title)

            if bundle is None and self.title in bundle.keys():
                print("$" * 39)
                print(bundle.get(self.title).get("packages"))
                print("$" * 39)


                print(f"*****************************************************\n{counter}")
                for i in range(len(pkgs), len(self.list_store)):
                    self.list_store.remove(i)

            else:
                print(f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n{counter}")

                print(len(self.list_store))


                self.list_store.remove_all()

                # for i, ls in enumerate(self.list_store):
                #
                #
                #     print(i)
                #     print(ls)
                #     if i > len(pkgs):
                #         self.list_store.remove(i)
                #         ls.run_dispose()

                # for k in keepers:
                #     self.list_store.append(k)
                # for i in range(defined_count, current_count):
                #
                #     test = self.list_store.get_item(i)
                #
                #     print(test)
                #     self.list_store.remove(i)




        # if page == self.__key:
        #     tmp_finals = self.__window.builder.get_temp_finals("packages")
        #
        #     # if no package manager is selected, use Flatpak as default
        #     if tmp_finals is None:
        #         self.bundle_list.set_sensitive(True)
        #         return
        #
        #     packages_vars = tmp_finals["vars"]
        #     has_flatpak = packages_vars.get("flatpak", False)
        #     self.bundle_list.set_sensitive(has_flatpak)
