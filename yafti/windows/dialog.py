from gi.repository import Adw, Gtk


@Gtk.Template(resource_path="/org/ublue-os/yafti/dialog.ui")
class YaftiDialog(Adw.Window):
    __gtype_name__ = "YaftiDialog"

    label_text = Gtk.Template.Child()

    def __init__(self, window, title, text, **kwargs):
        super().__init__(**kwargs)
        self.set_transient_for(window)
        self.set_title(title)
        self.label_text.set_text(text)
