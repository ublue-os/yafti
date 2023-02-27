from gi.repository import Adw, Gtk

_xml = """\
<?xml version="1.0" encoding="UTF-8"?>
<interface>
    <requires lib="gtk" version="4.0"/>
    <requires lib="libadwaita" version="1.0"/>
    <template class="YaftiDialog" parent="AdwWindow">
        <property name="title" translatable="yes">Showing Information</property>
        <property name="default-width">500</property>
        <property name="modal">True</property>
        <child>
            <object class="GtkBox">
                <property name="orientation">vertical</property>
                <child>
                    <object class="AdwHeaderBar">
                        <style>
                            <class name="flat"/>
                        </style>
                    </object>
                </child>
                <child>
                  <object class="GtkLabel" id="label_text">
                    <property name="margin-top">10</property>
                    <property name="margin-start">10</property>
                    <property name="margin-end">10</property>
                    <property name="margin-bottom">20</property>
                    <property name="wrap">True</property>
                  </object>
                </child>
            </object>
        </child>
    </template>
</interface>
"""


@Gtk.Template(string=_xml)
class DialogBox(Adw.Window):
    __gtype_name__ = "YaftiDialog"

    def __init__(self, parent=None, **kwargs):
        super().__init__(**kwargs)
        if parent:
            self.set_transient_for(parent)

        sc = Gtk.ShortcutController.new()
        sc.add_shortcut(
            Gtk.Shortcut.new(
                Gtk.ShortcutTrigger.parse_string("Escape"),
                Gtk.CallbackAction.new(lambda x: self.hide()),
            )
        )
        self.add_controller(sc)
