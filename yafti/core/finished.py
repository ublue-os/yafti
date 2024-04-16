import subprocess
from gettext import gettext as _

from gi.repository import Adw, Gtk


# TODO: MAKE WORK


@Gtk.Template(filename="yafti/screen/assets/finished.ui")
class YaftiFinished(Adw.Bin):
    __gtype_name__ = "YaftiFinished"

    status_page = Gtk.Template.Child()
    btn_reboot = Gtk.Template.Child()
    btn_close = Gtk.Template.Child()
    btn_log = Gtk.Template.Child()

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)
        self.__window = window
        self.__log = None
