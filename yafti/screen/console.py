from gi.repository import Gtk

from yafti.abc import YaftiScreen

_xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<interface>
    <requires lib="gtk" version="4.0"/>
    <template class="YaftiConsoleScreen" parent="GtkScrolledWindow">
        <property name="margin-start">40</property>
        <property name="margin-end">40</property>
        <property name="margin-bottom">40</property>
        <property name="height-request">350</property>
        <child>
            <object class="GtkBox" id="console_output">
                <property name="visible">True</property>
                <property name="margin-top">12</property>
                <property name="margin-start">12</property>
                <property name="margin-end">12</property>
                <property name="orientation">vertical</property>
            </object>
        </child>
        <style>
            <class name="card"/>
        </style>
    </template>
</interface>
"""


@Gtk.Template(string=_xml)
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
