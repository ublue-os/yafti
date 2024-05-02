import asyncio
from typing import Optional

from gi.repository import Adw, Gdk, Gio, GObject, Gtk, Pango, Vte

from yafti import log
from yafti.abc import YaftiScreen, YaftiScreenConfig
from yafti.core.models import PackageConfig, PackageGroupConfig

# TODO: move to .ui file this might be able to just be removed.
__xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<interface>
    <requires lib="gtk" version="4.0"/>
    <requires lib="libadwaita" version="1.0" />
    <template class="YaftiApplyChanges" parent="AdwBin">
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
                        <property name="title" translatable="yes">Apply Changes to initialize!</property>
                        <property name="description" translatable="yes">Your scientists were so preoccupied with whether or not they could, they didn’t stop to think if they should.</property>
                                                
                        <child>
                            <object class="GtkBox" id="tour_box">
                                <property name="orientation">vertical</property>
                                <property name="vexpand">true</property>
                                <property name="hexpand">true</property>
                                <property name="valign">center</property>
                                                                                                      
                            </object>
                        </child>
                            <child>
                                <object class="AdwPreferencesPage">
                                    <child>
                                        <object class="AdwPreferencesGroup" id="bundle_list"></object>
                                    </child>
                                </object>
                            </child>
                            
                            <child>
                                <object class="GtkImage" id="logo">
                                    <property name="resource">/yafti/assets/pivot_raptor.png</property>
                                    <property name="pixel-size">400</property>
                                    <property name="margin-start">200</property>
                                    <property name="margin-end">200</property>
                                </object>
                            </child>
                            
                            <child>
                                <object class="GtkLabel" id="no_internet">
                                     <property name="label">Please connect to the internet first!</property>
                                     <property name="visible">true</property>
                                     <style>
                                         <class name="error"/>
                                     </style>
                                </object>
                            </child>
                                
                            <child>
                                <object class="GtkBox" id="console_box">
                                    <property name="visible">False</property>
                                    <property name="margin-start">40</property>
                                    <property name="margin-end">40</property>
                                    <property name="margin-top">1</property>
                                    <property name="margin-bottom">18</property>
                                    <property name="height-request">400</property>
                                    <property name="orientation">vertical</property>
                                    <child>
                                        <object class="GtkBox" id="console_output">
                                            <property name="visible">True</property>
                                            <property name="margin-top">12</property>
                                            <property name="margin-start">12</property>
                                            <property name="margin-end">12</property>
                                            <property name="orientation">vertical</property>
                                        </object>
                                    </child>
                                </object>
                            </child>

                            <child>
                                 <object class="GtkButton" id="console_button">
                                     <property name="visible">True</property>
                                     <property name="margin-end">40</property>
                                     <property name="margin-start">12</property>
                                     <property name="margin-top">40</property>
                                     <property name="icon-name">terminal-symbolic</property>
                                     <property name="halign">end</property>
                                     <property name="valign">center</property>
                                     <property name="tooltip-text" translatable="yes">Open Terminal Output</property>
                                     <style>
                                         <class name="circular" />
                                     </style>
                                 </object>
                             </child>
                             <child>
                                 <object class="GtkButton" id="tour_button">
                                     <property name="visible">False</property>
                                     <property name="margin-end">40</property>
                                     <property name="margin-start">12</property>
                                     <property name="margin-top">40</property>
                                     <property name="icon-name">action-unavailable-symbolic</property>
                                     <property name="halign">end</property>
                                     <property name="valign">center</property>
                                     <property name="tooltip-text" translatable="yes">Close Terminal</property>
                                     <style>
                                         <class name="circular" />
                                     </style>
                                 </object>
                             </child>                        
                        
                            <child>
                                <object class="GtkProgressBar" id="progressbar">
                                    <property name="show-text">false</property>
                                    <property name="margin-top">12</property>
                                    <property name="margin-start">40</property>
                                    <property name="margin-bottom">40</property>
                                    <property name="margin-end">40</property>
                                </object>
                            </child>
                        
                    </object>

                </child>
            </object>
        </child>
    </template>
</interface>
"""


# @Gtk.Template(filename="yafti/screen/assets/console.ui")
@Gtk.Template(string=__xml)
class YaftiApplyChanges(YaftiScreen, Adw.Bin):
    __gtype_name__ = "YaftiApplyChanges"

    # carousel_tour = Gtk.Template.Child()
    tour_button = Gtk.Template.Child()
    tour_box = Gtk.Template.Child()
    progressbar = Gtk.Template.Child()
    console_button = Gtk.Template.Child()
    console_box = Gtk.Template.Child()
    console_output = Gtk.Template.Child()
    install_button = Gtk.Template.Child()
    # installer_state = Gtk.Template.Child()
    status_page = Gtk.Template.Child()

    class Config(YaftiScreenConfig):
        title: str
        show_terminal: bool = True
        package_manager: str
        groups: Optional[PackageGroupConfig] = None
        packages: Optional[list[PackageConfig]] = None
        package_manager_defaults: Optional[dict] = None

    def __init__(self, title, window, package_list, **kwargs):
        """ """

        log.debug("YaftiApplyChanges")
        super().__init__(**kwargs)

        self.__window = window
        self.title: str = title
        log.debug(GObject.signal_list_names(self))
        self.set_property("visible", True)
        self.set_vexpand(True)
        self.__packages = package_list or []
        # self.__success_fn = None
        # self.__terminal = Vte.Terminal()
        # self.__font = Pango.FontDescription()
        # self.__font.set_family("Source Code Pro 10")
        # self.__font.set_size(13 * Pango.SCALE)
        # self.__font.set_weight(Pango.Weight.NORMAL)
        # self.__font.set_stretch(Pango.Stretch.NORMAL)
        # self.__style_manager = self.__window.style_manager
        # self.__build_ui()
        # self.__on_setup_terminal_colors()
        # asyncio.ensure_future(self.crap(PLUGINS.get(package_manager).list()))
        asyncio.ensure_future(self.build_screens(package_list))
        # self.__style_manager.connect("notify::dark", self.__on_setup_terminal_colors)
        # self.tour_button.connect("clicked", self.__on_tour_button)
        # self.console_button.connect("clicked", self.__on_console_button)
        # self.install_button.connect("clicked", self.__install_packages)
        # self.scrolled_window = Gtk.ScrolledWindow()
        # self.scrolled_window.set_vexpand(True)
        # self.content_box = Gtk.Box()
        # self.content_box.set_halign(Gtk.Align.CENTER)
        # self.content_box.set_valign(Gtk.Align.CENTER)
        # # Connect to root application to get config object
        # application = Gio.Application.get_default()
        #
        # self.scrolled_window.set_child(self.content_box)

    async def build_screens(self, package_list=None):
        """
        This entire function needs to be refactored
        theming - cappica mocca
        """
        # package_manager: str = "yafti.plugins.flatpak"
        self.__success_fn = None
        self.__terminal = Vte.Terminal()
        self.__font = Pango.FontDescription()
        self.__font.set_family("Source Code Pro 10")
        self.__font.set_size(13 * Pango.SCALE)
        self.__font.set_weight(Pango.Weight.NORMAL)
        self.__font.set_stretch(Pango.Stretch.NORMAL)
        self.__style_manager = self.__window.style_manager
        self.__build_ui()

        self.__on_setup_terminal_colors()
        self.__style_manager.connect("notify::dark", self.__on_setup_terminal_colors)
        self.tour_button.connect("clicked", self.__on_tour_button)
        self.console_button.connect("clicked", self.__on_console_button)
        self.install_button.connect("clicked", self.__install_packages)

        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_vexpand(True)
        # self.content_box = Gtk.Box()
        # self.content_box.set_halign(Gtk.Align.CENTER)
        # self.content_box.set_valign(Gtk.Align.CENTER)
        self.status_page.set_title(self.title)
        # Connect to root application to get config object
        # application = Gio.Application.get_default()
        self.status_page.set_child(self.console_box)
        self.scrolled_window.set_child(self.content_box)

    def __on_setup_terminal_colors(self, *args):
        is_dark: bool = self.__style_manager.get_dark()

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
        # TODO come back to this later
        [color.parse(s) for (color, s) in zip(self.colors, palette)]

        if is_dark:
            self.fg.parse(FOREGROUND_DARK)
            self.bg.parse(BACKGROUND_DARK)
        else:
            self.fg.parse(FOREGROUND)
            self.bg.parse(BACKGROUND)

        self.__terminal.set_colors(self.fg, self.bg, self.colors)

    def __on_console_button(self, *args):
        self.tour_box.set_visible(False)
        self.console_box.set_visible(True)
        self.tour_button.set_visible(True)
        self.console_button.set_visible(False)

    def __on_tour_button(self, *args):
        self.tour_box.set_visible(True)
        self.console_box.set_visible(False)
        self.tour_button.set_visible(False)
        self.console_button.set_visible(True)

    def __build_ui(self):
        self.__terminal.set_cursor_blink_mode(Vte.CursorBlinkMode.ON)
        self.__terminal.set_font(self.__font)
        self.__terminal.set_mouse_autohide(True)
        self.__terminal.set_input_enabled(False)

        if self.console_output is None:
            self.console_output = []

        self.console_output.append(self.__terminal)
        self.__terminal.connect("child-exited", self.on_vte_child_exited)

    def __packages(self):
        """ """
        print("PACKAGES ACTIVATED")

        raise NotImplementedError

    def __install_packages(self, content):
        """ """
        print("INSTALLED PACKAGES ACTIVATED")

        raise NotImplementedError

    def on_vte_child_exited(self, terminal, status, *args):
        terminal.get_parent().remove(terminal)
        status = not bool(status)
        if self.__success_fn is not None and status:
            self.__success_fn(*self.__success_fn_args)

        self.__window.set_installation_result(status, self.__terminal)

    def stdout(self, text):
        if isinstance(text, bytes):
            t = text.decode()
            for line in t.split("\n"):
                if not line:
                    continue

                self.stdout(Gtk.Text(text=line))
        else:
            self.console_output.append(text)

        self.scroll_to_bottom()

    def stderr(self, text):
        if isinstance(text, bytes):
            t = text.decode()
            for line in t.split("\n"):
                if not line:
                    continue

                self.stderr(Gtk.Text(text=line))
        else:
            self.console_output.append(text)

        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        adj = self.get_vadjustment()
        adj.set_value(adj.get_upper())
        self.set_vadjustment(adj)

    def scroll_to_top(self):
        adj = self.get_vadjustment()
        adj.set_value(adj.get_lower())

    def hide(self):
        self.set_visible(False)

    def show(self):
        self.set_visible(True)

    def toggle_visible(self):
        self.set_visible(self.get_visible() is False)

    def set_content(self, button):
        content = Gio.Application.get_default().split_view.get_content()
        self.__build_ui()
        content.pane.set_content(self)
        content.set_title("Installation")
        content.set_visible(True)
        content.pane.set_content(self.scrolled_window)
        content.pane.set_reveal_bottom_bars(False)
