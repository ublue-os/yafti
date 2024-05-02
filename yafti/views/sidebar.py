from gi.repository import Adw, Gdk, Gio, GObject, Gtk

from yafti import log
from yafti.core.apply import YaftiProgress
from yafti.views.about import About
from yafti.views.content import Packages
from yafti.views.settings import Settings


class ListItem:
    """
    ListItem class defines the sidebar button widget
    """

    def __init__(self, title: str, icon: str, pane: object) -> None:
        self.title = title
        self.icon = icon
        self.pane = pane


class Sidebar(Adw.NavigationPage):
    """
    Sidebar class defines the sidebar pane
    """

    def __init__(self, window=None, **kwargs):
        super().__init__(**kwargs)

        # Primary Settings for Sidebar
        self.set_title("yafti")
        self.set_vexpand(True)

        # Set menu bar min width
        self.set_size_request(220, -1)

        # Define sidebar header box
        self.header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
        self.theme.add_search_path(path="icons")

        # TODO: get image and label from config file.
        self.header_logo = Gtk.Image.new_from_file("yafti/assets/small_logo.png")
        self.header_label = Gtk.Label(label="Bluefin Portal")

        self.header_box.append(self.header_logo)
        self.header_box.append(self.header_label)

        # The sidebar show content button when collapsed
        self.show_button = Gtk.ToggleButton(
            icon_name="go-next-symbolic",
            active=False,
            visible=False,
            margin_top=0,
            margin_bottom=0,
        )

        # Bind to the parent Window split view show-content property
        self.application = Gio.Application.get_default()
        self.show_button.bind_property(
            "active",
            self.application.split_view,
            "show-content",
            GObject.BindingFlags.BIDIRECTIONAL,
        )

        # Connect to the 'notify::folded' signal of the Adw.NavigationSplitView to show the button
        self.application.split_view.connect(
            "notify::collapsed", self.on_split_view_folded, self.show_button
        )

        # TODO: fix issues with header
        # Add the toolbar and header to the sidebar
        self.toolbar = Adw.ToolbarView()
        self.header = Adw.HeaderBar()
        self.header.set_title_widget(self.header_box)
        self.header.set_show_back_button(True)
        self.header.set_can_focus(False)
        self.header.set_decoration_layout("menu:close")
        self.header.pack_end(self.show_button)
        self.toolbar.set_content()
        self.toolbar.add_top_bar(self.header)

        try:
            self.set_child(self.toolbar)
        except Exception:
            self.set_child(Adw.ToolbarView())

        self.list = Gtk.ListBox()
        self.list.set_vexpand(False)
        self.list.set_margin_top(12)
        self.list.set_margin_start(6)
        self.list.set_margin_end(6)
        self.list.set_selection_mode(Gtk.SelectionMode.SINGLE)

        # Connect the signal
        self.list.connect("row-activated", self.on_row_activated)
        # TODO: need to add start and end screens to workflow still
        # for name, details  in self.application.yafti_config.screens.items():
        #     if details.source not in SCREENS:
        #         continue
        #
        #     screen = SCREENS.get(details.source)
        #     s = asyncio.ensure_future(screen.from_config(details.values))

        # get plugins and make sidebar.
        __list_items = []
        for b in window.bundle_list:
            for k, v in b.items():
                # TODO: get a icon from config
                __list_items.append(
                    ListItem(k, "package-x-generic-symbolic", Packages(k, window, v))
                )

        top_list_items = __list_items + [
            # TODO: future support incoming
            # ListItem(
            #     "Flatpaks",
            #     "package-x-generic-symbolic",
            #     Packages("flatpaks", window, package_list=[]),
            # ),
            # ListItem(
            #     "Gnome Extensions",
            #     "extension",
            #     Packages("gnome_extensions", window, package_list=[])
            # ),
            ListItem(
                "Currently Installed",
                "applications-system-symbolic",
                Packages("Installed", window, package_list=[]),
            ),
        ]

        # TODO: remove currently installed tab for initial release
        # store all installed apps in glib settings. along with a sha256.
        bottom_list_items = [
            ListItem("Settings", "emblem-system-symbolic", Settings()),
            ListItem("About", "help-about-symbolic", About()),
            ListItem(
                "Apply",
                "thunderbolt-symbolic",
                YaftiProgress("apply", window, package_list=[]),
            ),
        ]

        separator = Gtk.Separator(
            orientation=Gtk.Orientation.HORIZONTAL,
            margin_start=2,
            margin_end=2,
            focusable=False,
            focus_on_click=False,
            can_focus=False,
            can_target=False,
        )

        # Populate the sidebar list buttons
        for k in top_list_items:
            button = Adw.ActionRow(
                activatable=True,
                title=k.title,
                icon_name=k.icon,
                margin_bottom=0,
                margin_top=0,
                css_classes=["action-row-rounded"],
            )
            button.set_focus_on_click(True)
            button.set_can_focus(True)
            button.connect("activated", self.on_button_activated, k.pane)
            self.list.append(button)

        # Separator
        self.list.append(separator)

        for k in bottom_list_items:
            button = Adw.ActionRow(
                activatable=True,
                title=k.title,
                icon_name=k.icon,
                margin_bottom=0,
                margin_top=0,
                css_classes=["action-row-rounded"],
            )
            button.set_focus_on_click(True)
            button.set_can_focus(True)
            button.connect("activated", self.on_button_activated, k.pane)
            self.list.append(button)

        # Assign the list to the sidebar
        self.toolbar.set_content(self.list)

    def on_button_activated(self, button, content):
        """
        Set the accepted consent when a button is clicked
        """
        log.debug("on btn activated: sidebar")
        try:
            btn_title = button.get_title()
            for i in self.list:
                invert_op = getattr(i, "get_title", None)
                if callable(invert_op):
                    title = invert_op()

                    if title == btn_title:
                        # content.set_parent(i.get_child())
                        # i.set_parent(button)
                        # button.set_parent(i)
                        # self.get_child().set_focus_child(content)
                        content.set_content(button)
                        break
                else:
                    continue

            # content.set_parent()
            # content.set_content(button)
            log.debug("XxXxXx" * 14)
            # content.emit("noarg-signal")
        except Exception as e:
            content.connect("activate", button)
            content.set_parent(button)
            log.debug(f"on_button_activated Exception: {e}")
            # TODO: this should be handled correctly

    def on_row_activated(self, list_box, row):
        log.debug("on row activated: side bar")

        # self.set_child(list_box)
        self.application.split_view.set_property("show-content", True)

    def on_split_view_folded(self, split_view, allocation, button):
        """
        on_split_view_folded shows a button to return to content view in collapsed sidebar mode
        """
        log.debug(f"on_split_view_folded: {allocation}")
        # If the Adw.NavigationSplitView is folded, show the button
        # If the Adw.NavigationSplitView is not folded, hide the button
        if self.application.split_view.get_collapsed():
            button.set_visible(True)
        else:
            button.set_visible(False)
