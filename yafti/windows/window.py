import asyncio
import logging
import pprint
from functools import partial
from typing import List

import gi.repository.GIRepository
from gi.repository import Adw, Gio, GLib, Gtk

from yafti import events, log
from yafti.registry import PLUGINS, SCREENS


@Gtk.Template(filename="yafti/gtk/window.ui")
# class Window(Adw.ApplicationWindow):
class Window(Gtk.ScrolledWindow):
    __gtype_name__ = "YaftiWindow"

    # carousel_indicator = Gtk.Template.Child()
    # carousel = Gtk.Template.Child()
    headerbar = Gtk.Template.Child()
    main_menu = Gtk.Template.Child()
    # btn_back = Gtk.Template.Child()
    # toasts = Gtk.Template.Child()
    # tasks_list = Gtk.Template.Child()
    split_view = Gtk.Template.Child()
    # btn_continue = Gtk.Template.Child()
    # collections_list = Gtk.Template.Child()
    package_list = Gtk.Template.Child()

    def __init__(self, **kwargs):
        print("Loading old window")
        super().__init__(**kwargs)
        self._idx: int = 0
        self.install_action("win.remove-completed-tasks", None, self.changed)
        self._collections_list: List = []
        # self.app = kwargs.get("application")
        self.app = Gio.Application.get_default()
        events.register("Done")
        events.register("show")
        events.register("win.filter")
        events.on("Done", self.next)
        events.on("show", self.back)
        events.on("win.filter", self.set_stack)

        # TODO(GH-2): not a huge fan of this
        #  yafti.share.BTN_BACK = self.btn_back
        #  yafti.share.BTN_NEXT = self.btn_next

        def do_emit(*args, **kwargs):
            asyncio.create_task(events.emit(*args, **kwargs))

        _continue = partial(do_emit, "btn_continue", True)
        _back = partial(do_emit, "win.filter")
        _next = partial(do_emit, "show")

        self.btn_continue = _continue
        self.install_action("win.new-collection", None, self.changed)

        self.connect("show", self.draw)
        self.connect("close-request", self.app.quit)
        # self.btn_next.connect("clicked", _next)
        # self.btn_back.connect("clicked", _back)

        self.main_menu.connect("page-changed", self.changed)

        # if self.collections_list is not None:
        #     pprint.pprint(self.collections_list)
        #     # self.collections_list.connect("show", self.changed)
        #
        #     for i in self._collections_list:
        #         print("this is here")
        #         pprint.pprint(i.as_ref())
        #         # i.connect("changed", self.changed)
        #
        # if self.carousel is not None:
        #     self.carousel.connect("page-changed", self.changed)

    def draw(self, _) -> None:
        asyncio.ensure_future(self.build_screens())

    def set_content(self, button, content=None):
        """
        set_content sets the Packages pane content in the navigation split view
        """
        print("@@@@@@@@@@@@@@@ Old Window Entrypoint @@@@@@@@@@@@@@@@@@@@@")
        if content is None:
            content = Gio.Application.get_default().split_view.get_content()
            content.set_title("Cars")

        # if button is None:
        #     button = Gtk.Button(label='punch it')
        #
        # button.connect('clicked', lambda event: self.content_box.append(Gtk.Label()))
        # self.scrolled_window.set_child(button)

        print("BEFORE SET CONTENT WINDOW")
        print(self._collections_list)
        self._all_packages = []
        content.pane.set_content(self)
        content.pane.set_reveal_bottom_bars(True)
        asyncio.ensure_future(self.build_screens())

    async def build_screens(self):
        package_manager: str = "yafti.plugins.flatpak"
        results = await PLUGINS.get(package_manager).ls()

        decoded_current = results.stdout.decode("utf-8").replace(
            "current packages: ", ""
        )

        # move to config
        headers = ["application", "ref", "name", "runtime", "installation", "version"]

        # view = Gtk.ListView.new(self.task_selection, tasks_signals)
        # view.set_show_separators(True)
        # view.add_css_class('task-list')

        list_store = Gtk.ListStore(str, str, str, str, str, str)
        trees = Gtk.TreeView.new_with_model(model=list_store)
        total_header_count = len(headers)

        for p in decoded_current.splitlines():
            turds = p.split("\t")
            # list_store.append([])
            renderer = Gtk.CellRendererText()

            parsed = []
            for v in turds:
                parsed_count = len(parsed)
                column = Gtk.TreeViewColumn(parsed_count, renderer)
                if parsed == total_header_count:
                    list_store.append(parsed)
                    column = Gtk.TreeViewColumn()
                    print(list_store[:])
                    parsed = []
                else:
                    natural = parsed_count
                    print(natural)
                    print(headers[natural])
                    print(parsed)

                    trees.append_column(column)
                    parsed.append(v)

        screens = self.app.config.screens
        for name, details in screens.items():
            log.debug(f"{name}  ======================   {details}")
            log.debug(f"****************{details.source}***************")

            if details.source not in SCREENS:
                continue

            screen = SCREENS.get(details.source)
            screen_config = await screen.from_config(details.values)
            if screen_config is None:
                continue

            # if self.collections_list is not None:
            #     self.collections_list.append(s)
            #     print("collections list")

            if self.package_list is not None and details.source == "yafti.screen.package":
                self.package_list.append(screen_config)

            # if self.carousel is not None:
            #     self.carousel.append(s)

    @property
    def idx(self) -> float:
        return self.carousel.get_position()

    def goto(self, page: int, animate: bool = True) -> None:
        """
        goto <page>
        """
        if page >= self.carousel.get_n_pages():
            page = self.carousel.get_n_pages()
        else:
            page = 0

        current_screen = self.carousel.get_nth_page(self.idx)
        next_screen = self.carousel.get_nth_page(page)

        current_screen.deactivate()
        self.carousel.scroll_to(next_screen, animate)

    @property
    def is_last_page(self):
        return self._idx + 1 >= self.carousel.get_n_pages()

    async def next(self, _) -> None:
        if self.idx + 1 >= self.carousel.get_n_pages():
            self.app.quit()
        else:
            self.goto(self._idx + 1)

    async def back(self, _) -> None:
        self.goto(self._idx - 1)

    async def install(self, _) -> None:
        self.goto(self._idx - 1)

    def changed(self, *args) -> None:
        print("window changed tips")
        if hasattr(self.btn_continue, "set_visible"):
            self.btn_continue.set_visible(self._idx > 0)
            current_screen = self.carousel.get_nth_page(self.idx)
            if self._idx + 1 >= self.carousel.get_n_pages():
                self.btn_continue.set_label("Done")
                # self.btn_back.set_visible(False)
            else:
                self.btn_continue.set_label("")

            current_screen.activate()
        else:
            log.debug("something went wrong during changed event")

    def stack(self):
        # Gtk.Stack()
        # return self.get_settings().connect_data()
        raise NotImplementedError

    def entity(self) -> Gtk.ListStore:
        raise NotImplementedError

    def current_collection(self):
        raise NotImplementedError

    def split_view(self):
        # -> Adw.NavigationSplitView:
        raise NotImplementedError

    def set_filter(self) -> Gtk.ListStore:
        # return Gtk.ListStore()
        raise NotImplementedError

    def collection_from_row(self):
        raise NotImplementedError

    def select_collection_row(self):
        raise NotImplementedError

    def tasks(self) -> Gtk.ListStore:
        # return self.current_collection().tasks()
        raise NotImplementedError

    # TODO Need to still implement this. might not be needed due to no carousel
    # def next(self,widget: Gtk.Widget = None, result: bool = None, rebuild: bool = False, mode: int = 0, *args):
    #     if rebuild:
    #         self.rebuild_ui(mode)
    #
    #     if result is not None:
    #         self.__last_result = result
    #
    #     cur_index = self.carousel.get_position()
    #     page = self.carousel.get_nth_page(cur_index + 1)
    #     self.carousel.scroll_to(page, True)

    def set_stack(self):
        print("@@@@@@@@@@@@@@@ Old Window Setting Stack @@@@@@@@@@@@@@@@@@@@@")
        if len(self.stack()) > 0:
            self.get_settings().__setattr__('set_visible_child_name', 'placeholder')
        else:
            self.get_settings().__setattr__('set_visible_child_name', 'placeholder')

        self.set_show_menubar(True)
        self.get_settings().connect('filter', self.changed)
        self.get_settings().ref()


XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="main_menu">
    <submenu>
      <attribute name="label" translatable="yes">Filter</attribute>
      <item>
        <attribute name="label" translatable="yes">All</attribute>
        <attribute name="action">win.filter</attribute>
        <attribute name="target">All</attribute>
      </item>
      <item>
        <attribute name="label" translatable="yes">Open</attribute>
        <attribute name="action">win.filter</attribute>
        <attribute name="target">Open</attribute>
      </item>
      <item>
        <attribute name="label" translatable="yes">Done</attribute>
        <attribute name="action">win.filter</attribute>
        <attribute name="target">Done</attribute>
      </item>
    </submenu>
    <item>
      <attribute name="label" translatable="yes">Done Tasks</attribute>
      <attribute name="action">win.remove-done-tasks</attribute>
    </item>
    <item>
      <attribute name="label" translatable="yes">Shortcuts</attribute>
      <attribute name="action">win.show-help-overlay</attribute>
    </item>
  </menu>
"""


class ApplicationWindow(Adw.ApplicationWindow):
    """
    ApplicationWindow is the primary window
    """
    # TODO fix top bar so it works.

    def __init__(self, **kwargs):
        print("@@@@@@@@@@@@@@@ New Window Entrypoint @@@@@@@@@@@@@@@@@@@@@")
        super().__init__(**kwargs)

        # Bind Application window dimensions to store state
        application = Gio.Application.get_default()
        application.config.window.bind(
            "width", self, "default-width", Gio.SettingsBindFlags.DEFAULT
        )
        application.config.window.bind(
            "height", self, "default-height", Gio.SettingsBindFlags.DEFAULT
        )
        application.config.window.bind(
            "is-maximized", self, "maximized", Gio.SettingsBindFlags.DEFAULT
        )
        application.config.window.bind(
            "is-fullscreen", self, "fullscreened", Gio.SettingsBindFlags.DEFAULT
        )

        # builder = Gtk.Builder.new_from_string(XML, -1)
        # application.add_main_option_entries(builder.get_object('main_menu'))

        # Dark Mode settings
        # TODO: Get this working, the menu currently doesn't toggle
        dark_mode = application.config.window.get_boolean("dark-mode")
        self.style_manager = Adw.StyleManager.get_default()

        if dark_mode:
            self.style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        else:
            self.style_manager.set_color_scheme(Adw.ColorScheme.DEFAULT)

        dark_mode_action = Gio.SimpleAction(
            name="dark-mode", state=GLib.Variant.new_boolean(dark_mode)
        )

        dark_mode_action.connect("activate", self.toggle_dark_mode)
        dark_mode_action.connect("change-state", self.change_color_scheme)
        self.add_action(dark_mode_action)

        on_quit = Gio.SimpleAction(name="quit")
        on_quit.connect("activate", application.quit)
        self.add_action(on_quit)

    def toggle_dark_mode(self, action, _):
        state = action.get_state()
        old_state = state.get_boolean()
        new_state = not old_state
        action.change_state(GLib.Variant.new_boolean(new_state))

    def change_color_scheme(self, action, new_state):
        dark_mode = new_state.get_boolean()
        style_manager = Adw.StyleManager.get_default()

        if dark_mode:
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        else:
            style_manager.set_color_scheme(Adw.ColorScheme.DEFAULT)

        action.set_state(new_state)

    def next(self, widget: Gtk.Widget = None, result: bool = None, rebuild: bool = False, mode: int = 0, *args):
        # TODO not working this is the button on the left hand side of the screen and should switch content views
        if rebuild:
            self.rebuild_ui(mode)

        if result is not None:
            self.__last_result = result

        content = Gio.Application.get_default().split_view.get_content()
        content.set_title("Random Title")

        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        # if button is None:
        #     button = Gtk.Button(label='punch it')
        #
        # button.connect('clicked', lambda event: self.content_box.append(Gtk.Label()))
        # self.scrolled_window.set_child(button)

        # content.pane.set_content(content.get_next_sibling())
        # content.pane.set_reveal_bottom_bars(True)

        # cur_index = self.carousel.get_position()
        # page = self.carousel.get_nth_page(cur_index + 1)
        # self.carousel.scroll_to(page, True)
