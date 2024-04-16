import gi
from gi.repository import Adw, Gtk
# from gi.repository import Gtk, Adw


@Gtk.Template(filename="yafti/gtk/dialog.ui")
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


# @Gtk.Template(filename="yafti/screen/assets/dialog.ui")
# class DialogBox(Adw.Window):
#     __gtype_name__ = "YaftiDialog"
#
#     label_text = Gtk.Template.Child()
#
#     def __init__(self, window, title, text, **kwargs):
#         super().__init__(**kwargs)
#         self.set_transient_for(window)
#         self.set_title(title)
#         self.label_text.set_text(text)
#
#         def hide(action, callback=None):
#             self.hide()
#
#         shortcut_controller = Gtk.ShortcutController.new()
#         shortcut_controller.add_shortcut(
#             Gtk.Shortcut.new(
#                 Gtk.ShortcutTrigger.parse_string("Escape"), Gtk.CallbackAction.new(hide)
#             )
#         )
#         self.add_controller(shortcut_controller)
