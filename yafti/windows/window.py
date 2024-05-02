from gi.repository import Adw, Gio, GLib, Gtk

from yafti import log

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
        log.debug("@@@@@@ New Window Entrypoint @@@@@@")
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

    def next(
        self,
        widget: Gtk.Widget = None,
        result: bool = None,
        rebuild: bool = False,
        mode: int = 0,
        *args
    ):
        # TODO not working this is the button on the left hand side of the screen and should switch content views
        # if rebuild:
        #     self.rebuild_ui(mode)
        #
        # if result is not None:
        #     self.__last_result = result

        content = Gio.Application.get_default().split_view.get_content()
        content.set_title("You shouldn't see this title")

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
