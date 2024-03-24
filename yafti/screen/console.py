import gi

from yafti.abc import YaftiScreen

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


@Gtk.Template(filename="yafti/screen/assets/console.ui")
class ConsoleScreen(YaftiScreen, Gtk.ScrolledWindow):
    __gtype_name__ = "YaftiConsoleScreen"

    console_output = Gtk.Template.Child()

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
