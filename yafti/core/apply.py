import base64
import json
import time

# for localization
from gettext import gettext as _  # noqa
from typing import Optional

from gi.repository import Adw, Gdk, Gio, GLib, Gtk, Pango, Vte

from yafti import log
from yafti.abc import YaftiScreen, YaftiScreenConfig
from yafti.core.models import PackageConfig, PackageGroupConfig
from yafti.core.tasks import YaftiTasks
from yafti.views.tour import YaftiTour


@Gtk.Template(filename="yafti/gtk/progress.ui")
class YaftiProgress(YaftiScreen, Gtk.Box):
    __gtype_name__ = "YaftiProgress"

    carousel_tour = Gtk.Template.Child()
    tour_button = Gtk.Template.Child()
    toasts = Gtk.Template.Child()
    tour_box = Gtk.Template.Child()
    tour_btn_back = Gtk.Template.Child()
    tour_btn_next = Gtk.Template.Child()
    progressbar = Gtk.Template.Child()
    console_button = Gtk.Template.Child()
    console_box = Gtk.Template.Child()
    console_output = Gtk.Template.Child()
    install_button = Gtk.Template.Child()

    class Config(YaftiScreenConfig):
        title: str
        show_terminal: bool = True
        package_manager: str
        groups: Optional[PackageGroupConfig] = None
        packages: Optional[list[PackageConfig]] = None
        package_manager_defaults: Optional[dict] = None

    def __init__(self, title, window, package_list, **kwargs):
        """
        <property name="label" translatable="yes">Installing</property>
        """
        super().__init__(**kwargs)
        self.__window = window

        # TODO: needs to be retrieved from yafti config
        self.__tour = json.loads(
            b"""
        { 
            "apply": {
                "resource": "/org/ublue-os/yafti/assets/bluefin-small.png",
                "title": "Apply Changes to initialize!",
                "description": "Your scientists were so preoccupied with whether or not they could, they did\'t stop to think if they should."
            },
            "control": {
                "resource": "/org/ublue-os/yafti/assets/pivot_raptor.png",
                "title": "Evaluation",
                "description": "Featuring automatic image-based updates and a simple graphical application store, Bluefin is designed to get out of your way. Get what you want without sacrificing system stability. The Linux client has evolved."
            },
            "containerized": {
                "resource": "/org/ublue-os/yafti/assets/flatpak_logo.svg",
                "title": "Flatpaks",
                "description": "we got you!"
            },
            "completed": {
                "resource": "/org/ublue-os/yafti/assets/bluefin.svg",
                "title": "Our Mission",
                "description": "Bluefin is designed to be the tool you depend on to do what you do best. Bluefin is about sustainability, encompassing the software, the hardware, and the people."
            }
        }
        """
        )

        self.__app = Gio.Application.get_default()
        self.__title = title
        self.__package_list = package_list or []
        self.__terminal = Vte.Terminal()
        self.__pty = Vte.Pty().new_sync(Vte.PtyFlags.DEFAULT)
        self.__terminal.set_pty(self.__pty)
        self.__font = Pango.FontDescription()
        self.__font.set_family("Monospace")
        self.__font.set_size(13 * Pango.SCALE)
        self.__font.set_weight(Pango.Weight.NORMAL)
        self.__font.set_stretch(Pango.Stretch.NORMAL)
        self.style_manager = self.__window.style_manager
        self.__build_ui()
        self.__on_setup_terminal_colors()
        self.style_manager.connect("notify::dark", self.__on_setup_terminal_colors)
        self.tour_button.connect("clicked", self.__on_tour_button)
        self.tour_btn_back.connect("clicked", self.__on_tour_back)
        self.tour_btn_next.connect("clicked", self.__on_tour_next)
        self.install_button.connect("clicked", self.__apply)
        self.carousel_tour.connect("page-changed", self.__on_page_changed)
        self.console_button.connect("clicked", self.__on_console_button)

    def __on_setup_terminal_colors(self, *args):
        """ """
        is_dark: bool = self.style_manager.get_dark()

        palette = [
            "#363636",
            "#c01c28",
            "#26a269",
            "#a2734c",
            "#12488b",
            "#a347ba",
            "#2aa1b3",
            "#cfcfcf",
            "#5d5d5d",
            "#f66151",
            "#33d17a",
            "#e9ad0c",
            "#2a7bde",
            "#c061cb",
            "#33c7de",
            "#ffffff",
        ]

        FOREGROUND = palette[0]
        BACKGROUND = palette[15]
        FOREGROUND_DARK = palette[15]
        BACKGROUND_DARK = palette[0]

        self.fg = Gdk.RGBA()
        self.bg = Gdk.RGBA()

        self.colors = [Gdk.RGBA() for c in palette]
        [color.parse(s) for (color, s) in zip(self.colors, palette)]

        if is_dark:
            self.fg.parse(FOREGROUND_DARK)
            self.bg.parse(BACKGROUND_DARK)
        else:
            self.fg.parse(FOREGROUND)
            self.bg.parse(BACKGROUND)

        self.__terminal.set_colors(self.fg, self.bg, self.colors)

    def __on_tour_button(self, *args):
        self.tour_box.set_visible(True)
        self.console_box.set_visible(False)
        self.tour_button.set_visible(False)
        self.console_button.set_visible(True)

    def __on_tour_back(self, *args):
        cur_index = self.carousel_tour.get_position()
        page = self.carousel_tour.get_nth_page(cur_index - 1)
        self.carousel_tour.scroll_to(page, True)

    def __on_tour_next(self, *args):
        cur_index = self.carousel_tour.get_position()
        page = self.carousel_tour.get_nth_page(cur_index + 1)
        self.carousel_tour.scroll_to(page, True)

    def __on_page_changed(self, *args):
        position = self.carousel_tour.get_position()
        pages = self.carousel_tour.get_n_pages()

        self.tour_btn_back.set_visible(position < pages and position > 0)
        self.tour_btn_next.set_visible(position < pages - 1)

    def __on_console_button(self, *args):
        self.tour_box.set_visible(False)
        self.console_box.set_visible(True)
        self.tour_button.set_visible(True)
        self.console_button.set_visible(False)

    def __build_ui(self):
        self.__terminal.set_cursor_blink_mode(Vte.CursorBlinkMode.ON)
        self.__terminal.set_font(self.__font)
        self.__terminal.set_mouse_autohide(True)
        self.__terminal.set_input_enabled(False)
        self.console_output.append(self.__terminal)
        self.__terminal.connect("child-exited", self.on_vte_child_exited)

        for k, tour in self.__tour.items():
            self.carousel_tour.append(YaftiTour(self.__window, tour))

        self.__start_tour()

    def __switch_tour(self, *args):
        cur_index = self.carousel_tour.get_position() + 1
        if cur_index == self.carousel_tour.get_n_pages():
            cur_index = 0

        page = self.carousel_tour.get_nth_page(cur_index)
        self.carousel_tour.scroll_to(page, True)

    def __start_tour(self):
        log.debug("@@@@@ Tour Starting @@@@@")

        def squirrel():
            while True:
                GLib.idle_add(self.progressbar.pulse)
                GLib.idle_add(self.__switch_tour)
                time.sleep(10)

        # TODO: add callback
        YaftiTasks(squirrel, None)

    def on_vte_child_exited(self, terminal, status, *args):
        terminal.get_parent().remove(terminal)
        # to invert the status to get the correct result.
        status = not bool(status)
        # TODO: set results

    def start(self, cmd, *fn_args):
        log.debug("@@@@@@ Starting to apply changes @@@@@@")
        if not cmd:
            self.__window.set_installation_result(False, None)
            return None

        self.__terminal.pty_new_sync(Vte.PtyFlags.DEFAULT)
        self.__pty.new_sync(Vte.PtyFlags.DEFAULT, None)
        try:
            self.__pty.spawn_async(
                None,
                cmd,
                None,
                GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                None,
                None,
                -1,
                None,
                self.ready,
            )

        except AttributeError:
            # See issue #1.
            self.__terminal.spawn_sync(
                Vte.PtyFlags.DEFAULT,
                None,
                cmd,
                None,
                GLib.SpawnFlags.CLOEXEC_PIPES,
                None,
                self.ready,
            )

    def __apply(self, button):
        log.debug("Apply Changes, somethings...")
        self.progressbar.set_visible(True)
        self.console_button.set_visible(True)
        button.set_visible(False)
        # application = Gio.Application.get_default()
        # package_list = application.config.settings.included_packages

        included_packages = self.__app.config.settings.get_value("included-packages")
        bpkg_data = included_packages.get_data_as_bytes().get_data().decode("utf-8")
        try:
            pkg_data = json.loads(base64.b64decode(bpkg_data))
        except json.JSONDecodeError:
            pkg_data = {}
            pass

        self.toast(_("{} Launched. Applying changes...").format("YAFTI Installer"))
        # plug_and_play = PLUGINS.get(self.__app.config.package_manager)
        real_stupid = [b"/usr/bin/flatpak", "install", "--system", "-y", "--or-update"]
        real_stupid_remove = [b"/usr/bin/flatpak", "remove", "-y", "--system"]
        for k, v in pkg_data.items():
            action = v.get("action")
            if action is None:
                log.debug(f"noop --- {k}")
                continue

            elif action == "install":
                log.debug(f"install -----  {k}")
                real_stupid.append(k)

            elif action == "uninstall":
                log.debug(f"uninstall -----  {k}")
                real_stupid_remove.append(k)
            else:
                raise RuntimeError(f"Unknown action: {action}")

        if len(real_stupid_remove) > 4:
            self.start(real_stupid_remove)
        elif len(real_stupid) > 5:
            self.start(real_stupid)
        else:
            pass

    def set_content(self, button):
        self.progressbar.set_visible(False)
        self.console_button.set_visible(False)
        # button.set_visible(True)
        # button.set_text("Apply Changes")
        content = Gio.Application.get_default().split_view.get_content()
        content.pane.set_content(self)
        content.set_title("Installation")

    def toast(self, message, timeout=2):
        toast = Adw.Toast.new(message)
        toast.props.timeout = timeout
        self.toasts.add_toast(toast)

    def ready(self, pty, task):
        pty.spawn_finish(task)
