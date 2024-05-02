from gi.repository import Gio, Gtk, Rsvg


class About:
    """
    About class defines the About content pane

    It generates the structure in memory to apply to the navigation split view
    """

    def __init__(self):
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_vexpand(True)
        self.content_box = Gtk.Box()
        self.content_box.set_halign(Gtk.Align.CENTER)
        self.content_box.set_valign(Gtk.Align.CENTER)

        # Resolve the theme named colours to RGBA strings
        self.accent_fg_color = self.get_color("theme_selected_fg_color")
        self.accent_bg_color = self.get_color("theme_selected_bg_color")

        # Load the SVG file using librsvg
        # TODO get from config
        self.svg_data = Rsvg.Handle.new_from_file("yafti/assets/bluefin.svg")

        # Set the SVG colours to the theme colours
        # Check: print(self.accent_fg_color, self.accent_bg_color)
        # maybe this is something that folks might want to modify??
        self.svg_style_sheet = f"""
            #fg1, #fg2, #fg3, #fg4 {{ fill: {self.accent_fg_color} ; }}
            #bg1, #bg2, #bg3 {{ fill: {self.accent_bg_color} ; }}
            #svg5 {{ width: 256px; height: 256px;}}
        """
        self.svg_data.set_stylesheet(self.svg_style_sheet.encode())

        # Draw the Gtk.Image from the SVG pixel buffer
        self.logo = Gtk.Image(height_request=250, width_request=250)
        self.logo.set_from_pixbuf(self.svg_data.get_pixbuf())  # TODO below
        self.logo.set_margin_end(40)

        self.content_box.append(self.logo)

        # checkbox-checked-symbolic
        # self.content_box.append(Gtk.Label(label=''))
        # self.content_box.append(Gtk.Text("""
        # Installs Flatpaks and system packages on first boot after a user finishes installation. Yafti is idempotent.
        # This allows users to run GUI as may times as they would like
        # """))

        self.scrolled_window.set_child(self.content_box)

        # TODO:
        #  Deprecated since version 4.12: Use [ctor`Gtk`.Image.new_from_paintable] and [ctor`Gdk`.Texture.new_for_pixbuf] instead
        #  https://github.com/python-pillow/Pillow

    def set_content(self, button):
        """
        set_content sets the About pane content in the navigation split view
        """
        content = Gio.Application.get_default().split_view.get_content()
        content.set_title("About")
        content.pane.set_content(self.scrolled_window)
        content.pane.set_reveal_bottom_bars(False)

    def get_color(self, named_color):
        """
        Return the libadwaita named color in RGBA from CSS provider
        """
        label = Gtk.Label(label="Coloured Text")
        label.set_css_classes([f"cc_{named_color}"])
        rgba_color = label.get_color()

        return rgba_color.to_string()
